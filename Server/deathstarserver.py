import socket
import threading
import random


def handle_client(client_socket, addr):
    flag1, flag2 = False, False
    countdown = -1
    errorcode = "00"
    try:
        while True:
            request = client_socket.recv(1024).decode("utf-8")
            print(f"Received: {request}")
            #Message code to initiate countdown
            if (len(request) == 4) and request[:2] == "01" and request[2:4] == "00":
                if flag1:
                    errorcode = "01"
                    break
                flag1 = True
                countdown = random.randint(5, 100)
                msg = f'{countdown:x}'.zfill(4)
            #Message code to count down by one
            elif request[:2] == "02" and request[2:4] == "00":
                countdown = countdown - 1
                if (len(request) <= 4) or (len(request) > 8) or int(request[4:8], 16) != countdown:
                    errorcode = "01"
                    break
                else:
                    msg = f'{countdown:x}'.zfill(4)
            #Message code to fire the laser
            elif (len(request) == 4) and request[:2] == "03" and request[2:4] == "00":
                if flag2:
                    errorcode = "01"
                    break
                flag2 = True
                msg = "Fired"
            #Message code to request the flag
            elif (len(request) == 4) and request[:2] == "04" and request[2:4] == "00":
                if flag1 and flag2:
                    msg = "assignment2{d3aThsT4r_f1r3d_g0oD_j0b}".zfill(40)
                else:
                    errorcode = "01"
                    break
            elif request[:2] == "05" and request[2:4] == "00":
                break
            else:
                errorcode = "02"
                break
            response = request[:2] + errorcode + msg
            client_socket.send(response.encode("utf-8"))
    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        client_socket.send(("05"+errorcode).encode("utf-8"))
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


def ds_server():
    ip = "localhost"
    port = 1977
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen()
        print(f"Listening on {ip}:{port}")

        while True:
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            # start a new thread to handle the client
            thread = threading.Thread(target=handle_client, args=(client_socket, addr,))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        #Throw because exception might be thrown and this safely closes the connection
        server.close()


ds_server()
