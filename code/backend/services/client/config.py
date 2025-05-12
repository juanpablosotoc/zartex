class Config:
    SECRET_KEY = "secret"
    JWT_ALGORITHM = "HS256"

    # Database
    DATABASE_URL = "sqlite+aiosqlite://"
    ECHO_SQL = True

    # Logging
    DEBUG_LOGS = True
