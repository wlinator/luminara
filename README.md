# You can invite me with [this link](https://discord.com/oauth2/authorize?client_id=1038050427272429588&permissions=8&scope=bot). Thanks for using Luminara!

![Lumi art](https://git.wlinator.org/assets/img/logo.png)

## Self-host

**The next part of this README explains how to self-host Lumi, this allows you to host your own version of my code and
create a personalized Discord bot.**

**Note: because the `.slots` and `.blackjack` commands use custom (animated) emoji, these commands will break when you self-host Lumi. Please replace the ID values in `config/JSON/resources.json` with your own set of emotes.**

### Installation
#### Docker
Lumi comes containerized with essential components such as MariaDB, its core application and Adminer. 

To install Lumi, run these commands:

```commandline
git clone https://git.wlinator.org/Luminara/Lumi && cd Lumi
```

Copy `.env.template` to `.env` and fill out the [variables](#environment-variables).

```commandline
docker compose up -d --build
```

Please note that it's highly recommended to establish a reverse proxy setup for Adminer, ensuring better security and accessibility.
- Adminer should be directed to port 8080.

#### Alternative
You can run Lumi without Docker, however I don't provide support or documentation for this. Here are some requirements to get you started.

- MariaDB server on port 3306.
- Python 3.11 with the [required pip packages](requirements.txt).
- See the environment variables in [docker-compose.yml](docker-compose.yml) and set them manually.


## Environment variables (.env)

- `TOKEN`: your Discord Bot Token, you can get this [here](https://discord.com/developers/applications).  
- `DBX_*`: set these up if you want to make database backups to your Dropbox app.  
- `MARIADB_USER`: the username for your MariaDB database.  
- `MARIADB_PASSWORD`: the password for your database.  
- `MARIADB_ROOT_PASSWORD`: can be ignored unless you have a specific use for it.
- `MARIADB_DATABASE`: the name of your database.

Other variables can be specified in `docker.compose.yml` (core)

---

Some icons used in Lumi are provided by [Icons8](https://icons8.com/).
