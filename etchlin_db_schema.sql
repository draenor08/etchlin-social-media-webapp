USE etchlin_db;

-- USER TABLE
CREATE TABLE user (
    user_id VARCHAR(12) PRIMARY KEY,
    first_name VARCHAR(30),
    last_name VARCHAR(30),
    bio VARCHAR(250),
    password VARCHAR(100), -- for storing hashed password
    date_of_birth DATE,
    email VARCHAR(100)
);

-- ADMIN TABLE
CREATE TABLE admin (
    admin_id CHAR(4) PRIMARY KEY,
    user_id VARCHAR(12),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- POST TABLE
CREATE TABLE post (
    post_id VARCHAR(16) PRIMARY KEY,
    user_id VARCHAR(12),
    caption VARCHAR(2200),
    image_url VARCHAR(255) NOT NULL, -- image required
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- COMMENT TABLE
CREATE TABLE comment (
    comment_id VARCHAR(20) PRIMARY KEY,
    post_id VARCHAR(16),
    user_id VARCHAR(12),
    content VARCHAR(250),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES post(post_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- COMMENT LIST TABLE (junction table, possibly redundant)
CREATE TABLE comment_list (
    post_id VARCHAR(16),
    comment_id VARCHAR(20),
    FOREIGN KEY (post_id) REFERENCES post(post_id),
    FOREIGN KEY (comment_id) REFERENCES comment(comment_id),
    PRIMARY KEY (post_id, comment_id)
);

-- LIKE TABLE
CREATE TABLE likes (
    like_id VARCHAR(24) PRIMARY KEY,
    post_id VARCHAR(16),
    user_id VARCHAR(12),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES post(post_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id)
);

-- MESSAGE TABLE
CREATE TABLE message (
    message_number INT AUTO_INCREMENT PRIMARY KEY,
    sender_id VARCHAR(12),
    receiver_id VARCHAR(12),
    text VARCHAR(1000),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES user(user_id),
    FOREIGN KEY (receiver_id) REFERENCES user(user_id)
);

-- FRIENDS TABLE
CREATE TABLE friends (
    request VARCHAR(12),
    acceptance VARCHAR(12),
    FOREIGN KEY (request) REFERENCES user(user_id),
    FOREIGN KEY (acceptance) REFERENCES user(user_id),
    PRIMARY KEY (request, acceptance)
);

-- AUDIT LIST TABLE
CREATE TABLE audit_list (
    admin_id CHAR(4),
    user_id VARCHAR(12),
    post_id VARCHAR(16),
    comment_id VARCHAR(20),
    message VARCHAR(15),
    FOREIGN KEY (admin_id) REFERENCES admin(admin_id),
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (post_id) REFERENCES post(post_id),
    FOREIGN KEY (comment_id) REFERENCES comment(comment_id),
    PRIMARY KEY (admin_id, user_id, post_id, comment_id)
);

CREATE INDEX idx_user_email ON user(email);
CREATE INDEX idx_post_timestamp ON post(timestamp);
CREATE INDEX idx_comment_timestamp ON comment(timestamp);

-- Add status column with ENUM
ALTER TABLE friends 
ADD COLUMN status ENUM('pending', 'accepted', 'rejected') DEFAULT 'pending';

-- Add created_at timestamp column
ALTER TABLE friends 
ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- Add CHECK constraint to ensure consistent ordering
ALTER TABLE friends 
ADD CONSTRAINT chk_friends_order CHECK (request < acceptance);

-- Create indexes for performance
CREATE INDEX idx_request ON friends(request);
CREATE INDEX idx_acceptance ON friends(acceptance);

ALTER TABLE post 
ADD CONSTRAINT chk_post_content CHECK (caption IS NOT NULL OR image_url IS NOT NULL);

DROP TABLE comment_list;

ALTER TABLE post 
ADD COLUMN is_flagged BOOLEAN DEFAULT FALSE,
ADD COLUMN flag_reason VARCHAR(500);

CREATE INDEX idx_user_name ON user(first_name, last_name);
CREATE INDEX idx_flagged_posts ON post(is_flagged);

ALTER TABLE user
ADD COLUMN profile_picture VARCHAR(255) DEFAULT NULL;
