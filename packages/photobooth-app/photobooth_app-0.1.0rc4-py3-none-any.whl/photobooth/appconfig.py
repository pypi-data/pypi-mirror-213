"""
AppConfig class providing central config

"""

import json
import logging
import os
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

import jsonref
from pydantic import BaseModel, BaseSettings, Extra, Field, PrivateAttr
from pydantic.color import Color

logger = logging.getLogger(__name__)

CONFIG_FILENAME = "./config/config.json"


class EnumDebugLevel(str, Enum):
    """enum for debuglevel"""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class GroupCommon(BaseModel):
    """Common config for photobooth."""

    class Config:
        title = "Common Config"

    CAPTURE_CAM_RESOLUTION_WIDTH: int = Field(
        default=1280,
        description="still photo camera resolution width on supported backends",
    )
    CAPTURE_CAM_RESOLUTION_HEIGHT: int = Field(
        default=720,
        description="still photo camera resolution height on supported backends",
    )
    PREVIEW_CAM_RESOLUTION_WIDTH: int = Field(
        default=1280,
        description="liveview camera resolution width on supported backends",
    )
    PREVIEW_CAM_RESOLUTION_HEIGHT: int = Field(
        default=720,
        description="liveview camera resolution height on supported backends",
    )
    LIVEVIEW_RESOLUTION_WIDTH: int = Field(
        default=1280,
        description="Liveview resolution width",
    )
    LIVEVIEW_RESOLUTION_HEIGHT: int = Field(
        default=720,
        description="Liveview resolution height",
    )
    LIVEPREVIEW_QUALITY: int = Field(
        default=80,
        ge=10,
        le=100,
        description="Livepreview stream JPEG image quality on supported backends",
        ui_component="QSlider",
    )
    THUMBNAIL_STILL_QUALITY: int = Field(
        default=60,
        ge=10,
        le=100,
        description="Still JPEG thumbnail quality, thumbs used in gallery list",
        ui_component="QSlider",
    )
    PREVIEW_STILL_QUALITY: int = Field(
        default=75,
        ge=10,
        le=100,
        description="Still JPEG preview quality, preview still shown in gallery detail",
        ui_component="QSlider",
    )
    HIRES_STILL_QUALITY: int = Field(
        default=90,
        ge=10,
        le=100,
        description="Still JPEG full resolution quality, applied to download images and images with filter",
        ui_component="QSlider",
    )

    FULL_STILL_WIDTH: int = Field(
        default=1500,
        ge=800,
        le=5000,
        description="Width of resized full image with filters applied. For performance choose as low as possible but still gives decent print quality. Example: 1500/6inch=250dpi",
    )
    PREVIEW_STILL_WIDTH: int = Field(
        default=900,
        ge=200,
        le=2000,
        description="Width of resized preview image, height is automatically calculated to keep aspect ratio",
    )
    THUMBNAIL_STILL_WIDTH: int = Field(
        default=400,
        ge=100,
        le=1000,
        description="Width of resized thumbnail image, height is automatically calculated to keep aspect ratio",
    )
    DEBUG_LEVEL: EnumDebugLevel = Field(
        title="Debug Level",
        default=EnumDebugLevel.DEBUG,
        description="Log verbosity. File is writte to disc, and latest log is displayed also in UI.",
    )
    LIVEPREVIEW_FRAMERATE: int = Field(
        default=15,
        ge=5,
        le=30,
        description="Reduce the framerate to save cpu/gpu on device displaying the live preview",
        ui_component="QSlider",
    )

    # flip camera source horizontal/vertical
    CAMERA_TRANSFORM_HFLIP: bool = Field(
        default=False,
        description="Apply horizontal flip to image source on supported backends",
    )
    CAMERA_TRANSFORM_VFLIP: bool = Field(
        default=False,
        description="Apply vertical flip to image source on supported backends",
    )
    PROCESS_COUNTDOWN_TIMER: float = Field(
        default=3,
        description="Countdown in seconds, started when user start a capture process",
    )
    PROCESS_COUNTDOWN_OFFSET: float = Field(
        default=0.25,
        description="Trigger capture offset in seconds. 0 trigger exactly when countdown is 0. Triggers the capture offset by the given seconds to compensate for delay in camera.",
    )
    webserver_bind_ip: str = Field(
        default="0.0.0.0",
        description="IP/Hostname to bind the webserver to. 0.0.0.0 means bind to all IP adresses of host.",
    )
    webserver_port: int = Field(
        default=8000,
        description="Port to serve the photobooth website. Ensure the port is available.",
    )


class EnumImageBackendsMain(str, Enum):
    """enum to choose image backend MAIN from"""

    SIMULATED = "Simulated"
    PICAMERA2 = "Picamera2"
    WEBCAMCV2 = "WebcamCv2"
    WEBCAMV4L = "WebcamV4l"
    GPHOTO2 = "Gphoto2"
    # Not yet finished backends:
    # Digicamcontrol = 'Digicamcontrol'


class EnumImageBackendsLive(str, Enum):
    """enum to choose image backend LIVE from"""

    DISABLED = "Disabled"
    SIMULATED = "Simulated"
    PICAMERA2 = "Picamera2"
    WEBCAMCV2 = "WebcamCv2"
    WEBCAMV4L = "WebcamV4l"


class EnumFocuserModule(str, Enum):
    """List to choose focuser module from"""

    NULL = None
    LIBCAM_AF_CONTINUOUS = "LibcamAfContinuous"
    LIBCAM_AF_INTERVAL = "LibcamAfInterval"


class EnumPicamStreamQuality(str, Enum):
    """Enum type to describe the quality wanted from an encoder.
    This may be passed if a specific value (such as bitrate) has not been set.
    """

    VERY_LOW = "very low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very high"


class GroupBackends(BaseModel):
    """
    Choose backends for still images/high quality images captured on main backend.
    If the livepreview is enabled, the video is captured from live backend (if configured)
    or main backend.
    """

    class Config:
        title = "Camera Backend Config"

    MAIN_BACKEND: EnumImageBackendsMain = Field(
        title="Main Backend",
        default=EnumImageBackendsMain.SIMULATED,
        description="Main backend to use for high quality still captures. Also used for livepreview if backend is capable of.",
    )
    LIVE_BACKEND: EnumImageBackendsLive = Field(
        title="Live Backend",
        default=EnumImageBackendsLive.DISABLED,
        description="Secondary backend used for live streaming only. Useful to stream from webcam if DSLR camera has no livestream capability.",
    )
    LIVEPREVIEW_ENABLED: bool = Field(default=True, description="Enable livestream (if possible)")

    cv2_device_index: int = Field(default=0, description="Device index of webcam opened in cv2 backend")
    v4l_device_index: int = Field(default=0, description="Device index of webcam opened in v4l backend")

    gphoto2_disable_viewfinder_before_capture: bool = Field(
        default=True,
        description="Disable viewfinder before capture might speed up following capture autofocus. Might not work with every camera.",
    )

    gphoto2_wait_event_after_capture_trigger: bool = Field(
        default=False,
        description="Usually wait_for_event not necessary before downloading the file from camera. Adjust if necessary.",
    )

    picamera2_AE_EXPOSURE_MODE: int = Field(
        default=1,
        ge=0,
        le=4,
        description="Usually 0=normal exposure, 1=short, 2=long, 3=custom. Not all necessarily supported by camera!",
    )

    picamera2_focuser_module: EnumFocuserModule = Field(
        title="Picamera2 Focuser Module",
        default=EnumFocuserModule.NULL,
        description="Choose continuous or interval mode to trigger autofocus of picamera2 cam.",
    )

    picamera2_stream_quality: EnumPicamStreamQuality = Field(
        title="Picamera2 Stream Quality (for livepreview)",
        default=EnumPicamStreamQuality.MEDIUM,
        description="Lower quality results in less data to be transferred and may reduce load on display device.",
    )

    picamera2_focuser_interval: int = Field(
        default=10,
        description="Every x seconds trigger autofocus",
    )


class EnumPilgramFilter(str, Enum):
    """enum to choose image filter from, pilgram filter"""

    original = "original"

    _1977 = "_1977"
    aden = "aden"
    brannan = "brannan"
    brooklyn = "brooklyn"
    clarendon = "clarendon"
    earlybird = "earlybird"
    gingham = "gingham"
    hudson = "hudson"
    inkwell = "inkwell"
    kelvin = "kelvin"
    lark = "lark"
    lofi = "lofi"
    maven = "maven"
    mayfair = "mayfair"
    moon = "moon"
    nashville = "nashville"
    perpetua = "perpetua"
    reyes = "reyes"
    rise = "rise"
    slumber = "slumber"
    stinson = "stinson"
    toaster = "toaster"
    valencia = "valencia"
    walden = "walden"
    willow = "willow"
    xpro2 = "xpro2"


class TextStageConfig(BaseModel):
    text: str = ""
    pos_x: int = 50
    pos_y: int = 50
    # rotation: int = 0 # TODO: not yet implemented
    font_size: int = 20
    font: str = "Roboto-Bold.ttf"
    color: Color = Color("red")


class GroupMediaprocessing(BaseModel):
    """Configure stages how to process images after capture."""

    class Config:
        title = "Process media after capture"

    pic1_enable_pipeline: bool = Field(
        default=False,
        description="Enable/Disable 1pic processing pipeline completely",
    )

    pic1_filter: EnumPilgramFilter = Field(
        title="Pic1 Filter",
        default=EnumPilgramFilter.original,
        description="Instagram-like filter to apply per default. 'original' applies no filter.",
    )
    """#TODO:
    pic1_filter_userselectable: list[EnumPilgramFilter] = Field(
        title="Pic1 Filter Userselectable",
        default=[EnumPilgramFilter.original, EnumPilgramFilter._1977],
        description="Filter the user may choose from in the gallery. 'original' applies no filter.",
    )
    """
    pic1_text_overlay: list[TextStageConfig] = Field(
        default=[],
        description="Text to overlay on images after capture. Pos_x/Pos_y measure in pixel starting 0/0 at top-left in image. Font to use in text stages. File needs to be located in DATA_DIR/fonts/",
    )


class GroupHardwareInput(BaseModel):
    """Configure GPIO, keyboard and more."""

    class Config:
        title = "Hardware Input/Output Config"

    keyboard_input_enabled: bool = Field(
        default=False,
        description="Enable keyboard input globally",
    )
    keyboard_input_keycode_takepic: str = Field(
        default="down",
        description="Keycode triggers capture of one image",
    )


class GroupUiSettings(BaseModel):
    """Personalize the booth's UI."""

    class Config:
        title = "Personalize the User Interface"

    FRONTPAGE_TEXT: str = Field(
        default='<div class="fixed-center text-h2 text-weight-bold text-center text-white" style="text-shadow: 4px 4px 4px #666;">Hey!<br>Let\'s take some pictures <br>📷💕</div>',
        description="Text/HTML displayed on frontpage.",
    )
    GALLERY_ENABLE: bool = Field(
        default=True,
        description="Enable gallery for user.",
    )
    GALLERY_EMPTY_MSG: str = Field(
        default="So boring here...🤷‍♂️<br>Let's take some pictures 📷💕",
        description="Message displayed if gallery is empty.",
    )
    TAKEPIC_MSG: str = Field(
        default="CHEEESE!",
        description="Message shown during capture. Use icons also.",
    )
    TAKEPIC_MSG_TIME: float = Field(
        default=0.5,
        description="Offset in seconds, the message above shall be shown.",
    )
    AUTOCLOSE_NEW_ITEM_ARRIVED: int = Field(
        default=30,
        description="Timeout in seconds a new item popup closes automatically.",
    )
    SHOW_ADMIN_LINK_ON_FRONTPAGE: bool = Field(
        default=True,
        description="Show link to admin center, usually only during setup.",
    )
    EXT_DOWNLOAD_URL: str = Field(
        default="http://dl.qbooth.net/{filename}",
        description="URL encoded by QR code to download images from onlineservice. {filename} is replaced by actual filename",
    )
    gallery_show_filter: bool = Field(
        default=False,
        description="",
    )
    gallery_show_download: bool = Field(
        default=False,
        description="",
    )
    gallery_show_delete: bool = Field(
        default=False,
        description="",
    )
    gallery_show_print: bool = Field(
        default=False,
        description="",
    )


class GroupWled(BaseModel):
    """
    WLED integration for countdown led / shoot animation
    needs WLED module connected via USB serial port and
    three presets:
    1: standby (usually LEDs off)
    2: countdown (animates countdown)
    3: shoot (imitate a flash)
    Please define presets on your own in WLED webfrontend
    """

    class Config:
        title = "WLED Integration Config"

    # WledService Config
    ENABLED: bool = Field(
        default=False,
        description="Enable WLED integration for user feedback during countdown and capture by LEDs.",
    )
    SERIAL_PORT: str = Field(
        default="",
        description="Serial port the WLED device is connected to.",
    )


class GroupMisc(BaseModel):
    """
    Quite advanced, usually not necessary to touch.
    """

    class Config:
        title = "Miscellaneous Config"


def json_config_settings_source(_config: BaseSettings) -> dict[str, Any]:
    """
    custom parser to read json config file
    """
    encoding = _config.__config__.env_file_encoding
    json_config = {}
    try:
        json_config = json.loads(Path(CONFIG_FILENAME).read_text(encoding))
    except FileNotFoundError:
        # ignore file not found, because it could have been deleted or not yet initialized
        # using defaults
        pass

    return json_config


class AppConfig(BaseSettings):
    """
    AppConfig class glueing all together

    In the case where a value is specified for the same Settings field in multiple ways, the selected value is determined as follows (in descending order of priority):

    1 Arguments passed to the Settings class initialiser.
    2 Environment variables, e.g. my_prefix_special_function as described above.
    3 Variables loaded from a dotenv (.env) file.
    4 Variables loaded from the secrets directory.
    5 The default field values for the Settings model.
    """

    _processed_at: datetime = PrivateAttr(default_factory=datetime.now)  # private attributes

    # groups -> setting items
    common: GroupCommon = GroupCommon()
    mediaprocessing: GroupMediaprocessing = GroupMediaprocessing()
    uisettings: GroupUiSettings = GroupUiSettings()
    backends: GroupBackends = GroupBackends()
    wled: GroupWled = GroupWled()
    hardwareinput: GroupHardwareInput = GroupHardwareInput()
    misc: GroupMisc = GroupMisc()

    class Config:
        """
        pydantic config class modified
        """

        env_file_encoding = "utf-8"
        # first in following list is least important; last .env file overwrites the other.
        env_file = ".env.installer", ".env.dev", ".env.prod"
        env_nested_delimiter = "__"
        case_sensitive = True
        extra = Extra.ignore

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            """customize sources"""
            return (
                init_settings,
                json_config_settings_source,
                env_settings,
                file_secret_settings,
            )

    def get_schema(self, schema_type: str = "default"):
        """Get schema to build UI. Schema is polished to the needs of UI"""
        if schema_type == "dereferenced":
            # https://github.com/pydantic/pydantic/issues/889#issuecomment-1064688675
            return jsonref.loads(self.schema_json())

        return self.schema()

    def persist(self):
        """Persist config to file"""
        logger.debug("persist config to json file")

        with open(CONFIG_FILENAME, mode="w", encoding="utf-8") as write_file:
            write_file.write(self.json(indent=2))

    def deleteconfig(self):
        """Reset to defaults"""
        logger.debug("config reset to default")

        try:
            os.remove(CONFIG_FILENAME)
            logger.debug(f"deleted {CONFIG_FILENAME} file.")
        except (FileNotFoundError, PermissionError):
            logger.info(f"delete {CONFIG_FILENAME} file failed.")
