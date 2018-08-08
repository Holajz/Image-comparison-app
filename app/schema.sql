DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS user_display;
DROP TABLE IF EXISTS rating;
DROP TABLE IF EXISTS images;

CREATE TABLE user (
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

CREATE TABLE rating (
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

CREATE TABLE images (
  image_id INTEGER PRIMARY KEY AUTOINCREMENT,
  image_url TEXT UNIQUE NOT NULL
);

INSERT INTO images (image_url) VALUES ("images/cat1.jpg");
INSERT INTO images (image_url) VALUES ("images/cat2.jpg");
INSERT INTO images (image_url) VALUES ("images/cat3.jpg");
INSERT INTO images (image_url) VALUES ("images/cat4.jpg");
INSERT INTO images (image_url) VALUES ("images/cat5.jpg");
INSERT INTO images (image_url) VALUES ("images/cat6.jpg");
INSERT INTO images (image_url) VALUES ("images/cat7.jpg");
INSERT INTO images (image_url) VALUES ("images/cat8.jpg");
INSERT INTO images (image_url) VALUES ("images/cat9.jpg");
INSERT INTO images (image_url) VALUES ("images/cat10.jpg");
INSERT INTO images (image_url) VALUES ("images/cat11.jpg");
INSERT INTO images (image_url) VALUES ("images/cat12.jpg");
