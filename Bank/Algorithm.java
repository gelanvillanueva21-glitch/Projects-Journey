package Bank;

import java.util.*;
import java.io.*;

public class Algorithm {
    
    public void main_sort()throws IOException{
        try {
            BufferedReader read = new BufferedReader
            (new FileReader("/Users/user/OneDrive/Desktop/ProgrammingLanguages/Java.Language/Bank/Accounts.txt"));
            String line;
            ArrayList<String> array = new ArrayList<>();
            while((line = read.readLine()) != null) {
                array.add(line);
            }
            if (array.size() != 0) {
                Quick_Sort.quick_sort(array, 0, array.size() - 1);
                BufferedWriter rewrite = new BufferedWriter(new FileWriter("/Users/user/OneDrive/Desktop/ProgrammingLanguages/Java.Language/Bank/Accounts.txt"));

                for (int i = 0; i < array.size(); i++) {
                    rewrite.write(array.get(i));
                }
                rewrite.close();
            }
            read.close();
        } catch (IOException e) {
            System.out.println("Something Error Occured To The File");
        }
        
    }
    private static class Quick_Sort {

        private static void quick_sort(ArrayList<String> array, int low, int high) {
            if (high <= low) {
                return;
            }
            int pivot_index = partition(array, low, high);
            quick_sort(array, low, pivot_index - 1);
            quick_sort(array, pivot_index + 1, high);

        } private static int partition(ArrayList<String> array, int low, int high) {
            String pivot = array.get(high);
            int i = low - 1;
            for (int j = low; j < high; j++) {
                if (array.get(j).compareTo(pivot) <= 0) {
                    i++;
                    String temp = array.get(i);
                    array.set(i, array.get(j) + "\n");
                    array.set(j, temp);
                }
            }

            String temp = array.get(i + 1);
            array.set(i + 1, array.get(high));
            array.set(high, temp);

            return i + 1;
        }
    }
}
