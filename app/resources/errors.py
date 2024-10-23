from werkzeug.exceptions import HTTPException

class InternalServerError(HTTPException):
    code = 500
    description = "Sesuatu yang tidak terduga terjadi, Internal Server Error"

class EmailAlreadyExistsError(HTTPException):
    code = 400
    description = "Pengguna dengan alamat e-mail tersebut sudah terdaftar"

class EmailDoesnotExistsError(HTTPException):
    code = 400
    description = "Tidak ada pengguna dengan alamat e-mail tersebut"

class EmailIsInvalidError(HTTPException):
    code = 400
    description = "Alamat e-mail tidak valid"

class PasswordLengthError(HTTPException):
    code = 400
    description = "Panjang password minimal 6 karakter"

class BadTokenError(HTTPException):
    code = 403
    description = "Token tidak valid"

class ExpiredTokenError(HTTPException):
    code = 401
    description = "Token sudah kadaluarsa"

class UnauthorizedError(HTTPException):
    code = 401
    description = "Alamat email atau password tersebut salah!"