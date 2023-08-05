class idevisionerror(Exception):
    pass

class ApiError(idevisionerror):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return str(self.message)

class Banned(idevisionerror):
    def __init__(self, message="You have been banned from the api. Please contact IAmTomahawkx#1000 on discord to appeal."):
        self.message = message

    def __str__(self):
        return str(self.message)

class MaxRetryReached(idevisionerror):
    def __init__(self, retry_times):
        self.retry_times = retry_times

    def __str__(self):
        return f"The maximum {self.retry_times} times to retry has been reached!"

class InvalidRtfmLibrary(idevisionerror):
    def __init__(self, library):
        self.library = library

    def __str__(self):
        return f"{self.library} is not a valid rtfm library"

class InvalidRtfsLibrary(idevisionerror):
    def __init__(self, library, *allowed):
        self.library = library
        self.allowed = allowed

    def __str__(self):
        return f"{self.library} is not a valid rtfs library. It must be one of {', '.join(self.allowed)}"

class InvalidToken(idevisionerror):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class TagAlreadyAssigned(idevisionerror):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
    
class NotFound(idevisionerror):
    def __str__(self):
        return "404 Not Found"