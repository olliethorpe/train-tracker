from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import time


class OriginDestination(BaseModel):
    tiploc: str
    description: str
    working_time: str = Field(alias="workingTime")
    public_time: str = Field(alias="publicTime")


class LocationDetail(BaseModel):
    realtime_activated: bool = Field(alias="realtimeActivated")
    tiploc: str
    crs: str
    description: str
    scheduled_arrival: str = Field(alias="gbttBookedArrival")
    scheduled_departure: str = Field(alias="gbttBookedDeparture")
    origin: List[OriginDestination]
    destination: List[OriginDestination]
    is_call: bool = Field(alias="isCall")
    is_public_call: bool = Field(alias="isPublicCall")
    actual_arrival: str = Field(alias="realtimeArrival")
    realtime_arrival_enabled: bool = Field(alias="realtimeArrivalActual")
    actual_departure: str = Field(alias="realtimeDeparture")
    realtime_departure_enabled: bool = Field(alias="realtimeDepartureActual")
    platform: Optional[str] = Field(None)
    platform_confirmed: Optional[bool] = Field(None, alias="platformConfirmed")
    platform_changed: Optional[bool] = Field(None, alias="platformChanged")
    service_location: Optional[str] = Field(None, alias="serviceLocation")
    display_as: str = Field(alias="displayAs")

    @field_validator('scheduled_arrival', 'scheduled_departure', 'actual_arrival', 'actual_departure')
    def convert_hhmm_to_time(cls, value: str) -> time:
        """Convert 'HHMM' string to a time object."""
        if len(value) == 4 and value.isdigit():
            return time(int(value[:2]), int(value[2:]))
        raise ValueError(f"Invalid time format: {value}")


class Service(BaseModel):
    location_detail: LocationDetail = Field(alias="locationDetail")
    service_uid: str = Field(alias="serviceUid")
    run_date: str = Field(alias="runDate")
    train_identity: str = Field(alias="trainIdentity")
    running_identity: str = Field(alias="runningIdentity")
    atoc_code: str = Field(alias="atocCode")
    atoc_name: str = Field(alias="atocName")
    service_type: str = Field(alias="serviceType")
    is_passenger: bool = Field(alias="isPassenger")
