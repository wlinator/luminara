CREATE TABLE IF NOT EXISTS mod_log (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT UNSIGNED NOT NULL,
    channel_id BIGINT UNSIGNED NOT NULL,
    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS action_types (
    id SERIAL PRIMARY KEY,
    name ENUM(
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
    ) NOT NULL
);

CREATE TABLE IF NOT EXISTS cases (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT UNSIGNED NOT NULL,
    case_number INT UNSIGNED NOT NULL,
    target_id BIGINT UNSIGNED NOT NULL,
    moderator_id BIGINT UNSIGNED NOT NULL,
    action_type_id INT UNSIGNED NOT NULL,
    reason TEXT,
    duration INT UNSIGNED, -- for timeouts
    expires_at TIMESTAMP, -- for tempbans & mutes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (action_type_id) REFERENCES action_types(id)
);

CREATE TABLE IF NOT EXISTS permissions (
    id SERIAL PRIMARY KEY,
    guild_id BIGINT UNSIGNED NOT NULL,
    role_id BIGINT UNSIGNED NOT NULL,
    action_type_id INT UNSIGNED NOT NULL,
    is_allowed BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (action_type_id) REFERENCES action_types(id)
);

CREATE INDEX idx_cases_guild_id ON cases(guild_id);
CREATE INDEX idx_cases_target_id ON cases(target_id);
CREATE INDEX idx_cases_moderator_id ON cases(moderator_id);
CREATE INDEX idx_cases_action_type_id ON cases(action_type_id);
CREATE INDEX idx_permissions_guild_id ON permissions(guild_id);
CREATE INDEX idx_permissions_role_id ON permissions(role_id);
CREATE INDEX idx_permissions_action_type_id ON permissions(action_type_id);
