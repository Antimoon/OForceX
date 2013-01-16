#!/usr/bin/python
# OForceX.py
# A Python OFX Server Audit Toolkit
# 
__version__ = '0.8'
# Author: Antimoon
# E-Mail: antimoon (at) antimoon (dot) org

try:
    import sys
    import socket
    import getopt
    #import urllib
    import urlparse
    import ssl
    import datetime
    import random
except ImportError, e:
    print '[!] Error: %s' % e

attack = 'Plain'

#TODO: remove these
path           = '/path/on/server'
httphost       = 'hostname'

# TODO Implement attack methods
#brute-force
#    username
#    mfa answer
#    password

def make_ofx_request(path, httphost):
    ofxbody        = ofx_body_builder()
    ofxheaders     = ofxheaders()
    content_length = str(len(ofxheaders + ofxbody))

    httpheaders    = header_builder(path, httphost, content_length)
    requestfull    = httpheaders + ofxheaders + ofxbody
    log_status     = oforcex_log(str('Connecting to '+httphost+' at '+dateformat()), requestfull, logfile)
    # HTTP Request happens here
    #out            = http_request(httphost, requestfull, ssl=True, port=443)
    out            = 'HTTP test response'
    log_status     = oforcex_log(str('Response from '+httphost+' at '+dateformat()), out, logfile)



def parseargs(argv):
    # Argument Handler
    opts, args = getopt.gnu_getopt(argv,
        'h, l:, u:, b:, L:',
       ['help',
    #    'verbose'
        'log=',
        'bruteforce=',
        'length='
    #    'username='
        'url='])

    # Parse Options
    for o, a in opts:

        if o in ('-h', '--help'):
            show_help()
            sys.exit(0)

        if o in ('-u', '--url'):
            u = url_parse(str(a))
            path     = u['path']
            scheme   = u['scheme']
            httphost = u['host']
            query    = u['query']

        if o in ('-l', '--log'):
            logfile = a
            logging == True

        if o in ('-b', '--bruteforce'):
            if a == 'userkey':
                attack = 'userkey'
            else:
                print '[!] Invalid Brute-Force Attack Type, Aborting'
                sys.exit(1)

        if o in ('-L', '--length'):
            attacklen = a

    if len(sys.argv) == 1:
        show_help()

    if attack == 'Plain':

        try:
    #        u        = url_parse(url)
    #        path     = u['path']
    #        httphost = u['host']
    #        logfile  = logfile
            if logfile == None:
                logfile = 'oforcex_%s.log' % dateformat()

        except:
            print "[!] something went wrong, required vars don't exist yet"

        try:
            oforcex_log('Starting up','',logfile)
            ofxbody        = ofx_body_builder()
            ofxheaders     = ofxheaders()
            content_length = str(len(ofxheaders + ofxbody))
            httpheaders    = header_builder(path, httphost, content_length)
            requestfull    = httpheaders + ofxheaders + ofxbody
            log_status     = oforcex_log(str('Connecting to '+httphost+' at '+dateformat()), requestfull, logfile)
    # HTTP Request happens here
    #        out            = http_request(httphost, requestfull, ssl=True, port=443)
            out            = 'HTTP test response'
            log_status     = oforcex_log(str('Response from '+httphost+' at '+dateformat()), out, logfile)
            sys.exit(0)

        except Exception, e:
            log_status = oforcex_log('ERROR at '+dateformat(), e, logfile, True)
            print '[!] Error: %s' % e
            sys.exit(1)

    if attack == 'userkey':

        if logfile != None:
            attack_bf_userkey_harvest(logfile, attacklen)

        else:
            attack_bf_userkey_harvest(attacklen=attacklen)

    sys.exit(1)
