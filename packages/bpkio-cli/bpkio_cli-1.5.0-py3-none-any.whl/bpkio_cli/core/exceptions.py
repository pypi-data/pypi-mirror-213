class BroadpeakIoCliError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)
        
class UnexepctedContentError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)