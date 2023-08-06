from flask import Blueprint, url_for
from flask_useful import register_blueprints


bp = Blueprint('api', __name__, url_prefix='/api')
register_blueprints(bp, '.', include_packages=True)


@bp.route('/')
def index():
    return {
        'v1': url_for('.v1.index', _external=True),
        'v2': url_for('.v2.index', _external=True),
    }
