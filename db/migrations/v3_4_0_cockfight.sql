-- Cockfight System Migration v3.4.0

-- Create table for roosters (player's fighting cocks)
CREATE TABLE IF NOT EXISTS roosters (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    name VARCHAR(50) NOT NULL,
    level INT NOT NULL DEFAULT 1,
    xp INT NOT NULL DEFAULT 0,
    xp_needed INT NOT NULL DEFAULT 100,
    wins INT NOT NULL DEFAULT 0,
    losses INT NOT NULL DEFAULT 0,
    strength INT NOT NULL DEFAULT 5,
    agility INT NOT NULL DEFAULT 5,
    endurance INT NOT NULL DEFAULT 5,
    technique INT NOT NULL DEFAULT 5,
    luck INT NOT NULL DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_battle TIMESTAMP NULL,
    UNIQUE KEY (user_id),
    INDEX (user_id)
);

-- Create table for rooster equipment slots
CREATE TABLE IF NOT EXISTS rooster_equipment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rooster_id INT NOT NULL,
    head_item_id INT NULL,
    body_item_id INT NULL,
    leg_item_id INT NULL,
    spur_item_id INT NULL,
    talisman_item_id INT NULL,
    FOREIGN KEY (rooster_id) REFERENCES roosters(id) ON DELETE CASCADE,
    INDEX (rooster_id)
);

-- Create table for items that can be equipped by roosters
CREATE TABLE IF NOT EXISTS rooster_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    item_type ENUM('head', 'body', 'leg', 'spur', 'talisman') NOT NULL,
    rarity ENUM('common', 'uncommon', 'rare', 'epic', 'legendary') NOT NULL DEFAULT 'common',
    strength_bonus INT NOT NULL DEFAULT 0,
    agility_bonus INT NOT NULL DEFAULT 0,
    endurance_bonus INT NOT NULL DEFAULT 0,
    technique_bonus INT NOT NULL DEFAULT 0,
    luck_bonus INT NOT NULL DEFAULT 0,
    special_effect TEXT NULL,
    created_by BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX (item_type),
    INDEX (rarity)
);

-- Create table for user inventory of rooster items
CREATE TABLE IF NOT EXISTS user_rooster_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES rooster_items(id) ON DELETE CASCADE,
    INDEX (user_id),
    INDEX (item_id)
);

-- Create table for campaign/story mode
CREATE TABLE IF NOT EXISTS cockfight_campaign (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    difficulty ENUM('tutorial', 'easy', 'medium', 'hard', 'expert', 'master') NOT NULL,
    required_level INT NOT NULL DEFAULT 1,
    xp_reward INT NOT NULL DEFAULT 10,
    coin_reward INT NOT NULL DEFAULT 5,
    item_reward_id INT NULL,
    opponent_strength INT NOT NULL DEFAULT 5,
    opponent_agility INT NOT NULL DEFAULT 5,
    opponent_endurance INT NOT NULL DEFAULT 5,
    opponent_technique INT NOT NULL DEFAULT 5,
    opponent_luck INT NOT NULL DEFAULT 5,
    is_boss BOOLEAN NOT NULL DEFAULT FALSE,
    unlock_campaign_id INT NULL,
    FOREIGN KEY (item_reward_id) REFERENCES rooster_items(id) ON DELETE SET NULL,
    FOREIGN KEY (unlock_campaign_id) REFERENCES cockfight_campaign(id) ON DELETE SET NULL,
    INDEX (difficulty),
    INDEX (required_level)
);

-- Create table for user campaign progress
CREATE TABLE IF NOT EXISTS user_campaign_progress (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    campaign_id INT NOT NULL,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    attempts INT NOT NULL DEFAULT 0,
    last_attempt TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (campaign_id) REFERENCES cockfight_campaign(id) ON DELETE CASCADE,
    UNIQUE KEY (user_id, campaign_id),
    INDEX (user_id),
    INDEX (campaign_id)
);

-- Create table for multiplayer battles
CREATE TABLE IF NOT EXISTS cockfight_battles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    challenger_rooster_id INT NOT NULL,
    opponent_rooster_id INT NOT NULL,
    winner_rooster_id INT NULL,
    wager_amount INT NOT NULL DEFAULT 0,
    battle_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    battle_log TEXT NULL,
    FOREIGN KEY (challenger_rooster_id) REFERENCES roosters(id) ON DELETE CASCADE,
    FOREIGN KEY (opponent_rooster_id) REFERENCES roosters(id) ON DELETE CASCADE,
    FOREIGN KEY (winner_rooster_id) REFERENCES roosters(id) ON DELETE SET NULL,
    INDEX (challenger_rooster_id),
    INDEX (opponent_rooster_id)
);

-- Create table for achievements
CREATE TABLE IF NOT EXISTS cockfight_achievements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    requirement_type ENUM('wins', 'battles', 'campaign', 'level', 'boss', 'streak') NOT NULL,
    requirement_value INT NOT NULL,
    xp_reward INT NOT NULL DEFAULT 0,
    coin_reward INT NOT NULL DEFAULT 0,
    item_reward_id INT NULL,
    icon_url VARCHAR(255) NULL,
    FOREIGN KEY (item_reward_id) REFERENCES rooster_items(id) ON DELETE SET NULL,
    INDEX (requirement_type)
);

-- Create table for user achievements
CREATE TABLE IF NOT EXISTS user_achievements (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    achievement_id INT NOT NULL,
    unlocked BOOLEAN NOT NULL DEFAULT FALSE,
    progress INT NOT NULL DEFAULT 0,
    unlocked_at TIMESTAMP NULL,
    FOREIGN KEY (achievement_id) REFERENCES cockfight_achievements(id) ON DELETE CASCADE,
    UNIQUE KEY (user_id, achievement_id),
    INDEX (user_id),
    INDEX (achievement_id)
);

-- Create table for daily quests
CREATE TABLE IF NOT EXISTS cockfight_quests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    quest_type ENUM('win_battles', 'participate_battles', 'train_rooster', 'defeat_campaign', 'equip_items') NOT NULL,
    target_count INT NOT NULL DEFAULT 1,
    xp_reward INT NOT NULL DEFAULT 10,
    coin_reward INT NOT NULL DEFAULT 5,
    item_reward_id INT NULL,
    is_daily BOOLEAN NOT NULL DEFAULT TRUE,
    is_weekly BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (item_reward_id) REFERENCES rooster_items(id) ON DELETE SET NULL,
    INDEX (quest_type),
    INDEX (is_daily),
    INDEX (is_weekly)
);

-- Create table for user quests
CREATE TABLE IF NOT EXISTS user_quests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    quest_id INT NOT NULL,
    progress INT NOT NULL DEFAULT 0,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (quest_id) REFERENCES cockfight_quests(id) ON DELETE CASCADE,
    INDEX (user_id),
    INDEX (quest_id),
    INDEX (completed)
);

-- Create table for rooster training sessions
CREATE TABLE IF NOT EXISTS rooster_training (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rooster_id INT NOT NULL,
    training_type ENUM('strength', 'agility', 'endurance', 'technique', 'luck') NOT NULL,
    points_gained INT NOT NULL DEFAULT 1,
    trained_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rooster_id) REFERENCES roosters(id) ON DELETE CASCADE,
    INDEX (rooster_id),
    INDEX (training_type)
);

-- Insert initial tutorial campaign stages
INSERT INTO cockfight_campaign (name, description, difficulty, required_level, xp_reward, coin_reward, opponent_strength, opponent_agility, opponent_endurance, opponent_technique, opponent_luck, is_boss)
VALUES 
('First Steps', 'Learn the basics of cockfighting with your new rooster.', 'tutorial', 1, 20, 10, 3, 3, 3, 3, 3, FALSE),
('Basic Training', 'Put your training to the test against a slightly tougher opponent.', 'tutorial', 1, 30, 15, 4, 4, 4, 4, 4, FALSE),
('The Challenger', 'Face your first real challenge in the ring.', 'easy', 2, 50, 25, 6, 6, 6, 5, 5, FALSE),
('Local Champion', 'Defeat the local champion to prove your worth.', 'easy', 3, 100, 50, 8, 8, 7, 7, 6, TRUE);

-- Insert some starter achievements
INSERT INTO cockfight_achievements (name, description, requirement_type, requirement_value, xp_reward, coin_reward)
VALUES 
('Novice Trainer', 'Reach level 5 with your rooster.', 'level', 5, 50, 25),
('Battle Hardened', 'Participate in 10 cockfights.', 'battles', 10, 30, 15),
('Victorious', 'Win 5 cockfights.', 'wins', 5, 40, 20),
('Campaign Hero', 'Complete all tutorial campaign stages.', 'campaign', 3, 100, 50),
('Boss Slayer', 'Defeat your first boss.', 'boss', 1, 150, 75),
('Winning Streak', 'Win 3 cockfights in a row.', 'streak', 3, 60, 30);

-- Insert some starter quests
INSERT INTO cockfight_quests (name, description, quest_type, target_count, xp_reward, coin_reward, is_daily, is_weekly)
VALUES 
('Daily Training', 'Train your rooster once today.', 'train_rooster', 1, 15, 10, TRUE, FALSE),
('Battle Ready', 'Participate in 3 cockfights today.', 'participate_battles', 3, 25, 15, TRUE, FALSE),
('Winner Winner', 'Win 2 cockfights today.', 'win_battles', 2, 30, 20, TRUE, FALSE),
('Campaign Progress', 'Complete a campaign stage.', 'defeat_campaign', 1, 20, 15, TRUE, FALSE),
('Weekly Champion', 'Win 10 cockfights this week.', 'win_battles', 10, 100, 75, FALSE, TRUE);

-- Insert some starter items
INSERT INTO rooster_items (name, description, item_type, rarity, strength_bonus, agility_bonus, endurance_bonus, technique_bonus, luck_bonus, created_by)
VALUES 
('Leather Helmet', 'A basic protective headgear for your rooster.', 'head', 'common', 1, 0, 1, 0, 0, 0),
('Steel Spurs', 'Basic metal spurs that increase attack power.', 'spur', 'common', 2, 0, 0, 0, 0, 0),
('Training Vest', 'A lightweight vest that improves endurance.', 'body', 'common', 0, 0, 2, 0, 0, 0),
('Agility Bands', 'Leg bands that improve movement speed.', 'leg', 'common', 0, 2, 0, 0, 0, 0),
('Lucky Feather', 'A special feather that brings good fortune.', 'talisman', 'uncommon', 0, 0, 0, 0, 2, 0),
('Champion\'s Crest', 'A prestigious headpiece worn by champion roosters.', 'head', 'rare', 2, 1, 2, 1, 0, 0),
('Razor Spurs', 'Dangerously sharp spurs for serious fighters.', 'spur', 'rare', 4, 1, 0, 1, 0, 0);
