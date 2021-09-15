import logging
import signal
import socket
import sys
import threading
from time import strftime, localtime

import utils


class Server:
    """ The server class """

    def __init__(self, config):
        # Shutdown on Ctrl+C
        signal.signal(signal.SIGINT, self.shutdown)

        # Save config in server
        self.config = config

        # Create a TCP socket
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Re-use the socket
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket a public host, and a port
        self.serverSocket.bind((config['HOST_NAME'], config['BIND_PORT']))

        self.serverSocket.listen(10)    # Become a server socket
        self.__clients = {}
        self.__client_no = 1

    def log(self, log_level, client, msg):
        """ Log the messages to appropriate place """
        LoggerDict = {
            'CurrentTime': strftime("%a, %d %b %Y %X", localtime()),
            'ThreadName': threading.currentThread().getName()
        }
        if client == -1:       # Main Thread
            formatedMSG = msg
        else:                  # Child threads or Request Threads
            formatedMSG = '{0}:{1} {2}'.format(client[0], client[1], msg)
        logging.debug('%s', utils.colorizeLog(self.config['COLORED_LOGGING'], log_level, formatedMSG), extra=LoggerDict)

    def shutdown(self, signum, frame):
        """ Handle the exiting server. Clean all traces """

        self.log("WARNING", -1, 'Shutting down gracefully...')
        main_thread = threading.currentThread()        # Wait for all clients to exit
        for t in threading.enumerate():
            if t is main_thread:
                continue
            self.log("FAIL", -1, 'joining ' + t.getName())
            t.join()
        self.serverSocket.close()
        sys.exit(0)

    def listen_for_client(self):
        """ Wait for clients to connect """
        while True:
            # Establish the connection
            (clientSocket, client_address) = self.serverSocket.accept()

            d = threading.Thread(name=self._getClientName(client_address), target=self.proxy_thread,
                                 args=(clientSocket, client_address))
            d.setDaemon(True)
            d.start()

    def _getClientName(self, cli_addr):
        """ Return the clientName with appropriate number.
        If already an old client then get the no from map, else
        assign a new number.
        """
        lock = threading.Lock()
        lock.acquire()
        ClientAddr = cli_addr[0]
        if ClientAddr in self.__clients:
            lock.release()
            return "Client-" + str(self.__clients[ClientAddr])

        self.__clients[ClientAddr] = self.__client_no
        self.__client_no += 1
        lock.release()
        return "Client-" + str(self.__clients[ClientAddr])

    def proxy_thread(self, conn, client_addr):
        """
        *******************************************
        ************ PROXY_THREAD FUNC ************
          A thread to handle request from browser
        *******************************************
        """

        # Get the request from browser
        # request = 'GET http://wttr.in/Grenoble HTTP/1.1\r\n ...'
        request = conn.recv(self.config['MAX_REQUEST_LEN'])
        print(request)
        if not request:                 # if request is in the cache ?
            conn.close()
            return

        # Parse the first line
        first_line = request.decode().split('\n')[0]

        # Get url
        url = first_line.split(' ')[1]
        http_pos = url.find("://")      # find pos of ://
        if http_pos == -1:
            temp = url
        else:
            temp = url[http_pos+3:]     # get the rest of url

        port_pos = temp.find(":")       # find the port pos if any

        # Find end of web server
        webserver_pos = temp.find("/")
        if webserver_pos == -1:
            webserver_pos = len(temp)

        webserver = ""
        port = -1
        if port_pos == -1 or webserver_pos < port_pos:
            # default port
            port = 80
            webserver = temp[:webserver_pos]
        else:
            # specific port
            port = int((temp[port_pos+1:])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        try:
            # Send original request to the real server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.config['CONNECTION_TIMEOUT'])
            s.connect((webserver, port))
            s.sendall(request)

            # Redirect the server's response the the client
            while True:
                # Receive data from the server
                data = s.recv(self.config['MAX_REQUEST_LEN'])

                if len(data) > 0:
                    conn.send(data)     # send to browser/client
                else:
                    break
            s.close()
            conn.close()
        except socket.error as error_msg:
            self.log("ERROR", client_addr, error_msg)
            if s:
                s.close()
            if conn:
                conn.close()
            self.log("WARNING", client_addr, "Peer Reset: " + first_line)


if __name__ == "__main__":
    config = utils.loadConfig('settings.conf')
    server = Server(config)
    server.listen_for_client()


