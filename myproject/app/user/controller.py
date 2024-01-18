import datetime

from flask import session, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user

from app import data_base
from app.common.common import render, upload_file
from app.domain.User import User
from . import auth_bp
from .forms import LoginForm, RegisterForm
