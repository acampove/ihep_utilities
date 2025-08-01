'''
Script holding functions that test JobSubmitter class
'''
import os
from ihep_utilities import JobSubmitter

from dmu.logging.log_store import LogStore

log=LogStore.add_logger('ihep_utilities:test_job_submitter')
# ----------------------
class Data:
    '''
    Class meant to be used to share attributes
    '''
    user    = os.environ['USER']
    out_dir = f'/tmp/{user}/tests/ihep_utilities'

    os.makedirs(out_dir, exist_ok=True)
# ----------------------
def _skip_submission() -> bool:
    '''
    Returns
    -------------
    True if not in IHEP
    '''
    host_name = os.environ['HOSTNAME']

    if 'ihep.ac.cn' in host_name:
        return False

    return True
# ----------------------
def test_simple() -> None:
    '''
    Parameters
    -------------
    None

    Returns
    -------------
    None
    '''
    d_job = {
        'j1' : ['echo 1', 'echo 2', 'echo 3'],
        'j2' : ['echo a', 'echo b', 'echo c'],
    }
    log.info('')

    sbt = JobSubmitter(jobs=d_job, environment='rx')
    sbt.run(skip_submit=_skip_submission())
# ----------------------
