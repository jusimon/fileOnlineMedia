#!flask/bin/python
import os
import json
import boto3
import aws 
import ast 

from flask import Flask
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import abort
from flask import url_for
from flask import jsonify
from flask import Response
from flask_sslify import SSLify
from werkzeug.utils import secure_filename
from fileHandler import filehandler
from clientDB import client
from attrDict import AttrDict
from gAuth import Auth 
 
application = Flask(__name__)
application.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
application.config['SESSION_TYPE'] = "fileonline.ggn4zi.0001.usw1.cache.amazonaws.com" 
application.config['SECRET_KEY'] = aws.getAwsAccess_key()

@application.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        files = filehandler()
        clnt = client()
        resp = files.list_files(session['username'])
        user = clnt.get_client(session['username'])
        return render_template('layout.html', files=resp, user=user)


@application.route('/confirm')
def confirm():
    desc = request.args['desc']
    action_url = (request.args['action_url'])

    return render_template('confirm.html', desc=desc, action_url=action_url)

@application.route('/error')
def error():
    desc = request.args['desc']
    action_url = (request.args['action_url'])

    return render_template('error.html', desc=desc, action_url=action_url)


@application.route('/login', methods=['POST'])
def login():
    c = client()
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        code, message = c.validate_client(username, password)
        if code != 0 :
            return redirect(url_for('error', desc=message,
                                    action_url=str.rstrip(request.url,'login')))
        else:
            session['logged_in'] = True
            session['username'] = username
            return home()

@application.route('/download', methods=['GET'])
def download():
    my_file = filehandler()
    if request.method == 'GET':
        base_url, infos = str(request.url).split("/download?")
        username  = ast.literal_eval(infos)['username']
        filename  = ast.literal_eval(infos)['filename']
        attach = "attachment;filename="+filename
        return Response(my_file.get_object(username, filename),
                        mimetype='text/plain',
                        headers={"Content-Disposition": attach})
    return home()


@application.route('/edit', methods=['GET'])
def edit():
    my_file = filehandler() 
    base_url, infos = str(request.url).split("/edit?")
    username  = ast.literal_eval(infos)['username']
    filename  = ast.literal_eval(infos)['filename']
    filedesc  = ast.literal_eval(infos)['filedesc']
    session['editname']  = username 
    session['editfile']  = filename
    session['editdesc']  = filedesc
    return render_template('edit.html', username=username, filename=filename, filedesc=filedesc)


@application.route('/save', methods=['POST'])
def save():
    my_file = filehandler() 
    new_file = request.form['filename']
    new_desc = request.form['filedesc']

    if(new_file == ''):
        new_file = session['editfile']

    if(new_desc == ''):
        new_desc = session['editdesc']

    my_file.update_object(session['editname'], session['editfile'], new_file, new_desc)
    return home()



@application.route('/delete', methods=['POST'])
def delete():
    my_file = filehandler()
    if request.method == 'POST':
        try:
            del_file = request.form['filename']
            my_file.del_file(session['username'], del_file)
        except:
            return home()
    return home()

@application.route('/upload', methods=['POST'])
def upload():
    my_file = filehandler()
    if request.method == 'POST':
        try:
            body = request.files['upload_file']
        except Exception as err:
            return redirect(url_for('error', desc=str(err),
                                            action_url=str.rstrip(request.url,'upload')))
        filename = secure_filename(body.filename)
        filedesc = request.form['filedesc']
        my_file.add_file(session['username'], filename, filedesc, body)
    return home()

 
@application.route("/logout")
def logout():
    session['logged_in'] = False
    return home()


@application.route("/new_user")
def new_user():
     return render_template('new_login.html')

@application.route("/signup", methods=['POST'])
def signup():
    c = client()
    error = None
    event = AttrDict()
    if request.method == 'POST':
        event['username']  = request.form['username']
        event['password']  = request.form['password']
        event['firstname'] = request.form['firstname']
        event['lastname']  = request.form['lastname']
        event['email']     = request.form['email']
        code, message = c.set_client(event)
        if code != 0:
            return redirect(url_for('error', desc=message,
                                    action_url=str.rstrip(request.url,'signup')))
        else:
            return redirect(url_for('error', desc="Successfully signed up",
                                    action_url=str.rstrip(request.url,'signup')))
        return home()            


@application.route("/admin")
def admin():
     clnt = client()
     if 0 == clnt.is_admin_user(session['username']):
         return redirect(url_for('error',
             desc=session['username']+" is not Admin User",
             action_url=str.rstrip(request.url,'admin')))
     admin = clnt.get_client(session['username'])
     users = clnt.get_clients()
     return render_template('admin.html', admin=admin, users=users)

@application.route('/user_delete', methods=['POST'])
def user_delete():
    my_clnt = client()
    files = filehandler()
    code  = 0
    message = '' 
    if request.method == 'POST':
        try:
            del_user = request.form['username']
            if(del_user == session['username']):
                return redirect(url_for('error', desc="Can't delete same Admin User",
                    action_url=str.rstrip(request.url,'user_delete')))
            
            files.del_userfiles(del_user)
            code, message = my_clnt.del_client(del_user)
        except:
            return redirect(url_for('error', desc=message,
                action_url=str.rstrip(request.url,'user_delete')))
            return home()
    return admin()




@application.route('/glogin', methods=['POST'])
def glogin():
    if session.get('logged_in'):
        return home() 
    google = Auth.get_google_auth(str.rstrip(request.url,'glogin'))
    auth_url, state = google.authorization_url(
        Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return render_template('google.html', auth_url=auth_url)


@application.route('/gAuthCallback')
def callback():
    if session.get('logged_in'):
        return redirect(url_for('index'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        google = Auth.get_google_auth(str.rstrip(request.url,'gAuthCallback'),
                state=session['oauth_state'])
        try:
            token = google.fetch_token(Auth.TOKEN_URI,
                client_secret=aws.getGoogleAccess(),
                authorization_response=request.url)
        except request.exceptions:
            return 'HTTPError occurred.'
        google = Auth.get_google_auth(str.rstrip(request.url,'gAuthCallback'),
                token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            c = client()
            event = AttrDict()
            user_data = resp.json()
            event['username'] = user_data['email'] 
            event['password'] = ""
            code, message = c.validate_client(event['username'], event['password'])
            if code == 254: 
                event['firstname'] = user_data['given_name']
                event['lastname'] = user_data['family_name']
                event['email']    = user_data['email']
                code, message = c.set_client(event) 
            if code != 0:
                return redirect(url_for('error', desc=message,
                action_url=str.rstrip(request.url,'gAuthCallback')))
            else: 
                session['logged_in'] = True
                session['username'] = user_data['email'] 
                return home()            

##@application.before_request
##def before_request():
##    if request.url.startswith('http://'):
##        url = request.url.replace('http://', 'https://', 1)
##        code = 301
##        return redirect(url, code=code)

if __name__ == "__main__":
##    ssl_dir: str = os.path.dirname(__file__)+'/ssl'
##    key_path: str = os.path.join(ssl_dir, 'server.key')
##    crt_path: str = os.path.join(ssl_dir, 'server.crt')
##    ssl_context: tuple = (crt_path, key_path)
##    sslify = SSLify(application, permanent=True) 
##    application.debug = True 
##    application.run(ssl_context=ssl_context)
    application.debug = True 
    application.run()
