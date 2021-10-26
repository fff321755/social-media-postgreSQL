CREATE TABLE Users
(uid CHAR(10),
name VARCHAR(20),
present_mood INTEGER,
email VARCHAR(35),
is_active BOOL,
PRIMARY KEY(uid),
UNIQUE(email));

CREATE TABLE Groups
(group_id CHAR(10),
 type INTEGER,
 group_name VARCHAR(50),
 PRIMARY KEY(group_id),
 UNIQUE(group_name));

CREATE TABLE Dep_posts              --weak entity relationship
(post_no INTEGER,
 time timestamp,
 uid CHAR(10),
 PRIMARY KEY(uid, post_no),
 FOREIGN KEY (uid) REFERENCES Users);

CREATE TABLE Group_posts
(uid CHAR(10),
 group_id CHAR(10) NOT NULL,
 post_no INTEGER,
 text VARCHAR(200),
 image_URL VARCHAR(100),
 PRIMARY KEY(uid, post_no),
 FOREIGN KEY(uid, post_no) REFERENCES Dep_posts ON DELETE CASCADE,
 FOREIGN KEY(group_id) REFERENCES Groups ON DELETE CASCADE);

--longitude and latitude represents location of the user when posting 

CREATE TABLE Personal_mood
(longitude DECIMAL,
 latitude DECIMAL, 
 uid CHAR(10),
 post_no INTEGER,
 image_URL VARCHAR(100),
 PRIMARY KEY(uid, post_no),
 FOREIGN KEY(uid, post_no) REFERENCES Dep_posts ON DELETE CASCADE);

-- total participation to the Dep_post
-- non-overlapping condition between Personal_mood and Group_post

CREATE TABLE Dep_comments         --weak entity relationship
(comment_no INTEGER,
 uid_comment CHAR(10),
 uid_post CHAR(10) NOT NULL,
 post_no INTEGER NOT NULL,
 text VARCHAR(200),
 PRIMARY KEY(uid_comment, comment_no),
 FOREIGN KEY(uid_comment) REFERENCES Users ON DELETE CASCADE,
 FOREIGN KEY(uid_post, post_no) REFERENCES Dep_posts ON DELETE CASCADE);


--  participation of Group to the User (If no users stays in a group, that group will be deleted automatically)

CREATE TABLE User_in_group
(uid CHAR(10),
 group_id CHAR(10),
 level INTEGER,
 PRIMARY KEY(uid, group_id),
 FOREIGN KEY(uid) REFERENCES Users ON DELETE CASCADE,
 FOREIGN KEY(group_id) REFERENCES Groups ON DELETE CASCADE);


CREATE TABLE Follow
(uid_following CHAR(10),
 uid_followed CHAR(10),
 PRIMARY KEY (uid_following, uid_followed),
 FOREIGN KEY(uid_following) REFERENCES Users ON DELETE CASCADE,
 FOREIGN KEY(uid_followed) REFERENCES Users ON DELETE CASCADE);

CREATE TABLE comments_to_comments
(uid1 CHAR(10),
 uid2 CHAR(10),
 comments_no1 INTEGER,
 comments_no2 INTEGER,
 PRIMARY KEY(uid1, comments_no1, uid2, comments_no2),
 FOREIGN KEY(uid1, comments_no1) REFERENCES Dep_comments,
 FOREIGN KEY(uid2, comments_no2) REFERENCES Dep_comments ON DELETE CASCADE);

CREATE TABLE Responses_to_post
(uid_post CHAR(10),
 post_no INTEGER,
 uid_like CHAR(10),
 mood INTEGER,
 time timestamp,
 PRIMARY KEY(uid_post, post_no, uid_like),
 FOREIGN KEY(uid_post, post_no) REFERENCES Dep_posts ON DELETE CASCADE,
 FOREIGN KEY(uid_like) REFERENCES Users ON DELETE CASCADE);


CREATE TABLE Responses_to_comment
(uid_comment CHAR(10),
 comment_no INTEGER,
 uid_like CHAR(10),
 mood INTEGER,
 time timestamp,
 PRIMARY KEY(uid_comment, comment_no, uid_like),
 FOREIGN KEY(uid_comment, comment_no) REFERENCES Dep_comments ON DELETE CASCADE,
 FOREIGN KEY(uid_like) REFERENCES Users ON DELETE CASCADE);