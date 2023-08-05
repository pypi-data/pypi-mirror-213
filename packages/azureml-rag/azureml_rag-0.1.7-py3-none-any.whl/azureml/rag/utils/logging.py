# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Logging utilities."""
from functools import lru_cache
import inspect
import logging
import pkg_resources
import sys


# class ExtraPrintHandler(logging.StreamHandler):
#     LEVELS = {0: 'DBUG', 1: 'INFO', 2: 'WARN', 3: 'ERRR'}

#     def emit(self, record):
#         if hasattr(record, 'print') and record.print:
#             print(f'[{datetime.utcnow()}] {record.levelname} - {record.msg}')
#         super().emit(record)

# handler = ExtraPrintHandler()

COMPONENT_NAME = 'azureml.rag'
instrumentation_key = ''
try:
    version = pkg_resources.get_distribution("azureml-rag").version
    langchain_version = pkg_resources.get_distribution("langchain").version
except Exception:
    version = ''
    langchain_version = ''
default_custom_dimensions = {'source': COMPONENT_NAME, 'version': version, 'langchain_version': langchain_version}
STACK_FMT = "%s, line %d in function %s."
DEFAULT_ACTIVITY_TYPE = "InternalCall"

try:
    from azureml.telemetry import get_telemetry_log_handler, INSTRUMENTATION_KEY
    from azureml.telemetry.activity import log_activity as _log_activity, ActivityType, ActivityLoggerAdapter
    from azureml._base_sdk_common import _ClientSessionId
    import os

    session_id = _ClientSessionId
    current_folder = os.path.dirname(os.path.realpath(__file__))
    telemetry_config_path = os.path.join(current_folder, '_telemetry.json')

    verbosity = logging.INFO
    instrumentation_key = INSTRUMENTATION_KEY
    telemetry_enabled = True
except Exception:
    from contextlib import contextmanager

    verbosity = None
    ActivityLoggerAdapter = None
    telemetry_enabled = False

    class ActivityLoggerAdapter(logging.LoggerAdapter):
        """Make logger look like Activity Logger"""

        def __init__(self, logger):
            """Initialize a new instance of the class
            """
            self._activity_info = {}
            super(ActivityLoggerAdapter, self).__init__(logger, None)

        @property
        def activity_info(self):
            """Return current activity info."""
            return self._activity_info

        def process(self, msg, kwargs):
            """Process the log message.
            """
            return msg, kwargs

    @contextmanager
    def _run_without_logging(logger, activity_name, activity_type, custom_dimensions):
        yield ActivityLoggerAdapter(logger)


known_modules = [
    "crack_and_chunk",
    "create_faiss_index",
    "create_promptflow",
    "data_import_acs",
    "git_clone",
    "generate_embeddings_parallel",
    "qa_data_generation",
    "register_mlindex_asset",
    "update_acs_index"
]


class LoggerFactory:
    """Factory for creating loggers"""
    def __init__(self, stdout=False):
        """Initialize the logger factory"""
        self.loggers = {}
        self.stdout = stdout
        self.appinsights = None
        self.with_appinsights()

    def with_stdout(self, stdout=True):
        """Set whether to log to stdout"""
        self.stdout = stdout
        # Add stdout handler to any loggers created before enabling stdout.
        for logger in self.loggers.values():
            if self.stdout:
                stdout_handler = logging.StreamHandler(stream=sys.stdout)
                stdout_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)-8s %(name)s - %(message)s (%(filename)s:%(lineno)s)', "%Y-%m-%d %H:%M:%S"))
                logger.addHandler(stdout_handler)
        return self

    def with_appinsights(self):
        """Set whether to log track_* events to appinsights"""
        if telemetry_enabled:
            import atexit

            self.appinsights = get_telemetry_log_handler(component_name=COMPONENT_NAME, path=telemetry_config_path)
            atexit.register(self.appinsights.flush)

    def get_logger(self, name, level=logging.INFO):
        """Get a logger with the given name and level"""
        if name not in self.loggers:
            logger = logging.getLogger(f'azureml.rag.{name}')
            logger.setLevel(level)
            if self.stdout:
                stdout_handler = logging.StreamHandler(stream=sys.stdout)
                stdout_handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)-8s %(name)s - %(message)s (%(filename)s:%(lineno)s)', "%Y-%m-%d %H:%M:%S"))
                logger.addHandler(stdout_handler)
            self.loggers[name] = logger
        return self.loggers[name]

    def track_activity(self, logger, name, activity_type=DEFAULT_ACTIVITY_TYPE, custom_dimensions={}):
        """Track the activity of the given logger"""
        if self.appinsights:
            stack = self.get_stack()
            custom_dimensions.update({**default_custom_dimensions, 'trace': stack})
            run_info = self._try_get_run_info()
            if run_info is not None:
                custom_dimensions.update(run_info)
            child_logger = logger.getChild(name)
            child_logger.addHandler(self.appinsights)
            return _log_activity(child_logger, name, activity_type, custom_dimensions)
        else:
            return _run_without_logging(logger, name, activity_type, custom_dimensions)

    def telemetry_info(self, logger, message, custom_dimensions={}):
        """Track info with given logger"""
        if self.appinsights:
            payload = custom_dimensions
            payload.update(default_custom_dimensions)
            child_logger = logger.getChild('appinsights')
            child_logger.addHandler(self.appinsights)
            if ActivityLoggerAdapter:
                activity_logger = ActivityLoggerAdapter(child_logger, payload)
                activity_logger.info(message)

    def telemetry_error(self, logger, message, custom_dimensions={}):
        """Track error with given logger"""
        if self.appinsights:
            payload = custom_dimensions
            payload.update(default_custom_dimensions)
            child_logger = logger.getChild('appinsights')
            child_logger.addHandler(self.appinsights)
            if ActivityLoggerAdapter:
                activity_logger = ActivityLoggerAdapter(child_logger, payload)
                activity_logger.error(message)

    @staticmethod
    def get_stack(limit=3, start=1) -> str:
        """Get the stack trace as a string"""
        try:
            stack = inspect.stack()
            # The index of the first frame to print.
            begin = start + 2
            # The index of the last frame to print.
            if limit:
                end = min(begin + limit, len(stack))
            else:
                end = len(stack)

            lines = []
            for frame in stack[begin:end]:
                file, line, func = frame[1:4]
                parts = file.rsplit('\\', 4)
                parts = parts if len(parts) > 1 else file.rsplit('/', 4)
                file = '|'.join(parts[-3:])
                lines.append(STACK_FMT % (file, line, func))
            return '\n'.join(lines)
        except Exception:
            pass
        return None

    @staticmethod
    @lru_cache(maxsize=1)
    def _try_get_run_info():
        info = {
            "subscription": os.environ.get('AZUREML_ARM_SUBSCRIPTION', ""),
            "run_id": os.environ.get("AZUREML_RUN_ID", ""),
            "resource_group": os.environ.get("AZUREML_ARM_RESOURCEGROUP", ""),
            "workspace_name": os.environ.get("AZUREML_ARM_WORKSPACE_NAME", ""),
            "experiment_id": os.environ.get("AZUREML_EXPERIMENT_ID", "")
        }
        try:
            import re
            location = os.environ.get("AZUREML_SERVICE_ENDPOINT")
            location = re.compile("//(.*?)\\.").search(location).group(1)
        except Exception:
            location = os.environ.get("AZUREML_SERVICE_ENDPOINT", "")
        info["location"] = location
        try:
            from azureml.core import Run
            run: Run = Run.get_context()
            if hasattr(run, 'experiment'):
                info["parent_run_id"] = run.properties.get('azureml.pipelinerunid', 'Unknown')
                info["mlIndexAssetKind"] = run.properties.get('azureml.mlIndexAssetKind', 'Unknown')
                info["mlIndexAssetSource"] = run.properties.get('azureml.mlIndexAssetSource', 'Unknown')
                module_name = run.properties.get('azureml.moduleName', 'Unknown')
                info["moduleName"] = module_name if module_name in known_modules or module_name.startswith('llm_') else 'Unknown'
                if info["moduleName"] != 'Unknown':
                    info["moduleVersion"] = run.properties.get('azureml.moduleVersion', 'Unknown')
        except Exception:
            pass
        return info


_logger_factory = LoggerFactory()


def enable_stdout_logging():
    """Enable logging to stdout"""
    _logger_factory.with_stdout(True)


def enable_appinsights_logging():
    """Enable logging to appinsights"""
    _logger_factory.with_appinsights()


def get_logger(name, level=logging.INFO):
    """Get a logger with the given name and level"""
    return _logger_factory.get_logger(name, level)


def track_activity(logger, name, activity_type=DEFAULT_ACTIVITY_TYPE, custom_dimensions={}):
    """Track the activity with given logger"""
    return _logger_factory.track_activity(logger, name, activity_type, custom_dimensions)


def track_info(logger, message, custom_dimensions={}):
    """Track info with given logger"""
    return _logger_factory.telemetry_info(logger, message, custom_dimensions)


def track_error(logger, message, custom_dimensions={}):
    """Track error with given logger"""
    return _logger_factory.telemetry_error(logger, message, custom_dimensions)
