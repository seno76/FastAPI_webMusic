from datetime import timedelta
from authx import AuthX, AuthXConfig


config = AuthXConfig()
config.JWT_SECRET_KEY = "secret"
config.JWT_ALGORITHM = "HS256"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_COOKIE_NAME = "token"
config.JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=2)


config.JWT_COOKIE_CSRF_PROTECT = True  #
config.JWT_CSRF_IN_COOKIES = True
config.JWT_ACCESS_CSRF_COOKIE_NAME = "csrf_token"
config.JWT_CSRF_METHODS = ["POST", "PUT", "PATCH", "DELETE"]

security = AuthX(config=config)
