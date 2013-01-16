#!/usr/bin/python
#
# bankmsgs.py
#
# A portion of OForceX
# Written by Antimoon
#
######################################################################
# BANKMSGSRQV1 #######################################################
######################################################################

def build(
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
