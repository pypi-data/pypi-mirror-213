# Oqtant Client

## Capabilities

- Access all the functionality of the Oqtant Web App (https://albert-dev.coldquanta.com)

  - BARRIER (Barrier Manipulator) jobs
  - BEC (Ultracold Matter) jobs

- Build parameterized (i.e. optimization) experiments using OqtantJobs

- Submit and retrieve OqtantJob results

## How Oqtant Works

- Construct a single or list of jobs using the OqtantJob class

  - 1D parameter sweeps are supported

- Run a single or list of jobs using run_jobs(). The jobs are submitted to run on hardware in FIFO queue.

  - job lists are run sequentially (uninterrupted) unless list exceeds 30 jobs

- As jobs run, OqtantJob objects are created automatically and stored in active_jobs.

  - View these jobs with see_active_jobs()
  - These jobs are available until the python session ends.

- To operate on jobs from a current or previous session, load them into active_jobs with

  - load_job_from_id(), load_job_from_id_list(), load_job_from_file(), load_job_from_file_list()

- To analyze job objects and use Oqtant's job analysis library, reference the OqtantJob class documentation.

## Considerations

- Oqtant cannot interact with jobs that have been deleted via the Oqtant Web App

- Job results and limits are restricted to the account used to authenticate the Oqtant client

- All jobs that have been submitted will be processed even if the Oqtant client session is ended before they complete

## Oqtant API

The Oqtant API provides everything you need to get started working with OqtantJobs and the Oqtant REST API. For more information regarding the Oqtant REST API refer to our [Oqtant REST API Docs](albert_api_docs.md)

### get_user_token

A utility function required for getting Oqtant authenticated with your Oqtant account. Starts up a server to handle the Auth0 authentication process and acquire a token. This helper function is located in `oqtant.util.auth`

```
Returns:
    str: Auth0 user token
```

### get_oqtant_client

A utility function to create a new OqtantClient instance. This helper method requires the token returned from `oqtant.util.auth.get_user_token` and is located in `oqtant.oqtant_client`

```
Args:
    token (str): the auth0 token required for interacting with the REST API
Returns:
    OqtantClient: authenticated instance of OqtantClient
```

### get_job

Gets an OqtantJob from the Oqtant REST API. This will always be a targeted query for a specific run. If the run is omitted then this will always return the first run of the job. Will return results for any job regardless of it's status. This function is a member of `OqtantClient`

```
Args:
    job_id (str): this is the external_id of the job to fetch
    run (int): the run to target, this defaults to the first run if omitted
Returns:
    OqtantJob: an OqtantJob instance with the values of the job queried
```

### get_job_inputs_without_output

Gets an OqtantJob from the Oqtant REST API. This can return all runs within a job or a single run based on whether a run value is provided. The OqtantJobs returned will be converted to dictionaries and will not have any output data, even if they are complete. This is useful for taking an existing job and creating a new one based on it's input data. This function is a member of `OqtantClient`

```
Args:
    job_id (str): this is the external_id of the job to fetch
    run (Union[int, None]): optional argument if caller wishes to only has a single run returned
    include_notes (bool): optional argument if caller wishes to include any notes associated with OqtantJob inputs. Defaults to False is not provided
Returns:
    Dict: a Dict representation of an OqtantJob instance
```

### generate_oqtant_job

Generates an instance of OqtantJob from the provided dictionary that contains the job details and input. Will validate the values and raise an informative error if any violations are found. This function is a member of `OqtantClient`

```
Args:
    job (Dict): dictionary containing job details and input
Returns:
    OqtantJob: an OqtantJob instance containing the details and input from the provided dictionary
```

### submit_job

Submits a single OqtantJob to the Oqtant REST API. Upon successful submission this function will return a dictionary containing the external_id of the job and it's position in the queue. This function is a member of `OqtantClient`

```
Args:
    job (OqtantJob): the OqtantJob instance to submit for processing
Returns:
    Dict: dictionary containing the external_id of the job and it's queue position
```

### run_jobs

Submits a list of OqtantJobs to the Oqtant REST API. This function provides some optional functionality to alter how it behaves. Providing it with an argument of track_status=True will make it wait and poll the Oqtant REST API until all jobs in the list have completed. The track_status functionality outputs each jobs current status as it is polling and opens up the ability to use the other optional arguments write and filename. The write and filename arguments enable the ability to have the results of each completed job written to a file. The value of filename is optional and if not provided will cause the files to be created using the external_id of each job. If running more than one job and using the filename argument it is required that the number of jobs in job_list match the number of values in filename. This function is a member of `OqtantClient`

```
Args:
    job_list (List[OqtantJob]): the list of OqtantJob instances to submit for processing
    track_status (bool): optional argument to tell this function to either return immediately or wait and poll until all jobs have completed
    write (bool): optional argument to tell this function to write the results of each job to file when complete
    filename (Union[str, List[str]]): optional argument to be used in conjunction with the write argument. allows the caller to customize the name(s) of the files being created
Returns:
    List[str]: list of the external_id(s) returned for each submitted job in job_list
```

### search_jobs

Submits a query to the REST API to search for jobs that match the provided criteria. The search results will be limited to jobs that meet your Oqtant account access. This function is a member of `OqtantClient`

```
Args:
    job_type (JobSchema.JobType): the type of the jobs to search for
    name (JobSchema.JobName): the name of the job to search for
    submit_start (str): the earliest submit date of the jobs to search for
    submit_start (str): the latest submit date of the jobs to search for
    notes (str): the notes of the jobs to search for
Returns:
    List[Dict]: a list of jobs matching the provided search criteria
```

### track_jobs

Polls the Oqtant REST API with a list of job external_ids and waits until all of them have completed. Will output each job's status while it is polling and will output a message when all jobs have completed. This function provides some optional functionality to alter how it behaves. Providing it with an argument of write will have it write the results of each completed job to a file. There is an additional argument that can be used with write called filename. The value of filename is optional and if not provided will cause the files to be created using the external_id of each job. If tracking more than one job and using the filename argument it is required that the number of jobs in job_list match the number of values in filename. This function is a member of `OqtantClient`

```
Args:
    pending_jobs (List[str]): list of job external_ids to track
    write (bool): optional argument to tell this function to write the results of each job to file when complete
    filename (Union[str, List[str]]): optional argument to be used in conjunction with the write argument. allows the caller to customize the name(s) of the files being created
```

### load_job_from_id_list

Loads OqtantJobs from the Oqtant REST API into the current active_jobs list using a list of job external_ids. The results of the jobs loaded by this function are limited to their first run. This function is a member of `OqtantClient`

```
Args:
    job_id_list (List[str]): list of job external_ids to load
```

### load_job_from_id

Loads an OqtantJob from the Oqtant REST API into the current active_jobs list using a job external_id. The results of the jobs loaded by this function can be targeted to a specific run if there are multiple. This function is a member of `OqtantClient`

```
Args:
    job_id (str): the external_id of the job to load
    run (int): optional argument to target a specific job run
```

### load_job_from_file_list

Loads OqtantJobs from the Oqtant REST API into the current active_jobs list using a list of filenames containing OqtantJob info. The results of the jobs loaded by this function are limited to their first run. This function is a member of `OqtantClient`

```
Args:
    file_list (List[str]): list of filenames containing OqtantJob information
```

### load_job_from_file

Loads an OqtantJob from the Oqtant REST API into the current active_jobs list using a file containing OqtantJob info. The results of the jobs loaded by this function are limited to their first run. This function is a member of `OqtantClient`

```
Args:
    file_list (List[str]): list of filenames containing OqtantJob information
```

### see_active_jobs

Utility function to print out the current contents of the active_jobs list. The optional argument of refresh tells the function whether it should refresh the status of pending or running jobs before printing out the results. Refreshing also updates the data in active_jobs so if jobs were submitted but not tracked this is a way to check on their status. This function is a member of `OqtantClient`

```
Args:
    refresh (bool): optional argument to refresh the data of jobs in active_jobs
```

### \_write_job_to_file

Utility function to write an OqtantJob instance to a file. Requires the full filepath including the name of the file the write. Files that already exist will cannot be overwritten. This function is a member of `OqtantClient`

```
Args:
    job (OqtantJob): the OqtantJob instance to write to file
    filepath (str): the full path to the file to write, including the name of the file
```
