from site import venv
import sqlite3
import os
import sqlalchemy
import sys
import subprocess
from flask import Blueprint, session
from flask import Flask, redirect, render_template, request,flash, url_for
from werkzeug.exceptions import abort
from flask_login import login_required,current_user
from . import dbModels,db
main = Blueprint('main',__name__)
@main.route('/')
def home():
    return render_template('home.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html',name = current_user.name,codes = current_user.codes,datasets = current_user.dataSets)

@main.route('/profile',methods = ['POST'])
def profile_post():
    if 'file' not in request.files:
        flash('No files chosen','error')
        return redirect(request.url)
    code = request.files['file']
    if code:
        codeName = code.filename
        print(code.content_type)
        if code.content_type.startswith('text/x-python'):
            code = code.read()
            add_user_code(code,codeName)
            flash('Code submitted succefully','success')
        elif code.content_type.startswith('text/plain'):
            data = code.read()
            add_user_dataSet(data,codeName)
            flash('Data Submitted Successfully','success')
        else:
            flash('wrong Format','error')
    else:
        flash('Nothing to submitt','error')
    return redirect(url_for('main.profile'))

@main.route('/test')
@login_required
def test():
    return render_template('profileCodeEditor.html',user = current_user,datasets = current_user.dataSets,codes = current_user.codes)
@main.route('/test',methods = ['POST'])
@login_required
def test_post():
    command = request.form.get('terminalInput')
    return redirect(url_for('main.profile'))

@login_required
def get_profile_codes():
    id = current_user.id
    codes = dbModels.User.query.filter_by(id = id).codes.all()
    return codes
@login_required
def add_user_code(code,codeName):
    id = current_user.id
    new_code  = dbModels.CodeData(user_id = current_user.id,code= code,codeName = codeName)
    db.session.add(new_code)
    db.session.commit()
@login_required
def add_user_dataSet(data,dataName):
    id = current_user.id
    new_data  = dbModels.DataSet(user_id = current_user.id,code= data,codeName = dataName)
    db.session.add(new_data)
    db.session.commit()
        