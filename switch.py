"""Nanit API switch platform for Home Assistant."""

from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchEntity
import homeassistant.helpers.config_validation as cv

from .client import NanitClient

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    cv.Required("name"): cv.string,
    cv.Required("command"): cv.string,
})


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Nanit API switch platform."""
    # Create a Nanit client using the configuration
    nanit_client = NanitClient(
        config_entry.data["username"],
        config_entry.data["password"],
        config_entry.data["api_key"],
    )

    # Create a new switch entity for the command
    switch = NanitSwitch(nanit_client, config_entry.data["name"], config_entry.data["command"])
    async_add_entities([switch], True)


class NanitSwitch(SwitchEntity):
    """Nanit API switch entity."""

    def __init__(self, nanit_client, name, command):
        """Initialize the switch entity."""
        self._nanit_client = nanit_client
        self._name = name
        self._command = command
        self._state = False

    async def async_update(self):
        """Update the switch state."""
        # The Nanit API doesn't provide a way to get the state of the switch,
        # so we just assume it's always off

    @property
    def unique_id(self):
        """Return a unique ID for the switch."""
        return f"{self._name}_{self._command}"

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return the state of the switch."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        if self._command == "light_on":
            await self._nanit_client.async_turn_on_light()
        elif self._command == "white_noise_on":
            await self._nanit_client.async_turn_on_white_noise()
        self._state = True

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        if self._command == "light_on":
            await self._nanit_client.async_turn_off_light()
        elif self._command == "white_noise_on":
            await self._nanit_client.async_turn_off_white_noise()
        self._state = False
