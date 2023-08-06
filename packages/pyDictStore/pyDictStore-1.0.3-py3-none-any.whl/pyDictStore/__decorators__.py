from .__events__ import PropertyChangedEvent
#from functools import wraps
import functools


def storage(cls):
    @functools.wraps(cls, updated=())
    class storage_wrap(cls):
        def __init__(self, *args, **kwargs) -> None:
            self.wrapper = cls
            self.wrapper.__storage__ = {}
            self.wrapper.PropertyChanged = PropertyChangedEvent()
            #Add storageSet and default(none) to properties if not already present
            for name in [p for p in dir(self.wrapper) if isinstance(getattr(self.wrapper,p),property)]:
                prop = getattr(self.wrapper,name)
                fget = (prop.fget 
                        if prop.fget.__qualname__ == 'default.__call__.<locals>.wrapper'
                        else default(None)(prop.fget)
                        )
                fset = (prop.fset 
                        #if prop.fset.__qualname__ == 'storageSetter.<locals>.wrapper'
                        if isinstance(prop.fset,storageSetter)
                        else storageSetter(prop.fset)
                        )
                setattr(self.wrapper, name, property(fget, fset, prop.fdel))
            #Call Wrapped Class' initilizer
            super().__init__(*args,**kwargs)
            
            

        # def __call__(self, *args, **kwargs):
        #     # #Add storage variable to the object instance
        #     def decorate(fcn):
        #         def __new__(wrapper,*args, **kwargs):
        #             oCls = super(type(wrapper), wrapper).__new__(wrapper)
        #             oCls.__storage__ = {}
        #             wrapper.PropertyChanged = PropertyChangedEvent()
        #             from typing import cast
        #             return cast(type(wrapper),oCls)
        #         return __new__
        #     self.wrapper.__new__ = decorate(self.wrapper.__new__)
        #     #Add storageSet and default(none) to properties if not already present
        #     for name in [p for p in dir(self.wrapper) if isinstance(getattr(self.wrapper,p),property)]:
        #         prop = getattr(self.wrapper,name)
        #         fget = (prop.fget 
        #                 if prop.fget.__qualname__ == 'default.__call__.<locals>.wrapper'
        #                 else default(None)(prop.fget)
        #                 )
        #         fset = (prop.fset 
        #                 #if prop.fset.__qualname__ == 'storageSetter.<locals>.wrapper'
        #                 if isinstance(prop.fset,storageSetter)
        #                 else storageSetter(prop.fset)
        #                 )
        #         setattr(self.wrapper, name, property(fget, fset, prop.fdel)) 
        #     return self.wrapper(*args,**kwargs)
    return storage_wrap

class default:
    def __init__(self, value=None) -> None:
        self.value = value

    def __call__(self, function):
        def wrapper(*args, **kwargs):
            obj = args[0]
            v = self.value
            if hasattr(obj,'__storage__'): 
                strg = getattr(obj, '__storage__')
                if not function.__name__ in strg:
                    strg[function.__name__] = self.value
                v = strg[function.__name__]
            vOverride = function(*args, **kwargs)
            return v if vOverride is None else vOverride
        return wrapper

class storageSetter:
    def __init__(self, function) -> None:
        self.function = function

    def __call__(self, *args, **kwargs):
        obj = args[0]
        value = args[1]
        oValue = self.function(*args, **kwargs)
        if hasattr(obj,'__storage__'): 
            strg = getattr(obj, '__storage__')
            oldValue=getattr(obj, self.function.__name__)
            strg[self.function.__name__] = value if oValue is None else oValue
            if hasattr(obj,'PropertyChanged'):
                obj.PropertyChanged(
                            obj
                            ,self.function.__name__
                            , oldValue
                            , getattr(obj, self.function.__name__) #newValue
                            )