package Bank;
import java.util.*;

public class BankingSystem {


    public static void main(String[] args) throws InterruptedException, InputMismatchException {
        Scanner sc = new Scanner(System.in);
        AccMenu account = new AccMenu();     
        CheckingAccount check_Account = new CheckingAccount();
        SavingsAccount save_Account = new SavingsAccount();
        Loan loan = new Loan();
        int choice;

        while (true) {
            boolean login_Success = account.account_Menu(sc);
            if (login_Success == true) {
                System.out.println("\nSuccessfully LogIn\n");
                break;
            } else {
                return;
            }
        }
        try {
            while (true) {
                int choose;
                System.out.println("_____MENU_____");
                System.out.println("\n1. Check Account\n2. Savings Account\n3. Loan\n4. Exit");
                System.out.print("> ");
                choice = sc.nextInt();

                    if (choice == 1) {
                        do {
                            System.out.println("\n_____ACCOUNT_____");
                            System.out.println("1. Balance\n2. Deposit\n3. Withdrawr\n4. Return");
                            System.out.print("> ");
                            choose = sc.nextInt();

                                switch (choose) {
                                    case 1:
                                        check_Account.printInfo(sc);
                                        break;
                                    case 2:
                                        System.out.println("\n_____DEPOSIT_____\nEnter Ammount To Deposit");
                                        System.out.print("> ");
                                        int deposit = sc.nextInt();
                                        check_Account.deposit(deposit, sc);
                                        break;
                                    case 3:
                                        System.out.println("\n_____WITHDRAW_____\nEnter Amount To Withdraw");
                                        System.out.print("> ");
                                        int withdraw = sc.nextInt();
                                        check_Account.withdraw(withdraw, sc);
                                        break;
                                    case 4:
                                        break;
                                    default:
                                        System.out.println("\nInput Not Found\n"); 
                                        Thread.sleep(1000);
                                }
                            } while (choose != 4);
                    } else if (choice == 2) {
                        do {
                            System.out.println("\n_____SAVINGS_____");
                            System.out.println("1. Balance\n2. Deposit\n3. Withdraw\n4. Return");
                            System.out.print("> ");
                            choose = sc.nextInt();

                                switch (choose) {
                                    case 1:
                                        save_Account.printInfo(sc);
                                        break;
                                    case 2:
                                        System.out.println("\n_____SAVINGS ACCOUNT_____\nEnter Amount To Deposit To Your Account");
                                        System.out.print("> ");
                                        int deposit = sc.nextInt();
                                        save_Account.deposit(deposit, sc);
                                        break;
                                    case 3:
                                        System.out.println("\n_____SAVINGS ACCOUNT_____\nEnter Amount To Withdraw To Your Account");
                                        System.out.print("> ");
                                        int withdraw = sc.nextInt();
                                        save_Account.withdraw(withdraw, sc);
                                        break;
                                    case 4:
                                        break;
                                    default:
                                        System.out.println("\nInput Not Found\n");
                                        Thread.sleep(1000);

                                }
                        } while (choose != 4);
                    } else if (choice == 3) {
                        do {
                            System.out.println("\n_____LOAN_____");
                            System.out.println("1. Loan Balance\n2. Loan\n3. Pay Loan\n4. Return");
                            System.out.print("> ");
                            choose = sc.nextInt();

                                switch (choose) {
                                    case 1:
                                        loan.loan_Info(sc);
                                        break;
                                    case 2:
                                        System.out.println("\n_____LOAN_____\nEnter Loan Amount");
                                        System.out.print("> ");
                                        int loan_withdraw = sc.nextInt();
                                        loan.withdraw(loan_withdraw, sc);
                                        break;
                                    case 3:
                                        System.out.println("\n_____PAY LOAN_____\nEnter Amount To Pay Loan");
                                        System.out.print("> ");
                                        int pay_loan = sc.nextInt();
                                        loan.deposit(pay_loan, sc);
                                        break;
                                    case 4:
                                        break;
                                    default:
                                        System.out.println("\nInput Not Found\n");
                                        Thread.sleep(1000);

                                }
                        } while (choose != 4);
                    } else if (choice == 4) {
                        break;
                    } else {
                        System.out.println("\nNumber: " + choice + " Not Found\n");
                        Thread.sleep(1000);
                    }
                }

        } catch (InputMismatchException e) {
            System.out.println("Wrong Input!!");
        }
        

        sc.close();
    }

}

class Loan implements Transactable{

    final private int maximum_loan = 100000;
    private int loan_Amount;
    private int loan_Balance;

    public void loan_Info(Scanner sc) {
        System.out.println("\nLoan Balance: " + loan_Balance + "\nSum Of Loan Amount: " + loan_Amount);
        System.out.println("Enter To Return To The Menu...");
        sc.nextLine();
        sc.nextLine();
    }

    public void deposit(int pay_loan, Scanner sc) {
        if (pay_loan < 0) {
            System.out.println("YOU CAN'T PAY NEGATIVE\n\n");
        } else {
            int amount = loan_Balance - pay_loan;
            if (amount < 0) {
                System.out.println("Pay Enough To Your Loan\n\n");
            } else {
                loan_Balance -= pay_loan;
                System.out.println("You Successfully Paid " + pay_loan + "\n\n");
            }
            System.out.println("Enter To Return To The Menu...");
            sc.nextLine();
            sc.nextLine();
        }
    }
    public void withdraw(int loan_withdraw, Scanner sc) {
        if (loan_withdraw < 0) {
            System.out.println("YOU CAN'T LOAN NEGATIVE\n\n");
        } else {
            if (loan_withdraw > maximum_loan) {
                System.out.println("Maximum Loan!!\n\n");
            } else {
                int amount = loan_Balance + loan_withdraw;
                if (amount > maximum_loan) {
                    System.out.println("Pay Your Past Loan First To Loan Again In The Future\n\n");
                } else {
                    loan_Balance += loan_withdraw;
                    loan_Amount += loan_withdraw;
                    System.out.println("Successfully Withraw Loan\n\n");
                }
            }
            System.out.println("Enter To Return To The Menu...");
            sc.nextLine();
            sc.nextLine();
        }
    }

}
class SavingsAccount extends BankAccount {

    private int savings_Balance;

    public void printInfo(Scanner sc) {
        System.out.println("\nSavings Balance: " + savings_Balance + "\n");
        System.out.println("Enter To Return To The Menu...");
        sc.nextLine();
        sc.nextLine();
    }
    public void deposit(int deposit, Scanner sc) {
        if (deposit <= 0) {
            System.out.println("You Can't Deposit " + deposit + "\n\n");
        } else {
            savings_Balance += deposit;
            System.out.println("Successfully Deposit To Your Savings\n\n");
        }
        System.out.println("Enter To Return To The Menu...");
        sc.nextLine();
        sc.nextLine();

    }
    public void withdraw(int withdraw, Scanner sc) {
        if (withdraw > savings_Balance) {
            System.out.println("Insufficient Balance\n\n");
        } else {
            if (withdraw < 0) {
                System.out.println("YOU CAN'T WITHDRAW NEGATIVE!!\n\n");
            } else {
                savings_Balance -= withdraw;
                System.out.println("Successfully Withdraw\n\n");
            }
            System.out.println("Enter To Return To The Menu...");
            sc.nextLine();
            sc.nextLine();
        }

    }

}
class CheckingAccount extends BankAccount {

    public void printInfo(Scanner sc) {
        System.out.println("\nBalance: " + getBalance() + "\n");
        System.out.println("Enter To Retrun To The Menu...");
        sc.nextLine();
        sc.nextLine();
    }
    public void deposit(int deposit, Scanner sc) {
        if (deposit <= 0) {
            System.out.println("You Can't Deposit " + deposit + "\n\n");
        } else {
            setBalance(deposit);
            System.out.println("Succesfully Deposit!\n\n");
        }
        System.out.println("Enter To Return To The Menu...");
        sc.nextLine();
        sc.nextLine();
    }
    public void withdraw(int withdraw, Scanner sc) {
        if (withdraw > getBalance()) {
            System.out.println("Insufficient Balance!\n\n");
        } else {
            if (withdraw < 0) {
                System.out.println("YOU CAN'T WITHDRAW NEGATIVE!!");
            } else {
                int amount = getBalance() - withdraw;
                setBalance(amount);
                System.out.println("Succesfully Withdraw!\n\n");
            }
            
        }
        System.out.println("Enter To Return To The Menu...");
        sc.nextLine();
        sc.nextLine();

    }

} 
abstract class BankAccount implements Transactable{

    private int balance;

    abstract void printInfo(Scanner sc);

    public int getBalance() {
        return balance;
    }
    
    
    public void setBalance(int balance) {
        this.balance = balance;
    }
    
}
interface Transactable {
    void deposit(int deposit, Scanner sc);
    void withdraw(int withdraw, Scanner sc);
}