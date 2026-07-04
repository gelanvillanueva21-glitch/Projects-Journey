package Bank;

import java.util.*;

class AccMenu {

        Random ran = new Random();
        private File_Handling file = new File_Handling();
        private Hashtable<Integer, String> Account = new Hashtable<>();

        boolean account_Menu(Scanner sc) throws InputMismatchException {
            try {
                String[][] array = file.array_Read(); 
                for (String[] row : array) {
                    Account.put(Integer.parseInt(row[1]), row[0]);
                }
                
                for (Integer key : Account.keySet()) {
                    System.out.println(key + "\t" + Account.get(key));
                }
                System.out.println(Account.get(1234));
                while (true) {
                    System.out.println("\n\n_____ACCOUNT SYSTEM_____\n1. Log In\n2. Create Account\n3. Exit");
                    System.out.print("> ");
                    int choice = sc.nextInt();

                    if (choice == 1) {
                        if (login_AccNum(sc)) {
                            return true;
                        } else {
                            return false;
                        }
                    } else if (choice == 2) {
                        create_AccNum(sc);
                    } else if (choice == 3) {
                        break;
                    } else {
                        System.out.println("Can't Find Input Number " + choice + "\n");
                    }
                }
            } catch (InputMismatchException e) {
                System.out.println("Input A Number!!\n");
            }
            
            return false;
        }

        void create_AccNum(Scanner sc) {
        sc.nextLine();
        boolean exist;
        int num;
            
        do {
            num = ran.nextInt(1000, 9999);
            exist = false;

            for (Integer key : Account.keySet()) {
                if (num == key) {
                    exist = true;
                    break;
                }
            }
        } while (exist);

            System.out.println("Generated Account Number: " + num);

        while (true) {
            System.out.print("Create Username: ");
            String user = sc.nextLine();
            if (user.length() >= 8) {
                Account.put(num, user);
                System.out.println("Successfully Created Username\n\n");
                file.storing(num, user);
                break;
            } else {
                System.out.println("\nMust Atleast 8 Character\n");
            }
        }
        System.out.println("\nPress Enter To Return...\n");
        sc.nextLine();

        }
        boolean login_AccNum(Scanner sc) {
            int number_Attempt = 5;
            boolean StopContinue = true;
            int account_number = 0000;
            while (StopContinue) {
                System.out.println("\nNumber Of Attemp: " + number_Attempt);
                System.out.print("Enter Account Number: ");
                account_number = sc.nextInt();
                sc.nextLine();

                for (Integer key : Account.keySet()) {
                    if (account_number == key) {
                        System.out.println("\nProceed\n");
                        StopContinue = false;
                        break;
                    }
                }
                number_Attempt -= 1;

                    if (number_Attempt == 0) {
                        System.out.println("\nNo More Attemp Left\n");
                        return false;
                    } 
            }
            StopContinue = true;
            while (StopContinue) {
                System.out.print("Enter Username: ");
                String user = sc.nextLine();

                for (int i = 0; i < Account.size(); i++) {
                    if (user.equals(Account.get(account_number))) {
                        System.out.println("\nUsername Correct");
                        System.out.println("Procceed\n");
                        return true;
                    }
                }
                System.out.println("Username Incorrect or Not Found");
                System.out.println("Would You Like To Enter Again?[Y][N]");
                System.out.print("> ");
                String choice = sc.next().toUpperCase();
                if(choice.equals("Y")) { continue; } 
                else { break; }
            }
            System.out.println("Press Enter To Return...");
            sc.nextLine();
            return false;
        }
    }
