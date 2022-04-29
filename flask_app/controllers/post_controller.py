from flask_app import app
from flask import request, redirect, session, render_template
from flask_app.models.post import Post
@app.route('/create_post/<int:user_id>', methods = ['POST'])
def create_post(user_id):
    if not Post.validate_post(request.form):
        return redirect('/dashboard')
    post_data = {
        "body" : request.form['body'],
        "user_id" : user_id
    }
    Post.create(post_data)
    return redirect('/dashboard')

@app.route('/like/<int:post_id>')
def like_post(post_id):
    data = {
        "user_id" : session['user_id'],
        "post_id" : post_id
    }
    Post.like_post(data)
    return redirect('/dashboard')

@app.route('/unlike/<int:post_id>')
def unlike_post(post_id):
    data = {
        "user_id" : session['user_id'],
        "post_id" : post_id
    }
    Post.unlike_post(data)
    return redirect('/dashboard')




@app.route('/edit/<int:post_id>')
def edit_post_page(post_id):
    data = {
        "post_id" : post_id
    }
    return render_template('editpost.html', post = Post.get_post_by_id(data))

@app.route('/edit_post/<int:post_id>', methods = ['POST'])
def edit_post(post_id):
    data = {
        "post_id" : post_id,
        "body" : request.form['body']
    }
    Post.edit(data)

@app.route('/delete/<int:post_id>')
def delete_post(post_id):
    data = {
        "post_id" : post_id
    }
    Post.delete(data)
    return redirect('/dashboard')

@app.route('/repost/<int:post_id>')
def repost(post_id):
    data = {
        "user_id" : session['user_id'],
        "post_id" : post_id
    }
    Post.repost(data)
    return redirect('/dashboard')