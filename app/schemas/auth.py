from pydantic import BaseModel, EmailStr, field_validator


class BasePasswordModel(BaseModel):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")

        if len(value) > 16:
            raise ValueError("Password must be at most 16 characters long")

        if not any(char.isupper() for char in value):
            raise ValueError(
                "Password must contain at least one uppercase character"
            )

        if not any(char.islower() for char in value):
            raise ValueError(
                "Password must contain at least one lowercase character"
            )

        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")

        return value


class RegistrationModel(BasePasswordModel):
    email: EmailStr


class ResendActivationTokenModel(BaseModel):
    email: EmailStr


class LoginModel(BasePasswordModel):
    email: EmailStr


class TokenRefreshModel(BaseModel):
    refresh_token: str


class LogoutModel(BaseModel):
    refresh_token: str


class ChangePasswordModel(BasePasswordModel):
    old_password: str


class ResetPasswordRequestModel(BaseModel):
    email: EmailStr


class ResetPasswordModel(BaseModel):
    new_password: str
