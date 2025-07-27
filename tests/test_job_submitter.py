'''
Script holding functions that test JobSubmitter class
'''
import os
from ihep_utilities import JobSubmitter

# ----------------------
class Data:
    '''
    Class meant to be used to share attributes
    '''
    user    = os.environ['USER']
    out_dir = f'/tmp/{user}/tests/ihep_utilities'

    os.makedirs(out_dir, exist_ok=True)
# ----------------------
def _get_path(kind : str) -> str:
    '''
    Parameters
    -------------
    kind: Type of job submission

    Returns
    -------------
    Path to text file with commands to run as jobs
    '''
    l_command = []
    if kind == 'echo':
        l_command.append('echo 1')
        l_command.append('echo 2')
        l_command.append('echo 3')

    data = '\n'.join(l_command)
    path = f'{Data.out_dir}/{kind}.txt'
    with open(path, 'w', encoding='utf-8') as ofile:
        ofile.write(data)

    return path
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
    path = _get_path(kind='echo')

    sbt = JobSubmitter(path=path, environment='None')
    sbt.run() 
