# Database Project 1 Part 3
### Kyung Chae Park kp2900, Kuan-Hsuan Wu kw2963  
### November 2021  
  

## PostgreSQL  account:
    kw2963

## URL of web application:
    http://104.196.113.217:8111/

## Description
- Implemented:
  1. Post personal mood
  2. Post group post
  3. Comment under personal mood that post by someone you followed
  4. Comment under group post that in your group
  5. Delete Post, base on our design the post’s comment has subcomment, it could not delete unless we delete the subcomments before delete that post
  6. Delete Comment, base on our design the comment has subcomment, it could not delete unless we delete the subcomments before delete that comment
  7. Create Groups, don’t input some 
  8. Join Groups
  9. Leave Groups, and Automatically delete the group that have no users to guaranteed participation constraint, and will delete all the dangling Dep_post which its group_post are delete by cascade
  10. Response to personal mood, change response to group mood
  11. Response to group posts, change response to group posts
  12. Response to comments, change response to comments
  13. Follow other users
  14. Unfollow other users
  15. See the random Anonymous personal_mood that you didn’t follows, where you can see their profile and follow he/she
  16. See the random group post that you didn’t join
  17. See all the post you followed
  18. See the random Anonymous personal_mood
  19. See the random Anonymous Group Posts
  20. Show the recent personal mood of users you are following

- Not implemented:
  1. Order By Location: Since we use http not https for our web-application, we have no access to the location information of the user. So the personal_mood posts are ordered by time, not distance from the user. And the autofill location when posting won’t work for most browsers for the same issue.

## Two interesting pages.
1. post.html and comments.html
These two pages are similar, they both show the comment under the post or the comments. The most interesting part is that you can click the detail&comment button and redirect to the comments page and that shows all the comments under the comment. Once you are in the comments page, you can create a comment to that comment. This will create a Dep_comment depending on the Dep_post, and if we comment to a comment, it will also create a relationship in comment_to_cooment. Then you can click the detail&comment to its sub-comments. I think they are interesting because users can continue to comment to the sub-comments and comment to sub-sub-comments no matter how deep it goes.


2. group_page.html(include group_positng_page..html)
In a group page, users can post a new group_post or quit the group. Creating a new group_post requires insertion into entity sets that have most connections between other entity sets, creating entries in Dep_posts and Group_posts. These two relate groups, users and comments and created group_post starts to show in post_page.html, thus enabling other users who are not joining the group to see the post and join the group if they like. On the other hand, quitting a group seems simple, but when the user is the last person in the group and quits the group, the group should also be deleted thus it checks if there are no users in the group. In the case that a group with many group posts is deleted, those group_posts are also deleted(related entries in Dep_posts and Group_posts), so many other entries in the database referencing those entries are also deleted. 
