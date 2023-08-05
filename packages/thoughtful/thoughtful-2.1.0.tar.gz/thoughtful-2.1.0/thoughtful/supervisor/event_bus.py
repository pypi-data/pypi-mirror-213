from dataclasses import dataclass, field
from typing import Callable, Union

from thoughtful.supervisor.manifest import Manifest
from thoughtful.supervisor.reporting.status import Status
from thoughtful.supervisor.reporting.step_report import StepReport


@dataclass
class StepReportChangeEvent:
    step_report: StepReport


@dataclass
class NewManifestEvent:
    manifest: Manifest


@dataclass
class RunStatusChangeEvent:
    status: Status


@dataclass
class ArtifactsUploadedEvent:
    output_uri: str


Event = Union[
    StepReportChangeEvent,
    NewManifestEvent,
    RunStatusChangeEvent,
    ArtifactsUploadedEvent,
]


@dataclass
class EventBus:
    subscribers: list = field(default_factory=list)

    def subscribe(self, callback: Callable[[Event], None]):
        self.subscribers.append(callback)

    def emit(self, event: Event):
        for subscriber in self.subscribers:
            subscriber(event)
