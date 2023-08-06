# Copyright 2023 Iguazio
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import typing

import pydantic

import igz_mgmt.schemas


class AffectedResource(igz_mgmt.schemas._Base):
    """Affected resource."""

    type: str
    id_str: str
    id: int
    name: str


class ParametersText(igz_mgmt.schemas._Base):
    """Parameters text."""

    name: str
    value: str


class ParametersUint64(igz_mgmt.schemas._Base):
    """Parameters uint64."""

    name: str
    value: int


class ManualEventSchema(igz_mgmt.schemas._Base):
    """Manual event schema."""

    source: str = pydantic.Field(
        description="The originator of the event, in the form of a service ID (e.g. igz0.vn.3)"
    )
    kind: str = pydantic.Field(
        description="A string in dot notation representing which event occurred"
    )
    timestamp_uint64: typing.Optional[int] = pydantic.Field(
        description="64bit timestamp indicating when the event occurred. if 0 and timestampIso8601 is empty,"
        " the timestamp will added upon reception of the first platform step.",
        default=None,
    )
    timestamp_iso8601: typing.Optional[str] = pydantic.Field(
        description="string representation of the timestamp, in ISO8601 format",
        default=None,
    )
    timestamp_uint64_str: typing.Optional[str] = pydantic.Field(
        description="Same as 'timestampUint64' but in string form",
        default=None,
    )
    parameters_uint64: typing.Optional[typing.List[ParametersUint64]] = pydantic.Field(
        description="A list of parameters, each containing a name and an int value",
        default=None,
    )
    parameters_text: typing.Optional[typing.List[ParametersText]] = pydantic.Field(
        description="A list of parameters, each containing a name and a string value",
        default=None,
    )
    description: typing.Optional[str] = pydantic.Field(
        description="A description of the event", default=None
    )
    severity: typing.Optional[igz_mgmt.constants.EventSeverity] = pydantic.Field(
        description="The severity of the event, Required if event kind doesn't exists in the system",
        default=None,
    )
    tags: typing.Optional[typing.List[str]] = pydantic.Field(
        description="A list of tags to associate with the event, used for later filtering of events/alerts",
        default=None,
    )
    affected_resources: typing.Optional[typing.List[AffectedResource]] = pydantic.Field(
        description="Resources affected by this event",
        default=None,
    )
    classification: typing.Optional[
        igz_mgmt.constants.EventClassification
    ] = pydantic.Field(
        description="The classification of the event, Required if event kind doesn't exists in the system",
        default=None,
    )
    system_event: typing.Optional[bool] = pydantic.Field(
        description="Whether this event is a system event or not",
        default=False,
    )
    visibility: typing.Optional[igz_mgmt.constants.EventVisibility] = pydantic.Field(
        description="Whom the event will be visible to", default=None
    )


class ManualEventRequest(igz_mgmt.schemas._Base):
    """Manual event request."""

    type: str = pydantic.Field("event", const=True)
    attributes: ManualEventSchema
