
class ConstError(PermissionError):
    """
    Modify exception
    """
    pass

class ConstFixedError(ConstError):
    """
    Case exception
    """
    pass

class ConstCaseError(ConstError):
    """
    Case exception
    """
    pass


class _bdconst(object):
    def __init__(self):
        self.__dict__["__FIX_LOCKER"] = True

    
    def unlock(self,):
        """
        Modify lock release
        """
        self.__dict__["__FIX_LOCKER"] = False
    

    def locked(self,):
        """
        Modify lock require
        """
        self.__dict__["__FIX_LOCKER"] = True
    

    @property
    def lock(self,) -> bool:
        """
        Get lock results
        """
        return self.__dict__["__FIX_LOCKER"]
    

    def __setattr__(self, name: str, value):
        """
        Constant setting
        """
        if name in self.__dict__ and self.lock:
            raise ConstFixedError("Can't change const `%s`" % name)
        
        if not name.isupper():
            raise ConstCaseError("Const name `%s` is not all uppercase" % name)
        
        self.__dict__[name] = value
    

    def __delattr__(self, name: str):
        """
        Constant deletion
        """
        pass
    

    def __getattr__(self, name):
        """
        Returns None for non-existent constants
        """
        return None

import sys
# Add constant instance to system module
sys.modules[__name__] = _bdconst()