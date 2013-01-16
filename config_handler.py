#!/usr/bin/python
#
# config_handler.py
#
# A portion of OForceX
# Written by Antimoon
#

import ConfigParser

config  = ConfigParser.ConfigParser()
config.read('config.cfg')

signon_var_dict = {
    'finame'       : config.get('Signon','finame')                     ,
    'fid'          : config.get('Signon','fid')                        ,
    'ofxtimestamp' : datetime.datetime.now().strftime('%Y%m%d%H%M%S')  ,
    'userid'       : config.get('Signon','userid')                     ,
    'userpass'     : config.get('Signon','userpass')                   ,
    'genuserkey'   : config.get('Signon','genuserkey')                 ,
    'userkey'      : config.get('Signon','userkey')                    ,
    'lang'         : config.get('Signon','lang')                       ,
    'appid'        : config.get('Signon','appid')                      ,
    'appver'       : config.get('Signon','appver')                     ,
    'clientuid'    : trnuid_gen()                                      ,
    'sesscookie'   : config.get('Signon','sesscookie')                 ,
    'mfa_trnuid'   : trnuid_gen()                                      ,
    'mfa_id'       : config.get('Signon','mfa_id')                     ,
    'mfa_answer'   : config.get('Signon','mfa_answer')                 ,
    'newuserpass'  : config.get('Signon','newuserpass')                ,
    'ficertid'     : config.get('Signon','ficertid')                   }

bankmsgs_var_dict = {
    'bankid'       : config.get('Bankmsgs','bankid')                   ,
    'acctid'       : config.get('Bankmsgs','acctid')                   ,
    'accttype'     : config.get('Bankmsgs','accttype')                 ,
    'bank_include' : config.get('Bankmsgs','bank_include')             }

creditcardmsgs_var_dict = {
    'startdate' : config.get('Creditcardmsgs','startdate')             ,
    'enddate'   : config.get('Creditcardmsgs','enddate')               ,
    'include'   : config.get('Creditcardmsgs','include')               ,
    'acctid'    : config.get('Creditcardmsgs','acctid')                ,
    'key'       : config.get('Creditcardmsgs','key')                   }

profmsgs_var_dict = {
    'clientrouting' : config.get('Profmsgs','clientrouting')           ,
    'dtprofup'      : config.get('Profmsgs','dtprofup')                }

signupmsgs_var_dict = {
    'dtacctup' : config.get('Signupmsgs','dtacctup')                   }

def gen_dict(msgs):
    '''Returns a variable dictionary based on an input string'''
    if not msgs in ('signon', 'bank', 'creditcard', 'prof', 'signup'):
        print '[!] ERROR: ATTEMPTED TO RETRIEVE var_dict FOR INVALID MESSAGESET %s' % str(msgs)
        sys.exit(1)

    if msgs == 'signon':
        return signon_var_dict
    elif msgs == 'bank':
        return bankmsgs_var_dict
    elif msgs == 'creditcard':
        return creditcardmsgs_var_dict
    elif msgs == 'prof':
        return profmsgs_var_dict
    elif msgs == 'signup':
        return signupmsgs_var_dict

