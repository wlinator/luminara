ALTER TABLE XP
ADD COLUMN guild_id BIGINT NOT NULL;

CREATE TABLE guild_config (
    guild_id BIGINT NOT NULL,
    birthday_channel_id BIGINT,
    command_channel_id BIGINT, /* NULL: users can do XP & Currency commands everywhere. */
    intro_channel_id BIGINT,
    welcome_channel_id BIGINT,
    level_channel_id BIGINT,   /* level-up messages, if NULL the level-up message will be shown in current msg channel*/
    level_message TEXT,  /* if NOT NULL and LEVEL_TYPE = 2, this can be a custom level up message. */
    level_message_type TINYINT(1) NOT NULL DEFAULT 1,   /* 0: no level up messages, 1: levels.en-US.json, 2: generic message */
    PRIMARY KEY (guild_id)
);

CREATE TABLE blacklist_user (
    user_id BIGINT NOT NULL,
    reason TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    active BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (user_id)
);

UPDATE XP
SET guild_id = 719227135151046699
WHERE guild_id IS NULL;