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
(uid INTEGER,
 group_id INTEGER NOT NULL,
 post_no INTEGER CHECK (post_no > 0),
 text ARCHAR(200),
 image_URL VARCHAR(100) CHECK(image_URL LIKE 'https://_%'),
 PRIMARY KEY(uid, post_no),
 FOREIGN KEY(uid, post_no) REFERENCES Dep_posts ON DELETE CASCADE,
 FOREIGN KEY(group_id) REFERENCES Groups ON DELETE CASCADE);

--longitude and latitude represents location of the user when posting 

CREATE TABLE Personal_mood
(longitude DECIMAL CHECK (longitude <= 180 AND longitude >= -180),
 latitude DECIMAL CHECK (latitude <= 90 AND latitude >= -90), 
 uid INTEGER,
 post_no INTEGER CHECK (post_no > 0),
 mood INTEGER CHECK (mood > 0 AND mood < 7), -- we have 6 catagory of mood
 PRIMARY KEY(uid, post_no),
 FOREIGN KEY(uid, post_no) REFERENCES Dep_posts ON DELETE CASCADE);

-- total participation to the Dep_post
-- non-overlapping condition between Personal_mood and Group_post

CREATE TABLE Dep_comments         --weak entity relationship
(comment_no SERIAL CHECK (comment_no > 0),
 uid_comment INTEGER,
 uid_post INTEGER,
 post_no INTEGER CHECK (post_no > 0),
 text VARCHAR(200),
 time timestamp,
 CHECK ((uid_post = NULL AND post_no = NULL) OR (uid_post <> NULL AND post_no <> NULL)),    -- uid_post and post_no should be NULL together when the comment is comment to another comment
 PRIMARY KEY(uid_comment, comment_no),
 FOREIGN KEY(uid_comment) REFERENCES Users ON DELETE CASCADE,
 FOREIGN KEY(uid_post, post_no) REFERENCES Dep_posts ON DELETE CASCADE);


--  participation of Group to the User (If no users stays in a group, that group will be deleted automatically)

CREATE TABLE User_in_group
(uid INTEGER,
 group_id INTEGER,
 level INTEGER CHECK (level < 6 AND level > 0),     -- we have 5 level in total
 PRIMARY KEY(uid, group_id),
 FOREIGN KEY(uid) REFERENCES Users ON DELETE CASCADE,
 FOREIGN KEY(group_id) REFERENCES Groups ON DELETE CASCADE);


CREATE TABLE Follow
(uid_following INTEGER,
 uid_followed INTEGER,
 PRIMARY KEY (uid_following, uid_followed),
 FOREIGN KEY(uid_following) REFERENCES Users ON DELETE CASCADE,
 FOREIGN KEY(uid_followed) REFERENCES Users ON DELETE CASCADE);

CREATE TABLE comments_to_comments
(uid1 INTEGER,
 uid2 INTEGER,
 comments_no1 INTEGER CHECK (comments_no1 > 0),
 comments_no2 INTEGER CHECK (comments_no2 > 0),
 PRIMARY KEY(uid1, comments_no1, uid2, comments_no2),
 FOREIGN KEY(uid1, comments_no1) REFERENCES Dep_comments,
 FOREIGN KEY(uid2, comments_no2) REFERENCES Dep_comments ON DELETE CASCADE);

CREATE TABLE Responses_to_post
(uid_post INTEGER,
 post_no INTEGER CHECK (post_no > 0),
 uid_like INTEGER,
 mood INTEGER CHECK (mood > 0 AND mood < 7),
 time timestamp,
 PRIMARY KEY(uid_post, post_no, uid_like),
 FOREIGN KEY(uid_post, post_no) REFERENCES Dep_posts ON DELETE CASCADE,
 FOREIGN KEY(uid_like) REFERENCES Users ON DELETE CASCADE);


CREATE TABLE Responses_to_comment
(uid_comment INTEGER,
 comment_no INTEGER CHECK (comment_no > 0),
 uid_like INTEGER,
 mood INTEGER CHECK (mood > 0 AND mood < 7),
 time timestamp,
 PRIMARY KEY(uid_comment, comment_no, uid_like),
 FOREIGN KEY(uid_comment, comment_no) REFERENCES Dep_comments ON DELETE CASCADE,
 FOREIGN KEY(uid_like) REFERENCES Users ON DELETE CASCADE);

 ------------------------------Triggers---------------------------

-- CREATE CONSTRAINT TRIGGER TotalPartGrpUsr1
-- AFTER INSERT ON Groups
-- DEFERRABLE INITIALLY DEFERRED
-- REFERENCING New ROW AS NewGroup
-- FOR EACH ROW
-- WHEN (NewGroup.group_id NOT IN(SELECT group_id
--                               FROM User_in_group))
-- DELETE FROM Groups G
-- WHERE G.group_id = NewGroup.group_id

-- -----PROPER?----
-- CREATE CONSTRAINT TRIGGER TotalPartGrpUsr2
-- AFTER UPDATE OF group_id ON Groups
-- DEFERRABLE INITIALLY DEFERRED
-- REFERENCING Old ROW AS OldGroup
--             New ROW AS NewGroup
-- FOR EACH ROW
-- WHEN (NewGroup.group_id NOT IN(SELECT group_id
--                               FROM User_in_group))
-- DELETE FROM Groups G
-- WHERE G.group_id = NewGroup.group_id


--------------------------------------------------------
CREATE FUNCTION empty_group() RETURNS TRIGGER AS $empty_group$
    BEGIN
        IF (TG_OP = 'INSERT') THEN
            INSERT INTO Groups VALUES (NEW.group_id, NEW.type, NEW.group_name)

            NEW.last_updated = now();
            IF (NEW.group_id NOT IN (SELECT group_id FROM User_int_group)) THEN
                DELETE FROM Groups G 
                WHERE G.group_id = NEW.group_id
            END IF;
            RETURN NEW;
                
        ELSIF (TG_OP = 'UPDATE') THEN
            UPDATE Groups SET group_id = NEW.group_id, type= NEW.type, group_name = NEW.group_name
            WHERE group_id = OLD.group_id

            IF (NEW.group_id NOT IN (SELECT group_id FROM User_in_group))
                DELETE FROM Groups G 
                WHERE G.group_id = NEW.group_id
            END IF;
            RETURN NEW;

        END IF;
    END;
$empty_group$ LANGUAGE plpgsql;

CREATE TRIGGER empty_group
AFTER INSERT OR UPDATE ON Groups
    FOR EACH ROW EXECUTE empty_group();

SET CONSTRAINT empty_group DEFERRED

D
--------------------------------------------------------




-- CREATE CONSTRAINT TRIGGER TotalPartGrpUsr3
-- AFTER DELETE ON User_in_group
-- DEFERRABLE INITIALLY DEFERRED
-- REFERENCING Old ROW AS Old
-- FOR EACH ROW
-- WHEN (1>(SELECT COUNT(*)
--          FROM User_in_group
--          WHERE group_id = Old.group_id))
-- DELETE FROM Groups G 
-- WHERE G.group_id = Old.group_id

-- CREATE CONSTRAINT TRIGGER TotalPartGrpUsr4
-- AFTER UPDATE OF group_id ON User_in_group
-- REFERENCING Old ROW AS Old
--             New ROW AS New
-- FOR EACH ROW
-- WHEN (Old.group_id NOT IN (SELECT group_id
--                            FROM User_in_group))
-- DELETE FROM Groups G
-- WEHRE G.group_id = Old.group_id

--------------------------------------------------------
CREATE FUNCTION empty_group2() RETURNS TRIGGER AS $empty_group2$
    BEGIN
        IF (TG_OP = 'DELETE') THEN
            DELETE FROM User_in_group WHERE group_id = OLD.group_id AND uid =OLD.uid
            IF NOT FOUND THEN RETURN NULL; END IF;
            IF (1>(SELECT COUNT(*) FROM User_in_group WHERE group_id = OLD.group_id))
                DELETE FROM Groups G 
                WHERE G.group_id = OLD.group_id
            END IF;
        ELSIF (TG_OP ='UPDATE') THEN
            UPDATE User_in_group SET group_id=NEW.group_id, uid=NEW.uid, level = NEW.level 
            WHERE group_id = OLD.group_id AND uid=OLD.uid
            IF NOT FOUND THEN RETURN NULL; END IF;

            IF (OLD.group_id NOT IN (SELECT gropu_id FROM User_in_group))
                DELETE FROM Groups G 
                WHERE G.gropu_id = OLD.group_id
            END IF;
        
        END IF;
    END;

$empty_group2$ LANGUAGE plpgsql;

CREATE TRIGGER empty_group2
AFTER DELETE OR UPDATE ON User_in_group
    FOR EACH ROW EXECUTE FUNCTION empty_group2();

SET CONSTRAINT empty_group2 DEFERRED 
--------------------------------------------------------


CREATE TYPE location AS 
(longitude DECIMAL CHECK (longitude <= 180 AND longitude >=-180)
 latitude DECIMAL CHECK (latitude <= 90 AND latitude >= -90))


---- QUERIES ----

SELECT U.name, U.present_mood
FROM Users U Group_posts GP 
WHERE to_tsvector(GP.text) @@ to_tsquery(really<->good) AND U.uid=GP.uid;

DELETE FROM Groups
WHERE group_id IN (SELECT group_id
                   FROM User_in_group
                   GROUP BY group_id
                   HAVING COUNT(*)=1);


INSERT Groups VALUES ('00000099', 3, 'new group');


INSERT Groups VALUES ('00000099', 3, 'new group')
INSERT User_in_group VALUES ('00000001', '00000099', 5);




