# You can invite me with [this link](https://discord.com/oauth2/authorize?client_id=1038050427272429588&permissions=8&scope=bot). Thanks for using Luminara!

![Lumi art](https://git.wlinator.org/assets/img/logo.png)

## Self-Hosting

Self-hosting refers to running Luminara on your own server or computer, rather than using the publicly hosted version.
This approach offers the ability to manage your own instance of the bot and give it a custom name and avatar.

### Requirements

Before you begin, make sure you have the following installed on your system:

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Additionally, you'll need to create a Discord bot application and obtain a token:

1. Go to the [Discord Developer Portal](https://discord.com/developers/applications).
2. Click on "New Application" and give it a name.
3. Navigate to the "Bot" tab and click "Add Bot".
4. Under the bot's username, click "Reset Token" to reveal your bot token.
5. Copy this token; you'll need it for the `.env` file later.

*Note: remember to keep your bot token secret and never share it publicly.*

### Running Luminara:

1. Copy the contents from [`docker-compose.prod.yml`](docker-compose.prod.yml) to a new file named `docker-compose.yml`
   in an empty directory.

2. Copy the contents from [`.env.example`](.env.example) to a new file named `.env` in the same directory.

3. Fill out the `.env` file with your specific configuration details.

4. Run the following command in your terminal:

   ```
   docker compose up -d --build
   ```

This will build and start Luminara in detached mode.

---

Some icons used in Lumi are provided by [Icons8](https://icons8.com/).
