#!/usr/bin/python
#
# body_builder.py
#
# A portion of OForceX
# Written by Antimoon
#

import config_handler

######################################################################
# OFXBODY ############################################################
######################################################################
# TODO: set up body portion flags

def build(
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
    fi_profile   =False,

    # Variable Dictionaries
    signon_var_dict         = config_handler.gen_dict('signon'),
    bankmsgs_var_dict       = config_handler.gen_dict('bank'),
    creditcardmsgs_var_dict = config_handler.gen_dict('creditcard'),
    profmsgs_var_dict       = config_handler.gen_dict('prof'),
    signupmsgs_var_dict     = config_handler.gen_dict('signup')
    ):

    ofxbody = '<OFX>\r\n'

    if signon == True:
        ofxbody += signonmsgs.build(var_dict = signon_var_dict)

    if signup == True:
        ofxbody += signupmsgs.build()

    if banking == True:
        ofxbody += bankingmsgs.build()

    if cc_stmt == True:
        ofxbody += creditcardmsgs.build()

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
        ofxbody += profmsgs.build()

    ofxbody += '</OFX>\r\n\r\n'

    return ofxbody
