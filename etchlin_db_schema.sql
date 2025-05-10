-- DATABASE SETUP
DROP DATABASE IF EXISTS etchlin_db;
CREATE DATABASE etchlin_db;
USE etchlin_db;

-- USER TABLE
CREATE TABLE user (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    bio VARCHAR(250),
    password VARCHAR(100),
    date_of_birth DATE,
    email VARCHAR(100),
    profile_picture VARCHAR(255) DEFAULT NULL
);

-- ADMIN TABLE
CREATE TABLE admin (
    admin_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- POST TABLE
CREATE TABLE post (
    post_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    caption VARCHAR(2200),
    image_url VARCHAR(255),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_flagged BOOLEAN DEFAULT FALSE,
    flag_reason VARCHAR(500),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    CONSTRAINT chk_post_content CHECK (caption IS NOT NULL OR image_url IS NOT NULL)
);

-- COMMENT TABLE
CREATE TABLE comment (
    comment_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    post_id INT,
    user_id INT,
    content VARCHAR(250),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_blurred BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (post_id) REFERENCES post(post_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- LIKE TABLE
CREATE TABLE likes (
    like_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    post_id INT,
    user_id INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES post(post_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- MESSAGE TABLE
CREATE TABLE message (
    message_number INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    text VARCHAR(1000),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES user(user_id),
    FOREIGN KEY (receiver_id) REFERENCES user(user_id)
);

-- FRIENDS TABLE (one-way friendship model)
CREATE TABLE friends (
    request INT,
    acceptance INT,
    status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request) REFERENCES user(user_id),
    FOREIGN KEY (acceptance) REFERENCES user(user_id),
    PRIMARY KEY (request, acceptance),
    CONSTRAINT chk_friends_order CHECK (request < acceptance)
);

-- AUDIT LIST TABLE
CREATE TABLE audit_list (
    admin_id INT,
    user_id INT,
    post_id INT,
    comment_id INT,
    message VARCHAR(500),
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (post_id) REFERENCES post(post_id),
    FOREIGN KEY (comment_id) REFERENCES comment(comment_id),
    PRIMARY KEY (admin_id, user_id, post_id, comment_id)
);

-- INDEXES
CREATE INDEX idx_user_email ON user(email);
CREATE INDEX idx_user_name ON user(first_name, last_name);
CREATE INDEX idx_post_timestamp ON post(timestamp);
CREATE INDEX idx_flagged_posts ON post(is_flagged);
CREATE INDEX idx_comment_timestamp ON comment(timestamp);
CREATE INDEX idx_request ON friends(request);
CREATE INDEX idx_acceptance ON friends(acceptance);

-- OPTIONAL DUMMY USERS (edit as needed)
INSERT INTO user (first_name, last_name, email, password, bio, profile_picture)
VALUES 
('Abi', 'Nana', 'abi@email.com', '6b6406a2f2f2b8012c08e9c304e0ab6cbe0e2e6e3aa3a7a9f1b6a84c678a4c63$0a1b2c3d4e5f67890123456789abcdef', 'Just vibing', '/media/person/08.jpg'),
('Dummy', 'One', 'd1@email.com', '6b6406a2f2f2b8012c08e9c304e0ab6cbe0e2e6e3aa3a7a9f1b6a84c678a4c63$0a1b2c3d4e5f67890123456789abcdef', 'Bio 1', '/media/person/1.jpeg'),
('Dummy', 'Two', 'd2@email.com', '6b6406a2f2f2b8012c08e9c304e0ab6cbe0e2e6e3aa3a7a9f1b6a84c678a4c63$0a1b2c3d4e5f67890123456789abcdef', 'Bio 2', '/media/person/2.jpeg'),
('Dummy', 'Three', 'd3@email.com', '6b6406a2f2f2b8012c08e9c304e0ab6cbe0e2e6e3aa3a7a9f1b6a84c678a4c63$0a1b2c3d4e5f67890123456789abcdef', 'Bio 3', '/media/person/3.jpeg'),
('Dummy', 'Four', 'd4@email.com', '6b6406a2f2f2b8012c08e9c304e0ab6cbe0e2e6e3aa3a7a9f1b6a84c678a4c63$0a1b2c3d4e5f67890123456789abcdef', 'Bio 4', '/media/person/4.jpeg'),
('Dummy', 'Five', 'd5@email.com', '6b6406a2f2f2b8012c08e9c304e0ab6cbe0e2e6e3aa3a7a9f1b6a84c678a4c63$0a1b2c3d4e5f67890123456789abcdef', 'Bio 5', '/media/person/5.jpeg'),
('Dummy', 'Six', 'd6@email.com', '6b6406a2f2f2b8012c08e9c304e0ab6cbe0e2e6e3aa3a7a9f1b6a84c678a4c63$0a1b2c3d4e5f67890123456789abcdef', 'Bio 6', '/media/person/6.jpeg'),
('Dummy', 'Seven', 'd7@email.com', '6b6406a2f2f2b8012c08e9c304e0ab6cbe0e2e6e3aa3a7a9f1b6a84c678a4c63$0a1b2c3d4e5f67890123456789abcdef', 'Bio 7', '/media/person/7.jpeg'),
('Dummy', 'Eight', 'd8@email.com', '6b6406a2f2f2b8012c08e9c304e0ab6cbe0e2e6e3aa3a7a9f1b6a84c678a4c63$0a1b2c3d4e5f67890123456789abcdef', 'Bio 8', '/media/person/8.jpeg'),
('Dummy', 'Nine', 'd9@email.com', '6b6406a2f2f2b8012c08e9c304e0ab6cbe0e2e6e3aa3a7a9f1b6a84c678a4c63$0a1b2c3d4e5f67890123456789abcdef', 'Bio 9', '/media/person/9.jpeg'),
('Dummy', 'Ten', 'd10@email.com', '6b6406a2f2f2b8012c08e9c304e0ab6cbe0e2e6e3aa3a7a9f1b6a84c678a4c63$0a1b2c3d4e5f67890123456789abcdef', 'Bio 9', '/media/person/10.jpeg' );
-- FRIENDSHIPS (Abi follows all)
INSERT INTO friends (request, acceptance, status)
VALUES
(1, 2, 'accepted'), (1, 3, 'accepted'), (1, 4, 'accepted'),
(1, 5, 'accepted'), (1, 6, 'accepted'), (1, 7, 'accepted'),
(1, 8, 'accepted'), (1, 9, 'accepted'), (1, 10, 'accepted');

-- POSTS (one per dummy user)
INSERT INTO post (user_id, caption, image_url)
VALUES 
(2, 'Sunset hikes are the best.', '/media/post/1.jpeg'),
(3, 'Trying out my new camera 📸', '/media/post/2.jpeg'),
(4, 'Weekend vibes with coffee.', '/media/post/3.jpeg'),
(5, 'Beach day with the squad!', '/media/post/4.jpeg'),
(6, 'Morning runs hit different.', '/media/post/5.jpeg'),
(7, 'Chilling with my doggo 🐶', '/media/post/6.jpeg'),
(8, 'Old books, new memories.', '/media/post/7.jpeg'),
(9, 'Cloudy skies, moody mind.', '/media/post/8.jpeg'),
(10, 'Candid shot by a friend.', '/media/post/9.jpeg'),
(2, 'Nothing like homemade food.', '/media/post/10.jpeg');

-- COMMENTS (loop-style)
INSERT INTO comment (post_id, user_id, content)
VALUES 
(1, 3, 'Beautiful shot! 🔥'),
(2, 4, 'Love this vibe!'),
(3, 5, 'This is so calming.'),
(4, 6, 'Epic memories bro!'),
(5, 7, 'Healthy mornings are the best.'),
(6, 8, 'Cute dog!'),
(7, 9, 'Nice book collection!'),
(8, 10, 'You ok bud? Looks gloomy.'),
(9, 2, 'Great composition!'),
(10, 3, 'Yummy! Save some for me.');
