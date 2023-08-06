from seamapi.types import (
    AbstractDevices,
    AbstractUnmanagedDevices,
    ConnectWebview,
    ConnectWebviewId,
    ConnectedAccount,
    ConnectedAccountId,
    Device,
    DeviceId,
    UnmanagedDevice,
    AbstractSeam as Seam,
    DeviceType,
)
from typing import List, Union, Optional
from seamapi.utils.convert_to_id import (
    to_connect_webview_id,
    to_connected_account_id,
    to_device_id,
)
from seamapi.utils.report_error import report_error


class Devices(AbstractDevices):
    """
    A class used to retrieve device data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    list(connected_account=None, connect_webview=None, device_type=None, device_ids=None)
        Gets a list of devices
    get(device=None, name=None)
        Gets a device
    update(device, name=None, properties=None, location=None)
        Updates a device
    """

    seam: Seam

    def __init__(self, seam: Seam):
        """
        Parameters
        ----------
        seam : Seam
          Initial seam class
        """

        self.seam = seam
        self.unmanaged = UnmanagedDevices(seam)

    @report_error
    def list(
        self,
        connected_account: Union[ConnectedAccountId, ConnectedAccount] = None,
        connect_webview: Union[ConnectWebviewId, ConnectWebview] = None,
        device_type: Optional[DeviceType] = None,
        device_ids: Optional[list] = None,
    ) -> List[Device]:
        """Gets a list of devices.

        Parameters
        ----------
        connected_account : ConnectedAccountId or ConnectedAccount, optional
            Connected account id or ConnectedAccount to get devices associated with
        connect_webview : ConnectWebviewId or ConnectWebview, optional
            Connect webview id or ConnectWebview to get devices associated with
        device_type : DeviceType, optional
            Device type e.g. august_lock
        device_ids : Optional[list]
            Device IDs to filter devices by

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of devices.
        """

        params = parse_list_params(
            connected_account,
            connect_webview,
            device_type,
            device_ids
        )

        res = self.seam.make_request(
            "GET",
            "/devices/list",
            params=params,
        )
        devices = res["devices"]

        return [Device.from_dict(d) for d in devices]

    @report_error
    def get(
        self,
        device: Optional[Union[DeviceId, Device]] = None,
        name: Optional[str] = None,
    ) -> Device:
        """Gets a device.

        Parameters
        ----------
        device : DeviceId or Device, optional
            Device id or Device to get the state of
        name : str, optional
            Device name

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            Device
        """

        params = {}
        if device:
            params["device_id"] = to_device_id(device)
        if name:
            params["name"] = name
        res = self.seam.make_request("GET", "/devices/get", params=params)
        json_device = res["device"]
        return Device.from_dict(json_device)

    @report_error
    def update(
        self,
        device: Union[DeviceId, Device],
        name: Optional[str] = None,
        properties: Optional[dict] = None,
        location: Optional[dict] = None,
        is_managed: Optional[bool] = None,
    ) -> bool:
        """Updates a device.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to update
        name : str, optional
            New device name
        properties : dict, optional
            New device properties
        location : str, optional
            New device location
        is_managed : bool, optional
            The managed state of the device

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            Boolean
        """

        if not device:
            raise Exception("device is required")

        update_payload = {
            "device_id": to_device_id(device),
        }
        if name:
            update_payload["name"] = name
        if properties:
            update_payload["properties"] = properties
        if location:
            update_payload["location"] = location
        if is_managed is not None:
            update_payload["is_managed"] = is_managed

        self.seam.make_request(
            "POST",
            "/devices/update",
            json=update_payload,
        )

        return True

    @report_error
    def delete(self, device: Union[DeviceId, Device]) -> bool:
        """Deletes a device.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to delete

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            None
        """

        if not device:
            raise Exception("device is required")

        delete_payload = {"device_id": to_device_id(device)}
        self.seam.make_request(
            "DELETE",
            "/devices/delete",
            json=delete_payload,
        )

        return None

class UnmanagedDevices(AbstractUnmanagedDevices):
    """
    A class used to retrieve unmanaged device data
    through interaction with Seam API

    ...

    Attributes
    ----------
    seam : Seam
        Initial seam class

    Methods
    -------
    list(connected_account=None, connect_webview=None, device_type=None, device_ids=None)
        Gets a list of unmanaged devices
    update(device, is_managed=False)
        Updates an unmanaged device
    """

    seam: Seam

    def __init__(self, seam: Seam):
        """
        Parameters
        ----------
        seam : Seam
          Initial seam class
        """

        self.seam = seam

    @report_error
    def list(
        self,
        connected_account: Union[ConnectedAccountId, ConnectedAccount] = None,
        connect_webview: Union[ConnectWebviewId, ConnectWebview] = None,
        device_type: Optional[DeviceType] = None,
        device_ids: Optional[list] = None,
    ) -> List[Device]:
        """Gets a list of devices.

        Parameters
        ----------
        connected_account : ConnectedAccountId or ConnectedAccount, optional
            Connected account id or ConnectedAccount to get devices associated with
        connect_webview : ConnectWebviewId or ConnectWebview, optional
            Connect webview id or ConnectWebview to get devices associated with
        device_type : DeviceType, optional
            Device type e.g. august_lock
        device_ids : Optional[list]
            Device IDs to filter devices by

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            A list of devices.
        """

        params = parse_list_params(
            connected_account,
            connect_webview,
            device_type,
            device_ids
        )

        res = self.seam.make_request(
            "GET",
            "/devices/unmanaged/list",
            params=params,
        )
        devices = res["devices"]

        return [UnmanagedDevice.from_dict(d) for d in devices]

    @report_error
    def update(
        self,
        device: Union[DeviceId, UnmanagedDevice],
        is_managed: Optional[bool] = False,
    ) -> bool:
        """Updates a device.

        Parameters
        ----------
        device : DeviceId or Device
            Device id or Device to update
        is_managed : bool, optional
            The managed state of the device

        Raises
        ------
        Exception
            If the API request wasn't successful.

        Returns
        ------
            Boolean
        """

        if not device:
            raise Exception("device is required")

        update_payload = {
            "device_id": to_device_id(device),
        }
        if is_managed is not None:
            update_payload["is_managed"] = is_managed

        self.seam.make_request(
            "POST",
            "/devices/unmanaged/update",
            json=update_payload,
        )

        return True

def parse_list_params (
    connected_account,
    connect_webview,
    device_type,
    device_ids,
):
    params = {}
    if connected_account:
        params["connected_account_id"] = to_connected_account_id(
            connected_account
        )
    if connect_webview:
        params["connect_webview_id"] = to_connect_webview_id(
            connect_webview
        )
    if device_type:
        params["device_type"] = device_type
    if device_ids is not None:
        params["device_ids"] =  [to_device_id(d) for d in device_ids]
    return params
