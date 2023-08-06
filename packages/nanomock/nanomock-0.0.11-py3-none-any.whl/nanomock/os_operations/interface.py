from abc import ABC, abstractmethod
from typing import List, Optional

class OSOperationsInterface(ABC):

    @abstractmethod
    def reset_nodes_data(self, nodes: Optional[List[str]] = None):
        pass

    # Add more method signatures as needed
