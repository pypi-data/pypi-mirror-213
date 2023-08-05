# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import json
import openai
import pandas as pd
from pathlib import Path
import time
from typing import Iterator
import re

from azureml.rag.utils.logging import get_logger, enable_stdout_logging, enable_appinsights_logging, track_activity
from azureml.rag.documents import SUPPORTED_EXTENSIONS, DocumentChunksIterator, DocumentSource, split_documents, crack_documents
from azureml.rag.models import parse_model_uri
from azureml.rag.utils.azureml import get_secret_from_workspace


logger = get_logger('crack_and_chunk')


def chunks_to_dataframe(chunks) -> pd.DataFrame:
    metadata = []
    data = []
    for chunk in chunks:
        metadata.append(json.dumps(chunk.get_metadata()))
        data.append(chunk.load_data())
    #(metadata, data) = [(json.dumps(chunk.metadata), chunk.load_data()) for chunk in chunks]
    chunks_dict = {
        "Metadata": metadata,
        "Chunk": data
    }

    return pd.DataFrame(chunks_dict)


def write_chunks_to_csv(chunks_df, output_path):
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    chunks_df.to_csv(output_path, index=False)


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_data", type=str)
    parser.add_argument("--input_glob", type=str, default="**/*")
    parser.add_argument("--allowed_extensions", required=False, type=str, default=",".join(SUPPORTED_EXTENSIONS))
    parser.add_argument("--chunk_size", type=int)
    parser.add_argument("--chunk_overlap", type=int)
    parser.add_argument("--output_title_chunk", type=str)
    parser.add_argument("--output_summary_chunk", type=str, default=None)
    parser.add_argument("--data_source_url", type=str, required=False)
    parser.add_argument("--document_path_replacement_regex", type=str, required=False)
    parser.add_argument("--max_sample_files", type=int, default=-1)
    parser.add_argument("--include_summary", type=str, default="False")
    parser.add_argument("--summary_model_config", type=str, default='{"type": "azure_open_ai", "model_name": "gpt-35-turbo", "deployment_name": "gpt-35-turbo"}')
    parser.add_argument("--openai_api_version", type=str, default='2023-03-15-preview')
    parser.add_argument("--openai_api_type", type=str, default=None)
    parser.add_argument("--use_rcts", type=str2bool, default=True)

    args = parser.parse_args()
    print('\n'.join(f'{k}={v}' for k, v in vars(args).items()))

    enable_stdout_logging()
    enable_appinsights_logging()

    summary_model_config = None
    include_summary = (args.include_summary == "True" or args.include_summary == "true")
    if include_summary:
        try:
            summary_model_config = json.loads(args.summary_model_config)
            # TODO: For back compat, remove in a few weeks.
            summary_model_config['kind'] = summary_model_config['type']
            del summary_model_config['type']
            summary_model_config['model'] = summary_model_config['model_name']
            del summary_model_config['model_name']
            if 'deployment_name' in summary_model_config:
                summary_model_config['deployment'] = summary_model_config['deployment_name']
                del summary_model_config['deployment_name']
        except json.decoder.JSONDecodeError:
            # Try parse as uri
            summary_model_config = parse_model_uri(args.summary_model)

        logger.info(f"Using summary_model: {json.dumps(summary_model_config, indent=2)}")
        if summary_model_config.get("kind") == "azure_open_ai" or summary_model_config.get("api_type") == "azure":
            summary_model_config["key"] = get_secret_from_workspace("OPENAI-API-KEY")
            summary_model_config["kind"] = "open_ai"
            summary_model_config["api_type"] = "azure"
            summary_model_config["api_version"] = args.openai_api_version
            summary_model_config["api_base"] = summary_model_config.get('endpoint') if summary_model_config.get('endpoint') is not None else get_secret_from_workspace("OPENAI-API-BASE")
            openai.api_version = summary_model_config["api_version"]
            openai.api_type = summary_model_config["api_type"]
            openai.api_base = summary_model_config["api_base"]
            openai.api_key = summary_model_config["key"]

    splitter_args = {'chunk_size': args.chunk_size, 'chunk_overlap': args.chunk_overlap, 'use_rcts': args.use_rcts}

    with track_activity(logger, 'crack_and_chunk', custom_dimensions={**splitter_args}) as activity_logger:

        def filter_and_log_extensions(sources: Iterator[DocumentSource], allowed_extensions=SUPPORTED_EXTENSIONS) -> Iterator[DocumentSource]:
            """Filter out sources with extensions not in allowed_extensions."""
            total_files = 0
            skipped_files = 0
            skipped_extensions = {}
            kept_extension = {}
            for source in sources:
                total_files += 1
                if allowed_extensions is not None:
                    if source.path.suffix not in allowed_extensions:
                        skipped_files += 1
                        ext_skipped = skipped_extensions.get(source.path.suffix, 0)
                        skipped_extensions[source.path.suffix] = ext_skipped + 1
                        logger.debug(f'Filtering out extension "{source.path.suffix}" source: {source.filename}')
                        continue
                ext_kept = kept_extension.get(source.path.suffix, 0)
                kept_extension[source.path.suffix] = ext_kept + 1
                yield source
            logger.info(f"[DocumentChunksIterator::filter_extensions] Filtered {skipped_files} files out of {total_files}")
            activity_logger.activity_info['total_files'] = total_files
            activity_logger.activity_info['skipped_files'] = skipped_files
            activity_logger.activity_info['skipped_extensions'] = json.dumps(skipped_extensions)
            activity_logger.activity_info['kept_extensions'] = json.dumps(kept_extension)

        chunked_documents = DocumentChunksIterator(
            files_source=args.input_data,
            glob=args.input_glob,
            base_url=args.data_source_url,
            document_path_replacement_regex=args.document_path_replacement_regex,
            file_filter=filter_and_log_extensions,
            chunked_document_processors = [lambda docs: split_documents(docs, splitter_args=splitter_args)],
        )
        file_count = 0
        for document in chunked_documents:
            file_count += 1
            logger.info(f'Processing file: {document.source.filename}', extra={'print': True})
            # TODO: Ideally make it easy to limit number of files with a `- take: n` operation on input URI in MLTable
            if (args.max_sample_files != -1 and file_count >= args.max_sample_files):
                logger.info(f"file count: {file_count} - reached max sample file count: {args.max_sample_files}", extra={'print': True})
                break
            write_chunks_to_csv(chunks_to_dataframe(document.chunks), Path(args.output_title_chunk) / f"Chunks_{Path(document.source.filename).name}.csv")
        logger.info(f"Processed {file_count} files", extra={'print': True})
        activity_logger.activity_info["file_count"] = file_count

        if file_count == 0:
            logger.info(f"No files found in {args.input_data} with glob {args.input_glob}", extra={'print': True})
            activity_logger.activity_info["error"] = "No files found"
            activity_logger.activity_info["glob"] = args.input_glob if re.match("^[*/\\\"']+$", args.input_glob) is not None else "[REDACTED]"
            raise ValueError(f"No files found in {args.input_data} with glob {args.input_glob}, no chunks produced.")

        file_count = 0
        if include_summary:
            chunked_documents = DocumentChunksIterator(
                files_source=args.input_data,
                glob=args.input_glob,
                base_url=args.data_source_url,
                document_path_replacement_regex=args.document_path_replacement_regex,
                source_loader=lambda sources: crack_documents(sources, summary_model_config=summary_model_config),
                chunked_document_processors = [lambda docs: split_documents(docs, splitter_args={'chunk_size': args.chunk_size, 'chunk_overlap': args.chunk_overlap, 'use_rcts': args.use_rcts})]
            )
            total_time = 0
            for document in chunked_documents:
                file_start_time = time.time()
                if (args.max_sample_files != -1 and file_count >= args.max_sample_files):
                    logger.info(f"file count: {file_count} - reached max sample file count: {args.max_sample_files}", extra={'print': True})
                    break
                write_chunks_to_csv(chunks_to_dataframe(document.chunks), Path(args.output_summary_chunk) / f"Chunks_{Path(document.source.filename).name}.csv")
                file_end_time = time.time()
                file_time = file_end_time - file_start_time
            logger.info(f"Write chunks to {file_count} files in {total_time} seconds (chunk generation time excluded)", extra={'print': True})
