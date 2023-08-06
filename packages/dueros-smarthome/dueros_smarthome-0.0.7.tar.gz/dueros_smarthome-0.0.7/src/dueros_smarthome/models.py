from enum import Enum
from enum import auto

from . import const

class Connectivity(Enum):
    NONE = auto()
    REACHABLE = auto()
    UNREACHABLE = auto()

    @staticmethod
    def from_str(label: str):
        return Connectivity[label]

class ConnectivityAttribute:
    def __init__(self, connectivity_info: dict):
        self._connectivity = connectivity_info[const.VALUE]
        self._timestamp_of_sample = connectivity_info[const.TIMESTAMP_OF_SAMPLE]

class ConnectivitySetting:
    def __init__(self, connectivity_setting: dict):
        self._connectivity = connectivity_setting[const.VALUE]
        self._time = connectivity_setting[const.TIME]

class TurnOnState(Enum):
    NONE = auto()
    ON = auto()
    OFF = auto()

    @staticmethod
    def from_str(label: str):
        return TurnOnState[label]
    
class TurnOnStateSetting:
    def __init__(self, turn_on_state_setting: dict):
        self._turn_on_state = TurnOnState.from_str(turn_on_state_setting[const.VALUE])
        self._time = turn_on_state_setting[const.TIME]

class ApplianceType(Enum):
    NONE = auto()
    LIGHT = auto()
    AIR_CONDITION = auto()
    CURTAIN = auto()
    CURT_SIMP = auto()
    SOCKET = auto()
    SWITCH = auto()
    FRIDGE = auto()
    WATER_PURIFIER = auto()
    HUMIDIFIER = auto()
    DEHUMIDIFIER = auto()
    INDUCTION_COOKER = auto()
    AIR_PURIFIER = auto()
    WASHING_MACHINE = auto()
    WATER_HEATER = auto()
    GAS_STOVE = auto()
    TV_SET = auto()
    OTT_BOX = auto()
    RANGE_HOOD = auto()
    FAN = auto()
    PROJECTOR = auto()
    SWEEPING_ROBOT = auto()
    KETTLE = auto()
    MICROWAVE_OVEN = auto()
    PRESSURE_COOKER = auto()
    RICE_COOKER = auto()
    HIGH_SPEED_BLENDER = auto()
    AIR_FRESHER = auto()
    CLOTHES_RACK = auto()
    OVEN = auto()
    STEAM_OVEN = auto()
    STEAM_BOX = auto()
    HEATER = auto()
    WINDOW_OPENER = auto()
    WEBCAM = auto()
    CAMERA = auto()
    ROBOT = auto()
    PRINTER = auto()
    WATER_COOLER = auto()
    FISH_TANK = auto()
    WATERING_DEVICE = auto()
    SET_TOP_BOX = auto()
    AROMATHERAPY_MACHINE = auto()
    DVD = auto()
    SHOE_CABINET = auto()
    WALKING_MACHINE = auto()
    TREADMILL = auto()
    BED = auto()
    YUBA = auto()
    SHOWER = auto()
    BATHTUB = auto()
    DISINFECTION_CABINET = auto()
    DISHWASHER = auto()
    SOFA = auto()
    DOOR_BELL = auto()
    ELEVATOR = auto()
    WEIGHT_SCALE = auto()
    BODY_FAT_SCALE = auto()
    WALL_HUNG_GAS_BOILER = auto()
    SCENE_TRIGGER = auto()
    ACTIVITY_TRIGGER = auto()

    @staticmethod
    def from_str(label: str):
        return ApplianceType[label]

class Action(Enum):
    NONE = auto()
    turnOn = auto()
    turnOff = auto()
    timingTurnOn = auto()
    timingTurnOff = auto()
    pause = auto()
    Continue = auto()
    setColor = auto()
    setColorTemperature = auto()
    incrementColorTemperature = auto()
    decrementColorTemperature = auto()
    setBrightnessPercentage = auto()
    incrementBrightnessPercentage = auto()
    decrementBrightnessPercentage = auto()
    setPower = auto()
    incrementPower = auto()
    decrementPower = auto()
    incrementTemperature = auto()
    decrementTemperature = auto()
    setTemperature = auto()
    incrementFanSpeed = auto()
    decrementFanSpeed = auto()
    setFanSpeed = auto()
    setGear = auto()
    setMode = auto()
    unSetMode = auto()
    timingSetMode = auto()
    timingUnsetMode = auto()
    incrementVolume = auto()
    decrementVolume= auto()
    setVolume = auto()
    setVolumeMute = auto()
    decrementTVChannel = auto()
    incrementTVChannel = auto()
    setTVChannel = auto()
    returnTVChannel = auto()
    chargeTurnOn = auto()
    chargeTurnOff = auto()
    getTurnOnState = auto()
    getOilCapacity = auto()
    getElectricityCapacity = auto()
    setLockState = auto()
    getLockState = auto()
    setSuction = auto()
    setWaterLevel = auto()
    setCleaningLocation = auto()
    setComplexActions = auto()
    setDirection = auto()
    submitPrint = auto()
    getAirPM25 = auto()
    getAirPM10 = auto()
    getCO2Quantity = auto()
    getAirQualityIndex = auto()
    getTemperature = auto()
    getTemperatureReading = auto()
    getTargetTemperature = auto()
    getHumidity = auto()
    getTargetHumidity = auto()
    getWaterQuality = auto()
    getState = auto()
    getTimeLeft = auto()
    getRunningStatus = auto()
    getRunningTime = auto()
    getLocation = auto()
    setTimer = auto()
    timingCancel = auto()
    reset = auto()
    incrementHeight = auto()
    decrementHeight = auto()
    setSwingAngle = auto()
    getFanSpeed = auto()
    setHumidity = auto()
    incrementHumidity = auto()
    decrementHumidity = auto()
    incrementMist = auto()
    decrementMist = auto()
    setMist = auto()
    startUp = auto()
    setFloor = auto()
    decrementFloor = auto()
    incrementFloor = auto()
    incrementSpeed = auto()
    decrementSpeed = auto()
    setSpeed = auto()
    getSpeed = auto()
    getMotionInfo = auto()
    turnOnBurner = auto()
    turnOffBurner = auto()
    timingTurnOnBurner = auto()
    timingTurnOffBurner = auto()

    def __str__(self):
        if Action.Continue == self:
            return self.name.lower()
        return self.name

    @staticmethod
    def from_str(label: str):
        if "continne" == label:
            return Action.Continue
        return Action[label]

class Num:
    def __init__(self, value: int, scale: str, min: int, max: int):
        if min > max:
            raise ValueError(f'min {min} is larger than max {max}')
        if value < min:
            raise ValueError(f'value {value} is smaller than min {min}')
        if value > max:
            raise ValueError(f'value {value} is larger than max {max}')

        self._value = value
        self._scale = scale
        self._min = min
        self._max = max

class Brightness(Num):
    def __init__(self, value: int):
        super().__init__(value, scale = '%', min = 1, max = 100)

    def percentage(self) -> int:
        return self._value

class BrightnessSetting:
    def __init__(self, brightness_setting: dict):
        self._brightness = Brightness(brightness_setting[const.VALUE])
        self._time = brightness_setting[const.TIME]

class ColorTemperatureInKelvin(Num):
    def __init__(self, value: int, kelvin_min: int = '2700', kelvin_max: int = '6500'):
        if kelvin_min > kelvin_max:
            raise ValueError(f'kelvin_min {kelvin_min} is larger than kelvin_max {kelvin_max}')
        super().__init__(value, scale = '%', min = 1, max = 100)
        self._kelvin_min = kelvin_min
        self._kelvin_min = kelvin_max
    
    def get_kelvin(self) -> int:
        return self._kelvinMin + (self._kelvinMax - self._kelvinMin) * (self._value - self._min + 1) / (self._max - self._min + 1)

    def percentage(self) -> int:
        return self._value

class ColorTemperatureInKelvinSetting:
    def __init__(self, setting: dict):
        self._color_temperature_in_kelvin = ColorTemperatureInKelvin(setting[const.VALUE])
        self._time = setting[const.TIME]

class LightMode:
    def __init__(self, mode_info: dict):
        self._mode = mode_info[const.MODE]
        self._color_temperature_in_kelvin = ColorTemperatureInKelvin(mode_info[const.COLOR_TEMPERATURE_IN_KELVIN])
        self._brightness = Brightness(mode_info[const.BRIGHTNESS])
        self._name = mode_info[const.NAME]
        self._icon = mode_info[const.ICON_URL]

class ApplianceAttributes:
    def __init__(self, attributes: dict):
        if const.CONNECTIVITY in attributes:
            self._connectivity = ConnectivityAttribute(attributes[const.CONNECTIVITY])

class BrightnessAndColorTemperatureMode:
    def __init__(self, mode: dict):
        self._mode = mode[const.MODE]
        self._brightness = Brightness(mode[const.BRIGHTNESS])
        self._color_temperature_in_kelvin = ColorTemperatureInKelvin(mode[const.COLOR_TEMPERATURE_IN_KELVIN])
        self._name = mode[const.NAME]

class BrightnessAndColorTemperatureWithIconMode(BrightnessAndColorTemperatureMode):
    def __init__(self, mode: dict):
        super().__init__(mode)
        self._icon_url = mode[const.ICON_URL]

class ApplianceModes:
    def __init__(self, modes: dict):
        if const.BRIGHTNESS_AND_COLOR_TEMPERATURE in modes:
            self._brightness_and_color_temperature = {mode: BrightnessAndColorTemperatureMode(mode_setting) for (mode, mode_setting) in modes[const.BRIGHTNESS_AND_COLOR_TEMPERATURE]}
        if const.BRIGHTNESS_AND_COLOR_TEMPERATURE_WITH_ICON in modes:
            self._brightness_and_color_temperature_with_icon = {mode: BrightnessAndColorTemperatureWithIconMode(mode_setting) for (mode, mode_setting) in modes[const.BRIGHTNESS_AND_COLOR_TEMPERATURE_WITH_ICON]}

class ApplianceStateSettings:
    def __init__(self, state_settings: dict):
        if const.CONNECTIVITY in state_settings:
            self._connectivity = ConnectivitySetting(state_settings[const.CONNECTIVITY])
        if const.TURN_ON_STATE in state_settings:
            self._turn_on_state = TurnOnStateSetting(state_settings[const.TURN_ON_STATE])
        if const.BRIGHTNESS in state_settings:
            self._brightness = BrightnessSetting(state_settings[const.BRIGHTNESS])
        if const.COLOR_TEMPERATURE_IN_KELVIN in state_settings:
            self._color_temperature_in_kelvin = ColorTemperatureInKelvinSetting(state_settings[const.COLOR_TEMPERATURE_IN_KELVIN])
        if const.MODE in state_settings:
            self._modes = ApplianceModes(state_settings[const.MODE])

class Appliance:
    def __init__(self, appliance_info: dict):
        """Create an Appliance instance from JSON dict

        :param appliance_info: dict from JSON response
        :type appliance_info dict:
        """
        self._bot_name = appliance_info[const.BOT_NAME]
        self._bot_id = appliance_info[const.BOT_ID]
        self._bot_logo = appliance_info[const.BOT_LOGO_URL]
        self._appliance_id = appliance_info[const.APPLIANCE_ID]
        self._appliance_types = [ApplianceType.from_str(label) for label in appliance_info[const.APPLIANCE_TYPES]]
        self._nicknames = appliance_info[const.NICKNAMES]
        self._friendly_description = appliance_info[const.DESCRIPTION]
        self._supported_actions = [Action.from_str(label) for label in appliance_info[const.SUPPORTED_ACTIONS]]
        self._friendly_name = appliance_info[const.FRIENDLY_NAME]
        self._group_name = appliance_info[const.GROUP_NAME]
        self._group_id = appliance_info[const.GROUP_ID]
        self._room_name = appliance_info[const.ROOM_NAME]
        self._room_id = appliance_info[const.ROOM_ID]
        self._floor_id = appliance_info[const.FLOOR_ID]
        self._attributes = ApplianceAttributes(appliance_info[const.ATTRIBUTES])
        self._icon_urls = [icon_url for icon_url in appliance_info[const.ICON_URLS].values()] 
        self._status = appliance_info[const.STATUS]