from flask_app.config.mysqlconnection import connectToMySQL
class Post:
    def __init__( self , data ):
        self.id = data['id']
        self.body = data['body']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = {}
        self.comments = data['comments']
        self.likes = data['likes']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO posts (body, created_at, updated_at, user_id) VALUES (%(body)s, NOW(),NOW(),%(user_id)s)"
        connectToMySQL('project_schema').query_db(query, data)

    @classmethod
    def edit(cls, data):
        query = "UPDATE posts body = %(body)s, updated_at = NOW() WHERE id = %(id)s"

    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['body']) < 1:
            flash("Type something!", "post")
            is_valid = False
        return is_valid

    @classmethod
    def like_post(cls, data):
        query = "INSERT INTO likes (user_id, post_id) VALUES (%(user_id)s, %(post_id)s)"
        connectToMySQL('project_schema').query_db(query, data)

    @classmethod
    def unlike_post(cls, data):
        query = "DELETE FROM likes WHERE user_id = %(user_id)s AND post_id = %(post_id)s"
        connectToMySQL('project_schema').query_db(query, data)

    
    @classmethod
    def get_post_by_id(cls, data):
        query = "SELECT * FROM posts WHERE id = %(post_id)s"
        return connectToMySQL('project_schema').query_db(query, data)

    @classmethod
    def edit(cls, data):
        query = "UPDATE posts SET body = %(body)s, updated_at=NOW() WHERE id = %(post_id)s"
        connectToMySQL('project_schema').query_db(query, data)
    
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM posts WHERE id = %(post_id)s"
        connectToMySQL('project_schema').query_db(query, data)

    @classmethod
    def repost(cls, data):
        query = "INSERT INTO reposts (user_id, post_id) VALUES (%(user_id)s, %(post_id)s)"
        connectToMySQL('project_schema').query_db(query, data)

