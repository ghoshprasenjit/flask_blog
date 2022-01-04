# import  simplejson
import json
from flask import Blueprint, render_template, Response, jsonify
from app.models import Post
from flask_cors import cross_origin

main = Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('home.html', posts = posts, title = "Home")


@main.route("/about")
def about():
    return render_template('about.html')


@main.route("/posts-list", methods = ['GET', 'POST'])
@cross_origin()
def post_list():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    # print(type(posts))
    # data = [r.__dict__ for r in posts]
    post_list  = []
    for post in posts:
        post_dict = {
            'id' : post.id,
            'title' : post.title,
            'content' : post.content,
            'user' : post.author.username,
            'user_id' : post.user_id
        }
        post_list.append(post_dict)

    # print(data)

    return jsonify({'posts': post_list}),200