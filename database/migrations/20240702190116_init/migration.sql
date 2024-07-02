-- CreateTable
CREATE TABLE "xp" (
    "user_id" BIGINT NOT NULL,
    "guild_id" BIGINT NOT NULL,
    "user_xp" INTEGER NOT NULL,
    "user_level" INTEGER NOT NULL,
    "cooldown" REAL,

    PRIMARY KEY ("user_id", "guild_id")
);

-- CreateTable
CREATE TABLE "currency" (
    "user_id" BIGINT NOT NULL PRIMARY KEY,
    "balance" BIGINT NOT NULL
);

-- CreateTable
CREATE TABLE "blackjack" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "user_id" BIGINT,
    "is_won" BOOLEAN,
    "bet" BIGINT,
    "payout" BIGINT,
    "hand_player" TEXT,
    "hand_dealer" TEXT
);

-- CreateTable
CREATE TABLE "slots" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "user_id" BIGINT,
    "is_won" BOOLEAN,
    "bet" BIGINT,
    "payout" BIGINT,
    "spin_type" TEXT,
    "icons" TEXT
);

-- CreateTable
CREATE TABLE "dailies" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "user_id" BIGINT,
    "amount" BIGINT,
    "claimed_at" TEXT,
    "streak" INTEGER
);

-- CreateTable
CREATE TABLE "item" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "name" TEXT,
    "display_name" TEXT,
    "description" TEXT,
    "image_url" TEXT,
    "emote_id" BIGINT,
    "quote" TEXT,
    "type" TEXT
);

-- CreateTable
CREATE TABLE "inventory" (
    "user_id" BIGINT NOT NULL,
    "item_id" INTEGER NOT NULL,
    "quantity" INTEGER NOT NULL,

    PRIMARY KEY ("user_id", "item_id"),
    CONSTRAINT "inventory_item_id_fkey" FOREIGN KEY ("item_id") REFERENCES "item" ("id") ON DELETE RESTRICT ON UPDATE CASCADE
);

-- CreateTable
CREATE TABLE "birthdays" (
    "user_id" BIGINT NOT NULL,
    "guild_id" BIGINT NOT NULL,
    "birthday" DATETIME,

    PRIMARY KEY ("user_id", "guild_id")
);

-- CreateTable
CREATE TABLE "guild_config" (
    "guild_id" BIGINT NOT NULL PRIMARY KEY,
    "prefix" TEXT,
    "birthday_channel_id" BIGINT,
    "command_channel_id" BIGINT,
    "intro_channel_id" BIGINT,
    "welcome_channel_id" BIGINT,
    "welcome_message" TEXT,
    "boost_channel_id" BIGINT,
    "boost_message" TEXT,
    "boost_image_url" TEXT,
    "level_channel_id" BIGINT,
    "level_message" TEXT,
    "level_message_type" INTEGER NOT NULL DEFAULT 1
);

-- CreateTable
CREATE TABLE "level_rewards" (
    "guild_id" BIGINT NOT NULL,
    "level" INTEGER NOT NULL,
    "role_id" BIGINT,
    "persistent" BOOLEAN,

    PRIMARY KEY ("guild_id", "level")
);

-- CreateTable
CREATE TABLE "blacklist_user" (
    "user_id" BIGINT NOT NULL PRIMARY KEY,
    "reason" TEXT,
    "timestamp" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "active" BOOLEAN NOT NULL DEFAULT true
);
