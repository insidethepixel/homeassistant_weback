"""Battery sensor support for Weback Vacuum."""

import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE

from homeassistant.helpers.entity import DeviceInfo, EntityCategory

from . import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up Weback battery sensors."""

    entities = []

    for device in hass.data[DOMAIN]:
        entities.append(WebackVacuumBatterySensor(device))

    async_add_entities(entities, False)


class WebackVacuumBatterySensor(SensorEntity):
    """Representation of Weback battery sensor."""

    _attr_has_entity_name = True
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    _attr_device_class = SensorDeviceClass.BATTERY
    _attr_native_unit_of_measurement = PERCENTAGE
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, device):
        self.device = device

        self.device.subscribe(
            lambda vacdevice: self.schedule_update_ha_state(False)
        )

    @property
    def name(self):
        return f"{self.device.nickname} Battery"

    @property
    def unique_id(self):
        return f"{self.device.name}_battery"

    @property
    def native_value(self):
        return self.device.battery_level

    @property
    def available(self):
        return self.device.is_available

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.device.name)},
            "name": self.device.nickname,
            "manufacturer": "WeBack",
            "model": self.device.sub_type,
        }

