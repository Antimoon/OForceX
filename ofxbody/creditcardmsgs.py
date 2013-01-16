#!/usr/bin/python
#
# creditcardmsgs.py
#
# A portion of OForceX
# Written by Antimoon
#
######################################################################
# CREDITCARDMSGSRQV1 #################################################
######################################################################
def build(
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
