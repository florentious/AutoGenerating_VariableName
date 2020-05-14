import socketserver, sys
from pprint import pprint
import json

from AMVN_alpha.utils import option

opt = option.Options()
IP = opt.host_ip
PORT = opt.host_port


class SingleTCPHandler(socketserver.BaseRequestHandler):
    "One instance per connection.  Override handle(self) to customize action."

    def handle(self):
        # self.request is the client connection
        data = self.request.recv(1024)  # clip input at 1Kb
        text = data.decode('utf-8')
        # pprint(json.loads(text))

        inObj = json.loads(text)

        # json_data : input_path, isUseInputDict, inputDict_path, isUseDefaultDict
        #         for key in json.loads(text):
        #             pprint(json.loads(text)[key])

        output = {
            "status": True,
            "output_path": "output/test.xlsx",
            "newDict_path": "newDict.xlsx"
        }

        self.request.send(bytes(json.dumps(output), 'UTF-8'))
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