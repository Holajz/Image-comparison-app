

CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  first_name TEXT NOT NULL,
  second_name TEXT NOT NULL,
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  zip TEXT NOT NULL,
  role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rating (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  rated_first INTEGER,
  rated_second INTEGER,
  rated_third INTEGER,
  rated_forth INTEGER,
  rated_fifth INTEGER,
  rated_sixth INTEGER,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (rated_first) REFERENCES images (image_id),
  FOREIGN KEY (rated_second) REFERENCES images (image_id),
  FOREIGN KEY (rated_third) REFERENCES images (image_id),
  FOREIGN KEY (rated_forth) REFERENCES images (image_id),
  FOREIGN KEY (rated_fifth) REFERENCES images (image_id),
  FOREIGN KEY (rated_sixth) REFERENCES images (image_id)
);

CREATE TABLE IF NOT EXISTS selection (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  rated_first INTEGER,
  rated_second INTEGER,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (rated_first) REFERENCES images (image_id),
  FOREIGN KEY (rated_second) REFERENCES images (image_id)
);

CREATE TABLE IF NOT EXISTS amount (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  image_rated INTEGER,
  rating INTEGER,
  FOREIGN KEY (author_id) REFERENCES user (id),
  FOREIGN KEY (image_rated) REFERENCES images (image_id)
);

CREATE TABLE IF NOT EXISTS updates (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  rating_id INTEGER,
  image_id INTEGER,
  old_pos INTEGER,
  new_pos INTEGER
);

DROP TABLE IF EXISTS images;

CREATE TABLE IF NOT EXISTS images (
  image_id INTEGER PRIMARY KEY AUTOINCREMENT,
  image_url TEXT UNIQUE NOT NULL,
  group_status TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS groups (
  group_name TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS current_group (
  current_group_name TEXT
);

DELETE FROM images;
DELETE FROM groups;
DELETE FROM current_group;
delete from sqlite_sequence where name='images';
VACUUM;

INSERT INTO current_group VALUES ('default');

-- INSERT INTO images (image_url, group_status) VALUES ("images/cat1.jpg", "default");
-- INSERT INTO images (image_url, group_status) VALUES ("images/cat2.jpg", "default");
-- INSERT INTO images (image_url, group_status) VALUES ("images/cat3.jpg", "default");
-- INSERT INTO images (image_url, group_status) VALUES ("images/cat4.jpg", "default");
-- INSERT INTO images (image_url, group_status) VALUES ("images/cat5.jpg", "default");
-- INSERT INTO images (image_url, group_status) VALUES ("images/cat6.jpg", "default");
-- INSERT INTO images (image_url, group_status) VALUES ("images/cat7.jpg", "default");
-- INSERT INTO images (image_url, group_status) VALUES ("images/cat8.jpg", "default");
-- INSERT INTO images (image_url, group_status) VALUES ("images/cat9.jpg", "default");
-- INSERT INTO images (image_url, group_status) VALUES ("images/cat10.jpg", "default");
-- INSERT INTO images (image_url, group_status) VALUES ("images/cat11.jpg", "default");
-- INSERT INTO images (image_url, group_status) VALUES ("images/cat12.jpg", "default");