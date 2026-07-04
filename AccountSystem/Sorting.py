class Sorting:
    """
    This Class is to sort the file text.
    """
    def Quick_Sort(Array):
        if len(Array) <= 1:
            return Array

        less_than_list = []
        greater_than_list = []
        first_array = Array[0]
        for value in Array[1:]:
            if value <= first_array:
                less_than_list.append(value)
            else:
                greater_than_list.append(value)
        return sort.Quick_Sort(less_than_list) + [first_array] + sort.Quick_Sort(greater_than_list)


    def Array_List():
        file_info = open('/Users/user/OneDrive/Desktop/ProgrammingLanguages/Python.Language/PythonPractice2/AccountSystem/Accounts.txt', 'r')
        temp_list = []
        for item in file_info:
            temp_list.append(item)
        array_list = sort.Quick_Sort(temp_list)
        if len(array_list) != 0:
            rewrite = open('/Users/user/OneDrive/Desktop/ProgrammingLanguages/Python.Language/PythonPractice2/AccountSystem/Accounts.txt', 'w')
            rewrite.seek(0)
            for items in array_list:
                rewrite.write(items)



sort = Sorting
