import json
import os
import sys
import time
import warnings
from importlib.metadata import version

import jwt
import requests
import semver
from bert_schemas import job as job_schema
from pydantic import ValidationError

from oqtant.schemas.job import OqtantJob
from oqtant.settings import Settings
from oqtant.util import exceptions as api_exceptions

settings = Settings()


class OqtantClient:
    """Python class for interacting with Oqtant
    This class contains tools for:
        - Accessing all of the functionality of the Oqtant Web App (https://albert-dev.coldquanta.com)
            - BARRIER (Barrier Manipulator) jobs
            - BEC (Ultracold Matter) jobs
        - Building parameterized (i.e. optimization) experiments using OqtantJobs
        - Submitting and retrieving OqtantJob results
    How Oqtant works:
        1.) Construct a single or list of OqtantJobs using 'generate_oqtant_job()'
        2.) Run the single or list of OqtantJobs on the Oqtant hardware using 'run_jobs()'
            - There is a limit of 30 OqtantJobs per use of 'run_jobs()'
        3.) As OqtantJobs are running, the results are automatically stored in 'active_jobs'
            - The OqtantJobs stored in 'active_jobs' are available until the python session ends
        4.) If you choose to not track the status of OqtantJobs with 'run_jobs()' you can see the status
            of your session's active OqtantJobs with 'see_active_jobs()'
        5.) To operate on jobs submitted in a previous session you can load them into your 'active_jobs'
            by using either 'load_job_from_id()' or 'load_job_from_file()'
        6.) To analyze OqtantJob objects and use Oqtant's job analysis library reference the OqtantJob
            class documentation located in 'oqtant/job.py'
    Need help? Found a bug? Contact albert@infleqtion.com for support. Thank you!
    """

    def __init__(self, *, settings, token, debug: bool = False):
        self.base_url: str = settings.base_url
        self.active_jobs: dict[str, OqtantJob] = {}
        self.token: str = token
        self.max_ind_var: int = settings.max_ind_var
        self.max_job_batch_size: int = settings.max_job_batch_size
        self.debug: bool = debug
        self.version = version("oqtant")

        if not self.debug:
            sys.tracebacklimit = 0

    def __get_headers(self) -> dict:
        """Generate headers for use in calls to the REST API with requests
        Returns:
            dict: a dict of header information
        """
        return {
            "Authorization": f"Bearer {self.token}",
            "X-Client-Version": version("oqtant"),
        }

    def get_job(self, job_id: str, run: int = 1) -> OqtantJob:
        """Gets an OqtantJob from the Oqtant REST API. This will always be a targeted query
           for a specific run. If the run is omitted then this will always return the first
           run of the job. Will return results for any job regardless of it's status.
        Args:
            job_id (str): this is the external_id of the job to fetch
            run (int): the run to target, this defaults to the first run if omitted
        Returns:
            OqtantJob: an OqtantJob instance with the values of the job queried
        """
        request_url = f"{self.base_url}/{job_id}"
        params = {"run": run}
        response = requests.get(
            url=request_url,
            params=params,
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.AuthorizationError
        response.raise_for_status()
        job_data = response.json()
        try:
            job = OqtantJob(**job_data)
        except (KeyError, ValidationError) as err:
            raise api_exceptions.ValidationError(f"Failed to get job {job_id}: {err}")
        return job

    def get_job_inputs_without_output(
        self, job_id: str, run: int | None = None, include_notes: bool = False
    ) -> dict:
        """Gets an OqtantJob from the Oqtant REST API. This can return all runs within a job
           or a single run based on whether a run value is provided. The OqtantJobs returned
           will be converted to dictionaries and will not have any output data, even if
           they are complete. This is useful for taking an existing job and creating a new one
           based on it's input data.
        Args:
           job_id (str): this is the external_id of the job to fetch
           run (Union[int, None]): optional argument if caller wishes to only has a single run returned
           include_notes (bool): optional argument if caller wishes to include any notes associated
              with OqtantJob inputs. Defaults to False is not provided
        Returns:
           dict: a dict representation of an OqtantJob instance
        """
        request_url = f"{self.base_url}/{job_id}"
        params = {"exclude_input_output": True}
        if run:
            params["run"] = run
        response = requests.get(
            url=request_url,
            params=params,
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.AuthorizationError
        response.raise_for_status()
        job_data = response.json()
        try:
            job = OqtantJob(**job_data)
        except (KeyError, ValidationError) as err:
            raise api_exceptions.ValidationError(f"Failed to get job {job_id}: {err}")
        if not include_notes:
            job.inputs[0].notes = ""
        job = job.dict()
        job.pop("input_count")
        return job

    def generate_oqtant_job(self, *, job: dict) -> OqtantJob:
        """Generates an instance of OqtantJob from the provided dictionary that contains the
           job details and input. Will validate the values and raise an informative error if
           any violations are found.
        Args:
           job (dict): dictionary containing job details and input
        Returns:
           OqtantJob: an OqtantJob instance containing the details and input from the provided
              dictionary
        """
        try:
            oqtant_job = OqtantJob(**job)
        except ValidationError as err:
            raise api_exceptions.ValidationError(f"Failed to generate OqtantJob: {err}")
        return oqtant_job

    def submit_job(self, *, job: OqtantJob) -> dict:
        """Submits a single OqtantJob to the Oqtant REST API. Upon successful submission this
           function will return a dictionary containing the external_id of the job and it's
           position in the queue.
        Args:
           job (OqtantJob): the OqtantJob instance to submit for processing
        Returns:
           dict: dictionary containing the external_id of the job and it's queue position
        """
        if not isinstance(job, OqtantJob):
            try:
                job = OqtantJob(**job)
            except (TypeError, AttributeError, ValidationError) as err:
                raise api_exceptions.ValidationError(f"Job is invalid: {err}")
        data = {
            "name": job.name,
            "job_type": job.job_type,
            "input_count": len(job.inputs),
            "inputs": [input.dict() for input in job.inputs],
        }
        response = requests.post(
            url=self.base_url,
            json=data,
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.AuthorizationError
        response.raise_for_status()
        response_data = response.json()
        return response_data

    def run_jobs(
        self,
        job_list: list[OqtantJob],
        track_status: bool = False,
        write: bool = False,
        filename: str | list[str] = "",
    ) -> list[str]:
        """Submits a list of OqtantJobs to the Oqtant REST API. This function provides some
           optional functionality to alter how it behaves. Providing it with an argument of
           track_status=True will make it wait and poll the Oqtant REST API until all jobs
           in the list have completed. The track_status functionality outputs each jobs
           current status as it is polling and opens up the ability to use the other optional
           arguments write and filename. The write and filename arguments enable the ability
           to have the results of each completed job written to a file. The value of filename
           is optional and if not provided will cause the files to be created using the
           external_id of each job. If running more than one job and using the filename
           argument it is required that the number of jobs in job_list match the number of
           values in filename.
        Args:
           job_list (list[OqtantJob]): the list of OqtantJob instances to submit for processing
           track_status (bool): optional argument to tell this function to either return
             immediately or wait and poll until all jobs have completed
           write (bool): optional argument to tell this function to write the results of each
             job to file when complete
           filename (Union[str, list[str]]): optional argument to be used in conjunction with the
             write argument. allows the caller to customize the name(s) of the files being created
        Returns:
           list[str]: list of the external_id(s) returned for each submitted job in job_list
        """
        if len(job_list) > self.max_job_batch_size:
            raise AttributeError(
                f"Maximum number of jobs submitted per run is {self.max_job_batch_size}."
            )
        pending_jobs = []
        submitted_jobs = []
        for job in job_list:
            response = self.submit_job(job=job)
            external_id = response["job_id"]
            queue_position = response["queue_position"]
            est_time = response["est_time"]

            job.external_id = external_id
            self.active_jobs[external_id] = job

            pending_jobs.append(external_id)
            submitted_jobs.append(external_id)
            print(
                f"submitted {job.name} ID: {job.external_id} queue_position: {queue_position} \
                    est. time: {est_time} minutes"
            )
        print("Jobs submitted: \n")
        if track_status:
            self.track_jobs(pending_jobs=pending_jobs, filename=filename, write=write)
        return submitted_jobs

    def search_jobs(
        self,
        *,
        job_type: job_schema.JobType | None = None,
        name: job_schema.JobName | None = None,
        submit_start: str | None = None,
        submit_end: str | None = None,
        notes: str | None = None,
    ) -> list[dict]:
        """Submits a query to the REST API to search for jobs that match the provided criteria.
           The search results will be limited to jobs that meet your Oqtant account access.
        Args:
           job_type (job_schema.JobType): the type of the jobs to search for
           name (job_schema.JobName): the name of the job to search for
           submit_start (str): the earliest submit date of the jobs to search for
           submit_start (str): the latest submit date of the jobs to search for
           notes (str): the notes of the jobs to search for
        Returns:
           list[dict]: a list of jobs matching the provided search criteria
        """
        request_url = f"{self.base_url}/"
        params = {}
        for param in ["job_type", "name", "submit_start", "submit_end", "notes"]:
            if locals()[param] is not None:
                params[param] = locals()[param]

        response = requests.get(
            url=request_url,
            params=params,
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.AuthorizationError
        response.raise_for_status()
        job_data = response.json()
        return job_data["items"]

    def track_jobs(
        self,
        *,
        pending_jobs: list[str],
        filename: str | list = "",
        write: bool = False,
    ) -> None:
        """Polls the Oqtant REST API with a list of job external_ids and waits until all of them have
           completed. Will output each job's status while it is polling and will output a message when
           all jobs have completed. This function provides some optional functionality to alter how it
           behaves. Providing it with an argument of write will have it write the results of each
           completed job to a file. There is an additional argument that can be used with write called
           filename. The value of filename is optional and if not provided will cause the files to be
           created using the external_id of each job. If tracking more than one job and using the
           filename argument it is required that the number of jobs in job_list match the number of
           values in filename.
        Args:
           pending_jobs (list[str]): list of job external_ids to track
           write (bool): optional argument to tell this function to write the results of each job to
             file when complete
           filename (Union[str, list[str]]): optional argument to be used in conjunction with the write
             argument. allows the caller to customize the name(s) of the files being created
        """
        if write:
            if not filename:
                job_filenames = [f"{external_id}.txt" for external_id in pending_jobs]
            elif isinstance(filename, str):
                job_filenames = [filename]
            else:
                job_filenames = filename
            if len(job_filenames) != len(pending_jobs):
                raise AttributeError(
                    "Write filename list length does not match number of jobs."
                )

        status = None
        while pending_jobs:
            for pending_job in pending_jobs:
                job = self.get_job(job_id=pending_job)
                self.active_jobs[pending_job] = job
                if job.status != status:
                    print(f"job {pending_job} is in status {job.status}")
                    status = job.status
                if job.status == job_schema.JobStatus.COMPLETE:
                    print(f"job complete: {pending_job}")
                    pending_jobs.remove(pending_job)
                    if write:
                        self._write_job_to_file(
                            self.active_jobs[pending_job], job_filenames.pop(0)
                        )
                if job.status in [
                    job_schema.JobStatus.INCOMPLETE,
                    job_schema.JobStatus.FAILED,
                ]:
                    pending_jobs.remove(pending_job)
                    if write:
                        job_filenames.pop(0)
                time.sleep(2)
        print("all jobs complete")

    def load_job_from_id_list(self, job_id_list: list[str]) -> None:
        """Loads OqtantJobs from the Oqtant REST API into the current active_jobs list using a list
           of job external_ids. The results of the jobs loaded by this function are limited to their
           first run.
        Args:
           job_id_list (list[str]): list of job external_ids to load
        """
        for job_id in job_id_list:
            self.load_job_from_id(job_id)

    def load_job_from_id(self, job_id: str, run: int = 1) -> None:
        """Loads an OqtantJob from the Oqtant REST API into the current active_jobs list using a job
           external_id. The results of the jobs loaded by this function can be targeted to a specific
           run if there are multiple.
        Args:
           job_id (str): the external_id of the job to load
           run (int): optional argument to target a specific job run
        """
        try:
            job = self.get_job(job_id=job_id, run=run)
            self.active_jobs[job_id] = job
            print(f"Loaded job: {job.name} {job_id}")
        except Exception as err:
            raise api_exceptions.ValidationError(
                f"Failed to fetch job {job_id}: {err}. Please contact ColdQuanta if error persists"
            )

    def load_job_from_file_list(self, file_list: list[str]) -> None:
        """Loads OqtantJobs from the Oqtant REST API into the current active_jobs list using a list
           of filenames containing OqtantJob info. The results of the jobs loaded by this function are
           limited to their first run.
        Args:
           file_list (list[str]): list of filenames containing OqtantJob information
        """
        for f in file_list:
            self.load_job_from_file(f)

    def load_job_from_file(self, file: str) -> None:
        """Loads an OqtantJob from the Oqtant REST API into the current active_jobs list using a file
           containing OqtantJob info. The results of the jobs loaded by this function are limited to
           their first run.
        Args:
           file_list (list[str]): list of filenames containing OqtantJob information
        """
        try:
            with open(file) as json_file:
                data = json.load(json_file)
                self.load_job_from_id(data["external_id"])
        except (FileNotFoundError, Exception) as err:
            raise api_exceptions.JobReadError(f"Failed to load job from {file}: {err}")

    def see_active_jobs(self, refresh: bool = True) -> None:
        """Utility function to print out the current contents of the active_jobs list. The optional
           argument of refresh tells the function whether it should refresh the data of pending or
           running jobs stored in active_jobs before printing out the results. Refreshing also
           updates the data in active_jobs so if jobs were submitted but not tracked this is a way
           to check on their status.
        Args:
           refresh (bool): optional argument to refresh the data of jobs in active_jobs
        """
        if refresh:
            for external_id, job in self.active_jobs.items():
                if job.status in [
                    job_schema.JobStatus.PENDING,
                    job_schema.JobStatus.RUNNING,
                ]:
                    refreshed_job = self.get_job(
                        job_id=external_id, run=job.inputs[0].run
                    )
                    self.active_jobs[external_id] = refreshed_job
        print("ACTIVE JOBS")
        print("NAME\t\tSTATUS\t\tTIME SUBMIT\t\tID")
        print("_" * 50)
        for job_id, job in self.active_jobs.items():
            print(f"{job.name}\t\t{job.status}\t\t{job.time_submit}\t\t{job_id}")

    def _write_job_to_file(self, job: OqtantJob, filepath: str) -> None:
        """Utility function to write an OqtantJob instance to a file. Requires the full filepath
           including the name of the file the write. Files that already exist cannot be
           overwritten.
        Args:
           job (OqtantJob): the OqtantJob instance to write to file
           filepath (str): the full path to the file to write, including the name of the file
        """
        if os.path.exists(filepath):
            raise api_exceptions.JobWriteError(
                "File already exists. Please choose a unique filename."
            )

        try:
            with open(filepath, "w") as f:
                f.write(str(job.json()))
            print(f"Wrote job {job.external_id} to file {filepath}")
        except (FileNotFoundError, Exception) as err:
            print(f"Failed to write job {job.external_id} to {filepath}: {err}")

    def get_job_limits(self) -> dict:
        """Utility method to get job limits from the REST API
        Returns:
            dict: dictionary of job limits
        """
        try:
            token_data = jwt.decode(
                self.token, key=None, options={"verify_signature": False}
            )
            external_user_id = token_data["sub"]
        except Exception:
            raise api_exceptions.ValidationError(
                "Unable to decode JWT token. Please contact ColdQuanta."
            )

        url = f"{self.base_url.replace('jobs', 'users')}/{external_user_id}/job_limits"
        response = requests.get(
            url=url,
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.AuthorizationError("Unauthorized")
        response.raise_for_status()
        job_limits = response.json()
        return job_limits


def version_check(client_version: str) -> None:
    """Compares the given current Oqtant version with the version currently on pypi, and raises a warning if it is older.

    Args:
        client_version (str): the client semver version number
    """
    resp = requests.get("https://pypi.org/pypi/oqtant/json", timeout=5)
    if resp.status_code == 200:
        current_version = resp.json()["info"]["version"]
        if semver.compare(client_version, current_version) < 0:
            warnings.warn(
                f"Please upgrade to Oqtant version {current_version}. You are currently using version {client_version}."
            )


def get_oqtant_client(token: str) -> OqtantClient:
    """A utility function to create a new OqtantClient instance.
    Args:
        token (str): the auth0 token required for interacting with the REST API
    Returns:
        OqtantClient: authenticated instance of OqtantClient
    """

    client = OqtantClient(settings=settings, token=token)
    version_check(client.version)
    return client
