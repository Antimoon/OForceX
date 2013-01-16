#!/usr/bin/python
#
# oforcex_utils.py
#
# A portion of OForceX
# Written by Antimoon
#

try:
    import urlparse
    import ssl
    import socket
    import datetime
except ImportError, e:
    print '[!] Error while importing: %s' % e

def trnuid_gen():
    '''Generates a random string with acceptable formatting for a UID'''
    i = 0

    trnuid = ''.join(random.choice('abcdef1234567890') for a in range(8))+'-'

    while i < 3:
        trnuid += ''.join(random.choice('abcdef1234567890') for a in range(4))+'-'
        i+=1

    trnuid += ''.join(random.choice('abcdef1234567890') for a in range(12))

    return trnuid

def tag_maker(tagname, content=''):
    '''Builds an OFX compliant tag
    Accepts 2 strings as input and returns 1 string as output'''
    tagname = str(tagname).upper()
    built   = '<%s>%s</%s>\r\n' % (tagname, content, tagname)

    return built

def msg_maker(msgdict, text=True):
    '''Builds an OFX message set
    Accepts a dictionary and a string as input, returns a string
    or list as output.'''
    outlist = []

    for key in msgdict.keys():
        outlist.append(tag_maker(key, msgdict[key]))

    if text == True:
        outstring = ''.join(outlist)
        return outstring

    else:
        return outlist

def url_parse(string_url):
    u = urlparse.urlsplit(string_url)
    return {'scheme' :u.scheme,
            'host'   :u.netloc,
            'query'  :u.query,
            'path'   :u.path}

def http_request(host, data, ssl=True, port=443, l=4):
    '''Simple Sockets connection script, modify l for
    response data length'''
    try:
        hostip = socket.gethostbyname(host)
    except:
        hostip = host

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if ssl == True:
        try:
            s = ssl.wrap_socket(s)
            connect = s.connect((hostip, port))
        except Exception, e:
            print '[!] Error: %s' % e
    else:
        try:
            connect = s.connect((hostip, port))
        except Exception, e:
            print '[!] Error: %s' % e

    s.send(data)
    response = str(s.recv(1024*l))
    s.close()

    return response

def oforcex_log(messagehead='', messagebody='', logfile='', warning=False):
    '''Logging function'''
    #global logging
    if logfile == '':
        return 0
    else:

        if warning == False:
            x = '[*] '
        else:
            x = '[!] '

        try:
            file = open(logfile, "a")
            file.write('%s%s\n' % (x,messagehead))
            file.write('%s\n' % messagebody)
            file.close()
        except Exception, e:
            print '[!] %s' % e

        return 1

def dateformat(date=None):
    '''Format dates for use with OFX'''
    if date != None:
        out = date.strftime('%Y%m%d')
    else:
        out = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    return out

def show_help():
    # TODO
    print 'Usage: %s -u <URL> -l <LOGFILE> -b <ATTACKTYPE> -L <ATTACKLENGTH>'
    print ''
    print 'Accepted Attack Types:'
    print '\tuserkey\t\tHarvest OFX Session IDs'
    # Reserved for commandline functionality
    sys.exit(0)
