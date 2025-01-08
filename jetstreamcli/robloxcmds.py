import click
import inquirer

from colorama import Fore
from jetstreamcli.config import load_config, save_config
from jetstreamcli.robloxfuncs import keyTest

@click.command()
@click.option("-k", "--key", prompt="Enter Key", help="Your Roblox Cloud Key", type = str)
def set(key):
    """Set the Roblox Cloud API Key"""
    
    config = load_config()
    config["robloxKey"] = key
    
    save_config(config)

    click.echo(Fore.GREEN + "✅ Successfully saved Roblox API Key.")

@click.command()
@click.option("-i", "--id", prompt="Provide the User or Group ID of the uploader", help="The User or Group ID of the uploader", type = str)
def uploader(id):
    """Set the uploader for the Roblox assets"""
    
    questions = [
    inquirer.List('type',
                    message="Key Type",
                    choices=['User', 'Group'],
                ),
    ]
    
    answers = inquirer.prompt(questions)
    
    if answers == None:
        return
    
    config = load_config()
    
    match answers["type"]:
        case "User":
            config["groupKey"] = False
        case "Group":
            config["groupKey"] = True
    
    config["uploader"] = id
    
    save_config(config)

    click.echo(Fore.GREEN + "✅ Successfully saved Roblox uploader.")
    
@click.command()
def test():
    """Test your current key"""
    result = keyTest()

    if not result["ok"]:
        click.echo(result["msg"])
    else:
        click.echo("")
        click.echo(Fore.RED + "🚀 Jetstream Key Test")
        click.echo("")
        click.echo(Fore.CYAN + "User found!")
        click.echo("")
        click.echo(Fore.RESET + "Id: " + str(result["id"]))
        click.echo("Username: " + str(result["username"]))
        click.echo("Link: " + Fore.BLUE + f"https://roblox.com/users/{result['id']}")
        click.echo("")
        click.echo(Fore.GREEN + "✅ Key Works!")
