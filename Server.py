#!/usr/bin/env python3
import select, socket, sys, threading
from Client import Client


MAXCLIENTS = 10

class Server:
    """This is really just a delegator that creates new clients. Once this is
    run you use PC.py to fire up new clients. Then this Server will initialize
    some stuff and start a new thread for each client that connects.
    """
    def __init__(self):
        self.host = ''
        self.port = 5015
        self.backlog = 5
        self.size = 1024
        self.server = None
        self.threads = []
        self.vclock = [0]*MAXCLIENTS
        self.nclients = 0

    def open_socket(self):
        """Try to open a socket."""
        try:
            # Create a new socket object.
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Bind the new socket to host and port.
            self.server.bind((self.host, self.port))

            # Listen for at most self.backlog connections.
            self.server.listen(self.backlog)

        except OSError as message:
        # except(socket.error, (value, message)):
            # If the socket is open, but an error occured then close it.
            if self.server:
                self.server.close()

            print("Could not open socket: ", message)
            sys.exit(1)

    def run(self):
        """Open a socket and adds clients to the queue."""
        self.open_socket()
        input = [self.server, sys.stdin]
        running = 1
        while running:
            # Select returns a subset of the lists that are passed to it. The
            # lists that are returned are lists of elements that are ready.
            inputready, outputready, exceptready = select.select(input, [], [])

            for s in inputready:
                if s == self.server:
                    # A readable server socket is ready to receive a connnection.
                    self.client, self.address = self.server.accept()
                    print('---------\n',self.address,'\n---------\n')

                    # Initialize a new client thread.
                    # I'm just passing the whole object here cux WTF.
                    c = Client(self)

                    # Run the thread.
                    c.start()

                    # Add the client to the queue.
                    self.threads.append(c)
                elif s == sys.stdin:
                    # Wait until each client thread terminates
                    junk = sys.stdin.readline()
                    running = 0

        self.server.close()

        for c in self.threads:
            print("Left it.")
            c.join()

if __name__ == '__main__':
    s = Server()
    s.run()
