"""The |pydwf.core.dwf_device_subapi| module implements a single class: |AbstractDwfDeviceSubApi|."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydwf.core.dwf_device import DwfDevice


class AbstractDwfDeviceSubApi:
    """Abstract base class for the sub-API attributes of a |DwfDevice|."""

    def __init__(self, device: 'DwfDevice'):
        self._device = device

    @property
    def device(self):
        """Return the |DwfDevice| instance of which we are an attribute.

        This is useful if we have a variable that contains a reference to a |DwfDevice| attribute,
        but we need the |DwfDevice| itself.

        Returns:
            DwfDevice: The |DwfDevice| that this attribute belongs to.
        """
        return self._device

    @property
    def hdwf(self):
        """Return the HDWF device handle.

        Returns:
            int: The HDWF device handle.

        :meta private:
        """
        return self.device.hdwf

    @property
    def dwf(self):
        """Return the |DwfLibrary| instance.

        Returns:
            DwfLibrary: The |DwfLibrary| instance.

        :meta private:
        """
        return self.device.dwf

    @property
    def lib(self):
        """Return the |ctypes:link| library.

        Returns:
            ctypes.CDLL: The |ctypes| library.

        :meta private:
        """
        return self.dwf.lib
