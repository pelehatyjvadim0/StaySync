from fastapi import HTTPException, status

class StaySyncException(HTTPException):
    message = 'Произошла ошибка!'
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    
    def __init__(self, detail: str | None = None):
        self.custom_detail = detail or self.message
        super().__init__(
            detail=self.custom_detail,
            status_code=self.status_code
        )