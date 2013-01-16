#!/usr/bin/python
#
# signonmsgs.py
#
# A portion of OForceX
# Written by Antimoon
#
######################################################################
# SIGNONMSGSRQV1 ##################################################### 
######################################################################
# The Signon Message Set
#
# The signon message set is usually sent with every request. Auth happens
# here, so lots of attacks will be based around these params.
#
# Messages that appear in this section, in order, are:
# Signon message
# MFA challenge messages (request and answer)
# USERPASS change message
# Challenge message

import datetime

def build(
    switch_dict = {
        'sonrq'             :True                                        ,
        'mfachallengetrnrq' :False                                       ,
        'mfachallengea'     :False                                       ,
        'pinchtrnrq'        :False                                       ,
        'challengetrnrq'    :False                                      },

    var_dict = {
        ###########################
        # Financial Institution ID
        #
        # An identifier oprtion of the signon message, relevant to 
        # service providers who support multiple FIs
        #
        # Name of the FI
        'finame' : 'ChangeMeCU'                                          ,
        # 
        # Provider-Assigned FI ID number
        'fid'    : '9876'                                                ,

        # Current date and time, to the second. Handled automatically.
        'ofxtimestamp' : datetime.datetime.now().strftime('%Y%m%d%H%M%S'),
        #
        # Username, assigned by FI. can also be anonymous
        'userid'         : '123456'                                      ,
        #
        # Password/Pin
        'userpass'       : 'not-used',#'anonymous00000000000000000000000'
        #
        # Generate USERKEY, boolean Y/N value.
        'genuserkey'     : 'Y'                                           ,
        #
        # User Key
        #'userkey'        : ''                                            ,
        #
        # Language, ENG by default
        'lang'           : 'ENG'                                         ,
        #
        # App ID
        'appid'          : 'OForceX'                                     ,
        #
        # App Version
        'appver'         : '1.0'                                         ,
        # Client UID
        #'clientuid'      : ''                                            ,
        'clientuid'      : trnuid_gen()                                  ,
        #
        # session cookie, optional value that allows FIs to track users.
        # NOT involved in auth
        #'sesscookie' : ''                                                ,
        #
        # MFA transaction UID, auto generated
        'mfa_trnuid'     : trnuid_gen()                                  ,
        # MFA Question ID
        'mfa_id'         : '2'                                           ,
        #
        # MFA Question Answer
        'mfa_answer'     : ''                                            ,
        #
        # New Password
        'newuserpass'    : ''
        # FI certificate ID, only need to include if already have it
        #ficertid = ''
                                                                       }):

    # Init signon messageset fields
    ofxbody_signonmsgsrqv1_sonrq             = ''
    ofxbody_signonmsgsrqv1_mfachallengetrnrq = ''
    ofxbody_signonmsgsrqv1_mfachallengea     = ''
    ofxbody_signonmsgsrqv1_pinchtrnrq        = ''
    ofxbody_signonmsgsrqv1_challengetrnrq    = ''
    ofxbody_signonmsgsrqv1_dict              = {}

    # Signon Message #####################################################
    #
    # Must be in EVERY message, in standard implementations
    #
    if switch_dict['sonrq']:

        fi = msg_maker({
            'org':var_dict['finame']                                     ,
            'fid':var_dict['fid']                                       })

        ofxbody_signonmsgsrqv1_sonrq = msg_maker({
            'dtclient'   :var_dict['ofxtimestamp']                       ,
            'userid'     :var_dict['userid']                             ,
            'userpass'   :var_dict['userpass']                           ,
#            'userkey'    :var_dict['userkey']                            ,
            'genuserkey' :var_dict['genuserkey']                         ,
            'language'   :var_dict['lang']                               ,
            'fi'         :fi                                             ,
            'appid'      :var_dict['appid']                              ,
            'appver'     :var_dict['appver']                             ,
            'clientuid'  :var_dict['clientuid']                         })

    # MFA Challenge ######################################################
    if switch_dict['mfachallengetrnrq']:
        mfachallengerq = msg_maker({                                               
            'dtclient':var_dict['ofxtimestamp']                         })

        ofxbody_signonmsgsrqv1_mfachallengetrnrq = msg_maker({
            'trnuid'         :var_dict['mfa_trnuid']                     ,
            'mfachallengerq' :mfachallengerq                            })

    # MFA Challenge Answer ###############################################
    if switch_dict['mfachallengea']:
        ofxbody_signonmsgsrqv1_mfachallengea = msg_maker({
            'mfaphraseid':var_dict['mfa_id']                             ,
            'mfaphrasea' :var_dict['mfa_answer']                        })

    # USERPASS Change ####################################################
    if switch_dict['pinchtrnrq']:
        pinchrq = msg_maker({
            'userid'      :var_dict['userid']                            ,
            'newuserpass' :var_dict['newuserpass']                      })

        ofxbody_signonmsgsrqv1_pinchtrnrq = msg_maker({
            'pinchrq':pinchrq                                           })

    # Challenge Request ##################################################
    if switch_dict['challengetrnrq']:
        challengerq = msg_maker({
            'userid'   :var_dict['userid']                              })
#            'ficertid' :var_dict['ficertid']                            })

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
        if switch_dict[item]:
            ofxbody_signonmsgsrqv1_dict[item] = ofxbody_signonmsgsrqv1_dict_0[item]

    ofxbody_signonmsgsrqv1_0 = msg_maker(ofxbody_signonmsgsrqv1_dict)
    ofxbody_signonmsgsrqv1 = msg_maker({'signonmsgsrqv1':ofxbody_signonmsgsrqv1_0})

    return ofxbody_signonmsgsrqv1
