import glob
import os
from typing import List

try: 
    from src.config import FILEEXTENSIONS
except:
    from config import FILEEXTENSIONS
    
class DocumentFinder:
    def __init__(self, path: str) -> None:
        """
            Initialize the DocumentFinder object.

            Args:
                path (str): The directory path to search for documents.
        """
        self.path = path
        self.found_documents = []
        self.extensions = FILEEXTENSIONS
        
        for ext in self.extensions:
            self.found_documents.extend(glob.glob(os.path.join(self.path, ext)))

    def get_documents(self) -> List[str]:
        """
            Get the list of all found document paths.

            Returns:
                List[str]: A list of paths to all found documents.
        """
        return self.found_documents