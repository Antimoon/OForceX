#!/usr/bin/python
#
# signupmsgs.py
#
# A portion of OForceX
# Written by Antimoon
#
#######################################################################
# SIGNUPMSGSRQV1 ######################################################
#######################################################################

def build(
    signup_trnuid=trnuid_gen()                                       ,
    date='20120101000000'                                           ):

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
