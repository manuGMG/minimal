# Minimal
Minimal and Extensible Discord Bot *(Boilerplate).*

## How-To
In order to run `minimal`, Python 3.7+ and the `discord.py` package must be installed.

    pip install discord.py
    python3 /folder/to/minimal

After the first run, `config.json` will get created in the `/minimal` directory and should be edited with a valid token. Cogs can also be added and prefix(es) can be changed.

    {
        "token": "YOUR_TOKEN_HERE",
        "prefixes": [
            "min "
        ],
        "cogs": [
            "owner"
        ]
    }

Cogs can be added by copying them to the `cogs` folder and then loading them from Discord. For example, the music cog can be added by moving it from `minimal-cogs` to `minimal/cogs`, and then by running this command from Discord:

    min cog load music

Cogs can also be reloaded, unloaded and listed.

    min cog reload {cog_name}
    min cog unload {cog_folder}.{cog_name}
    min cog list

This functionality is provided by `owner.py`, so `owner` cog should not be unloaded. Note that this commands can only be executed by the bot owner.

# Example cogs
Some cogs are provided as an example.

### hello
* **description**: An example cog.
* **dependencies**: none.

### music
* **description**: Minimal 85 SLOC music cog. **Requires** `ffmpeg` installed and on path.
* **dependencies:** `pynacl`, `youtube_dl`.