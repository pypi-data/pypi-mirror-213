import os
import glob
from pathlib import Path
from typing import List, Optional
from nanomock.internal.utils import get_mock_logger

logger = get_mock_logger()


class OSOperationsMixin:

    def delete_nodes_data(self, path, nodes: Optional[List[str]] = None):

        nodes_to_process = nodes or ['.']
        for node in nodes_to_process:
            node_path = Path(path) / node if nodes else Path(path)

            for filename in glob.glob(str(node_path / '**' / '*.ldb'),
                                      recursive=True):
                try:
                    os.remove(filename)
                except OSError as err:
                    logger.error("Error removing file %s\n%s", filename, err)

    @staticmethod
    def makedirs(path):
        os.makedirs(path, exist_ok=True)
