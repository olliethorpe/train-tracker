from pydantic import BaseModel, Field
from typing import List, Optional


class LocationDetail(BaseModel):
    realtime_activated: bool = Field(alias="realtimeActivated")
    tiploc: str
    crs: str
    description: str
    gbtt_booked_arrival: str = Field(alias="gbttBookedArrival")
    gbtt_booked_departure: str = Field(alias="gbttBookedDeparture")
    origin: List[dict]
    destination: List[dict]
    is_call: bool = Field(alias="isCall")
    is_public_call: bool = Field(alias="isPublicCall")
    realtime_arrival: str = Field(alias="realtimeArrival")
    realtime_arrival_actual: bool = Field(alias="realtimeArrivalActual")
    realtime_departure: str = Field(alias="realtimeDeparture")
    realtime_departure_actual: bool = Field(alias="realtimeDepartureActual")
    platform: Optional[str] = Field(None)
    platform_confirmed: Optional[bool] = Field(None, alias="platformConfirmed")
    platform_changed: Optional[bool] = Field(None, alias="platformChanged")
    service_location: Optional[str] = Field(None, alias="serviceLocation")
    display_as: str = Field(alias="displayAs")


class OriginDestination(BaseModel):
    tiploc: str
    description: str
    working_time: str = Field(alias="workingTime")
    public_time: str = Field(alias="publicTime")


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
