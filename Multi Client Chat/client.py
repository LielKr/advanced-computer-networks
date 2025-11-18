import socket
import select
import msvcrt
import protocol

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))

    print("\nPlease Enter Command!\n")
    print("options:")
    print("NAME <name>")
    print("GET_NAMES")
    print("MSG <name/BROADCAST> <msg>")
    print("BLOCK <name>")
    print("EXIT\n")

    buffer = ""  # מה שהמשתמש כותב כרגע
    running = True

    while running:
        rlist, wlist, xlist = select.select([sock], [], [], 0.1)

        #  הודעה מהשרת
        if sock in rlist:
            data = protocol.get_message(sock)
            if data == "":
                print("\nServer disconnected.")
                break
            print("\n" + data)

        #  קלט משתמש
        if msvcrt.kbhit():
            ch = msvcrt.getch()

            if ch in (b"\r", b"\n"):
                # שליחת ההודעה
                if buffer.strip():
                    msg = buffer.strip()
                    sock.send(protocol.create_msg(msg))
                    if msg == "EXIT":     # אם המשתמש כתב EXIT  נסגור את הלקוח
                        running = False

                buffer = ""
                print("")

            elif ch == b"\x08":
                # backspace
                if len(buffer) > 0:
                    buffer = buffer[:-1]
                    print("\b \b", end="", flush=True)

            else:
                try:
                    c = ch.decode()
                    buffer += c
                    print(c, end="", flush=True)
                except:
                    pass

    # כשהלופ נגמר סוגרים את הסוקט
    sock.close()
    print("Client closed.")


if __name__ == "__main__":
    main()
