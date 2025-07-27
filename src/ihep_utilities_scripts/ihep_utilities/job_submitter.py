'''
Module holding JobSubmitter class
'''

from dmu.logging.log_store import LogStore

log=LogStore.add_logger('ihep_utilities:job_submitter')
# -----------------------------
class JobSubmitter:
    '''
    Class in charge of sending jobs to the IHEP cluster
    '''
    # ----------------------
    def __init__(self, path : str, environment : str) -> None:
        '''
        Parameters
        -------------
        path : Path to text file where each line is a command that will be run in a separate job

        Returns
        -------------
        environment: Conda environment that will be activated before running. 
                     With 'None', will run without any environment.
        '''
        self._path        = path
        self._environment = environment
    # ----------------------
    def run(self) -> None:
        '''
        Parameters
        -------------
        None

        Returns
        -------------
        None
        '''
# -----------------------------
