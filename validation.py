# Validator class for processing user-entered strings.
import re
from menu import menu_genres_years
from unknownexception import UnknownException


class Validator:

    PATTERN_WORD = r'[A-Za-z]+'
    PATTERN_WORDS = r'[\s,]+'
    PATTERN_NUM_NUM = r'(\d+)\s*-\s*(\d+)'
    PATTERN_MINUS_NUM = r'(?<!\d)\s*-\s*(\d+)'
    PATTERN_NUM_MINUS = r'(\d+)\s*-\s*(?=[\sA-Za-z]|[^\w\s\d]|$)'
    PATTERN_NO_MINUS_NUM = r'(?<!-)\b\d+\b(?!-)'
    PATTERN_WORD_WORD = r'([A-Za-z]+)\s*-\s*([A-Za-z]+)'
    PATTERN_MINUS_WORD = r'(?:^|[\s\d]|[^\w\s])\s*-\s*([A-Za-z]+)'
    PATTERN_WORD_MINUS = r'([A-Za-z]+)\s*-\s*(?=[\s\d]|$)'
    PATTERN_NO_MINUS_WORD = r'(?<!-)\b[A-Za-z]+\b(?!-)'
    # Patterns for years
    PATTERN_YEAR_YEAR = r'(\b\d{4})\s*-\s*(\d{4}\b)'
    PATTERN_MINUS_YEAR = r'(?<!\d)\s*-\s*(\d{4}\b)'
    PATTERN_YEAR_MINUS = r'(\b\d{4})\s*-\s*(?=[\sA-Za-z]|[^\w\s\d]|$)'
    PATTERN_NO_MINUS_YEAR = r'(?<!-)\b\d{4}\b(?!-)'
    LIST_PATTERN_YEAR = [PATTERN_YEAR_YEAR,PATTERN_MINUS_YEAR,PATTERN_YEAR_MINUS,PATTERN_NO_MINUS_YEAR]
    LIST_PATTERN_NUM = [PATTERN_NUM_NUM, PATTERN_MINUS_NUM, PATTERN_NUM_MINUS,PATTERN_NO_MINUS_NUM]
    LIST_PATTERN_WORD = [PATTERN_WORD_WORD, PATTERN_MINUS_WORD, PATTERN_WORD_MINUS,PATTERN_NO_MINUS_WORD]

    def validation_input(self,select,text_question,dict_param,key_param,type_data,method_input) :
        # The entered value must be an integer only
        if select == '' or select is None :
            raise UnknownException ('EXIT')
        if type_data == 'int' and method_input == 'one':
            max_value =  len(list(dict_param.get(key_param)))
            number = self.__checking_digits(select,max_value,text_question)
            good_param = self.__checking_selection_values(1,max_value,key_param,number
                                                        ,text_question,method_input,0)
            return good_param
            # Search by year
        elif type_data == 'int' and method_input == 'two':
            while True :

                min_value = list(dict_param[key_param].values())[0]
                max_value = list(dict_param[key_param].values())[-1]
                # Extract a list of year lists to form ranges
                list_years = self.__extract_enumeration(select,dict_param,key_param,type_data)
                # Get the list of years
                result_year = self.__data_request(list_years,min_value,max_value,
                                                  text_question,key_param,method_input,dict_param)

                # Remove duplicates
                if result_year :
                    result_year = self.__removing_duplicates_list(result_year)
                    return tuple(result_year)
                print('Вы ввели не корректный год !')
                select = input('Введите год : ')


            # Search by exact match
        elif type_data == 'string' and method_input == 'one':
            return tuple([select])
        # The entered value must be a string only
        elif type_data == 'string' and method_input == 'two':
            # Search by partial word
            return self.__get_words(select)
        # The entered value can be a number, a string, or a list of strings and numbers
        elif type_data == 'all' and method_input == 'two':
            if key_param == "По жанру и году" :
                # Check for the presence of a year
                min_value_year = list(list(dict_param[key_param])[1].values())[0]
                max_value_year = list(list(dict_param[key_param])[1].values())[-1]
                new_dict_param_year = {key_param: dict_param[key_param][1]}
                additional_menu_year = menu_genres_years['years']
                # Extract years from the string
                list_year = self.__extract_patterns(select, Validator.LIST_PATTERN_YEAR)
                # Get the list of years for the query
                result_year = self.__validator_genres_years(min_value_year,max_value_year,list_year,text_question
                                           ,new_dict_param_year,key_param,type_data,method_input,additional_menu_year)

                # Remove duplicate years
                if result_year:
                    result_year = self.__removing_duplicates_list(result_year)
                # Check for the presence of a genre
                min_value_genre = 1
                max_value_genre = len(list(dict_param[key_param])[0].values())
                new_dict_param_genre = {key_param: dict_param[key_param][0]}
                additional_menu_genre = menu_genres_years["genre"]
                # Extract years from the string
                list_year = self.__extract_patterns(select, Validator.LIST_PATTERN_YEAR)
                # Remove years and return the string without years
                string_tmp = self.__remove_years_from_text(select,list_year)
                # Try to extract numbers
                new_string = self.__extract_patterns(string_tmp , Validator.LIST_PATTERN_NUM)
                if not new_string :
                    new_string = self.__extract_enumeration(string_tmp,new_dict_param_genre,key_param, type_data)
                # Get the list of genres for the query
                result_genre = self.__validator_genres_years(min_value_genre, max_value_genre, new_string, text_question,
                                                             new_dict_param_genre,
                                                             key_param, type_data, method_input, additional_menu_genre)

                # Remove duplicate genres to prevent them from being included in the query
                if result_genre:
                    result_genre = self.__removing_duplicates_list(result_genre)
                # Form the actual data for the query
                if result_year and result_genre :
                    return tuple(result_year) + tuple( result_genre)
                elif not result_year and result_genre :
                    return tuple(result_genre)
                elif result_year and not result_genre :
                    return tuple(result_year)
                raise UnknownException ('request format error')
            else:
                while True :
                    # Get the maximum allowed value
                    max_value = len(list(dict_param.get(key_param)))
                    # Extract a list of year lists to form ranges
                    list_years = self.__extract_enumeration(select, dict_param, key_param, type_data)
                    # Get the list of genres
                    result_enum = self.__data_request(list_years, 1, max_value, text_question, key_param,
                                                      method_input, dict_param)
                    if result_enum:
                        # Convert to the required type
                        return  tuple(result_enum)
                    else:
                        print('Такого жанра не найдено ')
                        select = input('Введите жанр :')

        else:
            raise TypeError



    def __validator_genres_years(self,min_value,max_value,select,text_question,dict_param,
                                 key_param,type_data,method_input,text_ques):
        """
        Method to validate correctly entered user data.
        :param min_value: Minimum allowed parameter value
        :param max_value: Maximum allowed parameter value
        :param select: User-entered query string
        :param text_question: Question text for substitution
        :param dict_param: Dictionary with current data for matching
        :param key_param: Dictionary key to access the required data
        :param type_data: Type of data being validated
        :param method_input: Input method for parameters: number, text, or both
        :param text_ques: Text from the additional menu_genres_years for substitution in the input field
        :return: List of processed data for substitution in the database query
        """
        result = self.__data_request(select,min_value,max_value,text_question,key_param,method_input,dict_param)
        if not self.__validator_param_years_genres(result) :
            while True:
                print(f'Вы не ввели {text_ques["warning"]} !')
                string_inp = input(f'Искать c учетом {text_ques["question"]} ? Y/N : ')
                if self.get_yes_no(string_inp) :
                    while True :
                        string_inp = input(f'Введите {text_ques["warning"]} : ')
                        # Extract a list of values to form ranges
                        list_result = self.__extract_enumeration(string_inp, dict_param, key_param, type_data)
                        result = self.__data_request(list_result,min_value,max_value,
                                                          text_question,key_param,method_input,dict_param)

                        # Remove duplicates
                        if result :
                            result = self.__removing_duplicates_list(result)
                            return result
                break
        return result


    @staticmethod
    def __remove_years_from_text(text, years) :
        """
        Method to extract four-digit numbers from a string.
        :param text: Text from which numbers need to be extracted
        :param years: Target number
        :return: Text with years removed
        """
        flat_years = {year for sublist in years for year in sublist}
        for year in flat_years:
            text = re.sub(rf'\b{year}\b', '', text)
        return re.sub(r'\s+', ' ', text).strip()


    @staticmethod
    def get_yes_no(string):
        """
        Method for selecting yes/no.
        :param string: Value from the user's input string
        :return: False or True
        """
        string = str(string).lower().strip()
        while True:
            if string == 'y':
                return True
            elif string == 'n':
                return False
            else:
                print("Вы должны ввести только 'Y' или 'N' : ")
                string = input("Искать без учета года ? Y/N : ")


    @staticmethod
    def __validator_param_years_genres(list_result):
        """
        Method to check if the entered data matches the available values.
        :param list_result: List of parameters.
        :return: Parameters with valid values
        """
        if list_result:
            return True
        return False


    @staticmethod
    def __get_words(text):
        """
        Method to create a tuple of words.
        :param text: Text to be split into words
        :return: Tuple of words
        """
        words =  re.findall(Validator.PATTERN_WORD,text)
        return tuple(words)


    @staticmethod
    def validator_main_menu(dict_menu,count_param):
        """
        Method to check the state of menu items.
        Verifies if all menu items have the required parameters.
        :param dict_menu: Dictionary of the menu item
        :param count_param: Number of required parameters
        :return: List of menu item values
        """
        list_values_param = []
        for key,value in dict_menu.items() :
            if key == "data_type" :
                list_values_param.append(dict_menu[key])
            if key == "input_method" :
                list_values_param.append(dict_menu[key])
            if key == "question" :
                list_values_param.append(dict_menu[key])
        if len(list_values_param) == count_param :
            return list_values_param
        return None


    @staticmethod
    def validator_sub_menu(dict_menu,select, count_param):
        """
        Method to validate submenu parameters.
        :param dict_menu: Dictionary of the menu
        :param select: Selected menu item index
        :param count_param: Number of required parameters
        :return: List of parameter values or None
        """
        list_values_param = []
        if isinstance(dict_menu,dict) :
            for index,(key,value) in enumerate(dict_menu.items(),start=1) :
                if index == select :
                    if key == "data_type" :
                        list_values_param.append(dict_menu[key])
                    if key == "input_method" :
                        list_values_param.append(dict_menu[key])
                    if key == "question" :
                        list_values_param.append(dict_menu[key])
                if len(list_values_param) == count_param :
                    return list_values_param
        return None


    @staticmethod
    def __checking_digits(value, max_value, text_question):
        """
        Method to check the selection of menu items, ensuring the entered value is a number
        and falls within the allowed range.
        :param value: Entered value
        :param max_value: Maximum allowed value
        :param text_question: Question text for the selected menu item
        :return: String with a value within the allowed range
        """
        if isinstance(value,int):
            return value
        elif value.isdigit() :
            return int(value)
        else:
            while True:
                if value == ''.strip(): # Exit menu indicator
                    return None
                elif value == '<'.strip():  # Indicator to return to the previous menu (not implemented)
                    print('Возврат к предыдущему меню')
                    raise UnknownException('EXIT')
                elif value == '<<'.strip():  # Indicator to return to the main menu (not implemented)
                    print('Возврат к главному меню')
                    raise UnknownException ('EXIT')
                else:
                    print(f'Введенное значение должно целым числом и от 1 до {max_value} : ')
                    value = input(f'{text_question}')
                    if value.isdigit():
                        value = int(value)
                        break
            return value


    def __checking_selection_values(self,min_value,max_value,key_param,
                                    value_param, text_question, method_param, ind):
        """
        Method to ensure values do not exceed the allowed range.
        :param min_value: Minimum allowed value for the input parameter
        :param max_value: Maximum allowed value for the input parameter
        :param key_param: Key for which parameters are compared
        :param value_param: Numeric value of the passed parameter
        :param text_question: Question text for the selected menu item
        :param method_param: Value 'two' indicates multiple values can be passed for one key
        :param ind: Optional parameter, used only for method_param = "two"
        :return: Correct parameter value
        """
        int_inp = ''
        try:
            value_param = self.__checking_digits(value_param,max_value,text_question)

            value_param = int(value_param)
            while min_value > value_param or value_param > max_value:
                if method_param == 'one':
                    int_inp = input(f'Введите актуальное значение для {key_param} от {min_value} до '
                                    f'{max_value} Enter выход  : ')
                    int_inp = self.__checking_digits(int_inp, max_value, text_question)
                    if min_value <= int_inp <= max_value:
                        return int_inp
                if method_param == 'two':
                    int_inp = input(f'Введите актуальное значение для {key_param} от {min_value} до  '
                                    f'{max_value}'
                                    f' для значения № {ind + 1} Enter выход  : ')
                    int_inp = self.__checking_digits(int_inp, max_value, text_question)
                if method_param == 'two' and min_value <= int_inp <= max_value:
                    return int_inp
            return value_param
        except :
            raise UnknownException ("EXIT")


    @staticmethod
    def __isdigit(*args):
        """
        Method to check if values are numbers.
        :param args: List of numbers
        :return: True or False
        """
        for arg in args:
            if not arg.isdigit():
                return False
        return True


    def __extract_enumeration(self, string, dict_data,key_param,data_type): #, method_param
        """
        Method to extract data from a string.
        :param string: String with data to process
        :param dict_data: Dictionary with source data to convert string representations to numeric
        :param key_param: Dictionary key
        :param data_type: Type of processed values from the main/submenu dictionary
        :return: List of value lists for further processing to form query data
        """
        result = []
        total_data = []
        number_enum = []
        words_enum = []

        if data_type == 'int' or data_type == 'all' :
            # Extract numeric enumerations if present
            number_enum = self.__extract_patterns(string, Validator.LIST_PATTERN_NUM)
            # Sort in ascending order
            number_enum = self.__sorted_number(number_enum)
        if data_type == 'string' or data_type == 'all' :
            # Extract word enumerations if present
            words_enum = self.__extract_patterns(string, Validator.LIST_PATTERN_WORD)
            # Convert to numeric values
            words_enum = self.__words_to_int(words_enum, dict_data,key_param)
            # Sort in ascending order
            words_enum = self.__sorted_number(words_enum)
        # Combine queries
        if number_enum :
            total_data += number_enum
        if words_enum:
            total_data += words_enum
        if not total_data:
            return result
        return total_data


    def __data_request(self,list_data_checking,min_value,max_value,text_question
                       ,key_param,method_param, dict_data) :
        """
        Method to form a data string for a query from a list of values.
        :param list_data_checking: List of parameter lists to form the query data string
        :param min_value: Minimum allowed value to validate user-entered parameters
        :param max_value: Maximum allowed value to validate user-entered parameters
        :param text_question: Text to form a question if user data is incorrect
        :param key_param: Key for which parameters are compared
        :param method_param: Value 'two' indicates multiple values can be passed for one key
        :param dict_data: Dictionary with data to validate against user-entered data
        :return: List of data for further submission to the database query
        """
        result = []
        # Sort in ascending order
        list_data_checking = self.__sorted_number(list_data_checking)
        for item in list_data_checking :
            # Check for a smaller year value
            if self.__isdigit(item[0]) and (int(item[0]) > max_value or int(item[0]) < min_value) :
                if item[0] == item[1] :
                    item[0] = str(self.__checking_selection_values(min_value,max_value,key_param, item[0],
                                                                 text_question, method_param, 0))
                    item[1] = str(item[0])
                else:
                    item[0] = str(self.__checking_selection_values(min_value, max_value, key_param, item[0],
                                                             text_question,method_param, 0))
            if self.__isdigit(item[1]) and (int(item[1]) > max_value or int(item[1]) < min_value) :
                    item[1] = str(self.__checking_selection_values(min_value,max_value,key_param,
                                                                 item[1], text_question, method_param, 1))
        if list_data_checking :
            list_tmp = []
            for item in list_data_checking:
                for ind, value in enumerate(dict_data[key_param].values(), start=min_value):
                    # Both values are empty
                    if not item[0] and not item[1]:
                        list_tmp.append(value)
                        continue
                    # First is empty, second is not
                    elif not item[0] and item[1] :
                        if self.__isdigit(item[1]) and ind <= int(item[1]) :
                            list_tmp.append(value)
                            continue
                    # First is not empty, second is empty
                    elif item[0] and not item[1]:
                        if self.__isdigit(item[0]) and  ind >= int(item[0]) :
                            list_tmp.append(value)
                            continue
                    # Both are not empty
                    elif item[0] and item[1] :
                        if self.__isdigit(item[0], item[1]) and int(item[0]) <= ind <= int(item[1]): #and len(item[0]) == len(str(ind))
                            list_tmp.append(value)
                            continue
                result += list_tmp
        return result


    @staticmethod
    def type_casting(tuple_data):
        """
        Method to convert types to strings.
        :param tuple_data: List of data
        :return: Tuple with string data
        """
        new_list = []
        tuple_data = list(tuple_data)
        for value in tuple_data :
            if isinstance(value,int):
                value = str(value)
            new_list.append(value)
        return tuple(new_list)


    @staticmethod
    def __removing_duplicates_list(list_number):
        """
        Method to remove duplicates from a list.
        :param list_number: List of numbers
        :return: List without duplicates
        """
        if list_number :
            for number in list_number :
                if isinstance(number,int) :
                    return list(set(list_number))
                if isinstance(number,list):
                    return [list(set(number)) for number in list_number]
                else:
                    return list_number
        raise TypeError


    @classmethod
    def __extract_patterns(cls,string, list_pattern):
        """
        Method to process the input string with user-entered parameters.
        If the string contains a '-', it checks the values before and after the '-'.
        If there is no number before the '-', but there is one after, it takes a range from the minimum allowed value
        to the specified value, or if they are strings, it takes them alphabetically after the '-'.
        If there is a number before the '-' but not after, it takes a range from the number before the '-' to the end.
        The range size is dynamic and calculated based on the available number of copies for a given folder.
        :param string: String with user data
        :param list_pattern: List of patterns
        :return: List of tuples with extracted values
        """
        try:
            result = []
            string_tmp = string
            for pattern in list_pattern:
                matches = re.findall(pattern, string_tmp)
                format_result = []
                if pattern in [cls.PATTERN_NUM_NUM, cls.PATTERN_WORD_WORD,cls.PATTERN_YEAR_YEAR]:
                    format_result = [[str(item1), str(item2)] for item1, item2 in matches]
                elif pattern in [cls.PATTERN_MINUS_NUM, cls.PATTERN_MINUS_WORD,cls.PATTERN_MINUS_YEAR]:
                    format_result = [['', str(item)] for item in matches]
                elif pattern in [cls.PATTERN_NUM_MINUS, cls.PATTERN_WORD_MINUS,cls.PATTERN_YEAR_MINUS]:
                    format_result = [[str(item), ''] for item in matches]
                elif pattern in [cls.PATTERN_NO_MINUS_NUM,cls.PATTERN_NO_MINUS_WORD,cls.PATTERN_NO_MINUS_YEAR]:
                    format_result = [[str(item), str(item)] for item in matches]
                result.extend(format_result)
                # Remove matches from the string
                string_tmp = re.sub(pattern, '', string_tmp)
        except:
            raise  UnknownException ('request format error')
        return result


    def __sorted_number(self,list_value):
        """
        Method to sort numbers in a list in ascending order.
        :param list_value: List of values
        :return: Sorted list
        """
        number_sort = []
        if self.__clear_list_if_empty(list_value ):
            for values in list_value :
                if not self.__isdigit(values[0]) or not self.__isdigit(values[1]) :
                    number_sort.append(values)
                    continue
                else :
                    sorted_values = [str(num) for num in sorted([int(v) for v in values])]
                    number_sort.append(sorted_values)
        return number_sort


    def __words_to_int(self,words, dict_param,key_param):
        """
        Method to convert word representations of a selected parameter to numeric.
        :param words: List of words
        :param dict_param: Dictionary with parameters for comparison
        :param key_param: Dictionary key to access
        :return: List of numbers corresponding to the selected dictionary data
        """
        list_result = []
        for word in words:
            list_number = []
            for item in word:
                if item in dict_param[key_param].values():
                    for key, value in dict_param[key_param].items():
                        if item == value:
                            list_number.append(str(key))
                else:
                    list_number.append('')
            list_result.append(list_number)

        return self.__clear_list_if_empty(list_result)


    @staticmethod
    def __clear_list_if_empty(lst):
        """
        Method to clear a list of empty sublists.
        :param lst: List of lists
        :return: List without empty nested lists
        """
        clear = [[] if item == ['', ''] else item for item in lst]
        return [] if all(item == [] for item in clear) else clear


    @staticmethod
    def split_tuple_by_type(data_tuple):
        """
        Method to split a tuple into two tuples if it contains different types (words and numbers).
        :param data_tuple: Tuple to split
        :return: Tuple of tuples
        """
        numbers = []
        words = []
        for item in data_tuple:
            if isinstance(item, int) or (isinstance(item, str) and item.isdigit()):
                numbers.append(int(item))
            else:
                words.append(item)
        result = []
        if numbers:
            result.append(tuple(numbers))
        if words:
            result.append(tuple(words))
        return tuple(result) if len(result) > 1 else result[0]


    @staticmethod
    def is_tuple_numbers(data_tuple):
        """
        Method to check if a tuple contains at least one number.
        :param data_tuple: Tuple with data
        :return: True if yes, False otherwise
        """
        for value in data_tuple:
            if isinstance(value, int):
                return True
            if isinstance(value, str) and value.isdigit():
                return True
        return False


    @staticmethod
    def is_tuple_words(data_tuple) :
        """
        Method to check if a tuple contains at least one word.
        :param data_tuple: Tuple with data
        :return: True if yes, False otherwise
        """
        for value in data_tuple :
            if isinstance(value, str) and not value.isdigit():
                return True
            if not isinstance(value, (int, float, str)):
                return True
        return False