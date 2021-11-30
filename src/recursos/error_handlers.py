from flask_jwt_extended.exceptions import NoAuthorizationError, CSRFError, InvalidHeaderError, JWTDecodeError, WrongTokenError, RevokedTokenError, FreshTokenRequired
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from src import api
from src.servicios.exceptions import ObjetoNoEncontrado, ErrorDeIntegridad


@api.errorhandler(ObjetoNoEncontrado)
def handle_objeto_no_encontrado(e):
    return {"msg":str(e)}, 400

@api.errorhandler(ErrorDeIntegridad)
def handle_error_de_integridad(e):
    return {"msg":str(e)}, 400

@api.errorhandler(NoAuthorizationError)
def handle_error_no_autorizado(e):
    return {"msg":"Falta el token de autorización"}, 401

@api.errorhandler(CSRFError)
def handle_auth_error(e):
    return {"msg": str(e)}, 401

@api.errorhandler(ExpiredSignatureError)
def handle_expired_error(e):
    return {"msg": "El token ha expirado"}, 401

@api.errorhandler(InvalidHeaderError)
def handle_invalid_header_error(e):
    return {"msg": "El header es inválido"}, 422

@api.errorhandler(InvalidTokenError)
def handle_invalid_token_error(e):
    return {"msg": "El token es inválido"}, 422

@api.errorhandler(JWTDecodeError)
def handle_jwt_decode_error(e):
    return {"msg": "No se pudo decodificar el token"}, 422

@api.errorhandler(WrongTokenError)
def handle_wrong_token_error(e):
    return {"msg": "El token es inválido"}, 422

@api.errorhandler(RevokedTokenError)
def handle_revoked_token_error(e):
    return {"msg": "Se revocó el token"}, 401

@api.errorhandler(FreshTokenRequired)
def handle_fresh_token_required(e):
    return {"msg": "Se requiere un token nuevo"}, 401
