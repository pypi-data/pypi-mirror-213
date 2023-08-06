from flask import Blueprint


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.get('/')
def index():
    return [
        {'id': 1, 'name': 'Linus Torvalds'},
        {'id': 2, 'name': 'Richard Stallman'},
    ]
