
class UsersInfo():
    def __init__(self):
        self.info = {
            1000 : {
                "Username" : "gelanMar",
                "Password" : "Mypassis123pizz@",
                "To-Do-List" : [
                    "Buy some groceries",
                    "Train calisthenics"
                ],
                "Checked-List" : [
                    "Buy some groceries"
                ]
            }
        }
        self.taken_user = set()
        self.deleted_List = []
        