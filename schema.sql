CREATE TABLE users(
    id SERIAL PRIMARY KEY NOT NULL,
    username VARCHAR(40) NOT NULL,
    email TEXT NOT,
    pw VARCHAR(255) NOT NULL,
    is_active BOOLEAN

);

CREATE TABLE post(
    id SERIAL NOT NULL,
    title VARCHAR(100),
    body TEXT,
    img_url TEXT NOT NULL,
    user_id INT PRIMARY KEY NOT NULL,

    FOREIGN KEY (user_id) REFERENCES art.users (id)
);


CREATE TABLE about(
    user_id INTEGER PRIMARY KEY NOT NULL,
    body TEXT,

    FOREIGN KEY (user_id) REFERENCES art.users (id)
);