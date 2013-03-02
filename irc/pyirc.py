import sys
import socket
import string
import threading

class IRC:
    def __init__(self, nick):
        self.nick = nick

    def connect(self, host, port, channel):
        self.host = host
        self.port = port
        self.channel = channel

        s=socket.socket()
        s.connect((self.host, self.port))
        s.send("NICK %s\r\n" % self.nick)
        s.send("USER %s %s bla :%s\r\n" % (self.nick,
                        self.host, self.nick))
        self.socket = s
        self.running = True
        self.t = threading.Thread(target=self.main)
        self.t.start()

    def send(self, msg):
        msg = u"PRIVMSG #%s :%s\r\n" % (self.channel, msg)
        self.socket.send(msg.encode('utf8'))

    def msg(self, nick, msg):
        print msg

    def disconnect(self):
        self.running = False
        self.socket.send("QUIT\r\n")

    def main(self):
        s = self.socket
        readbuffer = ''
        while self.running:
            readbuffer = readbuffer + s.recv(1024)
            temp = string.split(readbuffer, "\n")
            readbuffer = temp.pop()

            for line in temp:
                line = string.rstrip(line)
                line = string.split(line)

                if line[-1] == ':+iwx':
                    s.send("JOIN #%s\r\n" % self.channel)
                elif line[0] == "PING":
                    s.send("PONG %s\r\n" % line[1])
                elif 'PRIVMSG' in line:
                    nick = line[0].split('!')[0][1:]
                    msg = ' '.join(line[3:])[1:]
                    self.msg(nick, msg)
