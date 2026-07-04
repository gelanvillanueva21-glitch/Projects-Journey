import Sorting

class Account:
    """
    This class is purpose is to handle data.
    A Passwords, Usernames, and Social.
    Using dictionary as a storing data.
    """
    def __init__(self):
        self.info_Account = {}
        self.File_Info = open('/Users/user/OneDrive/Desktop/ProgrammingLanguages/Python.Language/PythonPractice2/AccountSystem/Accounts.txt', 'a+')
        self.Open_File_Once = True 


    def file_handling(self):
        if self.Open_File_Once:
            try:
                self.File_Info.seek(0)
                for info in self.File_Info:
                    clean = info.strip()
                    if clean:
                        acc_Info = clean.split(", ")
                        if len(acc_Info) == 3:
                            social = acc_Info[0]
                            username = acc_Info[1]
                            password = acc_Info[2]
                            if social in self.info_Account:
                                self.info_Account[social].append({"Username": username,
                                                                "Password": password})
                            else:
                                self.info_Account[social] = [{"Username": username,
                                                            "Password": password}]
                            self.Open_File_Once = False
            except FileNotFoundError:
                print("\nNo existing file found\n")
        else:
            return

    def display_info(self):
        sort.Array_List()
        self.file_handling()
        for value, info in self.info_Account.items():
            print(f"{value}:")
            for index in info:
                User = index.get("Username", "N/A")
                Pass = index.get("Password", "N/A")
                print(f"    [Username: {User}]-[Password: {Pass}]")
        enter = input("\nPress Enter To Return To The Menu...\n")
        return


    def create_account(self):
        """
        In this function, when this called, its creating an account
        Then store it inside the Account.txt file
        """
        sort.Array_List()
        self.file_handling()
        Social = input("Enter Social Media: ")
        while True:
            Username = input("Create Username: ")
            if len(Username) >= 8:
                if Social in self.info_Account:
                    for account in self.info_Account[Social]:
                        if Username == account.get("Username"):
                            print("\nUsername already Exist\n")
                            return
                Password = input("Create Password: ")
                if len(Password) >= 8:
                    if Social in self.info_Account:
                        self.info_Account[Social].append({"Username": Username, 
                                                        "Password": Password})
                    else:
                        self.info_Account[Social] = [{"Username": Username, 
                                                "Password": Password}]
                    self.File_Info.write(f"{Social}, {Username}, {Password}\n")
                    break
                else:
                    print("\nMust atleast 8 Characters\n")
            else:
                print("\nMust atleast 8 Characters\n")
        enter = input("\nPress Enter To Return To The Menu...\n")
        return


    def log_In(self):
        sort.Array_List()
        self.file_handling()
        Return_Value_And_Loop = True
        social = input("Enter Social: ")
        if social in self.info_Account:
            while Return_Value_And_Loop:
                user = input("Enter Username: ")
                for info in self.info_Account[social]:
                    for index in info:
                        User = index.get("Username", "N/A")
                        if user == User:
                            password = input("Enter Password: ")
                            for ydex in info:
                                Pass = ydex.get("Password", "N/A")
                                if password == Pass:
                                    Return_Value_And_Loop = False
                                    print("\nSuccessfully Login\n")
                            break
        else:
            print("\nSocial Media Not Found\n")
        enter = input("\nPress Enter To Return To The Menu...\n")
        if Return_Value_And_Loop is False:
            return True
        else:
            return None


    def delete_account(self):
        """
        This Function Delete An Account.
        Then Overwite It With Updated New Info.
        """
        sort.Array_List()
        self.file_handling()
        print("\nEnter Account You Want To Delete")
        Continue_Loop = True
        found = False
        while Continue_Loop:
            social = input("Enter Social Media: ")
            if social not in self.info_Account:
                print(f'{social} Not Found')
                continue
            user = input("Enter Username: ")
            for account in self.info_Account[social]:
                if user == account["Username"]:
                    self.info_Account[social].remove(account)
                    found = True
                    info_list = []
                    self.File_Info.seek(0)
                    for info in self.File_Info:
                        if user in info:
                            deleted = info.strip()
                            del_info = open('/Users/user/OneDrive/Desktop/ProgrammingLanguages/Python.Language/PythonPractice2/AccountSystem/deleted_info.txt', 'a')
                            del_info.write(f'{deleted}\n')
                            self.info_Account.pop(social)
                        else:
                            clean = info.strip()
                            row_list = clean.split(', ')
                            if len(row_list) == 3:
                                info_list.append(row_list)
                    rewrite_file = open('Accounts.txt', 'w')
                    for row in info_list:
                        for info in row:
                            if info == row[2]:
                                rewrite_file.write(info)
                            else:
                                rewrite_file.write(f"{info}, ")
                        rewrite_file.write("\n")
                    return f"\nSuccessfuly Deleted Account Username: {user}\n"
            if found is False:
                return f"\n{user} not Found\n"
        enter = input("\nPress Enter To Return To The Menu...\n")
        if enter == "":
            return


sort = Sorting.Sorting