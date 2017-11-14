class errHandle:
    def __init__(self):
        return

    def delete_err(self,code):
        if code == 0:
            return "Message sent successfully?"
        elif code == 1:
            return "Error in deleting message?"
        elif code == 2:
            return "File does not exist?"


    def send_err(self,code):
        if code == 0:
            return "Message sent successfully?"
        elif code == 1:
            return "Error in sending message?"
        elif code == 2:
            return "File does not exist?"
        elif code == 3:
            return "This users inbox is full?"

    def update_err(self,code):
        if code== 0:
            return "update complete?"
        if code ==1:
            return "update failed?"

    def read_err(self,code):
        if code == 1:
            return "could not read messages?"
        if code == 2:
            return "could not open file?"

    def verify_err(self,code):
        if code == 1:
            return "file read error?"
        if code == 2:
            return "file open error?"

    def admin_err(self,code):
        if code == 1:
            return "could not read from file?"
        if code == 2:
            return "could not open file?"

    def duplicate_err(self,code):
        if code == 0:
            return "Account created successfully?"
        if code ==1:
            return "could not read from file?"
        if code ==2:
            return "could not open file?"
        if code ==3:
            return "username already exists?"
