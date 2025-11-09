--
-- File generated with SQLiteStudio v3.4.17 on Sun Nov 9 15:25:44 2025
--
-- Text encoding used: UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: companies
CREATE TABLE IF NOT EXISTS companies (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name TEXT (60) NOT NULL, country_code TEXT (2), parent REFERENCES companies (id));
INSERT INTO companies (id, name, country_code, parent) VALUES (1, 'Bethesda Softworks', 'US', 3);
INSERT INTO companies (id, name, country_code, parent) VALUES (2, 'Bethesda Game Studios', 'US', 1);
INSERT INTO companies (id, name, country_code, parent) VALUES (3, 'ZeniMax Media', 'US', 7);
INSERT INTO companies (id, name, country_code, parent) VALUES (4, 'Arkane Studios', 'FR', 3);
INSERT INTO companies (id, name, country_code, parent) VALUES (5, 'id Software', 'US', 3);
INSERT INTO companies (id, name, country_code, parent) VALUES (6, 'MachineGames', 'SE', 3);
INSERT INTO companies (id, name, country_code, parent) VALUES (7, 'Microsoft', 'US', NULL);
INSERT INTO companies (id, name, country_code, parent) VALUES (8, 'Activision Blizzard', 'US', 7);
INSERT INTO companies (id, name, country_code, parent) VALUES (9, 'Blizzard Entertainment', 'US', 8);

-- Table: games
CREATE TABLE IF NOT EXISTS games (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name TEXT (60) NOT NULL, publisher INTEGER REFERENCES companies (id) NOT NULL, developer INTEGER REFERENCES companies (id) NOT NULL, release_date TEXT (10) NOT NULL, score INTEGER, length REAL, has_multiplayer INTEGER (1));
INSERT INTO games (id, name, publisher, developer, release_date, score, length, has_multiplayer) VALUES (1, 'The Elder Scrolls V: Skyrim', 1, 2, '2011-11-11', NULL, 110.0, 0);
INSERT INTO games (id, name, publisher, developer, release_date, score, length, has_multiplayer) VALUES (2, 'Dishonored', 1, 4, '2012-10-09', NULL, 18.5, 0);
INSERT INTO games (id, name, publisher, developer, release_date, score, length, has_multiplayer) VALUES (3, 'Dishonored 2', 1, 4, '2016-11-11', 87, 23.0, 0);
INSERT INTO games (id, name, publisher, developer, release_date, score, length, has_multiplayer) VALUES (4, 'Prey', 1, 4, '2017-05-05', 81, 28.0, 0);
INSERT INTO games (id, name, publisher, developer, release_date, score, length, has_multiplayer) VALUES (5, 'Doom', 1, 5, '2016-05-13', 86, 16.5, 1);
INSERT INTO games (id, name, publisher, developer, release_date, score, length, has_multiplayer) VALUES (6, 'Doom Eternal', 1, 5, '2020-03-20', 89, 20.5, 1);
INSERT INTO games (id, name, publisher, developer, release_date, score, length, has_multiplayer) VALUES (7, 'Wolfenstein: The New Order', 1, 6, '2014-05-20', 82, 15.2, 0);
INSERT INTO games (id, name, publisher, developer, release_date, score, length, has_multiplayer) VALUES (8, 'Wolfenstein II: The New Colossus', 1, 6, '2017-10-27', 87, 17.0, 0);
INSERT INTO games (id, name, publisher, developer, release_date, score, length, has_multiplayer) VALUES (9, 'StarCraft', 9, 9, '1998-03-31', NULL, 27.5, 1);
INSERT INTO games (id, name, publisher, developer, release_date, score, length, has_multiplayer) VALUES (10, 'StarCraft II: Wings of Liberty', 9, 9, '2010-07-27', NULL, 21.5, 1);

-- Table: games_genres
CREATE TABLE IF NOT EXISTS games_genres (game INTEGER REFERENCES games (id) NOT NULL, genre TEXT (20) REFERENCES genres (name) NOT NULL);
INSERT INTO games_genres (game, genre) VALUES (1, 'ARPG');
INSERT INTO games_genres (game, genre) VALUES (2, 'IMM');
INSERT INTO games_genres (game, genre) VALUES (4, 'FPS');
INSERT INTO games_genres (game, genre) VALUES (3, 'IMM');
INSERT INTO games_genres (game, genre) VALUES (4, 'IMM');
INSERT INTO games_genres (game, genre) VALUES (5, 'FPS');
INSERT INTO games_genres (game, genre) VALUES (6, 'FPS');
INSERT INTO games_genres (game, genre) VALUES (8, 'FPS');
INSERT INTO games_genres (game, genre) VALUES (7, 'FPS');
INSERT INTO games_genres (game, genre) VALUES (9, 'RTS');
INSERT INTO games_genres (game, genre) VALUES (10, 'RTS');

-- Table: genres
CREATE TABLE IF NOT EXISTS genres (name TEXT (20) PRIMARY KEY UNIQUE NOT NULL, readable_name TEXT (60) UNIQUE NOT NULL, parent TEXT (20) REFERENCES genres (name));
INSERT INTO genres (name, readable_name, parent) VALUES ('ARPG', 'Action role-playing', 'RPG');
INSERT INTO genres (name, readable_name, parent) VALUES ('RPG', 'Role-playing', NULL);
INSERT INTO genres (name, readable_name, parent) VALUES ('FPS', 'First-person shooter', NULL);
INSERT INTO genres (name, readable_name, parent) VALUES ('IMM', 'Immersive sim', NULL);
INSERT INTO genres (name, readable_name, parent) VALUES ('STH', 'Stealth', NULL);
INSERT INTO genres (name, readable_name, parent) VALUES ('STR', 'Strategy', NULL);
INSERT INTO genres (name, readable_name, parent) VALUES ('RTS', 'Real-time strategy', 'STR');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
