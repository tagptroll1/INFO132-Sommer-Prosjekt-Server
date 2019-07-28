class BaseApiException(Exception):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)


class QuestionAlreadyExistsException(BaseApiException):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
