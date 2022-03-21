
import socket
import requests.packages.urllib3.util.connection as urllib3_conn

# 强制使用IPv4
urllib3_conn.allowed_gai_family = lambda: socket.AF_INET
