# This script locks the server, disconnects you from the servers RDP session
# sending the session back to console so hamachi does not get disconnected

tscon 0 /dest:console
tscon 1 /dest:console
tscon 2 /dest:console
Rundll32.exe User32.dll,LockWorkStation
