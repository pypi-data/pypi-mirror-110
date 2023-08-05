"""ai_object_detection - AI Object Detection"""
try:
  import importlib_resources as _resources
except ImportError:  # Python 2
  import importlib.resources as _resources

try:
  from configparser import ConfigParser as _ConfigParser
except ImportError:  # Python 2
  from ConfigParser import ConfigParser as _ConfigParser

__version__ = '1.1.7'
__author__ = 'Nhan Vo <nhanvpt102@gmail.com>'
__all__ = []

# Read URL from config file
#_cfg = _ConfigParser()
#with _resources.path("setup.cfg") as _path:
#  _cfg.read(str(_path))
#URL_REGISTER = _cfg.get("urls", "url_register")

from ai_object_detection.libimageprocessor import ImageProcessor
from ai_object_detection.libselenium import WebBrowser
from ai_object_detection.libexcel import ExcelReader
