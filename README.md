# Description

This project has utilities meant to be used in IHEP. They are site-specific and
not useful for anyone outside IHEP.

## Submit jobs from lists of commands

One can submit jobs to the cluster by doing:

```bash
job_run_commands -f jobs.txt -e my_env
```

where `jobs.txt` is a file with the commands to be ran, one per job, e.g.:

```bash
run_calculation -i 0
run_calculation -i 1
run_calculation -i 2
run_calculation -i 3
```

would run in parallel `run_calculation` for different arguments. The flag `-e`
specifies the virtual environment where this needs to be executed.

## Modify memory from jobs that are held

To modify the amount of memory used by the held jobs and release them do:

```bash
jmanager -m 8000 -t 0
```

`-t 1` will do a test run.

## Job sumission

To submit arrays of jobs to HTCondor in IHEP do:

```python
from ihep_utilities import JobSubmitter

d_job = {
    'j1' : ['echo 1', 'echo 2', 'echo 3'],
    'j2' : ['echo a', 'echo b', 'echo c'],
}

sbt = JobSubmitter(jobs=d_job, environment='None')
sbt.run(skip_submit=False)
```

Where 

- The `j1`, `j2`, etc can be replaced with the user's commands
- `environment` is the user's conda environment where this will run
- `skip_submit` can be `True` for dry runs.

The outputs will go to:

```
/publicfs/ucas/user/campoverde/Jobs/run_commands
```

but this can be changed with `JobsSubmitter._log_root`
