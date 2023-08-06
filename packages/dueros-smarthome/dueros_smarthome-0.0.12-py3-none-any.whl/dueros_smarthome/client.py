from . import const, models
import httpx
import json

class ResponseCommon:
    def __init__(self, response: dict):
        self._status = response[const.STATUS]
        self._msg = response[const.MSG]
        self._log_id = response[const.LOGID]

    @property
    def status(self):
        return self._status

    @property
    def msg(self):
        return self._msg

    @property
    def log_id(self):
        return self._log_id

class GetDeviceListResponse(ResponseCommon):
    def __init__(self, response: dict):
        super().__init__(response)
        self._appliances = [models.Appliance(appliance) for appliance in response[const.DATA][const.APPLIANCES]]
    
    @property
    def appliances(self):
        return self._appliances

class DeviceActionResponse(ResponseCommon):
    def __init__(self, response: dict):
        super().__init__(response)

class Request:
    def __init__(self, namespace: str, name: str, payload: dict, payloadVersion: int = const.DEFAULT_PAYLOAD_VERSION):
        self._dict = {const.REQUEST_HEADER: {const.REQUEST_HEADER_NAMESPACE: namespace, const.REQUEST_HEADER_NAME: name, const.PAYLOAD_VERSION: payloadVersion},
                      const.REQUEST_PAYLOAD: payload}
    
    def to_bytes(self):
        return json.dumps(self._dict)

class TurnOffRequest(Request):
    def __init__(self, appliance_id: str):
        payload = get_device_action_request_payload(appliance_id)
        super().__init__(const.CONTROL_REQUEST_NAMESPACE, const.TURN_OFF_REQUEST, payload)
    
def get_device_action_request_payload(appliance_id: str, proxy_connect_status: bool = False):
    return {const.APPLIANCE: {const.APPLIANCE_ID: [appliance_id]}, const.REQUEST_PARAMETERS: {const.PROXY_CONNECT_STATUS: proxy_connect_status}}

class TurnOnRequest(Request):
    def __init__(self, appliance_id: str):
        payload = get_device_action_request_payload(appliance_id)
        super().__init__(const.CONTROL_REQUEST_NAMESPACE, const.TURN_ON_REQUEST, payload)

class SetBrightnessPercentageRequest(Request):
    def __init__(self, appliance_id: str, brightness: models.Brightness):
        payload = get_device_action_request_payload(appliance_id)
        payload[const.BRIGHTNESS] = {const.VALUE: brightness.percentage}
        payload[const.REQUEST_PARAMETERS][const.ATTRIBUTE] = const.BRIGHTNESS
        payload[const.REQUEST_PARAMETERS][const.ATTRIBUTE_VALUE] = brightness.percentage
        super().__init__(const.CONTROL_REQUEST_NAMESPACE, const.SET_BRIGHTNESS_PERCENTAGE_REQUEST, payload)

class SetColorTemperatureRequest(Request):
    def __init__(self, appliance_id: str, color_temp: models.ColorTemperatureInKelvin):
        payload = get_device_action_request_payload(appliance_id)
        payload[const.COLOR_TEMPERATURE_IN_KELVIN] = color_temp.percentage()
        payload[const.REQUEST_PARAMETERS][const.ATTRIBUTE] = const.COLOR_TEMPERATURE_IN_KELVIN
        payload[const.REQUEST_PARAMETERS][const.ATTRIBUTE_VALUE] = color_temp.percentage()
        super().__init__(const.CONTROL_REQUEST_NAMESPACE, const.SET_COLOR_TEMPERATURE_REQUEST, payload)

class SmartHomeClient:
    def __init__(self, bduss: str, host: str = const.DEFAULT_HOST, schema: str = const.DEFAULT_SCHEMA) -> None:
        self._host = host
        self._schema = schema
        self._bduss = bduss
        self._cookies = httpx.Cookies()
        self._cookies.set(const.BDUSS_COOKIE_KEY, self._bduss, domain = self._host)
        for key in const.ADDITIONAL_COOKIES:
            self._cookies.set(key, const.ADDITIONAL_COOKIES[key], domain = self._host)
    
    @property
    def host(self):
        return self._host
    
    def _get_device_list_url(self) -> str:
        return f'{self._schema}{self._host}{const.DEVICE_LIST_QUERY}'

    async def get_device_list(self) -> GetDeviceListResponse:
        async with httpx.AsyncClient() as client:
            response = await client.get(self._get_device_list_url(), cookies=self._cookies)
            return GetDeviceListResponse(response.json())
    
    def _get_device_action_url(self) -> str:
        return f'{self._schema}{self._host}{const.DEVICE_ACTION_QUERY}'

    async def turn_off(self, appliance_id: str) -> DeviceActionResponse:
        async with httpx.AsyncClient() as client:
            response = await client.post(self._get_device_action_url(), cookies=self._cookies, content=TurnOffRequest(appliance_id).to_bytes())
            return DeviceActionResponse(response.json())

    async def turn_on(self, appliance_id: str) -> DeviceActionResponse:
        async with httpx.AsyncClient() as client:
            response = await client.post(self._get_device_action_url(), cookies=self._cookies, content=TurnOnRequest(appliance_id).to_bytes())
            return DeviceActionResponse(response.json())
    
    async def set_brightness_percentage(self, appliance_id: str, brightness: models.Brightness) -> DeviceActionResponse:
        async with httpx.AsyncClient() as client:
            response = await client.post(self._get_device_action_url(), cookies=self._cookies, content=SetBrightnessPercentageRequest(appliance_id, brightness).to_bytes())
            return DeviceActionResponse(response.json())

    async def set_color_temperature(self, applicance_id: str, color_temp: models.ColorTemperatureInKelvin) -> DeviceActionResponse:
        async with httpx.AsyncClient() as client:
            response = await client.post(self._get_device_action_url(), cookies=self._cookies, content=SetColorTemperatureRequest(applicance_id, color_temp).to_bytes())
            return DeviceActionResponse(response.json())


