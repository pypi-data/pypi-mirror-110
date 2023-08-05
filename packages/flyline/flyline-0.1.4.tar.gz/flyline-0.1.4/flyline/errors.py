class FlylineBadRequest(Exception):
    pass


class AuthenticationFailed(Exception):
    def __init__(self, *args, **kwargs):
        self.message = "Authentication Failed"
        super().__init__(self.message)


class FlylineItemNotFound(Exception):
    def __init__(self, *args, **kwargs):
        self.message = "Requested data not found"
        super().__init__(self.message)


class FlylineServerError(Exception):
    def __init__(self, *args, **kwargs):
        self.message = "FlylineServer Error"
        super().__init__(self.message)


class FlylinePayloadError(Exception):
    def __init__(self, *args, **kwargs):
        self.message = "Payload Error"
        super().__init__(self.message)
