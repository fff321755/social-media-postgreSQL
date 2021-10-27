-- Find all the personal mood post by users that followed by 'Smith Jones'
SELECT *
FROM personal_mood m
WHERE m.uid in (SELECT U2.uid
                FROM follow F, users U1, users U2
                WHERE F.uid_following = U1.uid AND U1.name = 'Smith Jones' AND F.uid_followed = U2.uid);



-- Find all the id and name of users that left comments to the post posted by 'Smith Jones'
SELECT DISTINCT U.uid, U.name
FROM Users U, Dep_comments C
WHERE U.uid = C.uid_comment
AND C.uid_post IN	(SELECT U2.uid
                    FROM Dep_posts P, Users U2
                    WHERE U2.uid = P.uid AND U2.name = 'Smith Jones');


-- Find all the users who have responded to post to 'Smith Jones' >= 10 times.
SELECT U0.name, U0.uid
FROM users U0
WHERE U0.uid In (SELECT R.uid_like
                    FROM Responses_to_post R, Users U1
                    WHERE R.uid_post = U1.uid AND U1.name = 'Smith Jones'
                    GROUP BY R.uid_like
                    HAVING Count(*) >= 10);
