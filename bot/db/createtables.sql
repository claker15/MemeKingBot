CREATE DATABASE IF NOT EXISTS MEMEKING;

USE MEMEKING;

DROP TABLE `user`;

CREATE TABLE `user` (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(50),
    guild_id VARCHAR(50),
    crowns INT DEFAULT (0),
    wand VARCHAR(20) DEFAULT ('Wood'),
    created TIMESTAMP DEFAULT (NOW()),
);

DROP TABLE post;

CREATE TABLE post(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    hash VARCHAR(500),
    path VARCHAR(150),
    user_id VARCHAR(50),
    guild_id VARCHAR(50),
    message_id VARCHAR(100),
    created TIMESTAMP DEFAULT (NOW())
);

DROP TABLE points;

CREATE TABLE points(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(50),
    guild_id VARCHAR(50),
    user_id_from VARCHAR(50),
    value INT,
    type VARCHAR(20),
    message_id VARCHAR(50),
    created TIMESTAMP DEFAULT (NOW())
);

DROP TABLE url;

CREATE TABLE url(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    url VARCHAR(500),
    guild_id VARCHAR(50),
    created TIMESTAMP DEFAULT (NOW())
);

DROP TABLE bets;

CREATE TABLE bets(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    message_id VARCHAR(50),
    user_id VARCHAR (50),
    target_id VARCHAR(50),
    guild_id VARCHAR(50),
    bet INT,
    valid BOOL,
    created TIMESTAMP DEFAULT (NOW())
);

DROP TABLE sounds;

CREATE TABLE sounds(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200),
    path VARCHAR(500),
    guild_id VARCHAR(50),
    created TIMESTAMP DEFAULT (NOW())
);

DROP TABLE music;

CREATE TABLE music(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(50),
    guild_id VARCHAR(50),
    title VARCHAR(200),
    artist_name VARCHAR(200),
    track_pop INT,
    artist_pop INT,
    created TIMESTAMP DEFAULT (NOW())
);

DROP TABLE song_winner;

CREATE TABLE song_winner(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    guild_id VARCHAR(50),
    title VARCHAR(200),
    artist_name VARCHAR(200),
    created TIMESTAMP DEFAULT (NOW())
);

DROP TABLE artist_winner;

CREATE TABLE artist_winner(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    guild_id VARCHAR(50),
    artist_name VARCHAR(200),
    created TIMESTAMP DEFAULT (NOW())
);

DROP TABLE login;

CREATE TABLE login(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(50),
    guild_id VARCHAR(50),
    created TIMESTAMP DEFAULT (NOW())
);
