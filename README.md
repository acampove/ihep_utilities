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
