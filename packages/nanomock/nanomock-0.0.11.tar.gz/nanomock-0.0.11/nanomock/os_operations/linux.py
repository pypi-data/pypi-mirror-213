from .interface import OSOperationsInterface
from .mixin import OSOperationsMixin

class LinuxOSOperations(OSOperationsInterface, OSOperationsMixin):
    pass
