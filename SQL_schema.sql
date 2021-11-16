CREATE TABLE Users
(uid SERIAL,
name VARCHAR(20) NOT NULL,
present_mood INTEGER CHECK (present_mood > 0 AND present_mood < 7), -- we have 6 catagory of mood
email VARCHAR(35) NOT NULL CHECK(email LIKE '%_@_%._%'),
password VARCHAR(50) NOT NULL,
is_active BOOL,
PRIMARY KEY(uid),
UNIQUE(email));

CREATE TABLE Groups
(group_id SERIAL,
 type INTEGER CHECK (type > 0 AND type < 7), -- we have 6 catagory of mood
 group_name VARCHAR(50) NOT NULL,
 PRIMARY KEY(group_id),
 UNIQUE(group_name));

CREATE TABLE Dep_posts              --weak entity relationship
(post_no SERIAL CHECK (post_no > 0),
 time timestamp,
 uid SERIAL,
 PRIMARY KEY(uid, post_no),
 FOREIGN KEY (uid) REFERENCES Users);

CREATE TABLE Group_posts
(uid SERIAL,
 group_id SERIAL NOT NULL,
 post_no SERIAL CHECK (post_no > 0),
 text VARCHAR(200),
 image_URL VARCHAR(100) CHECK(image_URL LIKE 'https://_%'),
 PRIMARY KEY(uid, post_no),
 FOREIGN KEY(uid, post_no) REFERENCES Dep_posts ON DELETE CASCADE,
 FOREIGN KEY(group_id) REFERENCES Groups ON DELETE CASCADE);

--longitude and latitude represents location of the user when posting 

CREATE TABLE Personal_mood
(longitude DECIMAL CHECK (longitude <= 180 AND longitude >= -180),
 latitude DECIMAL CHECK (latitude <= 90 AND latitude >= -90), 
 uid SERIAL,
 post_no SERIAL CHECK (post_no > 0),
 mood INTEGER CHECK (mood > 0 AND mood < 7), -- we have 6 catagory of mood
 PRIMARY KEY(uid, post_no),
 FOREIGN KEY(uid, post_no) REFERENCES Dep_posts ON DELETE CASCADE);

-- total participation to the Dep_post
-- non-overlapping condition between Personal_mood and Group_post

CREATE TABLE Dep_comments         --weak entity relationship
(comment_no SERIAL CHECK (comment_no > 0),
 uid_comment SERIAL,
 uid_post SERIAL,
 post_no SERIAL CHECK (post_no > 0),
 text VARCHAR(200),
 time timestamp,
 CHECK ((uid_post = NULL AND post_no = NULL) OR (uid_post <> NULL AND post_no <> NULL)),    -- uid_post and post_no should be NULL together when the comment is comment to another comment
 PRIMARY KEY(uid_comment, comment_no),
 FOREIGN KEY(uid_comment) REFERENCES Users ON DELETE CASCADE,
 FOREIGN KEY(uid_post, post_no) REFERENCES Dep_posts ON DELETE CASCADE);


--  participation of Group to the User (If no users stays in a group, that group will be deleted automatically)

CREATE TABLE User_in_group
(uid SERIAL,
 group_id SERIAL,
 level INTEGER CHECK (level < 6 AND level > 0),     -- we have 5 level in total
 PRIMARY KEY(uid, group_id),
 FOREIGN KEY(uid) REFERENCES Users ON DELETE CASCADE,
 FOREIGN KEY(group_id) REFERENCES Groups ON DELETE CASCADE);


CREATE TABLE Follow
(uid_following SERIAL,
 uid_followed SERIAL,
 PRIMARY KEY (uid_following, uid_followed),
 FOREIGN KEY(uid_following) REFERENCES Users ON DELETE CASCADE,
 FOREIGN KEY(uid_followed) REFERENCES Users ON DELETE CASCADE);

CREATE TABLE comments_to_comments
(uid1 SERIAL,
 uid2 SERIAL,
 comments_no1 SERIAL CHECK (comments_no1 > 0),
 comments_no2 SERIAL CHECK (comments_no2 > 0),
 PRIMARY KEY(uid1, comments_no1, uid2, comments_no2),
 FOREIGN KEY(uid1, comments_no1) REFERENCES Dep_comments,
 FOREIGN KEY(uid2, comments_no2) REFERENCES Dep_comments ON DELETE CASCADE);

CREATE TABLE Responses_to_post
(uid_post SERIAL,
 post_no SERIAL CHECK (post_no > 0),
 uid_like SERIAL,
 mood INTEGER CHECK (mood > 0 AND mood < 7),
 time timestamp,
 PRIMARY KEY(uid_post, post_no, uid_like),
 FOREIGN KEY(uid_post, post_no) REFERENCES Dep_posts ON DELETE CASCADE,
 FOREIGN KEY(uid_like) REFERENCES Users ON DELETE CASCADE);


CREATE TABLE Responses_to_comment
(uid_comment SERIAL,
 comment_no INTEGER CHECK (comment_no > 0),
 uid_like SERIAL,
 mood INTEGER CHECK (mood > 0 AND mood < 7),
 time timestamp,
 PRIMARY KEY(uid_comment, comment_no, uid_like),
 FOREIGN KEY(uid_comment, comment_no) REFERENCES Dep_comments ON DELETE CASCADE,
 FOREIGN KEY(uid_like) REFERENCES Users ON DELETE CASCADE);