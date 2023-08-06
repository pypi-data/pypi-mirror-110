"""The |pydwf.core.api.device_enumeration| module implements a single class: |Enum|."""

import ctypes
from typing import Optional, Tuple, Union

from pydwf.core.dwf_library_subapi import AbstractDwfLibrarySubApi

from pydwf.core.auxiliary.enum_types import DwfEnumFilter, DwfEnumConfigInfo
from pydwf.core.auxiliary.typespec_ctypes import typespec_ctypes
from pydwf.core.auxiliary.constants import RESULT_SUCCESS
from pydwf.core.auxiliary.exceptions import PyDwfError


class DeviceEnumeration(AbstractDwfLibrarySubApi):
    """The |DeviceEnumeration| class provides access to the device enumeration functionality of a
    |DwfLibrary:link|.

    Attention:
        Users of |pydwf| should not create instances of this class directly.

        It is instantiated during initialization of a |DwfLibrary| and subsequently assigned to its
        public |deviceEnum:link| attribute for access by the user.
    """

    def enumerateDevices(self, enum_filter: Optional[DwfEnumFilter] = None) -> int:
        """Build an internal list of available Digilent Waveforms devices and return the count of devices found.

        This method must be called before using other |DeviceEnumeration| methods described below, because they
        obtain information about the enumerated devices from the internal device list that is built by this method.

        Note:
            This method can take several seconds to complete.

        Parameters:
            enum_filter (Optional[DwfEnumFilter]): Specify which devices to enumerate.
                If None, enumerate all devices.

        Returns:
            int: The number of Digilent Waveforms devices detected.

        Raises:
            DwfLibraryError: The Digilent Waveforms devices cannot be enumerated.
        """
        if enum_filter is None:
            enum_filter = DwfEnumFilter.All

        c_device_count = typespec_ctypes.c_int()
        result = self.lib.FDwfEnum(enum_filter.value, c_device_count)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        device_count = c_device_count.value
        return device_count

    def deviceType(self, device_index: int) -> Tuple[int, int]:
        """Return the device ID and version (hardware revision) of the selected Digilent Waveforms device.

        Note:
            This method returns the integer values as reported by the 'FDwfEnumDeviceType()' function
            and does not cast them to |DwfDeviceID:link| and |DwfDeviceVersion:link| enumeration types.

            This is done to prevent unknown devices from raising an exception.

        Parameters:
            device_index (int): Zero-based index of the previously enumerated Digilent Waveforms device
                (see the :py:meth:`enumerateDevices` method).

        Returns:
            Tuple[int, int]: A tuple of the |DwfDeviceID:link| and |DwfDeviceVersion:link| integer
            values of the selected Digilent Waveforms device.

        Raises:
            DwfLibraryError: The device type and version cannot be retrieved.
        """
        c_device_id = typespec_ctypes.DwfDeviceID()
        c_device_revision = typespec_ctypes.DwfDeviceVersion()
        result = self.lib.FDwfEnumDeviceType(device_index, c_device_id, c_device_revision)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        # In the future, when we have full clarity on the kind of devices we have in the wild,
        # we may want to cast device_id to a DwdDeviceID enum, and device_revision to a DwfDeviceVersion enum.
        device_id = c_device_id.value
        device_revision = c_device_revision.value
        return (device_id, device_revision)

    def deviceIsOpened(self, device_index: int) -> bool:
        """Check if the specified Digilent Waveforms device is already opened by this or any other process.

        Parameters:
            device_index (int): Zero-based index of the previously enumerated Digilent Waveforms device
                (see the :py:meth:`enumerateDevices` method).

        Returns:
            bool: True if the Digilent Waveforms device is already opened, False otherwise.

        Raises:
            DwfLibraryError: The open state of the Digilent Waveforms device cannot be determined.
        """
        c_is_used = typespec_ctypes.c_int()
        result = self.lib.FDwfEnumDeviceIsOpened(device_index, c_is_used)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        is_used = bool(c_is_used.value)
        return is_used

    def userName(self, device_index: int) -> str:
        """Retrieve the user name of the selected Digilent Waveforms device.

        Parameters:
            device_index (int): Zero-based index of the previously enumerated Digilent Waveforms device
                (see the :py:meth:`enumerateDevices` method).

        Returns:
            str: The user name of the Digilent Waveforms device, which is a short name indicating the
            device type (e.g., "Discovery2", "DDiscovery").

        Raises:
            DwfLibraryError: The user name of the Digilent Waveforms device cannot be retrieved.
        """
        c_username = ctypes.create_string_buffer(32)
        result = self.lib.FDwfEnumUserName(device_index, c_username)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        username = c_username.value.decode()
        return username

    def deviceName(self, device_index: int) -> str:
        """Retrieve the device name of the selected Digilent Waveforms device.

        Parameters:
            device_index (int): Zero-based index of the previously enumerated Digilent Waveforms device
                (see the :py:meth:`enumerateDevices` method).

        Returns:
            str: The device name of the Digilent Waveforms device, which is a long name denoting the
            device type (e.g., "Analog Discovery 2", "Digital Discovery").

        Raises:
            DwfLibraryError: The device name of the Digilent Waveforms device cannot be retrieved.
        """
        c_device_name = ctypes.create_string_buffer(32)
        result = self.lib.FDwfEnumDeviceName(device_index, c_device_name)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        device_name = c_device_name.value.decode()
        return device_name

    def serialNumber(self, device_index: int) -> str:
        """Retrieve the 12-digit, unique serial number of the enumerated Digilent Waveforms device.

        Parameters:
            device_index (int): Zero-based index of the previously enumerated Digilent Waveforms device
                (see the :py:meth:`enumerateDevices` method).

        Returns:
            str: The 12 hex-digit unique serial number of the Digilent Waveforms device.

            The 'SN:' prefix returned by the underlying C API function is discarded.

        Raises:
            DwfLibraryError: The serial number of the Digilent Waveforms device cannot be retrieved.
            PyDwfError: The serial number returned by the library isn't of the form 'SN:XXXXXXXXXXXX'.
        """
        c_serial = ctypes.create_string_buffer(32)
        result = self.lib.FDwfEnumSN(device_index, c_serial)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        serial = c_serial.value.decode()
        if not serial.startswith("SN:"):
            raise PyDwfError("Bad serial number string received: {!r}".format(serial))
        serial = serial[3:]
        if len(serial) != 12:
            raise PyDwfError("Serial number isn't 12 characters: {!r}".format(serial))
        return serial

    def enumerateConfigurations(self, device_index: int) -> int:
        """Build an internal list of detected configurations for the specified Digilent Waveforms device.

        This method must be called before using the :py:meth:`configInfo` method described below, because
        that method obtains information from the internal device configuration list that is built by this method.

        Parameters:
            device_index (int): Zero-based index of the previously enumerated Digilent Waveforms device
                (see the :py:meth:`enumerateDevices` method).

        Returns:
            int: The count of configurations of the Digilent Waveforms device.

        Raises:
            DwfLibraryError: The configuration list of the Digilent Waveforms device cannot be retrieved.
        """
        c_config_count = typespec_ctypes.c_int()
        result = self.lib.FDwfEnumConfig(device_index, c_config_count)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        config_count = c_config_count.value
        return config_count

    def _configInfoString(self, config_index: int, info: DwfEnumConfigInfo, max_size: int) -> str:
        """Return device configuration information for parameters that return a string value."""

        c_configuration_parameter_value = ctypes.create_string_buffer(max_size)
        result = self.lib.FDwfEnumConfigInfo(
            config_index, info.value,
            ctypes.cast(c_configuration_parameter_value, typespec_ctypes.c_int_ptr))
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        configuration_parameter_value = c_configuration_parameter_value.value.decode()
        return configuration_parameter_value

    def configInfo(self, config_index: int, info: DwfEnumConfigInfo) -> Union[int, str]:
        """Return information about a Digilent Waveforms device configuration.

        Parameters:
            config_index (int): Zero-based index of the previously enumerated configuration
                (see the :py:meth:`enumerateConfigurations` method described above).

            info (DwfEnumConfigInfo): Selects which configuration parameter to retrieve.

        Note:
            For most values of the *info* parameter, this method returns an integer, but for some values
            it returns a string. Refer to the |DwfEnumConfigInfo:link| documentation for details.

            This explains the somewhat unusual *Union[int, str]* return type of this method.

        Returns:
            Union[int, str]: The value of the selected configuration parameter, of the selected configuration.

        Raises:
            DwfLibraryError: The requested configuration information of the Digilent Waveforms device cannot be
                retrieved.
        """

        if info == DwfEnumConfigInfo.TooltipText:
            return self._configInfoString(config_index, info, 2048)

        if info == DwfEnumConfigInfo.OtherInfoText:
            return self._configInfoString(config_index, info, 256)

        c_configuration_parameter_value = typespec_ctypes.c_int()
        result = self.lib.FDwfEnumConfigInfo(config_index, info.value, c_configuration_parameter_value)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        configuration_parameter_value = c_configuration_parameter_value.value
        return configuration_parameter_value

    def analogInChannels(self, device_index: int) -> int:
        """Return the analog input channel count of the selected Digilent Waveforms device.

        Warning:
            **This method is obsolete.**

            Use either of the following instead:

            * method :py:meth:`configInfo` to obtain the |DwfEnumConfigInfo.AnalogInChannelCount:link|
              configuration value;
            * |AnalogIn.channelCount:link|

        Parameters:
            device_index (int): Zero-based index of the previously enumerated Digilent Waveforms device
                (see the :py:meth:`enumerateDevices` method).

        Returns:
            int: The number of analog input channels of the Digilent Waveforms device.

        Raises:
            DwfLibraryError: The analog-in channel count of the Digilent Waveforms device cannot be retrieved.
        """
        c_channels = typespec_ctypes.c_int()
        result = self.lib.FDwfEnumAnalogInChannels(device_index, c_channels)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        channels = c_channels.value
        return channels

    def analogInBufferSize(self, device_index: int) -> int:
        """Retrieve the analog input buffer size of the selected Digilent Waveforms device.

        Warning:
            **This method is obsolete.**

            Use either of the following instead:

            * method :py:meth:`configInfo` to obtain the |DwfEnumConfigInfo.AnalogInBufferSize:link|
              configuration value;
            * |AnalogIn.bufferSizeGet:link|

        Parameters:
            device_index (int): Zero-based index of the previously enumerated Digilent Waveforms device
                (see the :py:meth:`enumerateDevices` method).

        Returns:
            int: The analog input buffer size of the selected Digilent Waveforms device.

        Raises:
            DwfLibraryError: The analog-in buffer size of the Digilent Waveforms device cannot be retrieved.
        """
        c_buffer_size = typespec_ctypes.c_int()
        result = self.lib.FDwfEnumAnalogInBufferSize(device_index, c_buffer_size)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        buffer_size = c_buffer_size.value
        return buffer_size

    def analogInBits(self, device_index: int) -> int:
        """Retrieve the analog input bit resolution of the selected Digilent Waveforms device.

        Warning:
            **This method is obsolete.**

            Use |AnalogIn.bitsInfo:link| instead.

        Parameters:
            device_index (int): Zero-based index of the previously enumerated Digilent Waveforms device
                (see the :py:meth:`enumerateDevices` method).

        Returns:
            int: The analog input bit resolution of the selected Digilent Waveforms device.

        Raises:
            DwfLibraryError: The analog-in bit resolution of the Digilent Waveforms device cannot be retrieved.
        """
        c_num_bits = typespec_ctypes.c_int()
        result = self.lib.FDwfEnumAnalogInBits(device_index, c_num_bits)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        num_bits = c_num_bits.value
        return num_bits

    def analogInFrequency(self, device_index: int) -> float:
        """Retrieve the analog input sample frequency of the selected Digilent Waveforms device.

        Warning:
            **This method is obsolete.**

            Use |AnalogIn.frequencyInfo:link| instead.

        Parameters:
            device_index (int): Zero-based index of the previously enumerated Digilent Waveforms device
                (see the :py:meth:`enumerateDevices` method).

        Returns:
            float: The analog input sample frequency of the selected Digilent Waveforms device, in samples per second.

        Raises:
            DwfLibraryError: The analog input sample frequency of the Digilent Waveforms device cannot be retrieved.
        """
        c_sample_frequency = typespec_ctypes.c_double()
        result = self.lib.FDwfEnumAnalogInFrequency(device_index, c_sample_frequency)
        if result != RESULT_SUCCESS:
            raise self.dwf.exception()
        sample_frequency = c_sample_frequency.value
        return sample_frequency
