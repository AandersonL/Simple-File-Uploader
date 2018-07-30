import cherrypy
from cherrypy import tools
import os, sys
import shutil

''' 
    TODO
    
    implement a simple sqlite db, api key system, divide code to utils

'''
RANDOM_LEN = 6
LOCAL_IP = None
API_KEY = None


def error_page_400(status, message, traceback, version):

    cherrypy.serving.response.headers['Content-Type'] = 'application/json'
    response = { "code": "400", "status": "Please verify if your file has 'file' as name" }
    return response

cherrypy.config.update({'error_page.400': error_page_400})


def log(msg):
    f = open("logs.txt", "a")
    f.write("\n\nReceived wrong request, headers: " + str(msg))
    f.close()

def parseRequest(request, api_key):
    print("Request: " + str(request))
    if ( "Api-Key" in request.keys() ):
        key = request['Api-Key']
        print("Key: " + key)
        if ( key != API_KEY ):
            log(request)
            return False
        else:
            return True
    else:
        log(request)
        return False

class Api(object):
    exposed = True
    def GET(self, file_name=None):
        if file_name == None or file_name[:2] in ['.', '..'] or file_name[:4] != "img_":
            log(cherrypy.request.headers)
            return "" 
        
        try:
            f = open("uploads/"+file_name, "rb")
            obj = f.read()
            f.close()
            cherrypy.serving.response.headers["Content-Type"] = 'application/octet-stream'
            return obj
        except Exception as e:
            return "error, no file"
    
    @tools.json_out()
    def POST(self, file=None):
        if (not parseRequest(cherrypy.request.headers, self.api_key)):
            return ""
    
        random_name = "img_"
        random_name += os.urandom(RANDOM_LEN).hex()
        url = "http://{}:8000/{}".format(LOCAL_IP, random_name)
        cherrypy.serving.response.headers['Content-Type'] = 'application/json'
        if file != None:
            if not os.path.exists('uploads'):
                os.mkdir('uploads')
            obj = open("uploads/"+random_name,"wb")
            shutil.copyfileobj(file.file, obj)
            obj.close()
            response = {
                "code": 200,
                "url": url
            }
            cherrypy.serving.response.headers['Content-Type'] = 'application/json'
            return response
        
        response = {
            "code": 500,
            "status": "Cant save file, file is Null" 
        }
        return response



if __name__ == '__main__':
    api_key = None
    ip = '0.0.0.0'

    if len(sys.argv) > 1:
        API_KEY = sys.argv[1] 
    conf = {
        'global': {
            'server.socket_host': ip,
            'server.socket_port': 8000,
            'environment': 'production',
            'log.screen': False,
            'show_tracebacks': False
        },
        '/': {
           'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        }
    }
    print("Starting api...")

    cherrypy.quickstart(Api(), '/', conf)
