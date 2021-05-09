# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from super_nft.extensions import csrf_protect

syncer_bp = Blueprint("syncer", __name__, url_prefix="/syncer", static_folder="../static")

@csrf_protect.exempt
@syncer_bp.route("/", methods=["GET", "POST"])
def index():
    data = {
        "result": "hello, world",
        "code": "200"
    }
    return jsonify(data), 200