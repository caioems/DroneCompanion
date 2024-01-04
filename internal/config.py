## Module that holds constants and configs
import simplekml

## DayChecker configs
MESSAGES = [
    "BAT",
    "CAM",
    "EV",
    "MSG",
    "POWR",
    "RCOU",
    "TRIG",
    "VIBE"
    ]           

CAMERA_ISO_RANGE = (100, 1600)
CAMERA_SHUTTER = "1/1600"
CAMERA_COPYRIGHT_PATTERN = r"a[0-9]r[0-9]_[a-z]{3}"
CAMERA_ARTIST_PATTERN = r"^\d{7}$"
RAW_GNSS_LOG_NAME = "SEQLOG00"

LINESTYLE_WIDTH = 2
LINESTYLE_COLOR = simplekml.Color.red

## HealthTests configs
MOTORS_WARN_LEVEL = 45
MOTORS_FAIL_LEVEL = 60
MAX_VIBRATION = 30
VCC_WARN_LEVEL = 4.9
VCC_FAIL_LEVEL = 4.8


