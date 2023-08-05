import json

import requests
import enum

class ITStatusEventType(enum.Enum):
    """ An enum class that contains all IT Status event types """
    Ping = "Ping"
    Start = "Start"
    Done = "Done"
    Timeout = "Timeout"
    Status = "Status"
    Log = "Log"
    Error = "Error"
    Warning = "Warning"

class ITStatusException(Exception):
    """ A custom exception for handling IT Status errors """
    def __init__(self, message):
        super().__init__(message)

class ITStatusJobNotFoundError(ITStatusException):
    """Exception raised for job not found error in IT Status

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, job_key, tenant_schema, message="Job Not Found in IT Status Dashboard."):
        self.job_key = job_key
        self.message = message
        self.tenant_schema = tenant_schema
        super().__init__(self.message)

    def __str__(self):
        return f'{self.tenant_schema}:{self.job_key} -> {self.message}'


def ITStatusStartDone(base_url, tenant_schema, job_key):
    """ This is a decorator for functions to report start, finish and time to complete.
     The decorator must be passed the base_url and the tenant schema to report to. """
    def wrapper_decorator(func, *args, **kwargs):
        # Create the IT Status Object
        it_status = ITStatus(base_url, tenant_schema)

        # Create a UUID for runkey and send to each event for this run of the process
        import uuid
        runkey = uuid.uuid4()
        try:
            # Send a start event and record the start time
            import time
            it_status.start(job_key, message=f"Process started.", runkey=runkey)
            start_time = time.time()

            # Call the function / process
            func(*args, **kwargs)

            # Record the end time, calculate time to complete and report done to IT Status
            end_time = time.time()
            time_to_complete = round(end_time - start_time, 1)
            it_status.done(job_key, message="Process completed successfully.", data=time_to_complete, runkey=runkey)
        except Exception as e:
            # Report an error to IT Status
            it_status.error(job_key, message=f"Error occurred in {func.__name__}: {e}", runkey=runkey)
    return wrapper_decorator

def ITStatusPing(base_url, tenant_schema, job_key):
    """ This is a decorator for functions to report start, finish and time to complete.
     The decorator must be passed the base_url and the tenant schema to report to. """
    def wrapper_decorator(func, *args, **kwargs):
        # Create the IT Status Object
        it_status = ITStatus(base_url, tenant_schema)
        # Create a UUID for runkey and send to each event for this run of the process
        import uuid
        runkey = uuid.uuid4()
        try:

            # Call the function / process
            func(*args, **kwargs)

            # Report to IT Status that it Succeeded
            it_status.ping(job_key, message="Process ping!", runkey=runkey)
        except Exception as e:
            # Report an error to IT Status
            it_status.error(job_key, message=f"Error occurred in {func.__name__}: {e}", runkey=runkey)
    return wrapper_decorator

class ITStatus():
    def __init__(self, base_url, tenant_schema):
        """ This class is use to report events to the IT Status Dashboard """
        self.base_url = base_url
        self.report_url = f"{base_url}/check"
        self.tenant_schema = tenant_schema

    def ping(self, job_key, message="", data=None, log=None, runkey=None):
        """
        Sends a PING event to IT Status Dashboard.
        :param job_key: The job_key of the job to report this event to.
        :param message: (optional) An accompanying message to be shown in the dashboard.
        :param data: (optional) An accompanying float to hold associated data.
        :param log: (optional) An optional object to report additional logging data.
        :param runkey: (optional) Used for processes that report multiple events to match up events to
        a specific run of the process. Generate a UUID and set runkey to it for all events for a run of a process.
        :return: None
        """
        self.__make_check_request(job_key, ITStatusEventType.Ping, message, data, log, runkey)

    def status(self, job_key, message="", data=None, log=None, runkey=None):
        """
        Sends a STATUS event to IT Status Dashboard.
        :param job_key: The job_key of the job to report this event to.
        :param message: (optional) An accompanying message to be shown in the dashboard.
        :param data: (optional) An accompanying float to hold associated data.
        :param log: (optional) An optional object to report additional logging data.
        :param runkey: (optional) Used for processes that report multiple events to match up events to
        a specific run of the process. Generate a UUID and set runkey to it for all events for a run of a process.
        :return: None
        """
        self.__make_check_request(job_key, ITStatusEventType.Status, message, data, log, runkey)

    def start(self, job_key, message="", data=None, log=None, runkey=None):
        """
        Sends a START event to IT Status Dashboard.
        :param job_key: The job_key of the job to report this event to.
        :param message: (optional) An accompanying message to be shown in the dashboard.
        :param data: (optional) An accompanying float to hold associated data.
        :param log: (optional) An optional object to report additional logging data.
        :param runkey: (optional) Used for processes that report multiple events to match up events to
        a specific run of the process. Generate a UUID and set runkey to it for all events for a run of a process.
        :return: None
        """
        self.__make_check_request(job_key, ITStatusEventType.Start, message, data, log, runkey)

    def done(self, job_key, message="", data=None, log=None, runkey=None):
        """
        Sends a DONE event to IT Status Dashboard.
        :param job_key: The job_key of the job to report this event to.
        :param message: (optional) An accompanying message to be shown in the dashboard.
        :param data: (optional) An accompanying float to hold associated data.
        :param log: (optional) An optional object to report additional logging data.
        :param runkey: (optional) Used for processes that report multiple events to match up events to
        a specific run of the process. Generate a UUID and set runkey to it for all events for a run of a process.
        :return: None
        """
        self.__make_check_request(job_key, ITStatusEventType.Done, message, data, log, runkey)

    def log(self, job_key, message="", data=None, log=None, runkey=None):
        """
        Sends a LOG event to IT Status Dashboard.
        :param job_key: The job_key of the job to report this event to.
        :param message: (optional) An accompanying message to be shown in the dashboard.
        :param data: (optional) An accompanying float to hold associated data.
        :param log: (optional) An optional object to report additional logging data.
        :param runkey: (optional) Used for processes that report multiple events to match up events to
        a specific run of the process. Generate a UUID and set runkey to it for all events for a run of a process.
        :return: None
        """
        self.__make_check_request(job_key, ITStatusEventType.Log, message, data, log, runkey)

    def error(self, job_key, message="", data=None, log=None, runkey=None):
        """
        Sends a ERROR event to IT Status Dashboard.
        :param job_key: The job_key of the job to report this event to.
        :param message: (optional) An accompanying message to be shown in the dashboard.
        :param data: (optional) An accompanying float to hold associated data.
        :param log: (optional) An optional object to report additional logging data.
        :param runkey: (optional) Used for processes that report multiple events to match up events to
        a specific run of the process. Generate a UUID and set runkey to it for all events for a run of a process.
        :return: None
        """
        self.__make_check_request(job_key, ITStatusEventType.Error, message, data, log, runkey)

    def warning(self, job_key, message="", data=None, log=None, runkey=None):
        """
        Sends a WARNING event to IT Status Dashboard.
        :param job_key: The job_key of the job to report this event to.
        :param message: (optional) An accompanying message to be shown in the dashboard.
        :param data: (optional) An accompanying float to hold associated data.
        :param log: (optional) An optional object to report additional logging data.
        :param runkey: (optional) Used for processes that report multiple events to match up events to
        a specific run of the process. Generate a UUID and set runkey to it for all events for a run of a process.
        :return: None
        """
        self.__make_check_request(job_key, ITStatusEventType.Warning, message, data, log, runkey)

    def __make_check_request(self, job_key, event_type, message=None, data=None, log=None, runkey=None):
        try:
            print(f"Sending {event_type.value} event to IT Status Board at {self.base_url} for Job Key {job_key}")
            url = f"{self.report_url}/{job_key}?tenant={self.tenant_schema}&eventType={event_type.value}"
            url += f"&message={message}" if message else ""
            url += f"&data={data}" if data else ""
            url += f"&runkey={runkey}" if runkey else ""
            response = requests.put(url, json.dumps({"log": log}), verify=False)

            if response.status_code == 200:
                print(f"Successfully created the event {event_type.value} at {self.base_url}")
            elif response.status_code == 404:
                print(f"Job key {job_key} not found in IT Status board at {self.base_url} for tenant {self.tenant_schema}")
                raise ITStatusJobNotFoundError(job_key, self.tenant_schema)
            else:
                raise ITStatusException(response)
        except Exception as e:
            print(f"An error occurred when sending event {event_type.value} to {self.base_url}: {e}")
