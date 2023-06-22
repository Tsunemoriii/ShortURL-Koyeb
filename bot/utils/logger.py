import importlib
import logging
import sys
from pathlib import Path

logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] [%(name)s] : %(message)s",
    level=logging.INFO,
    datefmt="%H:%M:%S",
)

logging.getLogger("pyrogram").setLevel(logging.WARNING)
Logger = logging.getLogger(__name__)


def load_plugins(plugin_name):
    path = Path(f"bot/plugins/{plugin_name}.py")
    name = "bot.plugins.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["bot.plugins." + plugin_name] = load
    print(f"Bot Imported {plugin_name}")
