import socketserver
from ast import literal_eval


HOST, PORT = "192.168.1.106", 9999
users = {}

class MyUDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = literal_eval((self.request[0].strip()).decode("utf-8"))
        socket = self.request[1]
        
        if data["action_type"] == "system":
            if data["action"] == "connect":
                if not str(data["name"]).lower() in users:
                    inp = input(f"[{self.client_address}] {data['name']}: Trying to connect [Y/n]?\n")
                    if str(inp).lower() == "y":
                        socket.sendto(b"{'action': 'connecting', 'status': 'allowed'}", self.client_address)
                        users.update({str(data["name"]).lower(): {"addr": self.client_address}})
                        print(users)
                    else: 
                        socket.sendto(b"{'action': 'connecting', 'status': 'denied', 'reason': ''}", self.client_address)
                else:
                    socket.sendto("{'action': 'connecting', 'status': 'denied', 'reason': 'Пользователь под этим ником уже присоединён к серверу'}".encode("utf-8"), self.client_address)
        else:
            print(f"[{data['player']}]: {data['message']}")
            #to_send1 = {}
            #for i in users:
            #    to_send2 = {
            #        "name": i,
            #        "message": data["message"]
            #    }
            #    to_send1.update(to_send2)
            
            for i in users:
                to_send = {
                    "name": data["player"],
                    "message": data["message"]
                }
                socket.sendto(bytes(str(to_send), "utf-8"), users[i]["addr"])

if __name__ == "__main__":
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()