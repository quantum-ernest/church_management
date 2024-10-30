import shutil
import uuid

from fastapi import HTTPException, UploadFile, status


def save_file(file: UploadFile | None = None) -> str:
    if file:
        if file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type"
            )
        filename = f"{uuid.uuid4()}_{file.filename.replace(' ', '')}"
        file_path = f"assets/{filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    else:
        filename = None
    return filename
