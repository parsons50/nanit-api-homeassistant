"""Custom component to integrate the Nanit API with Home Assistant."""

import logging

import voluptuous as vol
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import CONF_API_KEY, CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .client import NanitClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_USERNAME): cv.string,
                vol.Required(CONF_PASSWORD): cv.string,
                vol.Required(CONF_API_KEY): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Nanit API custom component."""
    if DOMAIN not in config:
        return True

    # Set up the Nanit API using the configuration
    nanit_client = NanitClient(
        config[DOMAIN][CONF_USERNAME], config[DOMAIN][CONF_PASSWORD], config[DOMAIN][CONF_API_KEY]
    )

    # Create a config entry for the Nanit API
    hass.async_create_task(
        hass.config_entries.flow.async_init(
            DOMAIN, context={"source": SOURCE_IMPORT}, data=config[DOMAIN]
        )
    )

    # Set up the Nanit API switch platform
    hass.async_create_task(
        hass.config_entries.async_setup_platforms(ConfigEntry.entry_id, ["switch"], {DOMAIN: nanit_client})
    )

    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Set up the Nanit API config entry."""
    # Create a Nanit client using the configuration
    nanit_client = NanitClient(
        config_entry.data[CONF_USERNAME], config_entry.data[CONF_PASSWORD], config_entry.data[CONF_API_KEY]
    )

    # Set up the Nanit API
