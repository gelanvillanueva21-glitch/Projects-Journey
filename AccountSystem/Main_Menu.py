import Sorting
import Account_Data

def main():
    acc = Account_Data.Account()
    sort = Sorting.Sorting
    while True:
        print("\n\n_____ACCOUNTS_____\n" \
        "1. Log In\n" \
        "2. Create Account\n" \
        "3. Display Account\n" \
        "4. Delete Account\n" \
        "5. Exit")

        try:
            choice = int(input("> "))
            print("\n\n")
            if choice == 1:
                LogIn_Success = acc.log_In()
                if LogIn_Success is True:
                    pass
                else:
                    print("\nLog In Failed\n")
            elif choice == 2:
                acc.create_account()
            elif choice == 3:
                acc.display_info()
            elif choice == 4:
                print(acc.delete_account())
            elif choice == 5:
                sort.Array_List()
                break
        except ValueError:
            print("Error Occur On Input!")

main()