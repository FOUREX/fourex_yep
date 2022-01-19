import socket
import threading
from ast import literal_eval
from sys import exit


class Client():
    def __init__(self) -> None:
        self.HOST = "192.168.1.106" # input("Ip: ")
        self.PORT = 9999 # int(input("Port: "))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.name = input("Введите свой никнейм: ")
        self.connect()
        self.connected = False
        
        
        
    
    
    def connect(self):
        if not self.connect is False:
            to_conn = {
                "action_type": "system",
                "action": "connect",
                "name": self.name
            }
            self.send(to_conn)
            try:
                print("[System] Отправка запроса на сервер")
                print("[System] Ожидание ответа от сервера...")
                self.sock.settimeout(100.0)
                data = literal_eval(self.sock.recv(2048).decode("utf-8"))
                
                if data["status"] == "allowed":
                    self.connected = self.HOST, self.PORT
                    print("[System] Сервер принял запрос на подключение")
                    t1 = threading.Thread(target=self.start)
                    t2 = threading.Thread(target=self.recive_message)
                    
                    t1.start()
                    t2.start()
                else:
                    print(data["reason"])
            except Exception as e:
                print(e)
                print("[System] Сервер не отвечает")
    
        
    def send(self, to_send):
        self.sock.sendto(bytes(str(to_send), "utf-8"), (self.HOST, self.PORT))
        
    
    def recive_message(self):
        while True:
            try:
                server_data = literal_eval(self.sock.recv(2048).decode("utf-8"))
                if server_data:
                    if not server_data["name"] == self.name:
                        print(f"[{server_data['name']}] {server_data['message']}")
            except Exception as e:
                pass
    
    
    def start(self):
        while True:
            data = input()
            if data != "STOP":
                to_send = {
                    "action_type": "player",
                    "player": self.name,
                    "action": "message",
                    "message": data
                }
                self.send(to_send)
            else:
                exit
            

if __name__ == "__main__":
    client = Client()