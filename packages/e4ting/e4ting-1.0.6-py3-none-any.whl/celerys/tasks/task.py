
from celerys.app import BaseCeleryApp

@BaseCeleryApp()
def test():
    print("test")
    return True

@BaseCeleryApp()
def flush_iptables():
    print("test")
    return True

@BaseCeleryApp()
def botnet_ws_keepalive():
    from modules.botnet.utilbot import BotUtil
    return BotUtil.all_keepalive()

@BaseCeleryApp()
def send_note():
    from modules.botnet.utilbot import BotUtil
    return BotUtil.all_keepalive()

@BaseCeleryApp()
def send_syslog(address, data):
    from modules.webhook.robot import send_syslog
    return send_syslog(address, data)
