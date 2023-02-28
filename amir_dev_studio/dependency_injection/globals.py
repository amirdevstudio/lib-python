class _Undefined(object):
    def __bool__(self):
        return False


undefined = _Undefined()
default_args = ()
default_kwargs = {}
default_namespace = 'default'
