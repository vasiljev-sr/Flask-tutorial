DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS current_position;
DROP TABLE IF EXISTS positions;
DROP TABLE IF EXISTS order_history;
DROP TABLE IF EXISTS bot_settings;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE current_position (
  id INTEGER NOT NULL,
  datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (id) REFERENCES positions (id)

);

CREATE TABLE positions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  opened_position TEXT NOT NULL,
  entry_price INTEGER NOT NULL,
  symbol TEXT NOT NULL,
  position_size INTEGER NOT NULL,
  margin INTEGER NOT NULL,
  profit INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL
);

CREATE TABLE order_history (
  id INTEGER NOT NULL,
  datetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  operation TEXT NOT NULL,
  amount INTEGER NOT NULL,
  price INTEGER NOT NULL,
  FOREIGN KEY (id) REFERENCES positions (id)
);

CREATE TABLE bot_settings (
  position_amt INTEGER NOT NULL DEFAULT 0.01 ,
  symbol TEXT NOT NULL DEFAULT 'ETHUSDT' ,
  stop_percent INTEGER NOT NULL DEFAULT 0.01

);

INSERT INTO positions (id,opened_position, entry_price, symbol, position_size, margin,profit, status)
VALUES (0, 0, 0, 0, 0, 0, 0, 0);

INSERT INTO current_position (id)
VALUES (0);

INSERT INTO bot_settings (position_amt)
VALUES (0.01)