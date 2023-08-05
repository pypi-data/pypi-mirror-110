import time
import sys
import os
from IutyLib.file.log import SimpleLog
from IutyLib.commonutil.config import Config
from flask import Flask
from flask_restful import *#Api,Resource
from flask_cors import *

#import multiprocessing

app = Flask(__name__)
api = Api(app)
CORS(app,supports_credentials=True)

host = '0.0.0.0'
port = int(config.get("Server","port"))

if __name__ == '__main__':
    #multiprocessing.freeze_support()
    app.run(host=host,port=port,debug=False ,use_reloader=False)