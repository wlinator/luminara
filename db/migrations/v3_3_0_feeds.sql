CREATE TABLE IF NOT EXISTS feeds (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT UNSIGNED NOT NULL,
    channel_id BIGINT UNSIGNED NOT NULL,
    announcement_message TEXT NOT NULL,
    feed_type ENUM('twitch', 'youtube_new', 'youtube_live') NOT NULL,
    username VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE OR REPLACE INDEX idx_feeds_guild_id ON feeds(guild_id);
CREATE OR REPLACE INDEX idx_feeds_feed_type ON feeds(feed_type);
