#!/usr/bin/python
#
# headers.py
#
# A portion of OForceX
# Written by Antimoon
#

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
