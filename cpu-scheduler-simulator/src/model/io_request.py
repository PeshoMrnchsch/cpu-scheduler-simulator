from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.model.process import Process
    from src.devices.io_device import IODevice


class IORequest:
    def __init__(
        self,
        process: Process,
        execution_point: int,
        duration: int,
        device: IODevice
    ):
        self.process = process
        self.device = device
        self.execution_point = execution_point
        self.duration = duration

        self.remaining_time = duration

        if duration <= 0:
            raise ValueError("Duration must be positive")

    def is_complete(self) -> bool:
        """
        Return whether this I/O request has completed.
        """
        return self.remaining_time <= 0

    def reset(self) -> None:
        """
        Reset the request for another simulation run.
        """
        self.remaining_time = self.duration

    def __repr__(self) -> str:
        return (
            f"IORequest("
            f"PID: {self.process.pid}, "
            f"DEVICE_TYPE: {self.device.device_type}, "
            f"EXEC POINT: {self.execution_point}"
            f")"
        )