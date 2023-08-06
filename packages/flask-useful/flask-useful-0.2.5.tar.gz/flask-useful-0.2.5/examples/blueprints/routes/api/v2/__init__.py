from flask import Blueprint, url_for
from flask_useful import register_blueprints


bp = Blueprint('v2', __name__, url_prefix='/v2')
register_blueprints(bp, '.')


@bp.get('/')
def index():
    return {
        'users': url_for('.users.index', _external=True),
    }
