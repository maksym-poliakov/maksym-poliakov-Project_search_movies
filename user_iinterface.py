from db_connect import DataBase
from databases_config import db_read,db_save
from config_sql_requests import modify_query
from validation import Validator
from unknownexception import UnknownException



class UserInterface :

    def __init__(self,count_param):
        # Number of required parameters for the menu
        self.count_param = count_param
        self.database_read = DataBase(db_read,5,5,10,None,10)
        self.database_save = DataBase(db_save,5,5,10,None,10)
        self.database_save.create_table()
        self.validator = Validator()

        # Set up the environment by establishing a connection to the database
        self.conn = self.database_read.db_connect()



    @staticmethod
    def dict_values(type_menu,data,key):
        """
        Method collects values into a dictionary for further processing
        :param type_menu: Type of menu the user is in
        :param key: Key to collect data by
        :param data: Data to select from based on the key
        :return: Dictionary with values
        """
        dict_data = {type_menu: {}}
        for ind, value in enumerate(data, start=1):
            if key in value:
                dict_data[type_menu][ind] = value[key]

        return dict_data



    def menu_navigation(self, menu):
        """
        Main method for menu navigation
        :param menu: Dictionary with menu items
        :return: None
        """
        value_text = ''
        for index,values in enumerate(menu) :
            data = menu[values]
            max_value = self.__get_number_menu_items(data)
            for ind, value in enumerate(data, start=1):
                if "text" in value:
                    if max_value > 1:
                        print(f'{ind} - {value["text"]}')
                    else:
                        print(f' -  {value["text"]}')
                    continue
                if isinstance(value,dict) :
                    if self.validator.validator_main_menu(value,self.count_param) :
                        text_question,type_data,method_input = self.validator.validator_main_menu(value,self.count_param)
                        dict_param = self.dict_values(values,data, "text")
                        # Result of main_menu/sub_menu selection that passed validation
                        select = input(text_question).strip()
                        select = self.validator.validation_input(select,text_question,dict_param,
                                                                 values,type_data,method_input)
                        # Get the key to extract the SQL query body from the query dictionary if it exists
                        action_main_menu = self.__get_value_key(data, select,"action")

                        if action_main_menu is not None  and select == 3 and values == 'main_menu':
                            # Get the SQL query body
                            request_body_sql_popular = modify_query(action_main_menu, 1, ())
                            # Execute the query
                            result_popular = self.database_save.get_result_query(request_body_sql_popular
                                                                                 ,type_request='all',offset=0)
                            self.__output_screen_result_popular(result_popular)
                        # Get the data type accepted by the sub_menu input field
                        type_data = self.__get_value_key(data, select, 'data_type')
                        method_input = self.__get_value_key(data, select,"input_method")
                        # If main_menu/sub_menu has the 'choice' key, display the selection list
                        choice = self.__get_value_key(data, select, 'choice')
                        if self.validator.validator_sub_menu(value, select,self.count_param):
                            text_question, type_data, method_input = self.validator.validator_sub_menu(value,select,
                                                                                                self.count_param)
                        if not choice is None:
                            result_choice = self.__get_result_request(data, select, 'choice',0)
                            # Get the value of the 'text' field for the dictionary key
                            value_text = self.__get_value_key(data, select, "text")
                            dict_param = self.__dict_data(result_choice,value_text,choice)
                            # Display the database selection list in the console
                            self.__show_choice(dict_param,value_text,choice)
                            # Get the question text for sub_menu
                        text_sub_question = self.__get_value_key(data, select, "question")
                        if not text_sub_question is None:
                            # Get the search data from the user
                            search_text = input(f'{text_sub_question}')
                            # Validate the input data for the database query
                            search_text = self.validator.validation_input(search_text,text_sub_question,
                                                                          dict_param,value_text,type_data,method_input)
                            # Get the key to extract the SQL query body from the query dictionary
                            key_sql_request = self.__get_value_key(data, select, "action")
                            # Save the search data after preparing it
                            save_text = Validator.type_casting(search_text)
                            self.database_save.save_search_query(key_sql_request,' '.join(save_text))
                            # Get the length of the search query
                            len_query = len(search_text)
                            # Get the SQL query body
                            request_body_sql = modify_query(key_sql_request,len_query,search_text )
                            # Database query results
                            # Perform two queries: one to get the total number of
                            # results and one to display a specified number at a time
                            total_result_search = self.database_read.get_result_query(request_body_sql,
                                                                         search_text,type_request='all',offset=0)
                            len_total_result_search = len(total_result_search)

                            result_search = self.database_read.get_result_query(request_body_sql,
                                                                     search_text,type_request='part',offset=0)

                            self.__show_result_search(result_search,len_total_result_search,
                                                      10,request_body_sql,search_text)

                        if not select is None:
                            return self.menu_navigation(menu[values][select - 1])

        return None


    def __output_screen_result_popular(self,list_result_search):
        """
        Method displays the results of popular queries on the screen
        :param list_result_search: List of dictionaries with search results
        """

        if not list_result_search:
            print("Популярные запросы отсутствуют.")
            return

        grouped_queries = {}
        for query in list_result_search:
            query_type = query.get("query_type")
            if query_type not in grouped_queries:
                grouped_queries[query_type] = []
            grouped_queries[query_type].append(query)

        # Dictionary for converting query_type to readable headers
        type_names = {
            "search_by_genre": "Поиск по жанру :",
            "search_by_year": "Поиск по году :",
            "search_by_genres_years": "Поиск по жанру и году :",
            "search_exact_word": "Поиск по точному совпадению :",
            "search_partial_word": "Поиск по частичному совпадению :",
            "show_popular_queries": "Вывод популярных запросов :"
        }

        # Display grouped queries
        for query_type, query_list in grouped_queries.items():
            # Get the header for the query type or use query_type as is
            header = type_names.get(query_type, f"{query_type} :")
            print(header)
            for query in query_list:
                query_text = query.get("query_text", "")
                query_count = query.get("query_count", 0)
                print(f"запрос : {query_text}  количество :    {query_count}")
            print()
        self.continuation_work()


    @staticmethod
    def __output_screen_result_search(list_result_search):
        """
        Method displays search results on the screen
        :param list_result_search: List of dictionaries with search results
        """
        for values in list_result_search:
            for key, value in values.items():
                if key == 'title':
                    print(f"Название фильма : {value}")
                if key == 'description':
                    print(f"Описание : {value}")
                if key == 'name':
                    print(f"Жанр : {value}")
                if key == 'release_year':
                    print(f"Год выхода : {value}\n")


    def __show_result_search(self,list_result_search,total_len_data,size_show,request_body_sql,search_text):
        """
        Method displays search results on the screen
        :param list_result_search: List of dictionaries with search results
        :param total_len_data: Total number of found results
        :param size_show: Number of results to display
        :param request_body_sql: SQL query body
        :param search_text: Search text
        :return: None
        """
        count_tmp = self.database_read.get_seize_request()
        if total_len_data == 0 :
            count = 0
            print(f"По вашему запросу {' '.join(search_text)} найдено {count} совпадений ")
        else:
            count = size_show
            if total_len_data < size_show :
                count = total_len_data
            print(f"Всего найдено результатов {total_len_data} : \n")
            self.__output_screen_result_search(list_result_search)
            print(f"Выведено {count} из {total_len_data}")
            while count < total_len_data :

                if total_len_data - count < count_tmp:
                    count_tmp = total_len_data - count

                string_inp = input(f"Вывести еще {count_tmp} Y/N : ").lower()
                if not Validator.get_yes_no(string_inp) :
                    break

                list_result_search = self.database_read.get_result_query(request_body_sql,
                                                               search_text, type_request='part',offset=count)
                self.__output_screen_result_search(list_result_search)
                count += count_tmp

                print(f"Выведено {count} из {total_len_data}")

        self.continuation_work()


    @staticmethod
    def continuation_work():
        """
        Method prompts the user to continue the search
        """
        string_inp = input(f"Продолжить поиск ? Y/N : ").lower()
        if Validator.get_yes_no(string_inp):
            return
        else:
            raise UnknownException('EXIT')


    @staticmethod
    def __get_number_menu_items(data):
        """
        Method counts the number of main_menu/sub_menu items
        :param data: Data of the main_menu/sub_menu to count items for
        :return: Number of items in the selected main_menu/sub_menu
        """
        number_menu_items = 0
        for value  in data :
            if "text" in value:
                number_menu_items += 1

        return number_menu_items


    @staticmethod
    def __dict_data(result_request,key_text, key_param):
        """
        Method collects the query result into a dictionary for further processing
        :param result_request: Dictionary with the query result
        :param key_text: Value of the 'text' field
        :param key_param: Query key
        :return: Dictionary with query results
        """
        if key_param == 'choice_genres_years' :
            list_genres = []
            list_years = []
            # Collect data into two lists
            for values in result_request:
                # Convert dictionary to list for indexed access to data
                list_values = list(values.values())
                list_genres.append(list_values[0])
                list_years.append(list_values[1])
            # Remove duplicates
            list_genres = list(set(list_genres))
            list_years = list(set(list_years))
            dict_genres = {key: value for key, value in enumerate(list_genres, start=1)}
            dict_years = {key: value for key, value in enumerate(list_years, start=1)}

            return {key_text: [dict_genres, dict_years]}
        else:
            dict_data = {key_text : {}}
            # Collect data into a list
            for index,values in enumerate(result_request,start=1):
                # Convert dictionary to list for indexed access to data
                list_values = list(values.values())
                if key_param == 'choice_years':
                    if isinstance(list_values[1],str) :
                        list_values[1] = int(list_values[1])
                    dict_data[key_text][list_values[1]] = list_values[1]
                else:
                    dict_data[key_text][index] = list_values[1]
            return dict_data


    @staticmethod
    def __show_choice_years(ranges_years):
        """
        Method displays years on the screen
        :param ranges_years: Range of years
        :return: None
        """
        list_ranges = []
        # Display years as a range from and to
        for item in ranges_years:
            list_ranges.append(f"[ {item} ]")
        print(f'Доступные года фильмов : {','.join(list_ranges)}')


    @staticmethod
    def __show_choice_genres(dict_items):
        """
        Method displays genres on the screen
        :param dict_items: Dictionary with genres
        :return: None
        """

        for key, value in dict_items:
            print(f'{key:>2} - {value}')


    def __show_choice(self, data_dict, key_param, method):
        """
        Method displays a selection list in the console
        :param data_dict: Dictionary of database query results
        :param key_param: Parameter key
        :param method: Selection method
        """
        if method == 'choice_years':
            years = sorted(data_dict[key_param].values())
            ranges_years = self.__range_collector(years)
            self.__show_choice_years(ranges_years)
        elif method == 'choice_genres_years':
            dict_items = data_dict[key_param][0].items()
            self.__show_choice_genres(dict_items)
            years = sorted(data_dict[key_param][1].values())
            ranges_years = self.__range_collector(years)
            self.__show_choice_years(ranges_years)
        else:
            dict_items = data_dict[key_param].items()
            self.__show_choice_genres(dict_items)


    @staticmethod
    def __range_collector(list_years):
        """
        Method collects data into ranges for a visually appealing display
        :param list_years: List of available years
        :return: List of ranges
        """
        ranges = []
        start = list_years[0]
        end = list_years[0]

        for year in list_years[1:] + [None]:
            if year is None or year != end + 1:
                # Complete the current range
                if start == end:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}-{end}")
                start = year
            end = year
        return ranges


    @staticmethod
    def __get_value_key(data,select,method):
        """
        Method returns values by keys from the selected sub_menu dictionary
        :param data: Key from the menu_structure dictionary to search for values by the selected key
        :param select: Index of the sub_menu selected by the user
        :param method: Key from the sub_menu dictionary to search for the desired value.
        :return: Value of the selected key from the dictionary
        """
        value_key = None
        for index, value in enumerate(data, start=1):
            if index == select :
                if method in value:
                    value_key = value[method]
        return value_key


    def __get_result_request(self,data,select,method,len_query):
        """
        Method retrieves a list of query results
        :param data: Key from the menu_structure dictionary to search for values by the selected key
        :param select: Index of the sub_menu selected by the user
        :param method: Key from the sub_menu dictionary to search for the desired value
        :param len_query: Length of the query
        :return: List of query results
        """
        # Key to retrieve the SQL query body from the query dictionary
        key_sql_request = self.__get_value_key(data, select, method)
        # Get the SQL query body
        request_body_sql = modify_query(key_sql_request,len_query,select)
        # Database search results
        result_search = self.database_read.get_result_query(request_body_sql,type_request='all',offset=0)
        return result_search





