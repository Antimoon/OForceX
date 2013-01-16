#!/usr/bin/python
#
# profmsgs.py
#
# A portion of OForceX
# Written by Antimoon
#
######################################################################
# PROFMSGSRQV1 #######################################################
######################################################################
def build(
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
