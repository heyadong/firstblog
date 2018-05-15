from flask import Blueprint
blog = Blueprint('blog', __name__)
import app.blog.views