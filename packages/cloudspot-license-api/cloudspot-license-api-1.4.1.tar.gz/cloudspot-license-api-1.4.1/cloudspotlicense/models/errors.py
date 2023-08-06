from .base import BaseModel

class Error(BaseModel):

    def __init__(self,
        message=None,
        error_code=None
    ):

        self.message = message
        self.error_code = error_code