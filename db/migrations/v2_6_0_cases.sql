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
    modlog_message_id BIGINT UNSIGNED,
    is_closed BOOLEAN NOT NULL DEFAULT FALSE, -- to indicate if the case is closed
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (action_type_id) REFERENCES action_types(id)
    UNIQUE KEY unique_case (guild_id, case_number)
);

DELIMITER //

CREATE PROCEDURE insert_case(
    IN p_guild_id BIGINT UNSIGNED,
    IN p_target_id BIGINT UNSIGNED,
    IN p_moderator_id BIGINT UNSIGNED,
    IN p_action_type_id INT UNSIGNED,
    IN p_reason TEXT,
    IN p_duration INT UNSIGNED,
    IN p_expires_at TIMESTAMP,
    IN p_modlog_message_id BIGINT UNSIGNED
)
BEGIN
    DECLARE v_case_number INT UNSIGNED;

    -- Get the next case number for the guild
    SELECT IFNULL(MAX(case_number), 0) + 1 INTO v_case_number
    FROM cases
    WHERE guild_id = p_guild_id;

    -- Insert the new case
    INSERT INTO cases (
        guild_id, case_number, target_id, moderator_id, action_type_id, reason, duration, expires_at, modlog_message_id
    ) VALUES (
        p_guild_id, v_case_number, p_target_id, p_moderator_id, p_action_type_id, p_reason, p_duration, p_expires_at, p_modlog_message_id
    );
END //

DELIMITER ;


CREATE INDEX idx_cases_guild_id ON cases(guild_id);
CREATE INDEX idx_cases_target_id ON cases(target_id);
CREATE INDEX idx_cases_moderator_id ON cases(moderator_id);
CREATE INDEX idx_cases_action_type_id ON cases(action_type_id);