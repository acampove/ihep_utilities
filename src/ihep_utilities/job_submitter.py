'''
Module holding JobSubmitter class
'''

import os
import shutil
import subprocess
from datetime import datetime

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
        self._submitter_command = 'submit_run_commands'
    # ----------------------
    def _validate_jobs(self, jobs : dict[str,list[str]]) -> None:
        '''
        Parameters
        -------------
        jobs : Dictionary with keys as job identifiers and values as list of commands
        '''
        log.debug('Validating jobs')

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

        log.debug(f'All jobs will do {njob} subjobs')
    # ----------------------
    def _make_job_file(
        self,
        job_dir  : str,
        commands : list[str]) -> str:
        '''
        Parameters
        -------------
        job_dir : Directory where log files and command file will go
        commands: List of commands needed to do job

        Returns
        -------------
        Path to text file containing these commands
        '''
        fpath = f'{job_dir}/commands.txt'
        data  = '\n'.join(commands)
        with open(fpath, 'w', encoding='utf-8') as ofile:
            ofile.write(data)

        log.debug(f'Using commands file: {fpath}')

        return fpath
    # ----------------------
    def _get_submit_script(self) -> str:
        '''
        Returns
        -------------
        Path to submit_run_commands, which is the script that will run the job
        '''
        submit_path = shutil.which(self._submitter_command)
        if submit_path is None:
            raise FileNotFoundError('Cannot find {self._submitter_command}')

        log.debug(f'Using submitter from: {submit_path}')

        return submit_path
    # ----------------------
    def _submit_job(
        self,
        name        : str,
        job_dir     : str,
        commands    : list[str],
        skip_submit : bool = False) -> None:
        '''
        Parameters
        -------------
        name        : Name of job, e.g. process_trees
        job_dir     : Directory where logfiles and command files will go
        commands    : List of commands to do the job
        skip_submit : If True, it will do everything but submission, needed for dry runs and tests
        '''
        path  = self._make_job_file(job_dir=job_dir, commands=commands)
        njob  = len(commands)
        submit_script = self._get_submit_script()

        l_arg = [
            'hep_sub',
            '-g',     'lhcb',
            '-n',    f'{njob}',
            '-e',    f'{name}.err',
            '-o',    f'{name}.out',
            '-wt',   f'{self._queue}',
            '-argu', f'"%{{ProcId}} {path} {self._environment}"',
            '-mem' , f'{self._memory}',
            submit_script]

        if skip_submit:
            log.warning('Skipping job submission')
            return

        log.info(f'Submitting: {name}')
        log.debug(f'Using args: {l_arg}')
        result = subprocess.run(l_arg, capture_output=True, text=True, check=False)

        log.info(f'Job[{name}]: {result.stdout}')
        if result.returncode == 0:
            return

        log.error(f'Job[{name}]: {result.stderr}')
    # ----------------------
    def _get_job_date(self) -> str:
        '''
        Returns
        -------------
        Date where this job was ran. Meant to be used for naming files
        '''
        now  = datetime.now()
        date = now.strftime('%Y_%m_%d_%H_%M_%S')

        return date
    # ----------------------
    def run(self, skip_submit : bool = False) -> None:
        '''
        Runs the submission of the job(s)

        Parameters
        ---------------
        skip_submit : If True, it will do everything but submission, needed for dry runs and tests
        '''
        job_date = self._get_job_date()

        for kind, l_command in self._jobs.items():
            job_dir = f'{JobSubmitter._log_root}/{kind}/{job_date}'
            os.makedirs(job_dir, exist_ok=True)
            os.chdir(job_dir)

            log.debug(f'Job directory: {job_dir}')

            self._submit_job(
                job_dir    = job_dir,
                skip_submit= skip_submit,
                name       = kind,
                commands   = l_command)

        log.info('Submission finished')
# -----------------------------
