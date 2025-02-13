'''
Script used to manage jobs sent to IHEP's cluster 
'''

import argparse
import subprocess
import re
import os
from dataclasses import dataclass

from dmu.logging.log_store import LogStore

log=LogStore.add_logger('rx_scripts:jmanager')
#------------------------------
@dataclass
class Data:
    user       = os.environ['USER']
    condor_cmd = ['hep_q', '-u', user]

    test       = None
    memory     = None
    l_held_job = None
#------------------------------
def get_args():
    parser = argparse.ArgumentParser(description='Used to perform several operations on held jobs')
    parser.add_argument('-m', '--memory', type=int, help='Memory, in MB')
    parser.add_argument('-t', '--test'  , type=int, help='Testing flag', choices=[0, 1], default=1)
    parser.add_argument('-l', '--level' , type=int, help='Log level'   , choices=[10, 20, 30, 40], default=20)
    args = parser.parse_args()

    Data.memory = args.memory
    Data.test   = args.test

    log.setLevel(args.level)
#------------------------------
def get_held_jobs():
    output = subprocess.check_output(Data.condor_cmd, text=True)
    l_line = output.splitlines()

    l_job_id = []
    for line in l_line[1:]:
        line   = re.sub(' +', ' ', line) 
        l_word = line.split(' ')
        if len(l_word) < 5 or l_word[5] != 'H':
            continue
    
        l_job_id.append(l_word[0])

    if len(l_job_id) == 0:
        log.error(f'No held jobs found in:')
        print(output)
        log.error(f'Used command: {Data.condor_cmd}')
        raise

    return l_job_id
#------------------------------
def run_command(cmd, options):
    if   Data.test == 1:
        log.info(f'{cmd}, {options}')
        return
    elif Data.test == 0:
        log.debug(f'{cmd}, {options}')
        stat = subprocess.run([cmd] + options)
    else:
        log.error(f'Invalid test flag: {Data.test}')
        raise

    if stat.returncode != 0:
        log.error(f'Process returned exit status: {stat.returncode}')
        raise
#------------------------------
def memory():
    '''
    Will change jobs memory
    '''

    for job_id in Data.l_held_job:
        run_command('hep_edit',  [job_id, '-m', str(Data.memory)])
#------------------------------
def release_jobs():
    for job_id in Data.l_held_job:
        run_command('hep_release',  [job_id])
#------------------------------
def main():
    get_args()
    Data.l_held_job = get_held_jobs()

    if Data.memory is not None:
        log.debug('Doing memory edit')
        memory()
    else:
        log.error('Not doing memory edit')
        raise

    release_jobs()
#------------------------------
if __name__ == '__main__':
    main()
