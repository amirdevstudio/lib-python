def copy_self_and_apply_mutator_fn(self, fn: callable, *args, **kwargs):
    if not hasattr(self, '__copy__'):
        raise Exception(f'Object of type {type(self)} does not have a __copy__ method.')
    
    self_copy = self.__copy__()
    fn(self_copy, *args, **kwargs)
    return self_copy
