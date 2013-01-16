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
except Exception, e:
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

def dateformat(date=None):
    # Format dates for use with OFX
    if date != None:
        out = date.strftime('%Y%m%d')
    else:
        out = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    return out

def oforcex_log(messagehead='', messagebody='', logfile='', warning=False):
    global logging
    if logfile == '':
        return 0
    else:
        if warning == False:
            x = '[*] '
        else:
            x = '[!] '
        try:
            file = open(logfile, "a")
            file.write('%s%s\n' % (x,messagehead))
            file.write(  '%s\n' % messagebody)
            file.close()
        except Exception, e:
            print '[!] %s' % e
        return 1

def trnuid_gen():
    # Generates a random string with acceptable formatting for a UID
    i = 0
    trnuid = ''.join(random.choice('abcdef1234567890') for a in range(8))+'-'
    while i < 3:
        trnuid += ''.join(random.choice('abcdef1234567890') for a in range(4))+'-'
        i+=1
    trnuid += ''.join(random.choice('abcdef1234567890') for a in range(12))
    return trnuid

def show_help():
    # TODO
    print 'Usage: %s -u <URL> -l <LOGFILE> -b <ATTACKTYPE> -L <ATTACKLENGTH>'
    print ''
    print 'Accepted Attack Types:'
    print '\tuserkey\t\tHarvest OFX Session IDs'
    # Reserved for commandline functionality
    sys.exit(0)

def tag_maker(tagname, content=''):
    # Builds an OFX compliant tag
    # Accepts 2 strings as input and returns 1 string as output
    tagname = str(tagname).upper()
    built   = '<%s>%s</%s>\r\n' % (tagname, content, tagname)
    return built

def msg_maker(msgdict, text=True):
    # Builds an OFX message set
    # Accepts a dictionary and a string as input, returns a string
    # or list as output.
    outlist = []
    for key in msgdict.keys():
        outlist.append(tag_maker(key, msgdict[key]))
    if text == True:
        outstring = ''.join(outlist)
        return outstring
    else:
        return outlist

def url_parse(string_url):
    u = urlparse.urlsplit(string_url)
    return {'scheme' :u.scheme,
            'host'   :u.netloc,
            'query'  :u.query,
            'path'   :u.path}

def http_request(host, data, ssl=True, port=443, l=4):
    # Simple Sockets connection script, modify l for
    # response data length
    try:
        hostip = socket.gethostbyname(host) 
    except:
        hostip = host
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if ssl == True:
        try:
            s = ssl.wrap_socket(s)
            connect = s.connect((hostip, port))
        except Exception, e:
            print '[!] Error: %s' % e
    else:
        try:
            connect = s.connect((hostip, port))
        except Exception, e:
            print '[!] Error: %s' % e
    s.send(data)
    response = str(s.recv(1024*l))
    s.close()
    return response

# OFX Header Vars #########################################
# TODO: Implement support for other versions of OFX
#ofxversion = ['1.02', '1.03', '1.6', '2.02', '2.03', '2.1', '2.1.1']
#ofxversion = ''.join(split(ofxversion, '.'))

# Construct OFX Headers ###################################
# TODO: improve header building.
def ofxheaders():
    ofxheaders =(
        'OFXHEADER:100\r\n'                                          +
        'DATA:OFXSGML\r\n'                                           +
        'VERSION:103\r\n'                                            +
        'SECURITY:NONE\r\n'                                          +
        'ENCODING:USASCII\r\n'                                       +
        'CHARSET:1252\r\n'                                           +
        'COMPRESSION:NONE\r\n'                                       +
        'OLDFILEUID:NONE\r\n'                                        +
        'NEWFILEUID:NONE\r\n\r\n'                                    )
    return ofxheaders

# Construct OFX Body ######################################
#
# TODO:
# Lots to do here, need a better way to construct the body, and a way
# to account for all vars. It would be best to construct the request
# going forwards instead of in reverse.
# 
# UPDATE 11/14/2012:
# Signon Message Set has gotten an overhaul, will be doing similar 
# things with the other message sets, so stay tuned.
#
# UPDATE 11/15/2012:
# TODO: Implement the rest of the base message sets
######################################################################
# SIGNONMSGSRQV1 ##################################################### 
######################################################################
# The Signon Message Set
#
# The signon message set is usually sent with every request. Auth happens
# here, so lots of attacks will be based around these params.
#
# TODO: handle the dictionary with a config file or commandline 
#
# Messages that appear in this section, in order, are:
# Signon message
# MFA challenge messages (request and answer)
# USERPASS change message
# Challenge message
def signonmsgs(
    switch_dict = {
        'sonrq'             :True                                    ,
        'mfachallengetrnrq' :False                                   ,
        'mfachallengea'     :False                                   ,
        'pinchtrnrq'        :False                                   ,
        'challengetrnrq'    :False                                  },

    var_dict = {}):
# Signon Message Set Builder Function
# TODO: implement passing the vars

# Init signon messageset fields
    ofxbody_signonmsgsrqv1_sonrq             = ''
    ofxbody_signonmsgsrqv1_mfachallengetrnrq = ''
    ofxbody_signonmsgsrqv1_mfachallengea     = ''
    ofxbody_signonmsgsrqv1_pinchtrnrq        = ''
    ofxbody_signonmsgsrqv1_challengetrnrq    = ''
    ofxbody_signonmsgsrqv1_dict              = {}

    # Signon Message #####################################################
    #
    # Must be in EVERY message
    #
    if switch_dict['sonrq'] == True:
        ###########################
        # Financial Institution ID
        #
        # An identifier oprtion of the signon message, relevant to service
        # providers who support multiple FIs
        # Name of the FI
        finame = 'viaFinancial'
        # 
        # Provider-Assigned FI ID number
        fid    = '9876'

        fi = msg_maker({
            'org':finame                                                 ,
            'fid':fid                                                   })

        # Current date and time, to the second. Handled automatically.
        # TODO: add timestamp validation check
        ofxtimestamp   = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        #
        # Username, assigned by FI. can also be anonymous
        # TODO: perform check for anonymous auth
        userid         = '123456'
        #
        # Password/Pin
        userpass       = 'not-used'#'anonymous00000000000000000000000'
        #
        # Generate USERKEY, boolean Y/N value.
        # TODO: log userkeys to file to test for entropy.
        genuserkey     = 'Y'
        #
        # User Key
        #    userkey        = ''
        #
        # Language, ENG by default
        lang           = 'ENG'
        #
        # App ID
        appid          = 'MobileApp'
        #
        # App Version
        appver         = '1.0'
        # Client UID
        #clientuid      = ''
        clientuid = trnuid_gen()
        #
        # session cookie, optional value that allows FIs to track users.
        # NOT involved in auth
        #    sesscookie = ''

        ofxbody_signonmsgsrqv1_sonrq = msg_maker({
            'dtclient'   :ofxtimestamp                                   ,
            'userid'     :userid                                         ,
            'userpass'   :userpass                                       ,
#            'userkey'    :userkey                                        ,
            'genuserkey' :genuserkey                                     ,
            'language'   :lang                                           ,
            'fi'         :fi                                             ,
            'appid'      :appid                                          ,
            'appver'     :appver                                         ,
            'clientuid'  :clientuid                                     })

    # MFA Challenge ######################################################
    if switch_dict['mfachallengetrnrq'] == True:
        # MFA transaction UID, auto generated
        mfa_trnuid = trnuid_gen()

        mfachallengerq = msg_maker({                                               
            'dtclient':ofxtimestamp                                     })

        ofxbody_signonmsgsrqv1_mfachallengetrnrq = msg_maker({
            'trnuid'         :mfa_trnuid                                 ,
            'mfachallengerq' :mfachallengerq                            })

    # MFA Challenge Answer ###############################################
    if switch_dict['mfachallengea'] == True:
        # MFA Question ID
        mfa_id         = '2'
        #
        # MFA Question Answer
        mfa_answer     = '' 

        ofxbody_signonmsgsrqv1_mfachallengea = msg_maker({
            'mfaphraseid':mfa_id                                         ,
            'mfaphrasea' :mfa_answer                                    })

    # USERPASS Change ####################################################
    if switch_dict['pinchtrnrq'] == True:
        # Username from above
        # TODO: attempt to change other users' passwords
        userid      = userid
        #
        # New Password
        newuserpass = ''

        pinchrq = msg_maker({
            'userid'      :userid                                         ,
            'newuserpass' :newuserpass                                   })

        ofxbody_signonmsgsrqv1_pinchtrnrq = msg_maker({
            'pinchrq':pinchrq                                            })

    # Challenge Request ##################################################
    if switch_dict['challengetrnrq'] == True:
        # Type 1 security only
        #
        # Username from above
        userid   = userid 
        #
        # FI certificate ID, only need to include if already have it
        # TODO: Fuzz cert IDs
        #ficertid = ''
        challengerq = msg_maker({
            'userid'   :userid                                          })
#            'ficertid' :ficertid                                        })
        ofxbody_signonmsgsrqv1_challengetrnrq = msg_maker({
            'challengerq':challengerq                                   })

    ofxbody_signonmsgsrqv1_dict_0 = {
        'sonrq'             :ofxbody_signonmsgsrqv1_sonrq                ,
        'mfachallengetrnrq' :ofxbody_signonmsgsrqv1_mfachallengetrnrq    ,
        'mfachallengea'     :ofxbody_signonmsgsrqv1_mfachallengea        ,
        'pinchtrnrq'        :ofxbody_signonmsgsrqv1_pinchtrnrq           ,
        'challengetrnrq'    :ofxbody_signonmsgsrqv1_challengetrnrq       }
#        'logout'            :'Y'                                         }

    for item in switch_dict.keys():
        if switch_dict[item] == True:
            ofxbody_signonmsgsrqv1_dict[item] = ofxbody_signonmsgsrqv1_dict_0[item]

    ofxbody_signonmsgsrqv1_0 = msg_maker(ofxbody_signonmsgsrqv1_dict)
    ofxbody_signonmsgsrqv1 = msg_maker({'signonmsgsrqv1':ofxbody_signonmsgsrqv1_0})

    return ofxbody_signonmsgsrqv1

######################################################################
# BANKMSGSRQV1 #######################################################
######################################################################
def bankmsgs(
    s_bankacctfrom  = True                                           ,
    s_inctran       = True                                           ,
    trnuid          = trnuid_gen()                                   ,
    bankid          = ''                                             ,
    acctid          = ''                                             ,
    accttype        = ''                                             ,
    bank_include    = 'N'
    ):

    if s_bankacctfrom == True:
        bankacctfrom = msg_maker({
            'bankid'   :bankid                                       ,
            'acctid'   :acctid                                       ,
            'accttype' :accttype                                    })
    if s_inctran == True:
        inctran = msg_maker({
            'include'  :bank_include                                })
    stmtrq = msg_maker({
        'bankacctfrom' :bankacctfrom                                 ,
        'inctran'      :inctran                                     })
    stmttrnrq = msg_maker({
        'trnuid'       :trnuid                                       ,
        'stmtrq'       :stmtrq                                      })
    bankmsgsrqv1 = msg_maker({
        'stmttrnrq'    :stmttrnrq                                   })
    ofxbody_bankmsgsrqv1 = msg_maker({
        'bankmsgsrqv1' :bankmsgsrqv1                                })
    return ofxbody_bankmsgsrqv1

#######################################################################
# SIGNUPMSGSRQV1 ######################################################
#######################################################################

def signupmsgs(
    signup_trnuid=trnuid_gen()                                       ,
    date='20120101000000'
    ):
    acctinforq = msg_maker({
        'dtacctup'       :date                                      })
    acctinfotrnrq = msg_maker({
        'trnuid'         :signup_trnuid                              ,
        'acctinforq'     :acctinforq                                })
    signupmsgsrqv1 = msg_maker({
        'acctinfotrnrq'  :acctinfotrnrq                             })
    ofxbody_signupmsgsrqv1 = msg_maker({
        'signupmsgsrqv1' :signupmsgsrqv1                            })
    return ofxbody_signupmsgsrqv1

######################################################################
# BILLPAYMSGSRQV1 ####################################################
######################################################################

######################################################################
# CREDITCARDMSGSRQV1 #################################################
######################################################################
def creditcardmsgs(
    cc_startdate = '20120101000000',
    cc_enddate   = dateformat(),
    cc_include   = '', # Y or N
    cc_acctid    = '',
    cc_key       = '',
    s_inctran    = False
    ):

    if s_inctran == True:
        inctran = msg_maker({
            'dtstart':cc_startdate                       ,
            'dtend':cc_enddate                           ,
            'include':cc_include                                    })                                            

    ccacctfrom = msg_maker({
        'acctid':cc_acctid                                           ,
        'acctkey':cc_key                                            })

    ccstmtrq = msg_maker({
        'ccacctfrom':ccacctfrom                                      ,
        'inctran':inctran                                           })

    ccstmttrnrq = msg_maker({
        'ccstmtrq':ccstmtrq                                         })                                 

    creditcardmsgsrqv1 = msg_maker({
        'ccstmttrnrq':ccstmttrnrq                                   })

    ofxbody_creditcardmsgsrqv1 = msg_maker({
        'creditcardmsgsrqv1':creditcardmsgsrqv1                     })

    return ofxbody_creditcardmsgsrqv1

######################################################################
# PROFMSGSRQV1 #######################################################
######################################################################
def profmsgs(
    # Profile Requests
    # Request profile contents as set by the Financial Institution.
    #
    # Set the transaction UID
    prof_trnuid   = trnuid_gen()                                     ,
    #
    # Set Client Routing Capabilities, choose from:
    # NONE, SERVICE, MSGSET
    clientrouting = ''                                               ,
    #
    # Set the date that the 'client' was last updated
    dtprofup      = '20120101000000'
    ):

    profrq = msg_maker({
        'clientrouting' :clientrouting                               ,
        'dtprofup'      :dtprofup                                   })
    proftrnrq = msg_maker({
        'profrq':profrq                                             })
    profmsgsrqv1 = msg_maker({
        'proftrnrq':proftrnrq                                       })
    ofxbody_profmsgsrqv1 = msg_maker({
        'profmsgsrqv1':profmsgsrqv1                                 })

    return ofxbody_profmsgsrqv1

######################################################################
# OFXBODY ############################################################
######################################################################
# TODO: set up body portion flags

def ofx_body_builder(
# OFX body portions MUST be added to the body in the order listed, as
# per the spec
    signon       =True, 
    signup       =False, 
    banking      =False, 
    cc_stmt      =False, 
    interbank    =False, 
    wiretransfer =False, 
    payments     =False, 
    email        =False, 
    investments  =False, 
    fi_profile   =False
    ):

    ofxbody = '<OFX>\r\n'

    if signon == True:
        ofxbody += signonmsgs()

    if signup == True:
        ofxbody += signupmsgs()

    if banking == True:
        ofxbody += bankingmsgs()

    if cc_stmt == True:
        ofxbody += creditcardmsgs()

# TODO: Implement the following message sets
#
#    if interbank == True:
#        ofxbody += ofxbody_interbankrqv1
#    if wiretransfer == True:
#        ofxbody += ofxbody_wiretransferrqv1
#    if payments == True:
#        ofxbody += ofxbody_paymentsrqv1
#    if email == True:
#        ofxbody += ofxbody_emailrqv1
#    if investments == True:
#        ofxbody += ofxbody_investmentsecurityrqv1

    if fi_profile == True:
        ofxbody += profmsgs()
    ofxbody += '</OFX>\r\n\r\n'
    return ofxbody

# Construct HTTP Request ##################################
#
def header_builder(string_url, contlen):
    u = url_parse(string_url)
    path = u['path']
    host = u['host']
    httpheaders =(
        'POST '+path+' HTTP/1.1\r\n'                                 +
        'Host: '+host+'\r\n'                                         +
        'Content-Type: application/x-ofx\r\n'                        +
        'Content-Length: '+contlen+'\r\n'                            +
        'Connection: Keep-Alive\r\n\r\n'                             )
    return httpheaders

#####################################################################
# ATTACKS ###########################################################
#####################################################################
def attack_bf_userkey_harvest(keyfile='userkeys', attacklen=1000):
    global path
    global httphost

    try:
        while i <= attacklen:
            ofxbody        = ofx_body_builder()
            ofxheaders     = ofxheaders()
            content_length = str(len(ofxheaders+ofxbody))
            httpheaders    = header_builder(path, httphost, content_length)
            requestfull    = httpheaders + ofxheaders + ofxbody
            out            = http_request(httphost, requestfull, ssl=True, port=443)
            key            = out.split('<USERKEY>')[1].split('</USERKEY>')[0]
            file = open(keyfile, "a")
            file.write(key)
            file.close()
            i+=1
        sys.exit(0)

    except Exception, e:
        print '[!] Error %s' % e
        sys.exit(1)
    
# Argument Handler
opts,args=getopt.gnu_getopt(sys.argv[1:],
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
