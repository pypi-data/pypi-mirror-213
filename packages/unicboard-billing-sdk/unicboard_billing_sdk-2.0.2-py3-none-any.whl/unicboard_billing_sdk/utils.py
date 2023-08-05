from typing import Dict, Any

from unicboard_billing_sdk.response_models import GetDeviceValueResponse, GetDeviceChannelValuePayloadResponse, \
    GetDeviceListInfoPayloadResponse, DataGatewayNetworkResponseModel, DeviceChannelResponseModel, NetworkResponseModel, \
    ProtokolResponseModel, DataGatewayResponseModel, DeviceManufacturerResponseModel, DeviceModificationResponseModel, \
    DeviceModificationTypeResponseModel, DeviceMeteringType, GetDeviceInfoResponse, GetDeviceListInfoResponse, \
    DeviceMeterResponseModel, GetDeviceBatteryLevelResponse, GetDeviceListBatteryLevelPayloadResponse, \
    GetDeviceListClockPayloadResponse, GetDeviceListEventPayloadResponse, GetDeviceListProfilePayloadResponse, \
    GetDeviceListTemperaturePayloadResponse, GetDeviceClockResponse, GetDeviceEventResponse, GetDeviceProfileResponse, \
    GetDeviceTemperatureResponse


def get_device_info_payload_structure(payload: Dict[str, Any]) -> GetDeviceListInfoPayloadResponse:
    """
    It takes a dictionary and returns a GetDeviceListInfoPayloadResponse object.

    Args:
      payload (Dict[str, Any]): Dict[str, Any] - this is the payload that is returned from the API

    Returns:
      GetDeviceListInfoPayloadResponse: Device information
    """
    data_gateway_network_device = payload.pop('data_gateway_network_device')
    network = data_gateway_network_device.pop('network')
    data_gateway = network.pop('data_gateway')
    protocol = data_gateway_network_device.pop('protocol')
    device_channels = payload.pop('device_channel')
    device_manufacturer = payload.pop('device_manufacturer')
    device_modification = payload.pop('device_modification')
    device_modification_type = device_modification.pop('device_modification_type')
    device_metering_type = device_modification_type.pop('device_metering_type')
    return GetDeviceListInfoPayloadResponse(
            **payload,
            data_gateway_network_device=DataGatewayNetworkResponseModel(
                **data_gateway_network_device,
                network=NetworkResponseModel(
                    **network,
                    data_gateway=DataGatewayResponseModel(**data_gateway),
                ),
                protocol=ProtokolResponseModel(**protocol),
            ),
            device_channel=[DeviceChannelResponseModel(
                inactivity_limit=device_channel['inactivity_limit'],
                last_date_event_no_data=device_channel['last_date_event_no_data'],
                serial_number=device_channel['serial_number'],
                device_meters=[DeviceMeterResponseModel(**device_meter) for device_meter in device_channel['device_meter']],
            ) for device_channel in device_channels],
            device_manufacturer=DeviceManufacturerResponseModel(**device_manufacturer),
            device_modification=DeviceModificationResponseModel(
                **device_modification,
                device_modification_type=DeviceModificationTypeResponseModel(
                    **device_modification_type,
                    device_metering_type=DeviceMeteringType(**device_metering_type)
                ),
            ),
        )


def get_device_info_structure(response: Dict[str, Any]) -> GetDeviceInfoResponse:
    """
    It takes a dictionary and returns a GetDeviceInfoResponse object

    Args:
      response (Dict[str, Any]): Dict[str, Any]

    Returns:
      GetDeviceInfoResponse: Device information list
    """
    payload = response.pop('payload')
    return GetDeviceInfoResponse(
        errors=response['errors'],
        ok=response['ok'],
        payload=get_device_info_payload_structure(payload)
    )


def get_device_battery_level_structure(response: Dict[str, Any]) -> GetDeviceBatteryLevelResponse:
    """
    """
    payload = response.pop('payload')
    return GetDeviceBatteryLevelResponse(
        count=response['count'],
        errors=response['errors'],
        ok=response['ok'],
        total_count=response['total_count'],
        payload=[GetDeviceListBatteryLevelPayloadResponse(**item) for item in payload]
    )


def get_device_clock_structure(response: Dict[str, Any]) -> GetDeviceClockResponse:
    """
    """
    payload = response.pop('payload')
    return GetDeviceClockResponse(
        count=response['count'],
        errors=response['errors'],
        ok=response['ok'],
        total_count=response['total_count'],
        payload=[GetDeviceListClockPayloadResponse(**item) for item in payload]
    )


def get_device_event_structure(response: Dict[str, Any]) -> GetDeviceEventResponse:
    """
    """
    payload = response.pop('payload')
    return GetDeviceEventResponse(
        count=response['count'],
        errors=response['errors'],
        ok=response['ok'],
        total_count=response['total_count'],
        payload=[GetDeviceListEventPayloadResponse(**item) for item in payload]
    )


def get_device_profile_structure(response: Dict[str, Any]) -> GetDeviceProfileResponse:
    """
    """
    payload = response.pop('payload')
    return GetDeviceProfileResponse(
        count=response['count'],
        errors=response['errors'],
        ok=response['ok'],
        total_count=response['total_count'],
        payload=[GetDeviceListProfilePayloadResponse(**item) for item in payload]
    )


def get_device_temperature_structure(response: Dict[str, Any]) -> GetDeviceTemperatureResponse:
    """
    """
    payload = response.pop('payload')
    return GetDeviceTemperatureResponse(
        count=response['count'],
        errors=response['errors'],
        ok=response['ok'],
        total_count=response['total_count'],
        payload=[GetDeviceListTemperaturePayloadResponse(**item) for item in payload]
    )


def get_device_list_info_structure(response: Dict[str, Any]) -> GetDeviceListInfoResponse:
    """
    It takes a dictionary and returns a GetDeviceListInfoResponse object

    Args:
      response (Dict[str, Any]): Dict[str, Any]

    Returns:
      GetDeviceListInfoResponse: Device information list
    """
    payload = response.pop('payload')
    return GetDeviceListInfoResponse(
        count=response['count'],
        errors=response['errors'],
        ok=response['ok'],
        total_count=response['total_count'],
        payload=[get_device_info_payload_structure(item) for item in payload]
    )


def get_device_value_structure(response: Dict[str, Any]) -> GetDeviceValueResponse:
    """
    It takes a dictionary and returns a `GetDeviceValueResponse` object

    Args:
      response (Dict[str, Any]): Dict[str, Any]

    Returns:
      GetDeviceValueResponse: Device information list
    """
    payload = response.pop('payload')
    return GetDeviceValueResponse(
        count=response['count'],
        errors=response['errors'],
        ok=response['ok'],
        total_count=response['total_count'],
        payload=[GetDeviceChannelValuePayloadResponse(**item) for item in payload]
    )


