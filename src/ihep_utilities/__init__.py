'''
This should put all the imports in the namespace
'''

__all__ = ['JobSubmitter']
# ----------------------
def __getattr__(name : str) -> None:
    '''
    Parameters
    -------------
    name: Name of module to import
    '''
    if name not in __all__:
        raise ValueError(f'Module {name} not found among: {__all__}')

    if name == 'JobSubmitter':
        from .job_submitter import JobSubmitter
        return JobSubmitter

    raise NotImplementedError(f'Module {name} not implemented')
# -----------------------
