#!/usr/bin/python3.7

# Copyright 2017 Earth Sciences Department, BSC-CNS

# This file is part of Autosubmit.

# Autosubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Autosubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Autosubmit.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import time
from datetime import datetime, timedelta
import requests
import logging
from flask_cors import CORS, cross_origin
from flask import Flask, request, session, redirect, url_for
from bscearth.utils.log import Log
from .database.db_common import get_current_running_exp, update_experiment_description_owner
from .experiment import common_requests as CommonRequests
from .experiment import utils as Utiles
from .performance.performance_metrics import PerformanceMetrics
from .database.db_common import search_experiment_by_id
from .config.basicConfig import BasicConfig
from .builders.joblist_helper_builder import JobListHelperBuilder, JobListHelperDirector
from multiprocessing import Manager, Lock
import jwt
import sys

JWT_SECRET = os.environ.get("SECRET_KEY")
JWT_ALGORITHM = "HS256"
JWT_EXP_DELTA_SECONDS = 84000*5  # 5 days

sys.path.insert(0, os.path.abspath('.'))

app = Flask(__name__)

D = Manager().dict()

# CAS Stuff
CAS_LOGIN_URL = os.environ.get("CAS_LOGIN_URL") # 'https://cas.bsc.es/cas/login'
CAS_VERIFY_URL = os.environ.get("CAS_VERIFY_URL") # 'https://cas.bsc.es/cas/serviceValidate'

CORS(app)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

app.logger.info("PYTHON VERSION: " + sys.version)

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

lock = Lock()

CommonRequests.enforceLocal(app.logger)

# CAS Login
@app.route('/login')
def login():
    BasicConfig.read()
    ticket = request.args.get('ticket')
    environment = request.args.get('env')
    referrer = request.referrer
    is_allowed = False
    for allowed_client in BasicConfig.ALLOWED_CLIENTS:
        if referrer.find(allowed_client) >= 0:
            referrer = allowed_client
            is_allowed = True
    if is_allowed == False:
        return {'authenticated': False, 'user': None, 'token': None, 'message': "Your client is not authorized for this operation. The API admin needs to add your URL to the list of allowed clients."}

    target_service = "{}{}/login".format(referrer, environment)
    if not ticket:
        route_to_request_ticket = "{}?service={}".format(CAS_LOGIN_URL, target_service)
        app.logger.info("Redirected to: " + str(route_to_request_ticket))
        return redirect(route_to_request_ticket)
    environment = environment if environment is not None else "autosubmitapp" # can be used to target the test environment
    cas_verify_ticket_route = CAS_VERIFY_URL + '?service=' + target_service + '&ticket=' + ticket
    response = requests.get(cas_verify_ticket_route)
    user = None
    if response:
        user = Utiles.get_cas_user_from_xml(response.content)
    app.logger.info('CAS verify ticket response: user %s', user)
    if not user:
        return {'authenticated': False, 'user': None, 'token': None, 'message': "Can't verify user."}
    else:  # Login successful
        payload = {
            'user_id': user,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
        }
        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        return {'authenticated': True, 'user': user, 'token': jwt_token, 'message': "Token generated."}


@app.route('/updatedesc', methods=['GET', 'POST'])
@cross_origin(expose_headers="Authorization")
def update_description():
    """
    Updates the description of an experiment. Requires authenticated user.
    """
    start_time = time.time()
    expid = None
    new_description = None
    if request.is_json:
        body_data = request.json
        expid = body_data.get("expid", None)
        new_description = body_data.get("description", None)
    current_token = request.headers.get("Authorization")
    try:
        jwt_token = jwt.decode(current_token, JWT_SECRET, JWT_ALGORITHM)
    except jwt.ExpiredSignatureError:
        jwt_token = {"user_id": None}
    except Exception as exp:
        jwt_token = {"user_id": None}
    valid_user = jwt_token.get("user_id", None)
    app.logger.info('UDESC|RECEIVED|')
    app.logger.info('UDESC|RTIME|' + str(time.time() - start_time))
    return update_experiment_description_owner(expid, new_description, valid_user)


@app.route('/tokentest', methods=['GET', 'POST'])
@cross_origin(expose_headers="Authorization")
def test_token():
    """
    Tests if a token is still valid
    """
    start_time = time.time()
    current_token = request.headers.get("Authorization")
    try:
        jwt_token = jwt.decode(current_token, JWT_SECRET, JWT_ALGORITHM)
    except jwt.ExpiredSignatureError:
        jwt_token = {"user_id": None}
    except Exception as exp:
        print(exp)
        jwt_token = {"user_id": None}

    valid_user = jwt_token.get("user_id", None)
    app.logger.info('TTEST|RECEIVED')
    app.logger.info('TTEST|RTIME|' + str(time.time() - start_time))
    return {
        "isValid": True if valid_user else False,
        "message": "Session expired" if not valid_user else None
    }


@app.route('/cconfig/<string:expid>', methods=['GET'])
@cross_origin(expose_headers="Authorization")
def get_current_configuration(expid):
    start_time = time.time()
    current_token = request.headers.get("Authorization")
    try:
        jwt_token = jwt.decode(current_token, JWT_SECRET, JWT_ALGORITHM)
    except Exception as exp:
        jwt_token = {"user_id": None}
    valid_user = jwt_token.get("user_id", None)
    app.logger.info('CCONFIG|RECEIVED|' + str(expid))
    result = CommonRequests.get_current_configuration_by_expid(expid, valid_user, app.logger)
    app.logger.info('CCONFIG|RTIME|' + str(expid) + "|" + str(time.time() - start_time))
    return result


@app.route('/expinfo/<string:expid>', methods=['GET'])
def exp_info(expid):
    start_time = time.time()
    app.logger.info('EXPINFO|RECEIVED|' + str(expid))
    result = CommonRequests.get_experiment_data(expid)
    app.logger.info('EXPINFO|RTIME|' + str(expid) + "|" + str(time.time() - start_time))
    return result


@app.route('/expcount/<string:expid>', methods=['GET'])
def exp_counters(expid):
    start_time = time.time()
    app.logger.info('EXPCOUNT|RECEIVED|' + str(expid))
    result = CommonRequests.get_experiment_counters(expid)
    app.logger.info('EXPCOUNT|RTIME|' + str(expid) + "|" + str(time.time() - start_time))
    return result


@app.route('/searchowner/<string:owner>/<string:exptype>/<string:onlyactive>', methods=['GET'])
@app.route('/searchowner/<string:owner>', methods=['GET'])
def search_owner(owner, exptype=None, onlyactive=None):
    """
    Same output format as search_expid
    """
    start_time = time.time()
    app.logger.info('SOWNER|RECEIVED|' + str(owner) + "|" + str(exptype) + "|" + str(onlyactive))
    result = search_experiment_by_id(searchString=None, owner=owner, typeExp=exptype, onlyActive=onlyactive)
    app.logger.info('SOWNER|RTIME|' + str(owner) + "|" + str(exptype) + "|" + str(onlyactive) + "|" + str(time.time() - start_time))
    return result


@app.route('/search/<string:expid>/<string:exptype>/<string:onlyactive>', methods=['GET'])
@app.route('/search/<string:expid>', methods=['GET'])
def search_expid(expid, exptype=None, onlyactive=None):
    start_time = time.time()
    app.logger.info('SEARCH|RECEIVED|' + str(expid) + "|" + str(exptype) + "|" + str(onlyactive))
    result = search_experiment_by_id(expid, owner=None, typeExp=exptype, onlyActive=onlyactive)
    app.logger.info('SEARCH|RTIME|' + str(expid) + "|" + str(exptype) + "|" + str(onlyactive) + "|" + str(time.time() - start_time))
    return result


@app.route('/running/', methods=['GET'])
def search_running():
    """
    Returns the list of all experiments that are currently running.
    """
    if 'username' in session:
        print(("USER {}".format(session['username'])))
    start_time = time.time()
    app.logger.info("Active proceses: " + str(D))
    app.logger.info('RUN|RECEIVED|')
    #app.logger.info("Received Currently Running query ")
    result = get_current_running_exp()
    app.logger.info('RUN|RTIME|' + str(time.time() - start_time))
    return result


@app.route('/runs/<string:expid>', methods=['GET'])
def get_runs(expid):
    """
    Get list of runs of the same experiment from the historical db
    """
    start_time = time.time()
    app.logger.info('ERUNS|RECEIVED|{0}'.format(expid))
    result = CommonRequests.get_experiment_runs(expid)
    app.logger.info('ERUNS|RTIME|{0}'.format(str(time.time() - start_time)))
    return result


@app.route('/ifrun/<string:expid>', methods=['GET'])
def get_if_running(expid):
    start_time = time.time()
    app.logger.info('IFRUN|RECEIVED|' + str(expid))
    result = CommonRequests.quick_test_run(expid)
    app.logger.info('IFRUN|RTIME|' + str(expid) + "|" + str(time.time() - start_time))
    return result


@app.route('/logrun/<string:expid>', methods=['GET'])
def get_log_running(expid):
    start_time = time.time()
    app.logger.info('LOGRUN|RECEIVED|' + str(expid))
    result = CommonRequests.get_current_status_log_plus(expid)
    app.logger.info('LOGRUN|RTIME|' + str(expid) + "|" + str(time.time() - start_time))
    return result


@app.route('/summary/<string:expid>', methods=['GET'])
def get_expsummary(expid):
    start_time = time.time()
    user = request.args.get("loggedUser", default="null", type=str)
    app.logger.info('SUMMARY|RECEIVED|' + str(expid))
    if user != "null": lock.acquire(); D[os.getpid()] = [user, "summary", True]; lock.release();
    result = CommonRequests.get_experiment_summary(expid, app.logger)
    app.logger.info('Process: ' + str(os.getpid()) + " workers: " + str(D))
    app.logger.info('SUMMARY|RTIME|' + str(expid) + "|" + str(time.time() - start_time))
    if user != "null": lock.acquire(); D[os.getpid()] = [user, "summary", False]; lock.release();
    if user != "null": lock.acquire(); D.pop(os.getpid(), None); lock.release();
    return result


@app.route('/shutdown/<string:route>')
def shutdown(route):
    """
    This function is invoked from the frontend (AS-GUI) to kill workers that are no longer needed.
    This call is common in heavy parts of the GUI such as the Tree and Graph generation or Summaries fetching.
    """
    start_time = time.time()

    try:
        user = request.args.get("loggedUser", default="null", type=str)
        expid = request.args.get("expid", default="null", type=str)
    except Exception as exp:
        app.logger.info("Bad parameters for user and expid in route.")

    if user != "null":
        app.logger.info('SHUTDOWN|RECEIVED for route: ' + route + " user: " + user + " expid: " + expid)
        try:
            # app.logger.info("user: " + user)
            # app.logger.info("expid: " + expid)
            app.logger.info("Workers before: " + str(D))
            lock.acquire()
            for k,v in list(D.items()):
                if v[0] == user and v[1] == route and v[-1] == True:
                    if v[2] == expid:
                        D[k] = [user, route, expid, False]
                    else:
                        D[k] = [user, route, False]
                    D.pop(k, None)
                    # reboot the worker
                    os.system('kill -HUP ' + str(k))
                    app.logger.info("killed worker " + str(k))
            lock.release()
            app.logger.info("Workers now: " + str(D))
        except Exception as exp:
            app.logger.info("[CRITICAL] Could not shutdown process " + expid + " by user \"" + user + "\"")
    app.logger.info('SHUTDOWN|DONE|RTIME' + "|" + str(time.time() - start_time))
    return ""


@app.route('/performance/<string:expid>', methods=['GET'])
def get_exp_performance(expid):
    start_time = time.time()
    app.logger.info('PRF|RECEIVED|' + str(expid))
    result = {}
    try:
        result = PerformanceMetrics(expid, JobListHelperDirector(JobListHelperBuilder(expid)).build_job_list_helper()).to_json()
    except Exception as exp:
        result = {"SYPD": None,
            "ASYPD": None,
            "RSYPD": None,
            "CHSY": None,
            "JPSY": None,
            "Parallelization": None,
            "considered": [],
            "error": True,
            "error_message": str(exp),
            "warnings_job_data": [],
        }
    app.logger.info('PRF|RTIME|' + str(expid) + "|" + str(time.time() - start_time))
    return result


@app.route('/graph/<string:expid>/<string:layout>/<string:grouped>', methods=['GET'])
def get_list_format(expid, layout='standard', grouped='none'):
    start_time = time.time()
    user = request.args.get("loggedUser", default="null", type=str)
    # app.logger.info("user: " + user)
    # app.logger.info("expid: " + expid)
    app.logger.info('GRAPH|RECEIVED|' + str(expid) + "~" + str(grouped) + "~" + str(layout))
    if user != "null": lock.acquire(); D[os.getpid()] = [user, "graph", expid, True]; lock.release();
    result = CommonRequests.get_experiment_graph(expid, app.logger, layout, grouped)
    app.logger.info('Process: ' + str(os.getpid()) + " graph workers: " + str(D))
    app.logger.info('GRAPH|RTIME|' + str(expid) + "|" + str(time.time() - start_time))
    if user != "null": lock.acquire(); D[os.getpid()] = [user, "graph", expid, False]; lock.release();
    if user != "null": lock.acquire(); D.pop(os.getpid(), None); lock.release();
    return result


@app.route('/tree/<string:expid>', methods=['GET'])
def get_exp_tree(expid):
    start_time = time.time()
    user = request.args.get("loggedUser", default="null", type=str)
    # app.logger.info("user: " + user)
    # app.logger.info("expid: " + expid)
    app.logger.info('TREE|RECEIVED|' + str(expid))
    if user != "null": lock.acquire(); D[os.getpid()] = [user, "tree", expid, True]; lock.release();
    result = CommonRequests.get_experiment_tree_structured(expid, app.logger)
    app.logger.info('Process: ' + str(os.getpid()) + " tree workers: " + str(D))
    app.logger.info('TREE|RTIME|' + str(expid) + "|" + str(time.time() - start_time))
    if user != "null": lock.acquire(); D[os.getpid()] = [user, "tree", expid, False]; lock.release();
    if user != "null": lock.acquire(); D.pop(os.getpid(), None); lock.release();
    return result


@app.route('/quick/<string:expid>', methods=['GET'])
def get_quick_view_data(expid):
    start_time = time.time()
    app.logger.info('QUICK|RECEIVED|' + str(expid))
    result = CommonRequests.get_quick_view(expid)
    app.logger.info('QUICK|RTIME|{0}|{1}'.format(str(expid), str(time.time() - start_time)))
    return result


@app.route('/exprun/<string:expid>', methods=['GET'])
def get_experiment_running(expid):
    """
    Finds log and gets the last 150 lines
    """
    start_time = time.time()
    app.logger.info('LOG|RECEIVED|' + str(expid))
    result = CommonRequests.get_experiment_log_last_lines(expid)
    app.logger.info('LOG|RTIME|' + str(expid) + "|" + str(time.time() - start_time))
    return result


@app.route('/joblog/<string:logfile>', methods=['GET'])
def get_job_log_from_path(logfile):
    """
    Get log from path
    """
    expid = logfile.split('_') if logfile is not None else ""
    expid = expid[0] if len(expid) > 0 else ""
    start_time = time.time()
    app.logger.info('JOBLOG|RECEIVED|{0}'.format(expid))
    result = CommonRequests.get_job_log(expid, logfile)
    app.logger.info('JOBLOG|RTIME|{0}|{1}'.format(expid, str(time.time() - start_time)))
    return result


@app.route('/pklinfo/<string:expid>/<string:timeStamp>', methods=['GET'])
def get_experiment_pklinfo(expid, timeStamp):
    start_time = time.time()
    app.logger.info('GPKL|RECEIVED|' + str(expid) + "~" + str(timeStamp))
    result = CommonRequests.get_experiment_pkl(expid)
    app.logger.info('GPKL|RTIME|' + str(expid) + "|" + str(time.time() - start_time))
    return result


@app.route('/pkltreeinfo/<string:expid>/<string:timeStamp>', methods=['GET'])
def get_experiment_tree_pklinfo(expid, timeStamp):
    start_time = time.time()
    app.logger.info('TPKL|RECEIVED|' + str(expid) + "~" + str(timeStamp))
    result = CommonRequests.get_experiment_tree_pkl(expid)
    app.logger.info('TPKL|RTIME|' + str(expid) + "|" + str(time.time() - start_time))
    return result


@app.route('/stats/<string:expid>/<string:filter_period>/<string:filter_type>')
def get_experiment_statistics(expid, filter_period, filter_type):
    start_time = time.time()
    app.logger.info('STAT|RECEIVED|' + str(expid) + "~" + str(filter_period) + "~" + str(filter_type))
    result = CommonRequests.get_experiment_stats(expid, filter_period, filter_type)
    app.logger.info('STAT|RTIME|' + str(expid) + "|" + str(time.time() - start_time))
    return result


@app.route('/history/<string:expid>/<string:jobname>')
def get_exp_job_history(expid, jobname):
    start_time = time.time()
    app.logger.info('HISTORY|RECEIVED|' + str(expid) + "~" + str(jobname))
    result = CommonRequests.get_job_history(expid, jobname)
    app.logger.info('HISTORY|RTIME|' + str(expid) + "|" + str(time.time() - start_time))
    return result


@app.route('/rundetail/<string:expid>/<string:runid>')
def get_experiment_run_job_detail(expid, runid):
    start_time = time.time()
    app.logger.info('RUNDETAIL|RECEIVED|' + str(expid) + "~" + str(runid))
    result = CommonRequests.get_experiment_tree_rundetail(expid, runid)
    app.logger.info('RUNDETAIL|RTIME|' + str(expid) + "|" + str(time.time() - start_time))
    return result


@app.route('/filestatus/')
def get_file_status():
    start_time = time.time()
    app.logger.info('FSTATUS|RECEIVED|')
    result = CommonRequests.get_last_test_archive_status()
    app.logger.info('FSTATUS|RTIME|' + str(time.time() - start_time))
    return result
