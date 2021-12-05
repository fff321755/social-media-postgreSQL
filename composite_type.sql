CREATE TYPE location_type AS(
longitude DECIMAL,
latitude DECIMAL,
country VARCHAR
);

CREATE TABLE location OF location_type(
PRIMARY KEY (longitude, latitude),
CHECK (longitude <= 180 AND longitude >= -180),
CHECK (latitude <= 90 AND latitude >= -90)
);

CREATE TABLE mood_in_location(
longitude DECIMAL,
latitude DECIMAL,
uid INTEGER,
post_no INTEGER,
PRIMARY KEY (uid,post_no),
FOREIGN KEY (uid,post_no) REFERENCES Personal_mood ON DELETE CASCADE ON UPDATE CASCADE,
FOREIGN KEY (longitude,latitude) REFERENCES location ON DELETE CASCADE ON UPDATE CASCADE
);

INSERT INTO location (longitude, latitude, country)
SELECT DISTINCT longitude, latitude, 'US'
FROM personal_mood;

INSERT INTO mood_in_location (longitude, latitude, uid, post_no)
SELECT l.longitude,l.latitude, pm.uid, pm.post_no
FROM personal_mood pm, location l 
WHERE pm.longitude=l.longitude AND pm.latitude = l.latitude;

ALTER TABLE Personal_mood
DROP COLUMN longitude,
DROP COLUMN latitude;