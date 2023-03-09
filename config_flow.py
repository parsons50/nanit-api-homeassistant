"""Config flow for the Nanit API custom component."""

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant

from .client import NanitClient

# Define the schema for the configuration data
CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
        vol.Required(CONF_API_KEY): str,
    }
)


class NanitConfigFlow(config_entries.ConfigFlow, domain="nanit"):
    """Nanit API configuration flow."""

    async def async_step_user(self, user_input=None):
        """Handle a user-initiated configuration flow."""
        errors = {}

        # If the user has submitted data, validate it
        if user_input is not None:
            try:
                # Create a Nanit client to validate the credentials
                nanit_client = NanitClient(
                    user_input[CONF_USERNAME], user_input[CONF_PASSWORD], user_input[CONF_API_KEY]
                )
                await nanit_client.async_get_latest_data()

                # Credentials are valid, create the config entry
                return self.async_create_entry(title="Nanit API", data=user_input)
            except Exception:
                # Invalid credentials
                errors["base"] = "invalid_credentials"

        # Display the configuration form to the user
        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_SCHEMA,
            errors=errors,
        )


async def async_get_or_create_config_entry(hass: HomeAssistant, config: dict):
    """Get or create a Nanit API config entry."""
    # Check if the config entry already exists
    existing_entries = hass.config_entries.async_entries("nanit")
    for entry in existing_entries:
        if (
            entry.data.get(CONF_USERNAME) == config[CONF_USERNAME]
            and entry.data.get(CONF_PASSWORD) == config[CONF_PASSWORD]
            and entry.data.get(CONF_API_KEY) == config[CONF_API_KEY]
        ):
            # Config entry already exists
            return entry

    # Config entry does not exist, create a new one
    config_entry = await hass.config_entries.flow.async_init(
        "nanit", context={"source": "import"}, data=config
    )
    return config_entry
