from settings_models._combat import SettingsModel, Field


class IntercomSettings(SettingsModel):
    """
    Settings for intercom on kiosk devices
    """
    enabled: bool = Field(..., description="If intercom enabled on kiosk devices")
    phone_number: str = Field(..., description="Phone number for intercom emergency calls")
