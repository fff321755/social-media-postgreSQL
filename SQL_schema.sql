CREATE TABLE Users
(uid : CHAR(10),
name : VARCHAR(20),
present_mood : INTEGER,
email : VARCHAR(35),
is_active : BOOL,
PRIMARY KEY(uid),
UNIQUE(email))

CREATE TABLE Group(
(group_id : CHAR(10),
 type : INTEGER,
 group_name : VARCHAR(50)
 PRIMARY KEY(group_id),
 UNIQUE(group_name))

CREATE TABLE Dep_post               **weak entity relationship
(post_no : INTEGER,
 time : DATETIME,
 uid : CHAR(10),
 PRIMARY KEY(post_num, uid),
 FOREIGN KEY (uid) REFERENCES Users)

CREATE TABLE Group_post
(uid : CHAR(10),
 group_id : CHAR(10),
 post_no : INTEGER,
 text : VARCHAR(200),
 image_URL : VARCHAR(100),
 PRIMARY KEY(uid, post_no),
 FOREIGN KEY(uid, post_no) REFERENCES Dep_post
 	ON DELETE CASCADE,
 FOREIGN KEY(group_id) REFERENCES Group,
    ON DELETE CASCADE)

CREATE TABLE Personal_mood
(location : CHAR(30), 
 uid : CHAR(10),
 post_no : INTEGER,
 PRIMARY KEY(uid, post_no),
 FOREIGN KEY(uid, post_no) REFERENCES Dep_post
	ON DELETE CASCADE)

-- total participation to the Dep_post
-- non-overlapping condition between Personal_mood and Group_post

CREATE TABLE Dep_comments         **weak entity relationship
(comment_no : INTEGER,
 uid_comment : CHAR(10),
 uid_post : CHAR(10),
 post_no : INTEGER,
 text : VARCHAR(200),
 PRIMARY KEY(uid_comment, comment_no),
 FOREIGN KEY(uid_comment) REFERENCES Users
 	ON DELETE CASCADE
 FOREIGN KEY(uid_post, post_no) REFERENCES Dep_post
    ON DELETE CASCADE)

CREATE TABLE User_in_group
(uid : INTEGER
 group_id : CHAR(10),
 level : INTEGER,
 PRIMARY KEY(uid, group_id),
 FOREIGN KEY(uid) REFERENCES Users
 	ON DELETE CASCADE
 FOREIGN KEY(group_id) REFERENCES Group
	ON DELETE CASCADE)

--  participation of Group to the User (If no users stays in a group, that group will be deleted automatically)


CREATE TABLE Follow
(uid_following : CHAR(10),
 uid_followed : CHAR(10),
 PRIMARY KEY (uid_following, uid_followed),
 FOREIGN KEY(uid_following) REFERENCES Users
	ON DELETE CASCADE
 FOREIGN KEY(uid_followed) REFERENCES Users
	ON DELETE CASACDE)


CREATE TABLE Responses_to_post
(uid_post : CHAR(10),
 post_no : INTEGER,
 uid_like : CHAR(10),
 mood : INTEGER,
 time : DATE
 PRIMARY KEY(uid_post, post_no, uid_like),
 FOREIGN KEY(uid_post, post_no) REFERENCES Dep_post
	ON DELETE CASCADE
 FOREIGN KEY(uid_like) REFERENCES Users
	ON DELETE CASCADE)


CREATE TABLE Responses_to_comment
(uid_comment : CHAR(10),
 comment_no : INTEGER,
 uid_like : CHAR(10),
 mood : INTEGER,
 time : DATE
 PRIMARY KEY(uid_comment, comment_no, uid_like),
 FOREIGN KEY(uid_comment, comment_no) REFERENCES Dep_comments
	ON DELETE CASCADE
 FOREIGN KEY(uid_like) REFERENCES Users
	ON DELETE CASCADE)