#!/usr/bin/env python

import socket

def get_format(tick):
    """
        The default format as set is #to#
        Your script can consist of any number of instructions
        It will only execute lines that start with a number, so you can leave text or non-numeric characters to explain the routes
    """
    pull = tick.split("to")
    a=int(pull[0])-1
    b=int(pull[1])-1
    return "%d %d\r\n"%(a,b)

def message_build(fileread):
    """
        Example usage: 3to5
            This would route output 3 to input 5
    """
    body = ""
    for line in intake:
        if line[0].isdigit():
            body+=get_format(line)
    head="VIDEO OUTPUT ROUTING:\r\n"
    message=head+body+"\r\n"
    return message

# The script uses an "instructions.txt" file in the same directory as the script for its routes.
intake = open('instructions.txt','r') 
body = ""
if not intake:
    quit()

routes=message_build(intake)
print routes
#your ip address
TCP_IP = '' 
#your port (9990 default)
TCP_PORT = 9990  
BUFFER_SIZE = 2048
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
s.connect((TCP_IP, TCP_PORT))
data = s.recv(BUFFER_SIZE)
while data.count("ACK") < 1:
    print "CYCLE"
    print "%s"%data
    s.send(routes)
    data=s.recv(BUFFER_SIZE) #This is just to discard the initial header, The server sends an ACK after the routing is done.
    data=s.recv(BUFFER_SIZE)
    print data.count("ACK")
    if data.count("ACK") >= 1:
        print "ACK"
        break
intake.close()
s.close()
