"""."""
import logging
from slrd.controllers.fs_controller import FSController


logging.getLogger(__name__).addHandler(logging.NullHandler())
fsctrl = FSController()
