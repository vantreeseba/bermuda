"""Sensor platform for Bermuda BLE Trilateration."""
from collections.abc import Mapping
from typing import Any

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import BermudaDataUpdateCoordinator
from .const import DOMAIN
from .entity import BermudaEntity

# from .const import DEFAULT_NAME
# from .const import ICON
# from .const import SENSOR


async def async_setup_entry(
    hass: HomeAssistant,
    entry: config_entries.ConfigEntry,
    async_add_devices: AddEntitiesCallback,
) -> None:
    """Setup sensor platform."""
    coordinator: BermudaDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    # We simply trawl the devices to set up sensors.
    entities = []
    for device in coordinator.devices.values():
        if device.create_sensor:
            entities.append(BermudaSensor(coordinator, entry, device.address))
    # async_add_devices([BermudaSensor(coordinator, entry)])
    async_add_devices(entities, True)


class BermudaSensor(BermudaEntity):
    """bermuda Sensor class."""

    @property
    def has_entity_name(self) -> bool:
        return True

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Area"

    @property
    def state(self):
        """Return the state of the sensor."""
        # return self.coordinator.data.get("body")
        return self._device.area_name

    # @property
    # def icon(self):
    #    """Return the icon of the sensor."""
    #    return ICON

    @property
    def device_class(self):
        """Return de device class of the sensor."""
        return "bermuda__custom_device_class"

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        return {
            "last_seen": self.coordinator.dt_mono_to_datetime(self._device.last_seen),
            "area_id": self._device.area_id,
            "area_name": self._device.area_name,
            "area_distance": self._device.area_distance,
        }
