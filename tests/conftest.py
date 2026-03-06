'''
File needed by pytest
'''
from _pytest.config import Config
from dmu.logging.log_store import LogStore

# ------------------------------
def pytest_configure(config : Config):
    '''
    This will run before any test by pytest
    '''
    _config = config

    LogStore.set_level('ihep_utilities:job_submitter', 10)
# ------------------------------
