-- trigger 1
ALTER TABLE user_in_group
DROP CONSTRAINT user_in_group_group_id_fkey,
ADD CONSTRAINT user_in_group_group_id_fkey
   FOREIGN KEY (group_id) REFERENCES Groups ON DELETE CASCADE ON UPDATE CASCADE
   DEFERRABLE INITIALLY DEFERRED;

CREATE FUNCTION empty_group() RETURNS TRIGGER AS $empty_group$
    BEGIN
        IF (NEW.group_id NOT IN (SELECT group_id FROM User_in_group)) THEN
            DELETE FROM Groups G 
            WHERE G.group_id = NEW.group_id;
        END IF;
        RETURN NULL;
    END;
$empty_group$ LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER empty_group
AFTER INSERT ON Groups
DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION empty_group();


-- trigger 2
CREATE FUNCTION delete_empty_group() RETURNS trigger AS $body$

    BEGIN
        IF (SELECT COUNT(*) FROM User_in_group ug WHERE group_id = old.group_id)= 0 THEN
            -- INSERT INTO User_in_group VALUES (OLD.*);
            DELETE FROM Groups g WHERE g.group_id = OLD.group_id;
        END IF;
        RETURN NULL;
    END;

$body$ LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER delete_empty_group
    AFTER DELETE OR UPDATE ON User_in_group
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION delete_empty_group();
