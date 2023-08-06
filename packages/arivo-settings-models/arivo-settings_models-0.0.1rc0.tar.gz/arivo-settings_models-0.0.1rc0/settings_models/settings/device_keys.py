from datetime import datetime

from pydantic import Field

from settings_models.validators import timezone_validator
from settings_models._combat import SettingsModel


class PairingKey(SettingsModel):
    """
    Pairing key data and metadata
    """
    key: str = Field(..., description="Pairing key")
    created_at: datetime = Field(..., description="Creation time of pairing key")
    revision: int = Field(..., ge=0, description="Revision of pairing key")

    created_at_validator = timezone_validator("created_at")
