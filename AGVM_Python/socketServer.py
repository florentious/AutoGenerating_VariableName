import socketserver, sys
from pprint import pprint
import json

from utils import option
from utils.convert import convert_File
from model.model import model_load

opt = option.Options()
IP = opt.host_ip
PORT = int(opt.host_port)
py2java_path = opt.py2java_path
model = model_load()


class SingleTCPHandler(socketserver.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."

    def handle(self):
        # self.request is the client connection
        data = self.request.recv(1024)  # clip input at 1Kb
        text = data.decode('utf-8')
        # pprint(json.loads(text))

        inObj = json.loads(text)
        # input check
        pprint(inObj)

        isSuccess = False
        output_path = ""
        try :
            isSuccess, output_path = convert_File(input_path=py2java_path+inObj['path'], output_path=py2java_path+'data/convert', model=model, isUseDict=inObj['isUse'],useType=inObj['model'])
        except Exception as ex:
            print(ex)

        outObj = {
            "status": isSuccess,
            "output_path": output_path
        }
        pprint('python status : '+str(isSuccess))


        self.request.send(bytes(json.dumps(outObj), 'UTF-8'))
        self.request.close()


class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    # Ctrl-C will cleanly kill all spawned threads
    daemon_threads = True
    # much faster rebinding
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


if __name__ == "__main__":
    # dl = model load

    server = SimpleServer((IP, PORT), SingleTCPHandler)
    # terminate with Ctrl-C
    print('Server On')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Server Down')
        sys.exit(0)