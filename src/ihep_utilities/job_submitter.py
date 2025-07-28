'''
Module holding JobSubmitter class
'''

import os
import subprocess
from dmu.logging.log_store import LogStore

log=LogStore.add_logger('ihep_utilities:job_submitter')
# -----------------------------
class JobSubmitter:
    '''
    Class in charge of sending jobs to the IHEP cluster
    '''
    _log_root = '/publicfs/ucas/user/campoverde/Jobs/run_commands'
    # ----------------------
    def __init__(
        self,
        jobs        : dict[str,list[str]],
        environment : str) -> None:
        '''
        Parameters
        -------------
        jobs : Dictionary where:
            key  : Is a job identifier, e.g. no_pid_file
            value: Is a list of commands associated to the job

        environment: Conda environment that will be activated before running.
                     With 'None', will run without any environment.
        '''
        self._validate_jobs(jobs=jobs)

        self._jobs        = jobs
        self._environment = environment
        self._memory      = 4000
        self._queue       = 'mid'
        self._tmp_dir     = self._get_tmp_dir()
    # ----------------------
    def _get_tmp_dir(self) -> str:
        '''
        Returns
        -------------
        Path to directory where temporary outputs, e.g. list of jobs, will go
        '''
        user    = os.environ['USER']
        tmp_dir = f'/tmp/{user}/ihep_jobs'
        os.makedirs(tmp_dir, exist_ok=True)

        return tmp_dir
    # ----------------------
    def _validate_jobs(self, jobs : dict[str,list[str]]) -> None:
        '''
        Parameters
        -------------
        jobs : Dictionary with keys as job identifiers and values as list of commands
        '''
        if len(jobs) == 0:
            raise ValueError('No jobs found')

        njob = -1
        for kind, l_command in jobs.items():
            this_njob = len(l_command)
            if this_njob == 0:
                raise ValueError(f'No commands found for job: {kind}')

            if njob == -1:
                njob = this_njob
                continue

            if njob != this_njob:
                log.warning(f'Number of commands vary between jobs {njob} -> {this_njob}')
    # ----------------------
    def _make_job_file(self, name : str, commands : list[str]) -> str:
        '''
        Parameters
        -------------
        name : Job identifier, e.g. process_trees
        commands: List of commands needed to do job

        Returns
        -------------
        Path to text file containing these commands
        '''
        fpath = f'{self._tmp_dir}/{name}.txt'
        data  = '\n'.join(commands)
        with open(fpath, 'w', encoding='utf-8') as ofile:
            ofile.write(data)

        return fpath
    # ----------------------
    def _submit_job(
        self,
        name        : str,
        commands    : list[str],
        skip_submit : bool = False) -> None:
        '''
        Parameters
        -------------
        name        : Name of job, e.g. process_trees
        commands    : List of commands to do the job
        skip_submit : If True, it will do everything but submission, needed for dry runs and tests
        '''
        path  = self._make_job_file(name=name, commands=commands)
        njob  = len(commands)

        l_arg = [
            'hep_sub',
            '-g    lhcb',
            f'-n   {njob}',
            f'-e   {name}.err',
            f'-o   {name}.out',
            f'-wt  {self._queue}',
            f'-argu "%{{ProcId}} {path} {self._environment}"',
            f'-mem {self._memory} submit_run_commands']

        if skip_submit:
            log.warning('Skipping job submission')
            return

        result = subprocess.run(l_arg, capture_output=True, text=True, check=False)

        log.info(f'Job[{name}]: {result.stdout}')
        if result.returncode == 0:
            return

        log.error(f'Job[{name}]: {result.stderr}')
    # ----------------------
    def run(self, skip_submit : bool = False) -> None:
        '''
        Runs the submission of the job(s)

        Parameters
        ---------------
        skip_submit : If True, it will do everything but submission, needed for dry runs and tests
        '''

        for kind, l_command in self._jobs.items():
            job_dir = f'{JobSubmitter._log_root}/{kind}'
            os.makedirs(job_dir, exist_ok=True)
            os.chdir(job_dir)

            self._submit_job(
                skip_submit=skip_submit,
                name       =kind,
                commands   =l_command)
# -----------------------------
