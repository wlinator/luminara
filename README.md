# You can invite me with [this link](https://discord.com/oauth2/authorize?client_id=1038050427272429588&permissions=8&scope=bot). Thanks for using Racu!

![Racu art](art/racu_logo.png)

## Self-host

**The next part of this README explains how to self-host Racu, this allows you to host your own version of my code and
create a personalized Discord bot.**

**Note: because the `.slots` and `.blackjack` commands use custom (animated) emoji, these commands will break when you self-host Racu. Please replace the ID values in `config/JSON/resources.json` with your own set of emotes, or ask [wlinator](<https://discord.com/users/784783517845946429>) to let your bot join [Racu's Emote Server](https://discord.gg/B9jm2NgX5H).**

### Installation
#### Docker
By default, Racu comes containerized with mariadb, its core application, [adminer](https://www.adminer.org/), and [dozzle](https://dozzle.dev/). 
However, to let Dozzle function as intended, copy `users.yml.example` to `users.yml` and configure an auth user. (See the file for more info).

To install Racu, run these commands:

```commandline
git clone https://gitlab.com/wlinator/racu && cd racu
```

Copy `.env.template` to `.env` and fill out the [variables](#environment-variables).

```commandline
docker compose up -d --build
```

Note: This won't affect the functioning of the bot, but it's best practice to set up a reverse proxy for adminer and dozzle.
- Adminer on `port 8080`
- Dozzle on `port 8081`

#### Alternative
You can run Racu without Docker, however I don't provide support or documentation for this. Here are some requirements to get you started.

- MariaDB server on port 3306.
- Python 3.11 with the [required pip packages](requirements.txt).
- See the environment variables in [docker-compose.yml](docker-compose.yml) and set them manually.


## Environment variables (.env)

`TOKEN`: your Discord Bot Token, you can get this [here](https://discord.com/developers/applications). </br>
`DBX_OAUTH2_REFRESH_TOKEN`, `DBX_APP_KEY`, `DBX_APP_SECRET`: set these up if you want to make database backups to your Dropbox app. </br>
`MARIADB_USER`: the username for your MariaDB database. </br>
`MARIADB_PASSWORD`: the password for your database. </br>
`MARIADB_ROOT_PASSWORD`: the root password for your database. (can be ignored unless you have a specific use for it) </br>
`MARIADB_DATABASE`: the name of your database.

Other variables can be specified in `docker.compose.yml` (core)

---

Some icons used in Racu are provided by [Icons8](https://icons8.com/).
