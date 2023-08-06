from flask import Blueprint


bp = Blueprint('docs', __name__, url_prefix='/docs')


@bp.get('/')
def index():
    return '<h1>Documentation</h1>'
