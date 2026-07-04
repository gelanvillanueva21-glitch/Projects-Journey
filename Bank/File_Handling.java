package Bank;

import java.io.*;

public class File_Handling {

    public void storing(int account_number, String username) {
        Algorithm sort = new Algorithm();
        try {
            BufferedWriter file_Writer = new BufferedWriter
            (new FileWriter("/Users/user/OneDrive/Desktop/ProgrammingLanguages/Java.Language/Bank/Accounts.txt", true));
            file_Writer.write(username + ", " + account_number + "\n");
            sort.main_sort();
            file_Writer.close();
        } catch (IOException e) {
            System.out.println("\nAn Error Occured To The File\n");
        }
    } public String[][] array_Read() {
        String[][] parts = new String[0][2];
        try {
            BufferedReader file_Reader = new BufferedReader
            (new FileReader("/Users/user/OneDrive/Desktop/ProgrammingLanguages/Java.Language/Bank/Accounts.txt"));
            String line;
            while ((line = file_Reader.readLine()) != null) {
                String[][] newParts = new String[parts.length + 1][2];

                for (int i = 0; i < parts.length; i++) {
                    newParts[i] = parts[i];
                }
                newParts[parts.length] = line.split(", ");
                parts = newParts;
            }
            file_Reader.close();
        } catch (IOException e) {
            System.out.println("\nAn Error Occured To The File\n");
        }
        return parts;
    }
}
