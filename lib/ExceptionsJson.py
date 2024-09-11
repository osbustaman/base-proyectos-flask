
class ExceptionsJson(Exception):
    def __init__(self, message={}):
        self.message = message
        super().__init__(self.message)


class Responses():
    @classmethod
    def create_response(self, message, success, status_code):

        return {
            'message': message,
            'success': success
        }, status_code
