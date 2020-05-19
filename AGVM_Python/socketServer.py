import socketserver, sys
from pprint import pprint
import json

from utils import option
from utils.convert import convert_File

opt = option.Options()
IP = opt.host_ip
PORT = int(opt.host_port)

py2java_path = opt.py2java_path


class SingleTCPHandler(socketserver.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."

    def handle(self):
        # self.request is the client connection
        data = self.request.recv(1024)  # clip input at 1Kb
        text = data.decode('utf-8')
        # pprint(json.loads(text))

        inObj = json.loads(text)

        # json_data : isUse, model, path, type
        # for key in json.loads(text):
        #     pprint(json.loads(text)[key])
        pprint(inObj['path'])

        isSuccess, output_path = convert_File(input_path=py2java_path+inObj['path'], output_path=py2java_path+'data/convert', isUseDict=inObj['isUse'],useType=inObj['model'])

        outObj = {
            "status": isSuccess,
            "output_path": output_path
        }

        pprint(outObj)

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
    server = SimpleServer((IP, PORT), SingleTCPHandler)
    # terminate with Ctrl-C
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)