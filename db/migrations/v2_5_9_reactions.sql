-- Create a table to store custom reactions
CREATE TABLE IF NOT EXISTS custom_reactions (
    id SERIAL PRIMARY KEY,  -- Unique identifier for each custom reaction
    trigger_text TEXT NOT NULL,  -- The text that triggers the custom reaction
    response TEXT,  -- The response text for the custom reaction (nullable for emoji reactions)
    emoji_id BIGINT UNSIGNED,  -- The emoji for the custom reaction (nullable for text responses)
    is_emoji BOOLEAN DEFAULT FALSE,  -- Indicates if the reaction is a discord emoji reaction
    is_full_match BOOLEAN DEFAULT FALSE,  -- Indicates if the trigger matches the full content of the message
    is_global BOOLEAN DEFAULT TRUE,  -- Indicates if the reaction is global or specific to a guild
    guild_id BIGINT UNSIGNED,  -- The ID of the guild where the custom reaction is used (nullable for global reactions)
    creator_id BIGINT UNSIGNED NOT NULL,  -- The ID of the user who created the custom reaction
    usage_count INT DEFAULT 0,  -- The number of times a custom reaction has been used
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp when the custom reaction was created
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Timestamp when the custom reaction was last updated
    CONSTRAINT unique_trigger_guild UNIQUE (trigger_text, guild_id)  -- Ensure that the combination of trigger_text, guild_id, and is_full_match is unique
);

-- Create indexes to speed up lookups
CREATE OR REPLACE INDEX idx_custom_reactions_guild_id ON custom_reactions(guild_id);
CREATE OR REPLACE INDEX idx_custom_reactions_creator_id ON custom_reactions(creator_id);
CREATE OR REPLACE INDEX idx_custom_reactions_trigger_text ON custom_reactions(trigger_text);