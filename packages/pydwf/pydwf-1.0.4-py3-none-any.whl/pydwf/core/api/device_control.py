"""The |pydwf.core.api.device_control| module implements a single class: |Device|."""

from typing import Optional

from pydwf.core.dwf_library_subapi import AbstractDwfLibrarySubApi

from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.constants import RESULT_SUCCESS
from pydwf.core.dwf_device import DwfDevice


class DeviceControl(AbstractDwfLibrarySubApi):
    """The |DeviceControl| class provides access to the device control functionality of a
    |DwfLibrary:link|.

    Attention:
        Users of |pydwf| should not create instances of this class directly.

        It is instantiated during initialization of a |DwfLibrary| and subsequently assigned to its
        public |deviceControl:link| attribute for access by the user.
    """

    def open(self, device_index: int, config_index: Optional[int] = None) -> DwfDevice:
        """Open a Digilent Waveforms device identified by the device index, using a specific
        device configuration index if specified.

        Note:
            This method combines the functionality of the C API functions 'FDwfDeviceOpen()' and
            'FDwfDeviceConfigOpen()' into a single method.
            The call that is actually made depends on the value of the *config_index* parameter.

        Note:
            This method can take several seconds to complete.

        Parameters:
            device_index (int): The zero-based index of the previously enumerated device (see the
                |DeviceEnum.enumerateDevices:link| method).

                To automatically enumerate all connected devices and open the first discovered device,
                use the value -1 for this parameter.

            config_index (Optional[int]): The zero-based index of the device configuration to use
                (see the |DeviceEnum.enumerateConfigurations:link| method).
                If None, open the default (first) device configuration.

        See Also:
            The |pydwf.utilities.openDwfDevice:link| convenience function provides a more powerful way to select
            and open a device and, if desired, specify its device configuration.

        Returns:
            DwfDevice: The |DwfDevice| instance created as a result of this call.

        Raises:
            DwfLibraryError: The specified device or configuration cannot be opened.
        """
        c_hdwf = typespec_ctypes.HDWF()
        if config_index is None:
            result = self.lib.FDwfDeviceOpen(device_index, c_hdwf)
        else:
            result = self.lib.FDwfDeviceConfigOpen(device_index, config_index, c_hdwf)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        hdwf = c_hdwf.value
        return DwfDevice(self.dwf, hdwf)

    def closeAll(self) -> None:
        """Close all Digilent Waveforms devices opened by the calling process.

        This method does not close all Digilent Waveforms devices across all processes.

        Raises:
            DwfLibraryError: The *close all* operation failed.
        """
        result = self.lib.FDwfDeviceCloseAll()
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
