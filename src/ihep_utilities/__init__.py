'''
This should put all the imports in the namespace
'''
from typing import TYPE_CHECKING, Type, Any

if TYPE_CHECKING:
    from .job_submitter import JobSubmitter

__all__ = ['JobSubmitter']
# ----------------------
def __getattr__(name : str) -> Type[Any]:
    '''
    Parameters
    -------------
    name: Name of class to import

    Return
    -------------
    Class to be imported
    '''
    if name not in __all__:
        raise ValueError(f'Module {name} not found among: {__all__}')

    if name == 'JobSubmitter':
        from .job_submitter import JobSubmitter
        return JobSubmitter

    raise NotImplementedError(f'Module {name} not implemented')
# -----------------------
