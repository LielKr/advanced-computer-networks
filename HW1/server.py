import socket
import select
import protocol

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5555


def handle_client_request(sock, sockets_names, names_sockets, blocks, data):
    """
    מטפל בפקודה של לקוח.
    מחזיר רשימת (socket, message_to_send)
    """
    responses = []

    data = data.strip()
    if data == "":
        return responses

    parts = data.split(" ", 2)  # ["MSG", "B", "hello there"]
    cmd = parts[0]

    sender_name = sockets_names.get(sock, None)

    #  COMMAND=NAME
    if cmd == "NAME":
        if len(parts) < 2:
            responses.append((sock, "ERROR No name given"))
            return responses

        new_name = parts[1].strip()

        # חוקי/לא חוקי
        if " " in new_name or new_name == "" or new_name.upper() == "BROADCAST":
            responses.append((sock, "ERROR Illegal name"))
            return responses

        if new_name in names_sockets:
            responses.append((sock, "ERROR Name already taken"))
            return responses

        if sender_name is not None:
            responses.append((sock, "ERROR You already have a name"))
            return responses

        # רישום השם
        sockets_names[sock] = new_name
        names_sockets[new_name] = sock
        blocks.setdefault(new_name, set())

        responses.append((sock, f"HELLO {new_name}"))
        return responses

    # כל הפקודות הבאות מחייבות שם מוגדר
    if sender_name is None:
        responses.append((sock, "ERROR You must set a name first"))
        return responses

    #  COMMAND= GET_NAMES
    if cmd == "GET_NAMES":
        names = ", ".join(sorted(names_sockets.keys()))
        responses.append((sock, f"NAMES {names}"))
        return responses

    #  COMMAND= MSG
    if cmd == "MSG":
        if len(parts) < 3:
            responses.append((sock, "ERROR Usage: MSG <name/BROADCAST> <msg>"))
            return responses

        target = parts[1]
        msg_text = parts[2].strip()

        if msg_text == "":
            responses.append((sock, "ERROR Empty message"))
            return responses

        # ---- Broadcast ----
        if target.upper() == "BROADCAST":
            for name, client_sock in names_sockets.items():
                if name == sender_name:
                    continue
                if sender_name in blocks.get(name, set()):
                    continue
                responses.append((client_sock, f"{sender_name} sent {msg_text}"))

            responses.append((sock, "MSG to BROADCAST sent"))
            return responses

        # ---- שליחה ללקוח ספציפי ----
        if target not in names_sockets:
            responses.append((sock, "ERROR No such client"))
            return responses

        dest_socket = names_sockets[target]

        # בדיקת חסימה
        if sender_name in blocks.get(target, set()):
            responses.append((sock, f"ERROR {target} blocked you"))
            return responses

        responses.append((dest_socket, f"{sender_name} sent {msg_text}"))
        responses.append((sock, f"MSG to {target} sent"))  # לא חייב..
        return responses

    #  COMMAND= BLOCK
    if cmd == "BLOCK":
        if len(parts) < 2:
            responses.append((sock, "ERROR Missing name"))
            return responses

        target_name = parts[1]
        if target_name == sender_name:
            responses.append((sock, "ERROR Cannot block yourself"))
            return responses

        blocks.setdefault(sender_name, set()).add(target_name)
        responses.append((sock, f"BLOCKED {target_name}"))
        return responses

    #  COMMAND= EXIT
    if cmd == "EXIT":
        responses.append((sock, "BYE"))
        return responses

    #  COMMAND= UNKNOWN
    responses.append((sock, "ERROR Unknown command"))
    return responses




def print_client_sockets(client_sockets):
    print("Clients:")
    for c in client_sockets:
        try:
            print("\t", c.getpeername())
        except:
            pass


def main():
    print("server is up")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Listening for clients...")

    client_sockets = []
    messages_to_send = []

    clients_names = {}     # name  -> socket
    sockets_names = {}     # socket -> name
    blocks = {}            # name -> set of blocked names

    while True:
        read_list = client_sockets + [server_socket]
        ready_to_read, ready_to_write, in_error = select.select(read_list, client_sockets, [])

        #                 READ SECTION

        for current_socket in ready_to_read:

            # חיבור חדש
            if current_socket is server_socket:
                client_socket, client_address = server_socket.accept()
                print("Client joined!\n", client_address)
                client_sockets.append(client_socket)
                print_client_sockets(client_sockets)

            # הודעה מלקוח קיים
            else:
                print("Data from client\n")
                data = protocol.get_message(current_socket)


                # לקוח התנתק

                if data == "":
                    print("Connection closed\n")

                    # למצוא את השם של הלקוח שהתנתק
                    sender_name = None
                    for name, sock in clients_names.items():
                        if sock == current_socket:
                            sender_name = name
                            break

                    # למחוק אותו משני המילונים
                    if sender_name:
                        clients_names.pop(sender_name, None)
                        blocks.pop(sender_name, None)

                        for bset in blocks.values():
                            bset.discard(sender_name)

                    if current_socket in sockets_names:
                        sockets_names.pop(current_socket, None)

                    # להסיר מהרשימות ולסגור
                    if current_socket in client_sockets:
                        client_sockets.remove(current_socket)

                    current_socket.close()

                # פקודה תקינה לטפל בה

                else:
                    print(data)

                    responses = handle_client_request(
                        current_socket,  # socket of sender
                        sockets_names,   # socket -> name
                        clients_names,   # name -> socket
                        blocks,          # blocks dict
                        data             # command text
                    )

                    # הוספת כל ההודעות לתור השליחה
                    for dest_socket, response in responses:
                        messages_to_send.append((dest_socket, response))

        #                 WRITE SECTION

        for dest_socket, msg in messages_to_send[:]:
            if dest_socket in ready_to_write:
                try:
                    full_msg = protocol.create_msg(msg)
                    dest_socket.send(full_msg)
                except:
                    # ...אם יש תקלה נסגור את הסוקט
                    if dest_socket in client_sockets:
                        client_sockets.remove(dest_socket)

                # להסיר מהרשימה אחרי שליחה
                messages_to_send.remove((dest_socket, msg))


if __name__ == '__main__':
    main()
