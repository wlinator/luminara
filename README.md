<h1 align="center">
  <a href="https://github.com/wlinator/luminara">
    <img
      src="https://git.wlinator.org/Luminara/Art/raw/branch/main/lumi_logo_transparent.png"
      alt="logo" width="128" height="128">
  </a>
  <br />
  Luminara
</h1>

<div align="center">
  <i>A General purpose Discord bot with a focus on robust moderation.</i>
  <br />
   <a href="https://discord.com/oauth2/authorize?client_id=1038050427272429588&permissions=8&scope=bot">
    Invite to Discord
  </a>
   · 
  <a href="https://github.com/wlinator/luminara/issues/new?assignees=&labels=&projects=&template=bug_report.md&title=">
    Report a Bug
  </a>
   · 
  <a href="https://github.com/wlinator/luminara/issues/new?assignees=&labels=&projects=&template=feature_request.md&title=">
    Request a Feature
  </a>
  <br /> <br />  

  [![Project
  license](https://img.shields.io/badge/license-GPL--3.0--only-blue
)](LICENSE)
  ![Pull Requests
  welcome](https://img.shields.io/badge/PRs-much_appreciated!-pink
)

</div>
     


---


## Self-Hosting

Self-hosting refers to running Luminara on your own server or computer, rather than using the publicly hosted version.
This approach offers the ability to manage your own instance of the bot and give it a custom name and avatar.

**Note:** From `v2.9.0` and onward, Lumi now utilizes a [settings.yaml](settings.yaml) file to manage configuration settings. This allows you to customize your bot's behavior without needing to modify the source code itself.

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

1. Copy [`docker-compose.prod.yml`](docker-compose.prod.yml), [`settings.yaml`](settings.yaml), and [`.env.example`](.env.example) to an empty directory.

2. Rename `docker-compose.prod.yml` to `docker-compose.yml`.

3. Rename `.env.example` to `.env` and fill it out with your specific configuration details.

4. Run the following command in your terminal:

   ```
   docker compose up -d --build
   ```

This will build and start Luminara in detached mode.

---

Some icons used in Lumi are provided by [Icons8](https://icons8.com/).
