import socket


def ds_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = "localhost"
    port = 1977
    client.connect((ip, port))

    try:
        while True:
            # get input message from user and send it to the server
            msg = input("Enter message: ")
            client.send(msg.encode()[:1024])

            # receive message from the server
            response = client.recv(1024)
            response = response.decode()

            # if server sent us "closed" in the payload, we break out of
            # the loop and close our socket
            print(f"Received: {response}")
            if response[:2] == "05":
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()
        print("Connection to server closed")


ds_client()
