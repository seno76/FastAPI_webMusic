from authx import AuthX, AuthXConfig




config = AuthXConfig()
config.JWT_SECRET_KEY = "secret"
config.JWT_ALGORITHM = "HS256"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ACCESS_COOKIE_NAME = "token"


security = AuthX(config=config)