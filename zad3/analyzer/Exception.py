class OnlyLiesSpeaking(Exception):
    def __init__(self):
        super(
            Exception, self).__init__(
            "You can't answer for "
            "simple question so you are speaking only lies")


class RequestError(Exception):
    def __init__(self):
        super(Exception, self).__init__("There is some problem with requests")
