from flask import Blueprint
from flask import render_template,request,flash,redirect
from flask_login import login_required
from .models import Blog
from . import db
from flask_paginate import Pagination,get_page_parameter
views = Blueprint('views',__name__)


@views.route('/')

def home():
    data = Blog.query.all()[0:4]
    return render_template('index.html',data=data)


@views.route('/blog',methods=['GET','POST'])
@login_required
def blog():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        if len(title) < 3:
            flash('title must be more than 3 character',category='error')
        elif len(author) < 3:
            flash('Author name must be more than 3 character', category='error')
        elif len(content) < 3:
            flash('Content must be more than 3 character', category='error')
        else:
            post_data = Blog(title=title,
                        author=author,content=content)
            db.session.add(post_data)
            db.session.commit()
            flash('Post has been Created Successfully!')
            return redirect('/')


    return render_template('blog.html')


@views.route('/blog_detail/<int:id>',methods=['GET','POST'])
@login_required
def blog_detail(id):
    blog = Blog.query.get(id)
    return render_template('blog_detail.html',blog=blog)


@views.route('/blog_edit/<int:id>',methods=['GET','POST'])
@login_required
def blog_edit(id):
    post = db.session.query(Blog).filter(Blog.blog_id == id).first()
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        post.title = title
        post.author = author
        post.content = content
        db.session.commit()
        flash('Updated Successfully', 'success')
        return redirect('/')
    else:


        return render_template('blog_edit.html', post=post)




@views.route('/blog_delete/<int:id>',methods=['GET','POST'])
@login_required
def blog_delete(id):
    blog = Blog.query.get(id)
    db.session.delete(blog)
    db.session.commit()
    flash('Post Deleted Successfully','success')
    return redirect('/')
