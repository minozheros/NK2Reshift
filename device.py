import typing
from itertools import zip_longest

from ableton.v3.base import depends
from ableton.v3.control_surface.components import (
    DeviceComponent as DeviceComponentBase,
)
from ableton.v3.control_surface.components import (
    DeviceParametersComponent as DeviceParametersComponentBase,
)
from ableton.v3.control_surface.controls import (
    MappedSensitivitySettingControl,
    control_list,
)

from .elements import NUM_TRACKS


class HybridDeviceParametersComponent(DeviceParametersComponentBase):
    controls: typing.Any = control_list(
        MappedSensitivitySettingControl, control_count=NUM_TRACKS * 2
    )

    def set_parameter_controls(self, encoders):
        controls = list(self.controls)[:NUM_TRACKS]
        for control, encoder in zip_longest(controls, encoders or []):
            control.set_control_element(encoder)
        self._connect_parameters()

    def set_secondary_parameter_controls(self, encoders):
        controls = list(self.controls)[NUM_TRACKS:]
        for control, encoder in zip_longest(controls, encoders or []):
            control.set_control_element(encoder)
        self._connect_parameters()


class DeviceComponent(DeviceComponentBase):
    @depends(show_message=None)
    def __init__(self, *a, show_message=None, **k):
        super().__init__(
            *a,
            parameters_component_type=HybridDeviceParametersComponent,
            bank_size=NUM_TRACKS * 2,
            show_message=show_message,
            **k,
        )

    def set_secondary_parameter_controls(self, controls):
        self._parameters_component.set_secondary_parameter_controls(controls)
        self._show_device_and_bank_info()
