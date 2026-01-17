from fasthtml import *


def bad_request_error(message=""):
    return JSONResponse(
        {"status": "Bad Request", "message": message, "response": None}, 400
    )


def unathorized_error(message=""):
    return JSONResponse(
        {"status": "Unauthorized", "message": message, "response": None}, 401
    )


def not_found_error(message=""):
    return JSONResponse(
        {"status": "Not Found", "message": message, "response": None}, 404
    )


def bad_method():
    return JSONResponse(
        {
            "status": "Method Not Allowed",
            "message": "Nedozvoljena HTTP metoda.",
            "response": None,
        },
        405,
    )


def internal_error(exc, cod):
    return JSONResponse(
        {"status": "Internal Error", "message": "Greška na serveru.", "response": None},
        500,
    )
