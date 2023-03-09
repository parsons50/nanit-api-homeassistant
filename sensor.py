"""Nanit API sensor platform for Home Assistant."""

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import TEMP_CELSIUS
import homeassistant.helpers.config_validation as cv

from .client import NanitClient
from .const import DOMAIN, SENSOR_TYPES

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({})

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the Nanit API sensor platform."""
    # Create a Nanit client using the configuration
    nanit_client = NanitClient(
        config_entry.data["username"],
        config_entry.data["password"],
        config_entry.data["api_key"],
    )

    # Create a new sensor entity for each sensor type
    sensors = []
    for sensor_type in SENSOR_TYPES:
        sensors.append(NanitSensor(nanit_client, sensor_type))

    async_add_entities(sensors, True)


class NanitSensor(SensorEntity):
    """Nanit API sensor entity."""

    def __init__(self, nanit_client, sensor_type):
        """Initialize the sensor entity."""
        self._nanit_client = nanit_client
        self._sensor_type = sensor_type
        self._name = SENSOR_TYPES[sensor_type][0]
        self._unit_of_measurement = SENSOR_TYPES[sensor_type][1]
        self._icon = SENSOR_TYPES[sensor_type][2]
        self._state = None

    async def async_update(self):
        """Update the sensor state."""
        latest_data = await self._nanit_client.async_get_latest_data()
        if self._sensor_type == "temperature":
            self._state = latest_data["sensors"]["temperature"]["value"]
        elif self._sensor_type == "humidity":
            self._state = latest_data["sensors"]["humidity"]["value"]
        elif self._sensor_type == "sound":
            self._state = latest_data["sensors"]["sound"]["value"]
        elif self._sensor_type == "motion":
            self._state = latest_data["sensors"]["motion"]["value"]
        elif self._sensor_type == "video":
            self._state = latest_data["streams"]["video"]["url"]

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"{DOMAIN}_{self._sensor_type}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of the sensor."""
        return self._unit_of_measurement

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
