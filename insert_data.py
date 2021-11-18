# %%
from math import radians
import pandas as pd
import random
from datetime import datetime, timezone


def df2SQL(df, table_name, mode='a'):
    with open("data.sql", mode) as f:
        df_values = df.values
        M = len(df_values)
        N = len(df_values[0])
        f.write("-- {}\n".format(table_name))
        # f.write("DELETE FROM {};\n".format(table_name))
        f.write("INSERT INTO {} VALUES\n".format(table_name))
        exstr = ["true", "false", "NULL"]
        exstr = set(exstr)

        for i in range(M):
            f.write('(')
            # f.write(str(df_values[i])[1:-1])
            for j in range(N):
                if(type(df_values[i][j])==type('str') and df_values[i][j] not in exstr):
                    f.write("\'")
                f.write(str(df_values[i][j]))
                if(type(df_values[i][j])==type('str') and df_values[i][j] not in exstr):
                    f.write("\'")
                if j!=N-1:
                    f.write(',')
            if i!=M-1:
                f.write('),\n')
            else:
                f.write(');\n\n')

    return


def Users():
    random.seed(0)
    df = pd.DataFrame(columns=['uid', 'name', 'present_mood', 'email', 'password', 'is_active'])
    
    name = ["Kelly", "Alex", "Cody", "Kim", "Halsey", "James", "Steve", "Kevin", "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
    name = [ n1+' '+n2 for n1 in name for n2 in name if n1!=n2]
    random.shuffle(name)
    tf = ['a', 'b', 'c', 'd', 'e']
    uni_number = list(range(1000,10000));
    random.shuffle(uni_number)

    for i in range(0,25):
        uni = name[i].split()[0][0].lower() + name[i].split()[1][0].lower() + str(uni_number[i])
        df.loc[len(df.index)] = [i, name[i], random.randint(1, 5), uni+"@columbia.edu", '1234' , random.choice(['true', 'false'])]


    return df

def Groups():
    random.seed(0)
    df = pd.DataFrame(columns=['group_id', 'type', 'group_name'])
    name1 = ["Happy", "Beautiful", "Fury", "Sound"]
    name2 = ["Land", "Garden", "Association", "Brothers"]
    name = [ n1+" "+n2 for n1 in name1 for n2 in name2]
    random.shuffle(name)
    
    for i in range(0,15):
        df.loc[len(df.index)] = [i, random.randint(1, 5), name[i]]

    return df


def Dep_post(df_user):
    random.seed(0)
    df = pd.DataFrame(columns=['post_no', 'time', 'uid'])
    uids = df_user['uid']
    random.shuffle(uids)
    for uid in uids:
        for j in range(0, random.randint(25,100)):
            df.loc[len(df.index)] = [j+1, str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')), uid]

    return df


def User_in_group(df_user, df_groups):
    random.seed(0)
    df = pd.DataFrame(columns=['uid', 'group_id', 'level'])
    uids = df_user['uid']
    groupids = df_groups['group_id']
    random.shuffle(uids)
    
    for u in uids:
        random.shuffle(groupids)
        for j in range(random.randint(0,5)):
            df.loc[len(df.index)] = [u, groupids[j], random.randint(1,3)]

    return df


def Group_posts_Personal_mood(df_dep_post, df_user_in_group):
    random.seed(0)
    df_g = pd.DataFrame(columns=['uid', 'group_id', 'post_no', 'text', 'image_URL'])
    df_p = pd.DataFrame(columns=['longitude', 'latitude', 'uid', 'post_no', 'mood'])
    posts = df_dep_post.values
    for p in posts:
        uid = p[2]
        post_no = p[0]
        user_group = df_user_in_group[df_user_in_group['uid']==uid].values
        if(len(user_group) == 0 or random.randint(1,10) > 5):
            df_p.loc[len(df_p.index)] = [40.7128+random.randint(1,100)/1000, 74.0061+random.randint(1,100)/1000,uid, post_no, random.randint(1,4)]
        else:
            random.shuffle(user_group)
            group_id = user_group[0][1]
            df_g.loc[len(df_g.index)] = [uid, group_id, post_no, "sample text", "https://i.imgur.com/HeGEEbu.jpeg"]

    return df_g, df_p


def Dep_comments(df_user, df_dep_post):
    random.seed(0)
    df = pd.DataFrame(columns=['comment_no', 'uid_comment', 'uid_post', 'post_no', 'text', 'time'])
    uid_comments = df_user['uid'].values
    random.shuffle(uid_comments)
    posts = df_dep_post.values

    for uid_comment in uid_comments:
        random.shuffle(posts)
        for j in range(random.randint(0,25)):
            if random.randint(1,100) > 40:
                df.loc[len(df.index)] = [j+1, uid_comment, posts[j][2], posts[j][0], 'sample comment', str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))]
            else:
                df.loc[len(df.index)] = [j+1, uid_comment, 'NULL', 'NULL', 'sample comment', str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))]
    
    return df


def Follow(df_user):
    random.seed(0)
    df = pd.DataFrame(columns=['uid_following', 'uid_followed'])
    uid_followings = df_user['uid'].values
    random.shuffle(uid_followings)
    uid_followeds = df_user['uid'].values
    
    for i in range(len(uid_followings)):
        random.shuffle(uid_followeds)
        for j in range(random.randint(0,25)):
            if uid_followings[i] != uid_followeds[j]:
                df.loc[len(df.index)] = [uid_followings[i], uid_followeds[j]]

    return df.drop_duplicates()


def comments_to_comments(df_Dep_comments):
    random.seed(0)
    df = pd.DataFrame(columns=['uid1', 'uid2', 'comments_no1', 'comments_no1'])
    comments_to_comments = df_Dep_comments[df_Dep_comments['uid_post'] == 'NULL'].values
    all_comments = df_Dep_comments.values

    for c1 in comments_to_comments:
        uid1 = c1[1]
        comments_no1 = c1[0]

        while(True):
            c2 = random.choice(all_comments)
            uid2 = c2[1]
            comments_no2 = c2[0]
            if uid1!=uid2 or comments_no1!=comments_no2:
                break
        df.loc[len(df.index)] = [uid1, uid2, comments_no1, comments_no2]

    return df


def Responses_to_post(df_user, df_dep_post):
    random.seed(0)
    df = pd.DataFrame(columns=['uid_post', 'post_no', 'uid_like', 'mood', 'time'])
    uid_likes = df_user['uid'].values
    posts = df_dep_post.values
    
    for p in posts:
        random.shuffle(uid_likes)
        for i in range(random.randint(0,10)):
            df.loc[len(df.index)] = [p[2], p[0], uid_likes[i], random.randint(1,4), str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))]
        
    return df


def Responses_to_comment(df_user, df_Dep_comments):
    random.seed(0)
    df = pd.DataFrame(columns=['uid_comment', 'comment_no', 'uid_like', 'mood', 'time'])
    uid_likes = df_user['uid'].values
    comments = df_Dep_comments.values
    
    for c in comments:
        random.shuffle(uid_likes)
        for i in range(random.randint(0,10)):
            df.loc[len(df.index)] = [c[1], c[0], uid_likes[i], random.randint(1,4), str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))]
        
    return df


#%%

df_user = Users()
df_groups = Groups()
df_dep_post = Dep_post(df_user.copy())
df_user_in_group = User_in_group(df_user.copy(), df_groups.copy())
df_Group_posts, df_Personal_mood = Group_posts_Personal_mood(df_dep_post.copy(), df_user_in_group.copy())
df_Dep_comments = Dep_comments(df_user.copy(), df_dep_post.copy())
df_Follow = Follow(df_user.copy())
df_comments_to_comments = comments_to_comments(df_Dep_comments.copy())
df_Responses_to_post = Responses_to_post(df_user.copy(), df_dep_post.copy())
df_Responses_to_comment = Responses_to_comment(df_user.copy(), df_Dep_comments.copy())



# %%
df2SQL(df_user,'Users', 'w')
df2SQL(df_groups,'Groups')
df2SQL(df_user_in_group,'User_in_group')
df2SQL(df_dep_post,'Dep_posts', 'a')
df2SQL(df_Group_posts,'Group_posts')
df2SQL(df_Personal_mood,'Personal_mood')
df2SQL(df_Dep_comments,'Dep_comments')
df2SQL(df_Follow,'Follow')
df2SQL(df_comments_to_comments,'comments_to_comments')
df2SQL(df_Responses_to_post,'Responses_to_post')
df2SQL(df_Responses_to_comment,'Responses_to_comment')





# %%
df_dep_post
# %%
