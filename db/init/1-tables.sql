SET FOREIGN_KEY_CHECKS=0;

CREATE TABLE xp (
    user_id BIGINT PRIMARY KEY NOT NULL,
    user_xp INT NOT NULL,
    user_level INT NOT NULL,
    cooldown DECIMAL(15,2)
);

CREATE TABLE currency (
    user_id BIGINT PRIMARY KEY NOT NULL,
    cash_balance BIGINT NOT NULL,
    special_balance BIGINT
);

CREATE TABLE stats_bj (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    is_won BOOLEAN,
    bet BIGINT,
    payout BIGINT,
    hand_player TEXT,
    hand_dealer TEXT
);

CREATE TABLE stats_slots (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    is_won BOOLEAN,
    bet BIGINT,
    payout BIGINT,
    spin_type TEXT,
    icons TEXT
);

CREATE TABLE stats_duel (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    is_won BOOLEAN,
    bet BIGINT
);

CREATE TABLE dailies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT,
    amount BIGINT,
    claimed_at TINYTEXT,
    streak INT
);

CREATE TABLE item (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name TEXT,
    display_name TEXT,
    description TEXT,
    image_url TEXT,
    emote_id BIGINT,
    quote TEXT,
    type TEXT
);

CREATE TABLE inventory (
    user_id BIGINT,
    item_id INT,
    quantity INT,

    PRIMARY KEY (user_id, item_id),
    FOREIGN KEY (item_id) REFERENCES item (id)
);

CREATE TABLE ShopItem (
    item_id INT PRIMARY KEY,
    price BIGINT,
    price_special BIGINT,
    worth BIGINT,
    description TEXT
);

CREATE TABLE birthdays (
  user_id BIGINT NOT NULL PRIMARY KEY,
  birthday DATETIME DEFAULT NULL
);
