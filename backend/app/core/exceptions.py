from fastapi import HTTPException, status

class DatabaseError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {detail}"
        )

class FileProcessingError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File processing error: {detail}"
        )

class InvalidFileFormatError(FileProcessingError):
    def __init__(self):
        super().__init__(
            "Invalid file format. Only Excel files (.xlsx, .xls) are allowed"
        )

class MalformedDataError(FileProcessingError):
    def __init__(self, detail: str):
        super().__init__(f"Malformed data in file: {detail}")

class TeamError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team error: {detail}"
        )