# Oqtant Walkthrough 3: BEC Experimentation #

### This walkthrough covers best practices for conducting experiments on the Oqtant system, including submitting batches of jobs, tracking experiment progress, and handling output data for later analysis. ###

For more information about Oqtant refer to our documentation: https://gitlab.com/infleqtion/albert/oqtant/-/blob/main/README.md

*Batch job functionality is available for users with a subscription tier of EXPLORER or INNOVATOR.*

# Sign into Oqtant

## Before you can view and submit jobs you must first sign into your Oqtant account

Run the below cell to be re-directed to our login page and provide your account credentials. Once authenticated you can safely close out of that tab and return to this notebook.


```python
from matplotlib import pyplot as plt
import copy
from oqtant.oqtant_client import get_oqtant_client
from oqtant.util.auth import get_user_token
from bert_schemas import job as JobSchema
from oqtant.schemas.job import (
    OqtantJob,
    Gaussian_dist_2D,
    TF_dist_2D,
    bimodal_dist_2D,
    round_sig
)

token = get_user_token()
```

## Creating a Oqtant Client Instance ##

### After successfully logged in, create an authorized session with the Oqtant Client ###
- the oqtant_client interacts with the Oqtant server to perform remote lab functions.
- the oqtant_client object also contains all the jobs which have been submitted, run, or loaded (from database or file) during this python session


```python
oqtant_client = get_oqtant_client(token)
```

## Design a simple experiment ##

For this example, we will investigate the effect of altering the final frequency of the RF knife on the evolution of the condensate and its temperature.

### Variables ###
1. The final frequency of the rf knife

### Observables ###
 - TOF images
 - Temperature (calculated from TOF images)
 - Atom number and condensate fraction (calculated from TOF images)

Let us explore the interplay between the final RF evaporation frequency and the resulting cloud temperature in a one-parameter scan "experiment".


```python
final_rf_freqs_mhz = [0.07, 0.03, 0.05]
```

## Performing the experiment ##

Depending on your subscription tier there are two different options for performing this experiment

- Users in the GROUND tier can create 3 separate jobs with each job's input representing a step in the experiment

- Users in the EXPLORER and INNOVATOR tiers can create a single job that contains three inputs for all of the steps in the experiment

The rest of this walkthrough will showcase how to perform and analyze the experiment using both options.

Both submission options / subscription tiers will make use of a 'base' job definition:


```python
base_bec_job = {
    "name": "RF Sweep Experiment",
    "job_type": "BEC",
    "inputs": [
        {
            "values": {
                "time_of_flight_ms": 8.0,
                "image_type": "TIME_OF_FLIGHT",
                "end_time_ms": 0.0,
                "rf_evaporation": {
                    "frequencies_mhz": [17.0, 8.0, 4.0, 1.2, 0.045],
                    "powers_mw": [500.0, 500.0, 475.0, 360.0, 220.0],
                    "interpolation": "LINEAR",
                    "times_ms": [-1600, -1200, -800, -400, 0],
                },
                "optical_barriers": None,
                "optical_landscape": None,
                "lasers": None,
            },
        }
    ],
}
```

## Generating parameter scan jobs as GROUND ##

This experiment will consist of 3 jobs and no repeated trials. Below we will create a BEC job with default parameters and copy it three times. Once we have three instances of the same job we can update the inputs for each one to match the steps in the experiment.

Print out the jobs once updated to review the input parameters before submitting to run on the Oqtant hardware. Once a job is submitted, it can only be cancelled by contacting **albert@infleqtion.com**


```python
njobs = len(final_rf_freqs_mhz)
jobs = []
for step in range(njobs):
    job = copy.deepcopy(base_bec_job)
    job["name"] = "RF sweep experiment step " + str(step+1)
    job["notes"] = "RF sweep experiment step " + str(step+1) + " of " + str(njobs)
    job["inputs"][0]["values"]["rf_evaporation"]["frequencies_mhz"][-1] = final_rf_freqs_mhz[step]
    jobs.append(job)

jobs = [oqtant_client.generate_oqtant_job(job=job) for job in jobs]

for job in jobs:
    print(
        job.name,
        "\n",
        job.inputs[0].values,
        "\n"
    )
```

## Generating job parameters as EXPLORER / INNOVATOR ##

This experiment will consist of a single job with 3 inputs and no repeated trials. Below we will create an input object with default BEC parameters. Next we will copy this input three times and make updates to match the steps in the experiment.

Print out the job inputs once updated to review the parameters before submitting to run on the Oqtant hardware. Once a job is submitted, it can only be cancelled by contacting **albert@infleqtion.com**


```python
batch_job = copy.deepcopy(base_bec_job)
batch_job["inputs"] = []
batch_job["name"] = "RF sweep experiment"
batch_job["notes"] = "RF sweep experiment as sequential runs"

for step in range(njobs):
    input = copy.deepcopy(base_bec_job["inputs"][0])
    input["values"]["rf_evaporation"]["frequencies_mhz"][-1] = final_rf_freqs_mhz[step]
    batch_job["inputs"].append(input)

print(batch_job["name"])
for input in batch_job["inputs"]:
    print(
        input,
        "\n"
    )

batch_job = oqtant_client.generate_oqtant_job(job=batch_job)
```


## Accessing the fields of an OqtantJob ##

The OqtantJob class is the python representation of an Oqtant job's input parameters and (if completed) its output results. When working in Oqtant this class will be used to generate new jobs and interact with submitted jobs. You can access the information inside each OqtantJob using dot-notation.

To get the input parameters for this experiment you would do the following:

**JOB.inputs[desired-input-index].values.FIELD_FROM_BELOW_LIST**

All OqtantJobs contain the same high-level input parameters, with some being empty depending on the type of job.

For BEC jobs the following parameters are used and required:

- end_time_ms
- image_type
- time_of_flight_ms
- rf_evaporation

For BARRIER jobs the following parameters are used and required:

- end_time_ms
- image_type
- time_of_flight_ms
- rf_evaporation
- optical_barriers

All of these inputs have constraints on them which are validated when given values. To view these constraints you can refer to 'Schemas' section of our OpenAPI Documentation: https://albert-dev.coldquanta.com/api/docs


```python
# if using the GROUND option
for job in jobs:
    print(
        job.name,
        job.inputs[0].values.rf_evaporation.frequencies_mhz[-1],
        job.inputs[0].values.time_of_flight_ms
    )

print("\n")

# if using the EXPLORER / INNOVATOR option
for i, input in enumerate(batch_job.inputs):
    print(
        batch_job.name,
        f"input run #{i + 1}",
        input.values.rf_evaporation.frequencies_mhz[-1],
        input.values.time_of_flight_ms
    )
```

## Submiting jobs and storing the job IDs as GROUND ##

Once you are ready to submit the experiment jobs you will have two options. One will be to track the status of them as they are processed and the other will be to not track their status. When you choose to track the status of your submitted jobs the function will not return immediately and will instead continuously ping the Albert service until all of the jobs have finished.

Track status: **track_status=True**

Dont track status: **track_status=False**

Regardless of which method you choose, it is always a good idea to save the IDs of your jobs for future reference.

Option to run the jobs and wait for results (**track_status=True**) OR submit the jobs and return later to retrieve the results (**track_status=False**). Either way, be sure to save the job ids to a file if you plan to retrieve the data for later processing.


```python
# track the status
rf_sweep_experiment_job_ids = oqtant_client.run_jobs(job_list=jobs, track_status=True)

# dont track the status
# rf_sweep_experiment_job_ids = oqtant_client.run_jobs(job_list=experiment_jobs, track_status=False)

with open('bec_rf_sweep_experiment.txt', 'w') as filewriter:
    for experiment_step_job_id in rf_sweep_experiment_job_ids:
        filewriter.write(experiment_step_job_id)
```

## Submiting jobs and storing the job IDs as EXPLORER / INNOVATOR ##

Once you are ready to submit the experiment job you will have two options. One will be to track the status of it as it is being processed and the other will be to not track it's status. When you choose to track the status of your submitted job the function will not return immediately and will instead continuously ping the Albert service until the job has finished.

Track status: **track_status=True**

Dont track status: **track_status=False**

Regardless of which method you choose, it is always a good idea to save the IDs of your jobs for future reference.

Option to run the jobs and wait for results (**track_status=True**) OR submit the jobs and return later to retrieve the results (**track_status=False**). Either way, be sure to save the job ids to a file if you plan to retrieve the data for later processing.


```python
# track the status
rf_sweep_experiment_job_id = oqtant_client.run_jobs(job_list=[batch_job], track_status=True)[0]

# dont track the status
# rf_sweep_experiment_job_id = oqtant_client.run_jobs(job_list=[experiment_job], track_status=False)[0]

with open('bec_rf_sweep_experiment.txt', 'w') as filewriter:
    filewriter.write(rf_sweep_experiment_job_id)
```

## Load results from completed jobs ##

Use **load_jobs_from_id** to retrieve jobs in any state from a previous run.


```python
with open('bec_rf_sweep_experiment.txt', 'r') as filereader:
    for line in filereader:
        # remove linebreak which is the last character of the string
        oqtant_client.load_job_from_id(line)
for job_id, job in oqtant_client.active_jobs.items():
    print("id: ", job_id, job.job_type, job.status)
```

## Plot completed jobs ##

When job status is COMPLETE above, plot the results


```python
for a, job in oqtant_client.active_jobs.items():
    if job.status == JobSchema.JobStatus.COMPLETE and job.job_type == JobSchema.JobType.BEC:
        job.atoms_2dplot()
        job.atoms_sliceplot()
# by default jobs that are loaded will only contain the first input/output entry
# if you have more than one input for a job you can view its details by specifying the 'run' like below
desired_input_run = 2 # here we are asking for the second input/output entry
with open('bec_rf_sweep_experiment.txt', 'r') as filereader:
    for line in filereader:
        # remove linebreak which is the last character of the string
        oqtant_client.load_job_from_id(line, run=desired_input_run)
# now we can display the second input/output entry results
for a, job in oqtant_client.active_jobs.items():
    if job.status == JobSchema.JobStatus.COMPLETE and job.job_type == JobSchema.JobType.BEC:
        job.atoms_2dplot()
        job.atoms_sliceplot()
```


```python

```
