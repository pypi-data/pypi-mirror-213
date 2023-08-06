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

    @property
    def connectivity(self):
        return self._connectivity
    
    @property
    def timestamp_of_sample(self):
        return self._timestamp_of_sample

class ConnectivitySetting:
    def __init__(self, connectivity_setting: dict):
        self._value = connectivity_setting[const.VALUE]
        self._time = connectivity_setting[const.TIME]
    
    @property
    def value(self):
        return self._value

    @property
    def time(self):
        return self._time

class TurnOnState(Enum):
    NONE = auto()
    ON = auto()
    OFF = auto()

    @staticmethod
    def from_str(label: str):
        return TurnOnState[label]
    
class TurnOnStateSetting:
    def __init__(self, turn_on_state_setting: dict):
        if turn_on_state_setting[const.VALUE]:
            self._value = TurnOnState.from_str(turn_on_state_setting[const.VALUE])
        else:
            self._value = None
        self._time = turn_on_state_setting[const.TIME]

    @property
    def value(self):
        return self._value

    @property
    def time(self):
        return self._time

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

    @property
    def value(self):
        return self._value
    
    @property
    def scale(self):
        return self._scale
    
    @property
    def min(self):
        return self._min
    
    @property
    def max(self):
        return self._max

class Brightness(Num):
    def __init__(self, value: int):
        super().__init__(value, scale = '%', min = 1, max = 100)

    @property
    def percentage(self) -> int:
        return self._value

class BrightnessSetting:
    def __init__(self, brightness_setting: dict):
        if brightness_setting[const.VALUE]:
            self._value = Brightness(brightness_setting[const.VALUE])
        else:
            self._value = None
        self._time = brightness_setting[const.TIME]

    @property
    def value(self):
        return self._value
    
    @property
    def time(self):
        return self._time

class ColorTemperatureInKelvin(Num):
    def __init__(self, value: int, kelvin_min: int = '2700', kelvin_max: int = '6500'):
        if kelvin_min > kelvin_max:
            raise ValueError(f'kelvin_min {kelvin_min} is larger than kelvin_max {kelvin_max}')
        super().__init__(value, scale = '%', min = 1, max = 100)
        self._kelvin_min = kelvin_min
        self._kelvin_max = kelvin_max
    
    @property
    def in_kelvin(self) -> int:
        return self._kelvinMin + (self._kelvinMax - self._kelvinMin) * (self._value - self._min + 1) / (self._max - self._min + 1)

    @property
    def percentage(self) -> int:
        return self._value

    @property
    def kelvin_min(self):
        return self._kelvin_min
    
    @property
    def kelvin_max(self):
        return self._kelvin_max

class ColorTemperatureInKelvinSetting:
    def __init__(self, setting: dict):
        if setting[const.VALUE]:
            self._value = ColorTemperatureInKelvin(setting[const.VALUE])
        else:
            self._value = None
        self._time = setting[const.TIME]
    
    @property
    def value(self):
        return self._value

    @property
    def time(self):
        return self._time

class LightMode:
    def __init__(self, mode_info: dict):
        self._mode = mode_info[const.MODE]
        self._color_temperature_in_kelvin = ColorTemperatureInKelvin(mode_info[const.COLOR_TEMPERATURE_IN_KELVIN])
        self._brightness = Brightness(mode_info[const.BRIGHTNESS])
        self._name = mode_info[const.NAME]
        self._icon = mode_info[const.ICON_URL]

    @property
    def mode(self):
        return self._mode
    
    @property
    def color_temperature_in_kelvin(self):
        return self._color_temperature_in_kelvin
    
    @property
    def brightness(self):
        return self._brightness
    
    @property
    def name(self):
        return self._name
    
    @property
    def icon_url(self):
        return self._icon

class ApplianceAttributes:
    def __init__(self, attributes: dict):
        if const.CONNECTIVITY in attributes:
            self._connectivity = ConnectivityAttribute(attributes[const.CONNECTIVITY])
        else:
            self._connectivity = None

    @property
    def connectivity(self):
        return self._connectivity

class BrightnessAndColorTemperatureMode:
    def __init__(self, mode: dict):
        self._mode = mode[const.MODE]
        self._brightness = Brightness(mode[const.BRIGHTNESS])
        self._color_temperature_in_kelvin = ColorTemperatureInKelvin(mode[const.COLOR_TEMPERATURE_IN_KELVIN])
        self._name = mode[const.NAME]

    @property
    def mode(self):
        return self._mode
    
    @property
    def brightness(self):
        return self._brightness
    
    @property
    def color_temperature_in_kelvin(self):
        return self._color_temperature_in_kelvin
    
    @property
    def name(self):
        return self._name

class BrightnessAndColorTemperatureWithIconMode(BrightnessAndColorTemperatureMode):
    def __init__(self, mode: dict):
        super().__init__(mode)
        self._icon_url = mode[const.ICON_URL]

    @property
    def icon_url(self):
        return self._icon_url

class ApplianceModes:
    def __init__(self, modes: dict):
        if const.BRIGHTNESS_AND_COLOR_TEMPERATURE in modes:
            self._brightness_and_color_temperature = {mode: BrightnessAndColorTemperatureMode(modes[const.BRIGHTNESS_AND_COLOR_TEMPERATURE][mode]) for mode in modes[const.BRIGHTNESS_AND_COLOR_TEMPERATURE]}
        else:
            self._brightness_and_color_temperature = None

        if const.BRIGHTNESS_AND_COLOR_TEMPERATURE_WITH_ICON in modes:
            self._brightness_and_color_temperature_with_icon = {mode: BrightnessAndColorTemperatureWithIconMode(modes[const.BRIGHTNESS_AND_COLOR_TEMPERATURE_WITH_ICON][mode]) for mode in modes[const.BRIGHTNESS_AND_COLOR_TEMPERATURE_WITH_ICON]}
        else:
            self._brightness_and_color_temperature_with_icon = None

    @property
    def brightness_and_color_temperature(self):
        return self._brightness_and_color_temperature
    
    @property
    def brightness_and_color_temperature_with_icon(self):
        return self._brightness_and_color_temperature_with_icon

class ApplianceStateSettings:
    def __init__(self, state_settings: dict):
        if const.CONNECTIVITY in state_settings:
            self._connectivity = ConnectivitySetting(state_settings[const.CONNECTIVITY])
        else:
            self._connectivity = None

        if const.TURN_ON_STATE in state_settings:
            self._turn_on_state = TurnOnStateSetting(state_settings[const.TURN_ON_STATE])
        else:
            self._turn_on_state = None

        if const.BRIGHTNESS in state_settings:
            self._brightness = BrightnessSetting(state_settings[const.BRIGHTNESS])
        else:
            self._brightness = None

        if const.COLOR_TEMPERATURE_IN_KELVIN in state_settings:
            self._color_temperature_in_kelvin = ColorTemperatureInKelvinSetting(state_settings[const.COLOR_TEMPERATURE_IN_KELVIN])
        else:
            self._color_temperature_in_kelvin = None

        if const.MODE in state_settings:
            self._modes = ApplianceModes(state_settings[const.MODE])
        else:
            self._modes = None
    
    @property
    def connectivity(self):
        return self._connectivity
    
    @property
    def turn_on_state(self):
        return self._turn_on_state
    
    @property
    def brightness(self):
        return self._brightness
    
    @property
    def color_temperature_in_kelvin(self):
        return self._color_temperature_in_kelvin
    
    @property
    def modes(self):
        return self._modes

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
        self._state_settings = ApplianceStateSettings(appliance_info[const.STATE_SETTING])
        self._icon_urls = [icon_url for icon_url in appliance_info[const.ICON_URLS].values()] 
        self._status = appliance_info[const.STATUS]
    
    @property
    def bot_name(self):
        return self._bot_name
    
    @property
    def bot_id(self):
        return self._bot_id
    
    @property
    def bot_logo_url(self):
        return self._bot_logo
    
    @property
    def appliance_id(self):
        return self._appliance_id
    
    @property
    def appliance_types(self):
        return self._appliance_types
    
    @property
    def nicknames(self):
        return self._nicknames
    
    @property
    def friendly_description(self):
        return self._friendly_description
    
    @property
    def supported_actions(self):
        return self._supported_actions
    
    @property
    def friendly_name(self):
        return self._friendly_name
    
    @property
    def group_name(self):
        return self._group_name
    
    @property
    def group_id(self):
        return self._group_id
    
    @property
    def room_name(self):
        return self._room_name
    
    @property
    def room_id(self):
        return self._room_id
    
    @property
    def floor_id(self):
        return self._floor_id
    
    @property
    def attributes(self):
        return self._attributes
    
    @property
    def state_settings(self):
        return self._state_settings
    
    @property
    def icon_urls(self):
        return self._icon_urls
    
    @property
    def status(self):
        return self._status