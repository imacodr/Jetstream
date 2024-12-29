from rblxopencloud import User, ApiKey
from colorama import Fore, Back, Style
from termcolor import colored

from config import load_config

def get_key():
    config = load_config()

    if config["robloxKey"] == None:
            return {"ok": False, "msg": Fore.YELLOW + "⚠️ You don't have a key! Add a key using " + colored("jetstream roblox set", "black", "on_yellow")}
    
    return {"ok": True, "key": config["robloxKey"]}


def keyTest():
    try:
        keyc = get_key()

        if not keyc["ok"]:
             return keyc
        
        user = User(501780776, keyc["key"])

        info = user.fetch_info()

        return {"ok": True, "id": info.id, "username": info.username}
    except:
        return {"ok": False, "msg": Fore.RED + "❌ An error occured. Key may be invalid or no permissions have been given."}