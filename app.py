from crawler.crawler_instance.application_controller.application_controller import application_controller
from crawler.crawler_instance.application_controller.application_enums import APPICATION_COMMANDS

application_controller.get_instance().invoke_triggers(APPICATION_COMMANDS.S_START_APPLICATION)
