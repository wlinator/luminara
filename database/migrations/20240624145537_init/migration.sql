-- CreateTable
CREATE TABLE "xp" (
    "user_id" BIGINT NOT NULL,
    "guild_id" BIGINT NOT NULL,
    "user_xp" INTEGER NOT NULL,
    "user_level" INTEGER NOT NULL,
    "cooldown" DOUBLE PRECISION,

    CONSTRAINT "xp_pkey" PRIMARY KEY ("user_id","guild_id")
);

-- CreateTable
CREATE TABLE "currency" (
    "user_id" BIGINT NOT NULL,
    "balance" BIGINT NOT NULL,

    CONSTRAINT "currency_pkey" PRIMARY KEY ("user_id")
);

-- CreateTable
CREATE TABLE "blackjack" (
    "id" SERIAL NOT NULL,
    "user_id" BIGINT,
    "is_won" BOOLEAN,
    "bet" BIGINT,
    "payout" BIGINT,
    "hand_player" TEXT,
    "hand_dealer" TEXT,

    CONSTRAINT "blackjack_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "slots" (
    "id" SERIAL NOT NULL,
    "user_id" BIGINT,
    "is_won" BOOLEAN,
    "bet" BIGINT,
    "payout" BIGINT,
    "spin_type" TEXT,
    "icons" TEXT,

    CONSTRAINT "slots_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "dailies" (
    "id" SERIAL NOT NULL,
    "user_id" BIGINT,
    "amount" BIGINT,
    "claimed_at" TEXT,
    "streak" INTEGER,

    CONSTRAINT "dailies_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "item" (
    "id" SERIAL NOT NULL,
    "name" TEXT,
    "display_name" TEXT,
    "description" TEXT,
    "image_url" TEXT,
    "emote_id" BIGINT,
    "quote" TEXT,
    "type" TEXT,

    CONSTRAINT "item_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "inventory" (
    "user_id" BIGINT NOT NULL,
    "item_id" INTEGER NOT NULL,
    "quantity" INTEGER NOT NULL,

    CONSTRAINT "inventory_pkey" PRIMARY KEY ("user_id","item_id")
);

-- CreateTable
CREATE TABLE "birthdays" (
    "user_id" BIGINT NOT NULL,
    "guild_id" BIGINT NOT NULL,
    "birthday" TIMESTAMP(3),

    CONSTRAINT "birthdays_pkey" PRIMARY KEY ("user_id","guild_id")
);

-- CreateTable
CREATE TABLE "guild_config" (
    "guild_id" BIGINT NOT NULL,
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
    "level_message_type" INTEGER NOT NULL DEFAULT 1,

    CONSTRAINT "guild_config_pkey" PRIMARY KEY ("guild_id")
);

-- CreateTable
CREATE TABLE "level_rewards" (
    "guild_id" BIGINT NOT NULL,
    "level" INTEGER NOT NULL,
    "role_id" BIGINT,
    "persistent" BOOLEAN,

    CONSTRAINT "level_rewards_pkey" PRIMARY KEY ("guild_id","level")
);

-- CreateTable
CREATE TABLE "blacklist_user" (
    "user_id" BIGINT NOT NULL,
    "reason" TEXT,
    "timestamp" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "active" BOOLEAN NOT NULL DEFAULT true,

    CONSTRAINT "blacklist_user_pkey" PRIMARY KEY ("user_id")
);

-- AddForeignKey
ALTER TABLE "inventory" ADD CONSTRAINT "inventory_item_id_fkey" FOREIGN KEY ("item_id") REFERENCES "item"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
