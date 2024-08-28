CREATE TABLE IF NOT EXISTS mod_log (
    guild_id BIGINT UNSIGNED NOT NULL PRIMARY KEY,
    channel_id BIGINT UNSIGNED NOT NULL,
    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cases (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT UNSIGNED NOT NULL,
    case_number INT UNSIGNED NOT NULL,
    target_id BIGINT UNSIGNED NOT NULL,
    moderator_id BIGINT UNSIGNED NOT NULL,
    action_type ENUM(
        'WARN',
        'TIMEOUT',
        'UNTIMEOUT',
        'KICK',
        'BAN',
        'UNBAN',
        'SOFTBAN',
        'TEMPBAN',
        'NOTE',
        'MUTE',
        'UNMUTE',
        'DEAFEN',
        'UNDEAFEN'
    ) NOT NULL,
    reason TEXT,
    duration INT UNSIGNED, -- for timeouts
    expires_at TIMESTAMP, -- for tempbans & mutes
    modlog_message_id BIGINT UNSIGNED,
    is_closed BOOLEAN NOT NULL DEFAULT FALSE, -- to indicate if the case is closed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_case (guild_id, case_number)
);


CREATE OR REPLACE INDEX idx_cases_guild_id ON cases(guild_id);
CREATE OR REPLACE INDEX idx_cases_target_id ON cases(target_id);
CREATE OR REPLACE INDEX idx_cases_moderator_id ON cases(moderator_id);
CREATE OR REPLACE INDEX idx_cases_action_type ON cases(action_type);