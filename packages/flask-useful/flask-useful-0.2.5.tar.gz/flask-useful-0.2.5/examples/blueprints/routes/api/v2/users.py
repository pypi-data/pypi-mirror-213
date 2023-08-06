from flask import Blueprint


bp = Blueprint('users', __name__, url_prefix='/users')


@bp.get('/')
def index():
    return [
        {'id': 1, 'firstname': 'Linus', 'lastname': 'Torvalds'},
        {'id': 2, 'firstname': 'Richard', 'lastname': 'Stallman'},
    ]
