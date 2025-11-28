"""
Domain entities for Dolorestec Auth.

Following Domain-Driven Design principles.
"""

from datetime import UTC, datetime

from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict, EmailStr, Field

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    """User domain entity."""

    id: int | None = None
    email: EmailStr = Field(..., description="User email address")
    hashed_password: str = Field(..., description="Bcrypt hashed password")
    is_active: bool = Field(default=True, description="User account status")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Account creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), description="Last update timestamp"
    )

    model_config = ConfigDict(from_attributes=True)

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(UTC)

    def deactivate(self) -> None:
        """Deactivate user account."""
        self.is_active = False
        self.update_timestamp()

    def activate(self) -> None:
        """Activate user account."""
        self.is_active = True
        self.update_timestamp()

    def verify_password(self, password: str) -> bool:
        """Verify plain password against hashed password."""
        return pwd_context.verify(password, self.hashed_password)  # type: ignore[no-any-return]

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash plain password."""
        return pwd_context.hash(password)  # type: ignore[no-any-return]


class UserCreate(BaseModel):
    """Schema for creating a new user."""

    email: EmailStr
    password: str = Field(..., min_length=8, description="Plain text password")


class UserUpdate(BaseModel):
    """Schema for updating user information."""

    email: EmailStr | None = None
    is_active: bool | None = None


class UserInDB(User):
    """User as stored in database."""
