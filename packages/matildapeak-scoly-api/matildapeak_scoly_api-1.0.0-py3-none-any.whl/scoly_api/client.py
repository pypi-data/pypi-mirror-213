"""The Scoly client API module.
"""
import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests

# Header fields used by Scoly
_SCOLY_LOCATION_HEADER_KEY: str = "X-Scoly-Location"
_SCOLY_LOCATION_API_ACCESS_CODE_HEADER_KEY: str = "X-Scoly-Location-API-Access-Code"
# Scoly URL endpoints
_SCOLY_SENSOR_EVENT_ENDPOINT: str = "/monitor/api/sensor-event/"

_DEFAULT_SENSOR_EVENT_CACHE_SIZE: int = 50
_DEFAULT_SENSOR_EVENT_CACHE_PERIOD_S: int = 360

_LOGGING: logging.Logger = logging.getLogger(__name__)


class Scoly:
    """The Scxoly client API class. Instantiate this class with the Scoly URL (and port)
    and Location that you'll be dealing with."""

    def __init__(
        self,
        *,
        scoly_url: str,
        location: str,
        location_api_access_code: str,
        sensor_event_cache_size: int = _DEFAULT_SENSOR_EVENT_CACHE_SIZE,
        sensor_event_cache_period_s: int = _DEFAULT_SENSOR_EVENT_CACHE_PERIOD_S,
    ):
        """Initialises the class with the Scoly URL (and port)
        and the Location name and API access code."""
        assert scoly_url
        assert location
        assert location_api_access_code
        assert sensor_event_cache_size >= 0
        assert sensor_event_cache_period_s >= 0

        self._scoly_url = scoly_url
        self._location = location
        self._location_api_access_code = location_api_access_code

        # The cache of sensor events, indexed by senor.
        # When the cache size or period has been met
        # the cache is transmitted to scoly.
        self._sensor_event_cache_size = sensor_event_cache_size
        self._sensor_event_cache_period: timedelta = timedelta(
            seconds=sensor_event_cache_period_s
        )
        self._sensor_event_cache: Dict[str, List] = {}
        self._sensor_cache_event_count: int = 0
        self._sensor_cache_timestamp_utc: datetime = datetime.now(timezone.utc)

        self._last_transmit_success: Optional[bool] = None

    def flush(self) -> None:
        """Flushes cached information like the sensor event cache to scoly."""
        now_utc: datetime = datetime.now(timezone.utc)
        _ = self._transmit_sensor_event_cache(now_utc)

    def add_sensor_data(
        self, *, sensor: str, timestamp_utc: datetime, data: Dict[str, Any]
    ) -> None:
        """Adds Given a sensor (name) and its data to the cache. If the cache is full
        or the cache period has been met, the cache is transmitted to scoly.
        """
        assert sensor
        assert timestamp_utc
        assert data

        now_utc: datetime = datetime.now(timezone.utc)

        if sensor not in self._sensor_event_cache:
            self._sensor_event_cache[sensor] = []
        sensor_data = {"timestamp": timestamp_utc.isoformat(), "data": data}
        self._sensor_event_cache[sensor].append(sensor_data)
        self._sensor_cache_event_count += 1

        if (
            self._sensor_cache_event_count >= self._sensor_event_cache_size
            or now_utc - self._sensor_cache_timestamp_utc
            >= self._sensor_event_cache_period
        ):
            _ = self._transmit_sensor_event_cache(now_utc)

    def _transmit_sensor_event_cache(self, now_utc: datetime) -> bool:
        """Transmits the sensor event cache to scoly. If there are transmission errors
        the cache is still cleared, i.e. data is lost.
        """
        assert now_utc

        events: List[Dict[str, Any]] = []
        for sensor, sensor_events in self._sensor_event_cache.items():
            events.append({"sensor": sensor, "events": sensor_events})
        data: Dict[str, Any] = {"events": events}

        url: str = f"{self._scoly_url}{_SCOLY_SENSOR_EVENT_ENDPOINT}"
        headers: Dict[str, str] = {
            _SCOLY_LOCATION_HEADER_KEY: self._location,
            _SCOLY_LOCATION_API_ACCESS_CODE_HEADER_KEY: self._location_api_access_code,
        }

        success: bool = False
        try:
            _ = requests.post(url, json=data, headers=headers, timeout=4)
        except Exception as ex:  # pylint: disable=broad-except
            _LOGGING.warning("Exception=%s", ex)

        # Reset the cache
        self._sensor_event_cache = {}
        self._sensor_cache_event_count = 0
        self._sensor_cache_timestamp_utc = now_utc

        self._last_transmit_success = success
        return self._last_transmit_success
