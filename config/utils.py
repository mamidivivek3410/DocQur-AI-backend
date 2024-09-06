from fastapi import HTTPException
import traceback
def handle_controller_error(error:HTTPException):
    if hasattr(error,'details'):
        for err in error.details:
            if hasattr(err,'message'):
                err.message = err.message.replace('"','')
                raise ValueError(err.message)
    else:
        raise ValueError(str(error).split(": ")[1])


def create_response(status, msg, payload):
    response_data = {
        "status": status,
        "message": msg,
        "data": payload,
    }
    return response_data

def create_error(status, error, options=None):
    if options is None:
        options = {}

    message = str(error) if error else "Error Occurred"
    stack_trace = traceback.format_exc()

    if 'returnStackTrace' in options and options['returnStackTrace']:
        other = {"error": message, "stack_trace": stack_trace}
    else:
        other = {"error": message}

    return create_response( status, message, {})