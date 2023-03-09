"""Constants for the Nanit API custom component."""

DOMAIN = "nanit"

SENSOR_TYPES = {
    "temperature": ["Temperature", "°C", "mdi:thermometer"],
    "humidity": ["Humidity", "%", "mdi:water-percent"],
    "sound": ["Sound", "dB", "mdi:ear-hearing"],
    "motion": ["Motion", "", "mdi:walk"],
    "video": ["Video", "", "mdi:video"],
}
