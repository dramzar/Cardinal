#!/usr/bin/env python3

''' Cardinal - An Open Source Cisco Wireless Access Point Controller

MIT License

Copyright © 2023 Cardinal Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import json
import MySQLdb
import multiprocessing
import os
from configparser import ConfigParser
from cryptography.fernet import Fernet
from redis import Redis
from rq import Queue
from rq import Retry
from scout import info
from scout import ssid
from scout import sys
from flask_login import UserMixin

class CardinalEnv():
    '''
    Object that defines how Cardinal ultimately
    behaves. CardinalEnv() will return a dict()
    with configuration options, which will be ingested
    on invocation.
    '''
    def __init__(self):

        # Ingest values from config file at CARDINALCONFIG

        self.cardinalConfig = ConfigParser()
        try:
            cardinalConfigFile = os.environ['CARDINALCONFIG']
        except:
            cardinalConfigFile = "/opt/cardinal.ini"

        self.cardinalConfig.read(cardinalConfigFile)
        # Create a dict() to hold tuning values
        self.tunings = dict()

        # Establish default behavior. If values are not defined
        # in CARDINALCONFIG, we'll try to handle accordingly.

        if self.cardinalConfig.has_option('cardinal', 'dbServer'):
            self.tunings['dbServer'] = self.cardinalConfig.get('cardinal', 'dbServer')
        else:
            self.tunings['dbServer'] = '127.0.0.1'

        if self.cardinalConfig.has_option('cardinal', 'dbUsername'):
            self.tunings['dbUsername'] = self.cardinalConfig.get('cardinal', 'dbUsername')
        else:
            self.tunings['dbUsername'] = 'root'

        if self.cardinalConfig.has_option('cardinal', 'dbPassword'):
            self.tunings['dbPassword'] = self.cardinalConfig.get('cardinal', 'dbPassword')
        else:
            self.tunings['dbPassword'] = ''

        if self.cardinalConfig.has_option('cardinal', 'dbName'):
            self.tunings['dbName'] = self.cardinalConfig.get('cardinal', 'dbName')
        else:
            self.tunings['dbName'] = 'cardinal'

        if self.cardinalConfig.has_option('cardinal', 'dbPort'):
            self.tunings['dbPort'] = int(self.cardinalConfig.get('cardinal', 'dbPort'))
        else:
            self.tunings['dbPort'] = 3306

        self.tunings['dbURI'] = f"mysql+pymysql://{self.tunings['dbUsername']}:{self.tunings['dbPassword']}@{self.tunings['dbServer']}:{self.tunings['dbPort']}/{self.tunings['dbName']}?charset=utf8mb4"

        if self.cardinalConfig.has_option('cardinal', 'flaskKey'):
            self.tunings['flaskKey'] = self.cardinalConfig.get('cardinal', 'flaskKey')
        else:
            self.tunings['flaskKey'] = '1eb88eb6c196cbbe488dfb3a128bc8230263aad7f32ec050da35d037cc1727c2'

        if self.cardinalConfig.has_option('cardinal', 'encryptKey'):
            self.tunings['encryptKey'] = self.cardinalConfig.get('cardinal', 'encryptKey')
        else:
            self.tunings['encryptKey'] = 'rFLoNiCTwoOa6o8QOXBy-9WK2-IdSTT8HKiiIzQFHVVZ='

        if self.cardinalConfig.has_option('cardinal', 'workers'):
            self.tunings['workers'] = int(self.cardinalConfig.get('cardinal', 'workers'))
        else:
            self.tunings['workers'] = 1

        if self.cardinalConfig.has_option('cardinal', 'sessionTimeout'):
            self.tunings['sessionTimeout'] = int(self.cardinalConfig.get('cardinal', 'sessionTimeout'))
        else:
            self.tunings['sessionTimeout'] = 1000

        if self.cardinalConfig.has_option('cardinal', 'redisServer'):
            self.tunings['redisServer'] = self.cardinalConfig.get('cardinal', 'redisServer')
        else:
            self.tunings['redisServer'] = "localhost"

        if self.cardinalConfig.has_option('cardinal', 'redisPort'):
            self.tunings['redisPort'] = int(self.cardinalConfig.get('cardinal', 'redisPort'))
        else:
            self.tunings['redisPort'] = 6379

        if self.cardinalConfig.has_option('cardinal', 'jobRetry'):
            self.tunings['jobRetry'] = int(self.cardinalConfig.get('cardinal', 'jobRetry'))
        else:
            self.tunings['jobRetry'] = 3



    def sql(self):
        '''
        Connection object for MySQLdb transactions.
        '''
        conn = MySQLdb.connect(host=self.tunings['dbServer'], user=self.tunings['dbUsername'], port=self.tunings['dbPort'], passwd=self.tunings['dbPassword'], db=self.tunings['dbName'])

        return conn

    def encryption(self, input, action):
        '''
        Encrypt/decrypt a sensitive value in Cardinal
        using Fernet.
        '''
        encryptKey = self.tunings['encryptKey']
        bytesKey = bytes(encryptKey, 'utf-8')
        cipherSuite = Fernet(bytesKey)

        if action == "encrypt":
            # Encrypt the value using cipherSuite
            value = cipherSuite.encrypt(bytes(input, 'utf-8')).decode('utf-8')
        elif action == "decrypt":
            # Decrypt the value using cipherSuite
            value = cipherSuite.decrypt(bytes(input, 'utf-8')).decode('utf-8')
        else:
            return "ERROR: Invalid action type."

        return value

    def config(self):
        '''
        List Cardinal tunings dictionary
        '''
        return self.tunings

    def users(self):
        '''
        List of users
        '''
        conn = self.sql()
        usercurs = conn.cursor()
        usercurs.execute("SELECT username, password FROM users")
        l = {}
        for user in usercurs.fetchall():
            l[user[0]] = User(user[0], user[1])

        usercurs.close()
        return l


class ToolkitJob(CardinalEnv):
    '''
    Object that defines how network toolkit
    jobs are handled in Cardinal.
    '''
    def __init__(self):
        '''
        Default constructor for Ssid() object.
        '''
        super().__init__()

    def add(self, command, arguments, duration, result):
        '''
        Add a new network toolkit job record
        to Cardinal backend.
        '''
        conn = self.sql()

        try:
            addToolkitJobCursor = conn.cursor()
            addToolkitJobCursor.execute("INSERT INTO network_toolkit_jobs (toolkit_job_command, toolkit_job_arguments, toolkit_job_duration, toolkit_job_result) \
            VALUES (%s, %s, %s, %s, %s)",(command, arguments, duration, result))
            addToolkitJobCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def delete(self, id):
        '''
        Delete a network toolkit job from Cardinal
        backend.
        '''
        conn = self.sql()

        try:
            deleteToolkitJobCursor = conn.cursor()
            deleteToolkitJobCursor.execute("DELETE FROM network_toolkit_jobs WHERE toolkit_job_id = %s", [id])
            deleteToolkitJobCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def info(self, id=None, **kwargs):
        '''
        Based on jobId provided, grab connection information from MySQL as a tuple
        and return a dict() object (by default).

        Supported keywords
        struct:
            dict: Returns a Python dict() object
        '''
        conn = self.sql()

        try:
            if id is None:
                toolkitJobInfoCursor = conn.cursor(MySQLdb.cursors.DictCursor)
                toolkitJobInfoCursor.execute("SELECT toolkit_job_id, toolkit_job_command, toolkit_job_arguments, toolkit_job_duration, toolkit_job_result FROM network_toolkit_jobs")
                toolkitJobInfo = toolkitJobInfoCursor.fetchall()
                toolkitJobInfoCursor.close()
            else:
                toolkitJobInfoCursor = conn.cursor(MySQLdb.cursors.DictCursor)
                toolkitJobInfoCursor.execute("SELECT toolkit_job_id, toolkit_job_command, toolkit_job_arguments, toolkit_job_duration, toolkit_job_result FROM network_toolkit_jobs WHERE \
                toolkit_job_id = %s", [id])
                toolkitJobInfo = toolkitJobInfoCursor.fetchall()
                toolkitJobInfoCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)

        else:
            return list(toolkitJobInfo)

class ScoutJob(CardinalEnv):
    '''
    Object that defines how scout
    jobs are handled in Cardinal.
    '''
    def __init__(self):
        '''
        Default constructor for ScoutJob() object.
        '''
        super().__init__()

    def add(self, command, arguments, duration, result):
        '''
        Add a new scout job record
        to Cardinal backend.
        '''
        conn = self.sql()

        try:
            addToolkitJobCursor = conn.cursor()
            addToolkitJobCursor.execute("INSERT INTO scout_jobs (toolkit_job_command, toolkit_job_arguments, toolkit_job_duration, toolkit_job_result) \
            VALUES (%s, %s, %s, %s)",(command, arguments, duration, result))
            addToolkitJobCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def delete(self, id):
        '''
        Delete a scout job from Cardinal
        backend.
        '''
        conn = self.sql()

        try:
            deleteToolkitJobCursor = conn.cursor()
            deleteToolkitJobCursor.execute("DELETE FROM network_toolkit_jobs WHERE toolkit_job_id = %s", [id])
            deleteToolkitJobCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)
        else:
            conn.commit()

    def info(self, id=None, **kwargs):
        '''
        Based on jobId provided, grab connection information from MySQL as a tuple
        and return a dict() object (by default).

        Supported keywords
        struct:
            dict: Returns a Python dict() object
        '''
        conn = self.sql()

        try:
            if id is None:
                toolkitJobInfoCursor = conn.cursor(MySQLdb.cursors.DictCursor)
                toolkitJobInfoCursor.execute("SELECT toolkit_job_id, toolkit_job_command, toolkit_job_arguments, toolkit_job_duration, toolkit_job_result FROM network_toolkit_jobs")
                toolkitJobInfo = toolkitJobInfoCursor.fetchall()
                toolkitJobInfoCursor.close()
            else:
                toolkitJobInfoCursor = conn.cursor(MySQLdb.cursors.DictCursor)
                toolkitJobInfoCursor.execute("SELECT toolkit_job_id, toolkit_job_command, toolkit_job_arguments, toolkit_job_duration, toolkit_job_result FROM network_toolkit_jobs WHERE \
                toolkit_job_id = %s", [id])
                toolkitJobInfo = toolkitJobInfoCursor.fetchall()
                toolkitJobInfoCursor.close()
        except Exception as e:
            return "ERROR: {}".format(e)

        else:
            return list(toolkitJobInfo)

# SYSTEM MESSAGES/UTILITIES

class AsyncOpsManager(CardinalEnv):
    '''
    Object that defines how asynchronous work
    is handled within Cardinal.
    '''
    def __init__(self):
        '''
        Default constructor for AsyncOpsManager() object.
        '''
        super().__init__()

        # Initiate connection to Redis backend
        conn = Redis(host=self.tunings["redisServer"], port=self.tunings["redisPort"])

        # Establish Redis queue for asynchronous work
        self.asyncQueue = Queue(connection=conn)

    def run(self, func, args):
        '''
        Run an unit of asynchronous work (by function)
        '''
        asyncResult = self.asyncQueue.enqueue(func, kwargs=args, retry=Retry(max=self.tunings["jobRetry"]), on_success=reportSuccess)
        return asyncResult

def reportSuccess(job, connection, result, *args, **kwargs):
    cenv = CardinalEnv()
    conn = cenv.sql()

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rqworker_results (job_id, result) VALUES (%s,%s)", (job._id, result))
        cursor-close()
    except Exception as e:
        return f"ERROR: {e}"
    else:
        conn.commit()

#    with open('/var/log/cardinal/fetcher.log', 'a') as f:
#        f.write(f"JobID:\t\t{job._id}\nConnection:\t{connection}\nResult:\t\t{result}\nArgs:\t\t{args}\nKwArgs:\t\t{kwargs}\n")


def jsonResponse(level, message, **kwargs):
    '''
    Temporary way of getting some simple logging
    into Cardinal.

    # TODO: Remove this in favor of the logging module.
    '''
    if "reference" in kwargs:
        responseDict = dict(level=level, message=message, reference=kwargs["reference"])
    else:
        responseDict = dict(level=level, message=message)

    return responseDict

def msgResourceDeleted(resource):
    msg = "{} was deleted successfully!".format(resource)
    return msg

def msgResourceAdded(resource):
    msg = "{} was registered successfully!".format(resource)
    return msg

msgAuthFailed = 'Authentication failed. Please check your credentials and try again by clicking <a href="/">here</a>.'

def msgSpecifyValidApGroup():
    return "Please select a valid access point group."

def msgSpecifyValidAp():
    return "Please select a valid access point."

def printCompletionTime(endTime):
    '''
    Prints completion time for parallel group processes.
    '''
    completionTime = "INFO: Group Operation Completed In: {}".format(endTime)
    return completionTime

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password

    def savePassword(self):
        pass
