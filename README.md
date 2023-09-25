# Versatileus

## Functionalities

- Keep threads alive once a week
- Support DCouter.space bot and ban main accounts of banned alt-accounts
- Kick @unverified group members every 8 hours

## Disclaimer

Slash commands can take some time to get registered globally, so if you want to test a command you should use
the `@app_commands.guilds()` decorator so that it gets registered instantly. Example:

```py
@commands.hybrid_command(
  name="command",
  description="Command description",
)
@app_commands.guilds(discord.Object(id=GUILD_ID)) # Place your guild ID here
```

When using the template you confirm that you have read the [license](LICENSE.md) and comprehend that I can take down
your repository if you do not meet these requirements.

Please do not open issues or pull requests about things that are written in the [TODO file](TODO.md), they are **already** under work for a future version of the template.

## How to download it

* Clone/Download the repository
    * To clone it and get the updates you can definitely use the command
      `git clone`
* Create a discord bot [here](https://discord.com/developers/applications)
* Get your bot token
* Invite your bot on servers using the following invite:
  https://discord.com/oauth2/authorize?&client_id=YOUR_APPLICATION_ID_HERE&scope=bot+applications.commands&permissions=PERMISSIONS (
  Replace `YOUR_APPLICATION_ID_HERE` with the application ID and replace `PERMISSIONS` with the required permissions
  your bot needs that it can be get at the bottom of a this
  page https://discord.com/developers/applications/YOUR_APPLICATION_ID_HERE/bot)

## How to set up

To set up the bot is as simple as possible. Copy the config.json.example to [config.json](config.json) file where you can put the needed things to edit.

Here is an explanation of what everything is:

| Variable                  | What it is                                                            |
| ------------------------- | ----------------------------------------------------------------------|
| prefix                    | The prefix you want to use for normal commands                        |
| token                     | The token of your bot                                                 |
| permissions               | The permissions integer your bot needs when it gets invited           |
| application_id            | The application ID of your bot                                        |
| owners                    | The user ID of all the bot owners                                     |
| dc_bot_channel            | The channel ID of the dcounter.space bot logs                         |
| unverified_role_name      | Human readable dcounter.space @Unverified group name                  |
| unverified_role_id        | The group ID of the dcounter.space @Unverified group                  |
| verified_role_id          | The group ID of the dcounter.space verified users group               |


## How to start

To start the bot you simply need to launch, either your terminal (Linux, Mac & Windows), or your Command Prompt (
Windows)
.

Before running the bot you will need to install all the requirements with this command:

```
python -m pip install -r requirements.txt
```

After that you can start it with

```
python bot.py
```

> **Note** You may need to replace `python` with `py`, `python3`, `python3.11`, etc. depending on what Python versions you have installed on the machine.

## Built With

* [Python 3.9.12](https://www.python.org/)

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE.md](LICENSE.md) file for details

## Original code

https://github.com/kkrypt0nn/Python-Discord-Bot-Template