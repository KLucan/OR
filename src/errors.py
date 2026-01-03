from fasthtml import *

def internal_error(exc, cod):
    return JSONResponse({
        "status": "Internal Error",
        "message": "Greška na serveru.",
        "response": None
    }, 500)

def not_found_error(message=""):
    return JSONResponse({
        "status": "Not Found",
        "message": message,
        "response": None
    }, 404)

def bad_request_error(message=""):
        return JSONResponse({
        "status": "Bad Request",
        "message": message,
        "response": None
    }, 400)