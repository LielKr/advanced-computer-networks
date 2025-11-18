LENGTH_FIELD = 3


def create_msg(data):
    """
    יוצר הודעה עם שדה אורך:
    <LEN:3><DATA>
    """
    if data is None:
        data = ""

    data = data.strip()
    length = len(data)

    # הפיכת האורך למחרוזת של 3 ספרות
    length_str = str(length).zfill(LENGTH_FIELD)

    full_msg = length_str + data
    return full_msg.encode()


def get_message(current_socket):
    """
    מקבל הודעה שלמה לפי הפרוטוקול:
    קורא 3 תווים = אורך
    קורא בדיוק length תווים נוספים.
    """
    try:
        length_bytes = current_socket.recv(LENGTH_FIELD)
        if not length_bytes:
            return ""

        length_str = length_bytes.decode()
        if not length_str.isdigit():
            return ""

        msg_length = int(length_str)
        if msg_length == 0:
            return ""

        data = b''
        while len(data) < msg_length:  # קוראים בלולאה עד שיש לנו בדיוק msg_length bytes
            part = current_socket.recv(msg_length - len(data))
            if not part:
                return ""
            data += part

        return data.decode()

    except:
        return ""   # במקרה של שגיאה כלשהי (רשת, פירוק הודעה וכו') נחזיר ריק
