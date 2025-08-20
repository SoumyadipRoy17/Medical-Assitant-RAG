import os 
import shutil
from fastapi import UploadFile

import tempfile

UPLOAD_DIR ="./uploaded_docs"

def save_uploaded_files(files:list[UploadFile]) -> list[str]:
    """
    Save uploaded files to the server's upload directory.
    
    Args:
        files (list[UploadFile]): List of uploaded files.
        
    Returns:
        list[str]: List of file paths where the files are saved.
    """
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)
    
    file_paths = []
    for file in files:
        file_location = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)
        file_paths.append(file_location)
    
    return file_paths
