from plyer import filechooser
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
import socket
import time


def server_loop(host, port, file):
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to the address and port
    server_socket.bind((host, int(port)))

    # Listen for incoming connections
    server_socket.listen(1)
    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print("Accepted connection from", client_address)

        try:
            while True:
                # Send an update to the client
                with open(file, 'r') as f:
                    file_data = f.read()
                    print(file_data)
                    client_socket.send(file_data.encode())

                # Wait for 1 second
                time.sleep(1)
        except KeyboardInterrupt:
            # Close the client connection when Ctrl+C is pressed
            client_socket.close()
            print("Server stopped.")
            break


KV = '''
BoxLayout:
    orientation: 'vertical'
    spacing: dp(10)
    padding: dp(20)

    MDTextField:
        id: ip_input
        hint_text: 'Enter IP address'
        helper_text: 'e.g., 192.168.1.1'
        helper_text_mode: 'on_focus'
        icon_right: 'lan'
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5}

    MDTextField:
        id: port_input
        hint_text: 'Enter port'
        helper_text: 'e.g., 8080'
        helper_text_mode: 'on_focus'
        icon_right: 'network'
        icon_right_color: app.theme_cls.primary_color
        pos_hint: {'center_x': 0.5}
    
    MDFlatButton:
        text: 'Choose File'
        pos_hint: {'center_x': 0.5}
        on_release: app.open_file()

    MDFlatButton:
        text: 'CONNECT'
        pos_hint: {'center_x': 0.5}
        on_release: app.on_connect(ip_input.text, port_input.text)
'''


class PyJniusServer(MDApp):
    file = None

    def build(self):
        return Builder.load_string(KV)

    def open_file(self):
        self.file = filechooser.open_file()[0]

    def on_connect(self, ip, port):
        server_loop(ip, port, self.file)


ServerApp = PyJniusServer()
ServerApp.run()
