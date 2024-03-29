# You can invite me with [this link](https://discord.com/oauth2/authorize?client_id=1038050427272429588&permissions=8&scope=bot). Thanks for using Racu!

![Racu art](art/racu_logo.png)

## Self host

**The next part of this README explains how to self-host Racu, this allows you to host your own version of my code and
create a personalized Discord bot.**

### 📲 Installation

Racu is containerized: its core, database, database admin platform and logger run on Docker without any extra
configuration.
However, you CAN run it locally without Docker by hosting MariaDB on your machine with the login credentials specified
in [.env](.env.template) and installing **Python 3.11** with the [required pip packages](requirements.txt). **Note: I
won't explain how to do this. Figure it out on your own.**

```sh
git clone https://gitlab.com/wlinator/racu && cd racu
```

Copy `.env.template` to `.env` and fill out the [variables](#env-keys).

**Optional:** copy `users.yml.example` to `users.yml` to properly configure Dozzle logs. Check the file for more
information.

```sh
docker compose up -d --build
```

## ⚙️ Environment variables

- `TOKEN`: your Discord Bot Token, you can get this [here](https://discord.com/developers/applications).
- `INSTANCE`: this should always be "MAIN" unless you plan to run multiple bots (for testing purposes).
- `OWNER_ID`: the Discord user ID of the person who will act as owner of this bot.

- `XP_GAIN_PER_MESSAGE`: how much XP should be awarded to a user per message.
- `XP_GAIN_COOLDOWN`: XP earning cooldown time in seconds.

- The values with "DBX" can be ignored unless you plan to make database backups with Dropbox. In that case enter your
  Dropbox API credentials.

- `MARIADB_USER`: the username for your MariaDB database.
- `MARIADB_PASSWORD`: the password for your database.
- `MARIADB_ROOT_PASSWORD`: the root password for your database. (can be ignored unless you have a specific use for it)

---

Some icons used in Racu are provided by [Icons8](https://icons8.com/).
