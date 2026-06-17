"""sensor.diele_board_scene — composed scene the ESP consumes.

IMPORTANT: a HA entity STATE is capped at 255 chars. The full scene JSON is therefore
exposed as the ATTRIBUTE `payload` (attributes are not length-capped). The ESP reads it via
an ESPHome `homeassistant` text_sensor with `attribute: payload`.
TODO Phase 2: verify ESPHome text_sensor max length; if the payload is too long, split the
scene per zone into multiple text_sensors. See ../../docs/02-architecture.md.
"""
from __future__ import annotations

import json

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([DieleSceneSensor(coordinator, entry)])


class DieleSceneSensor(CoordinatorEntity, SensorEntity):
    """Short status as state; full scene JSON as attribute `payload`."""

    _attr_has_entity_name = True
    _attr_name = "Scene"
    _attr_icon = "mdi:train"

    def __init__(self, coordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_scene"

    @property
    def native_value(self) -> str:
        # Keep state short (<255). Real status indicator TODO Phase 3.
        return "ok" if self.coordinator.last_update_success else "stale"

    @property
    def extra_state_attributes(self) -> dict:
        return {"payload": json.dumps(self.coordinator.data, separators=(",", ":"))}
