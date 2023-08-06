import socket, threading, sys, getpass, webbrowser, random
from optparse import OptionParser

class Client:
    def __init__(self, ip, port, nickname, admin_mode):
        self.admin_mode = admin_mode
        self.nickname = nickname
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        self.send_nickname_to_sever()
        self.is_running = True

    def send_nickname_to_sever(self):
        self.connection.send((self.nickname).encode())

    def send_message(self, message):
        try:
            self.connection.send(message.encode())
        except:
            exit()

    def exit_room(self):
        self.connection.close()
        self.is_running = False

    def open_url(self, url):
        webbrowser.open(url)

    def handle_admin_command(self, command):
        if self.admin_mode == True:
            self.send_message(command)
        else:
            print(self.convert_color("[-] Only admin can use this command", style="ENDC"))

    def convert_color(self, string, style):
        colors = {
        "WARNING": '\033[93m',
        "FAIL": '\033[91m',
        "ENDC": '\033[0m',
        "BOLD": '\033[1m'
        }
        return colors[style] + string

    def get_style_color(self):
        color_list = ["WARNING", "FAIL", "ENDC", "BOLD"]
        return random.choice(color_list)

    def out_sever(self):
        print(self.convert_color("[-] Admin closes the sever", style="FAIL"))
        content = f"/exit {self.nickname}"
        self.send_message(content)
        self.exit_room()
        print(self.convert_color("[+] Press 'Ctrl + C' or 'Enter' to exit", style="ENDC"))

    def recieve_message(self):
        while self.is_running:
            try:
                response = self.connection.recv(1024).decode()
                if not response and self.connection:
                    print("[-] Sever is not available")
                    break
                elif "admin/open-url" in response and self.admin_mode is not True:
                    url = response.split(" ")[1]
                    self.open_url(url)
                elif response == "/close-sever":
                    self.out_sever()
                else:
                    print(response)
            except:
                try:
                    print(self.convert_color("[-] Connection is closed", style="FAIL"))
                    self.connection.close()
                    break
                except:
                    sys.exit()
    
    def process_sending_message(self):
        while self.is_running:
            content = input()
            if content == "/exit":
                content = f"/exit {self.nickname}"
                self.send_message(content)
                self.exit_room()
                break
            elif content == "/ls":
                self.send_message(content)
            elif "/open-url" in content:
                self.handle_admin_command(content)
            elif "/close-sever" == content:
                self.handle_admin_command(content)

            else:
                content = self.convert_color(f"({self.nickname}): {content}", style="ENDC")
                self.send_message(content)

    def start(self):
        send_threading = threading.Thread(target=self.process_sending_message)
        send_threading.start()

        recieve_threading = threading.Thread(target=self.recieve_message)
        recieve_threading.start()

        send_threading.join()
        recieve_threading.join()

def main():
    def return_error(parser, options):
        if not options.port:
            parser.error("[-] Port not found")
        if not options.nickname:
            parser.error("[-] Nickname not found")

    def return_arguments():
        parser = OptionParser()
        parser.add_option("-p", "--port", dest="port", help="Connect to sever through this port")
        parser.add_option("-n", "--nickname", dest="nickname", help="Choose your name or a nickname")
        parser.add_option("-r", "--root", dest="root", help="Use root [on/off] to become the admin")
        (options, arguments) = parser.parse_args()
        return_error(parser, options)
        return options

    options = return_arguments()

    ip = "0.tcp.ap.ngrok.io"
    port = int(options.port)
    nickname = options.nickname

    if options.root == "on":
        keypass = getpass.getpass("Password: ")
        if keypass == "6626":
            print("[+] You're now the admin")
            admin_mode = True
        else:
            print("[-] Password is wrong!")
            admin_mode = False
    else:
        admin_mode = False

    try:
        client = Client(ip=ip, port=port, nickname=nickname, admin_mode=admin_mode)
        client.start()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    main()