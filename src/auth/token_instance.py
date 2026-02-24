from src.auth.service import TokenService
from src.config import Config

email_token_service = TokenService(
    Config.EMAIL_SECRET,
    "email-verification"
)

reset_token_service = TokenService(
    Config.PASSWORD_RESET_SECRET,
    "password-reset"
)
