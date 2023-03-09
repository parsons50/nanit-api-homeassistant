"""Config flow for the Nanit API custom component."""

import logging

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_PASSWORD, CONF_USERNAME

from .client import NanitClient

_LOGGER = logging.getLogger(__name__)


class NanitConfigFlow(config_entries.ConfigFlow, domain="nanit"):
    """Nanit API config flow."""

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}
        if user_input is not None:
            try:
                # Test the connection to the Nanit API with the provided credentials
                client = NanitClient(user_input[CONF_USERNAME], user_input[CONF_PASSWORD], user_input[CONF_API_KEY])
                await client.async_test_connection()

                # Return the configuration data to create the config entry
                return self.async_create_entry(title="Nanit API", data=user_input)

            except Exception as err:
                errors["base"] = "cannot_connect"
                _LOGGER.error("Cannot connect to Nanit API: %s", err)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_USERNAME): str,
                vol.Required(CONF_PASSWORD): str,
                vol.Required(CONF_API_KEY): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors,
        )
