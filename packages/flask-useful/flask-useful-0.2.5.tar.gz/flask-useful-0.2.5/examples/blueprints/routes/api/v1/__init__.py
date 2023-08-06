from flask import Blueprint, url_for
from flask_useful import register_blueprints


bp = Blueprint('v1', __name__, url_prefix='/v1')
register_blueprints(bp, '.')


@bp.get('/')
def index():
    return {
        'users': url_for('.users.index', _external=True),
    }
