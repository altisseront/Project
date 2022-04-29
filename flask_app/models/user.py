from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import post
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.feed = []
        self.friends = []
    
    @classmethod
    def create(cls , data):
        query = "INSERT INTO users (first_name , last_name , username, email , password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s, NOW(), NOW())"
        return connectToMySQL('project_schema').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('project_schema').query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users
            

    @staticmethod
    def validate_user(user, data):
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First Name must be at least two characters", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last Name must be at least two characters", "register")
            is_valid = False
        if len(user['username']) < 1:
            flash("Must input username")
            is_valid = False
        for existingUser in data:
            if user['username'] == existingUser.username:
                flash("Username is taken.")
                is_valid = False
        for existingUser in data:
            if user['username'] == existingUser.email:
                flash("Email is taken.")
                is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", "register")
            is_valid = False
        if user['passwordc'] != user['password']:
            flash("Password confirmation must match password", "register")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("project_schema").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(user_id)s"
        result = connectToMySQL("project_schema").query_db(query,data)
        user = cls(result[0])
        return user

    @classmethod
    def follow_user(cls, data):
        query = "INSERT INTO follows (user_id, followed_id) VALUES (%(user_id)s, %(followed_id)s)"
        connectToMySQL("project_schema").query_db(query,data)

    @classmethod
    def unfollow_user(cls, data):
        query = "DELETE FROM follows WHERE followed_id = %(followed_id)s AND user_id = %(user_id)s"
        connectToMySQL("project_schema").query_db(query,data)

    @classmethod
    def get_all_but(cls, data):
        query = f"SELECT * FROM users WHERE id != {data}"
        results = connectToMySQL('project_schema').query_db(query)
        users = []
        for row in results:
            users.append(cls(row))
        return users

    @classmethod
    def follows(cls, data):
        query = "SELECT followed_id FROM follows WHERE user_id = %(user_id)s"
        results = connectToMySQL("project_schema").query_db(query,data)
        follows = []
        for row in results:
            follows.append(row['followed_id'])
        print(follows)
        return follows













    @classmethod
    def get_feed(cls, data):
        feed = []
        query3 = "SELECT followed_id FROM follows JOIN users ON users.id = user_id WHERE users.id = %(user_id)s"
        results3 = connectToMySQL("project_schema").query_db(query3,data)
        followed_ids = ""
        if len(results3) > 0:
            for row in results3:
                if len(followed_ids) < 1:
                    followed_ids += f"{row['followed_id']}"
                else:
                    followed_ids += f" OR {row['followed_id']}"
            followed_query = f" UNION (SELECT posts.id, posts.body, posts.created_at, posts.updated_at, posts.user_id, users.id, users.first_name, users.last_name, users.username, users.email, users.password, users.created_at, users.updated_at FROM posts JOIN reposts ON posts.id = reposts.post_id JOIN users ON reposts.user_id = users.id WHERE users.id = {followed_ids}) UNION (SELECT posts.id, posts.body, posts.created_at, posts.updated_at, posts.user_id, users.id, users.first_name, users.last_name, users.username, users.email, users.password, users.created_at, users.updated_at FROM posts JOIN users ON user_id = users.id WHERE users.id = {followed_ids})"
        else:
            followed_query = ""
        print(f"followed_ids")
        user_id = data['user_id']
        query1 = f"(SELECT posts.id, posts.body, posts.created_at AS posttime, posts.updated_at, posts.user_id, users.id, users.first_name, users.last_name, users.username, users.email, users.password, users.created_at, users.updated_at FROM posts JOIN users ON user_id = users.id WHERE users.id = {user_id}) UNION (SELECT posts.id, posts.body, posts.created_at, posts.updated_at, posts.user_id, users.id, users.first_name, users.last_name, users.username, users.email, users.password, users.created_at, users.updated_at FROM posts JOIN reposts ON reposts.post_id = posts.id JOIN users ON reposts.user_id = users.id WHERE users.id = {user_id}){followed_query} ORDER BY posttime DESC;"
        results1 = connectToMySQL("project_schema").query_db(query1,data)
        print(results1)
        for row in results1:
            likes = []
            comments = []
            query5 = f"SELECT * FROM likes WHERE post_id = {row['id']}"
            query6 = f"SELECT * FROM comments WHERE post_id = {row['id']}"
            results5 = connectToMySQL("project_schema").query_db(query5,data)
            results6 = connectToMySQL("project_schema").query_db(query6,data)
            if len(results5) > 0:
                for row5 in results5:
                    likes.append(row5)
            if len(results6) > 0:
                for row6 in results6:
                    comments.append(row6)
            user_data = {
            "id" :  row['user_id'],
            "first_name" :  row['first_name'],
            "last_name" :  row['last_name'],
            "username" :  row['username'],
            "email" :  row['email'],
            "password" :  row['password'],
            "created_at" :  row['created_at'],
            "updated_at" :  row['.updated_at'],
            }
            post_data = {
            "id" : row['id'],
            "body" : row['body'],
            "created_at" : row['posttime'],
            "updated_at" : row['updated_at'],
            "likes" : likes,
            "comments" : comments
            }
            thispost = post.Post(post_data)
            thispost.user = cls(user_data)
            feed.append(thispost)
        print(feed)
        return feed

    @classmethod
    def has_liked(cls, data):
        query = "SELECT post_id FROM likes WHERE user_id = %(user_id)s"
        results = connectToMySQL("project_schema").query_db(query,data)
        hasliked = []
        for row in results:
            hasliked.append(row['post_id'])
        return hasliked

    @classmethod
    def get_all_reposts(cls, data):
        query = "SELECT * FROM reposts"
        results = connectToMySQL('project_schema').query_db(query, data)







        # #Gets all of users reposts
        # query2 = "SELECT * FROM posts JOIN reposts ON reposts.post_id = posts.id JOIN users ON reposts.user_id = users.id WHERE users.id = %(user_id)s;"
        # results2 = connectToMySQL("project_schema").query_db(query2,data)
        # for row in results2:
        #     user_data = {
        #     "id" :  row['users.id'],
        #     "first_name" :  data['first_name'],
        #     "last_name" :  data['last_name'],
        #     "username" :  data['username'],
        #     "email" :  data['email'],
        #     "password" :  data['password'],
        #     "created_at" :  data['users.created_at'],
        #     "updated_at" :  data['users.updated_at'],
        #     }
        #     post_data = {
        #     "id" : row['posts.id'],
        #     "title" : row['title'],
        #     "body" : row['body'],
        #     "created_at" : row['posts.created_at'],
        #     "updated_at" : row['posts.updated_at'],
        #     "user" : user_data
        #     }
        #     feed.append(post.Post(post_data))             

        #Gets all of friends ids


        # for row in results3:
        #     query = f"SELECT * FROM posts JOIN users ON user_id = users.id WHERE user_id = neverhappening {followed_ids}";
        #     result = connectToMySQL("project_schema").query_db(query,data)
        #     for row1 in result:
        #         user_data = {
        #         "id" :  row1['users.id'],
        #         "first_name" :  data['first_name'],
        #         "last_name" :  data['last_name'],
        #         "username" :  data['username'],
        #         "email" :  data['email'],
        #         "password" :  data['password'],
        #         "created_at" :  data['users.created_at'],
        #         "updated_at" :  data['users.updated_at'],
        #         }
        #         post_data = {
        #         "id" : row1['posts.id'],
        #         "title" : row1['title'],
        #         "body" : row1['body'],
        #         "created_at" : row1['posts.created_at'],
        #         "updated_at" : row1['posts.updated_at'],
        #         "user" : user_data
        #         }
        #         feed.append(post.Post(post_data))             
        #         #Appends all posts of friends
        # for row1 in results3:
        #     query = f"SELECT * FROM posts JOIN reposts ON posts.id = resposts.post_id JOIN users ON reposts.user_id = users.id WHERE user_id = neverhappening {followed_ids}";
        #     result = connectToMySQL("project_schema").query_db(query,data)
        #     for row2 in result:
        #         user_data = {
        #         "id" :  row2['users.id'],
        #         "first_name" :  data['first_name'],
        #         "last_name" :  data['last_name'],
        #         "username" :  data['username'],
        #         "email" :  data['email'],
        #         "password" :  data['password'],
        #         "created_at" :  data['users.created_at'],
        #         "updated_at" :  data['users.updated_at'],
        #         }
        #         post_data = {
        #         "id" : row2['posts.id'],
        #         "title" : row2['title'],
        #         "body" : row2['body'],
        #         "created_at" : row2['posts.created_at'],
        #         "updated_at" : row2['posts.updated_at'],
        #         "user" : user_data
        #         }
        #         feed.append(post.Post(post_data))  
        #         #Appends all resposts of friends
        # return feed

