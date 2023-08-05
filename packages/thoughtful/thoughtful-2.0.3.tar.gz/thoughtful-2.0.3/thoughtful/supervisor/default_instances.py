"""
Default instances for dynamic runs.

Typically, developers will only run one digital worker on a Python
runtime, and it is tricky to initialize an object and pass that object
instance down into other files in a project for a custom decorator.
This package provides a set of default instances of objects and contexts
for dynamic runs.

This file initializes a shared `ReportBuilder` object, which is used
individual steps and sub steps to share state.

See the quickstart for, well, quickstarts on each of these methods.
"""

import logging
import pathlib
from typing import Union

from thoughtful.environment_variables import EnvironmentVariables
from thoughtful.supervisor.event_bus import EventBus
from thoughtful.supervisor.main_context import MainContext
from thoughtful.supervisor.manifest import Manifest
from thoughtful.supervisor.reporting.report_builder import ReportBuilder
from thoughtful.supervisor.step_context import StepContext
from thoughtful.supervisor.step_decorator_factory import create_step_decorator
from thoughtful.supervisor.streaming.streamer import Streamer

logger = logging.getLogger(__name__)

shared_bus = EventBus()

#: A shared ``ReportBuilder`` for steps and step contexts to add step reports
#: to.
report_builder = ReportBuilder()

#: Use this decorator on your own functions to mark what workflow step each
#: Python function is matched to.
step = create_step_decorator(report_builder=report_builder, event_bus=shared_bus)

#: Use this function to mark a step as failed.
#: This is just a shortcut for ``set_step_status(step_id, "failed")``.
#: Exposes ``report_builder.fail_step``.
fail_step = report_builder.fail_step

#: Expose the report builder's ability to override a step's status as a
#: top-level call. Exposes ``report_builder.set_step_status``.
set_step_status = report_builder.set_step_status

#: Expose the report builder's ability to override a step's record's status as a
#: top-level call. Exposes ``report_builder.set_record_status``.
set_record_status = report_builder.set_record_status

#: Expose the report builder's ability to override a run's status as a
#: top-level call. Exposes ``report_builder.set_run_status``.
set_run_status = report_builder.set_run_status


# noinspection PyPep8Naming
class step_scope(StepContext):
    """
    It's a context manager that provides a scope for a step using the
    aforementioned default instances of ``report_builder`` and ``recorder``.
    """

    def __init__(self, step_id: str):
        """
        A default `StepContext` that uses the root level `report_builder` and
        `recorder`.

        Args:
            *step_id: The list of integers that represent the step ID.
        """
        super().__init__(
            builder=report_builder,
            step_id=step_id,
            event_bus=shared_bus,
        )


# noinspection PyPep8Naming
class supervise(MainContext):
    """
    It's a context manager that provides a scope for the main context using the
    aforementioned default instances of ``report_builder`` and ``recorder``.
    """

    def __init__(
        self,
        manifest: Union[Manifest, str, pathlib.Path] = "manifest.yaml",
        output_dir: Union[str, pathlib.Path] = "output/",
        *args,
        **kwargs,
    ):
        """
        A default `MainContext` that uses the root level `report_builder` and
        `recorder`.

        Args:
            *args: Extra arguments to the `MainContext` constructor.
            **kwargs: Extra keyword arguments to the `MainContext` constructor.
            manifest (str): The digital worker's manifest definition
            output_dir (str): Where the work report and drift report will
                be written to
        """
        super().__init__(
            report_builder=report_builder,
            manifest=manifest,
            output_dir=output_dir,
            upload_uri=EnvironmentVariables().s3_bucket_uri,
            event_bus=shared_bus,
            *args,
            **kwargs,
        )


if __name__ == "__main__":
    from thoughtful.supervisor.event_bus import RunStatusChangeEvent
    from thoughtful.supervisor.reporting.status import Status

    _streamer = Streamer.from_encoded_tokens(
        run_id=EnvironmentVariables().run_id,
        callback_url=EnvironmentVariables().callback_url,
        # The JWT token is set by the user later. If steamer is set to None,
        # then the step decorators can't be updated to stream if streamer is
        # changed to a new instance.
        #
        # See CX-2368 for the proper fix by lifting the streamer out of the contexts
        access_token="",
        refresh_token="",
        refresh_url="",
    )
    shared_bus.subscribe(_streamer.handle_event)
    test = RunStatusChangeEvent(status=Status.RUNNING)
    shared_bus.emit(test)
