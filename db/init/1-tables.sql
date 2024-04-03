SET FOREIGN_KEY_CHECKS=0;

CREATE TABLE xp (
    user_id BIGINT NOT NULL,
    guild_id BIGINT NOT NULL,
    user_xp INT NOT NULL,
    user_level INT NOT NULL,
    cooldown DECIMAL(15,2),
    PRIMARY KEY (user_id, guild_id)
);

CREATE TABLE currency (
    user_id BIGINT NOT NULL,
    balance BIGINT NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE blackjack (
    id INT AUTO_INCREMENT,
    user_id BIGINT,
    is_won BOOLEAN,
    bet BIGINT,
    payout BIGINT,
    hand_player TEXT,
    hand_dealer TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE slots (
    id INT AUTO_INCREMENT,
    user_id BIGINT,
    is_won BOOLEAN,
    bet BIGINT,
    payout BIGINT,
    spin_type TEXT,
    icons TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE dailies (
    id INT AUTO_INCREMENT,
    user_id BIGINT,
    amount BIGINT,
    claimed_at TINYTEXT,
    streak INT,
    PRIMARY KEY (id)
);

CREATE TABLE item (
    id INT AUTO_INCREMENT,
    name TEXT,
    display_name TEXT,
    description TEXT,
    image_url TEXT,
    emote_id BIGINT,
    quote TEXT,
    type TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE inventory (
    user_id BIGINT,
    item_id INT,
    quantity INT,

    PRIMARY KEY (user_id, item_id),
    FOREIGN KEY (item_id) REFERENCES item (id)
);

CREATE TABLE birthdays (
  user_id BIGINT NOT NULL,
  guild_id BIGINT NOT NULL,
  birthday DATETIME DEFAULT NULL,
  PRIMARY KEY (user_id, guild_id)
);

CREATE TABLE guild_config (
    guild_id BIGINT NOT NULL,
    prefix TINYTEXT,
    birthday_channel_id BIGINT, 
    command_channel_id BIGINT, /* NULL: users can do XP & Currency commands everywhere. */
    intro_channel_id BIGINT,
    welcome_channel_id BIGINT,
    welcome_message TEXT,
    level_channel_id BIGINT,   /* level-up messages, if NULL the level-up message will be shown in current msg channel*/
    level_message TEXT,  /* if NOT NULL and LEVEL_TYPE = 2, this can be a custom level up message. */
    level_message_type TINYINT(1) NOT NULL DEFAULT 1,   /* 0: no level up messages, 1: levels.en-US.json, 2: generic message */
    PRIMARY KEY (guild_id)
);

CREATE TABLE level_rewards (
    guild_id BIGINT NOT NULL,
    level INT NOT NULL,
    role_id BIGINT,
    persistent BOOLEAN,

    PRIMARY KEY (guild_id, role_id)
);

CREATE TABLE blacklist_user (
    user_id BIGINT NOT NULL,
    reason TEXT,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    active BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (user_id)
);
