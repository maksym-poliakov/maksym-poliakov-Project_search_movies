frequently_question = "Выберите интересующий пункт меню (Enter - выход): "
menu_structure = {
               "main_menu": [
            {
                "text": "Поиск по ключевому слову",
                "sub_menu": [
                    {"text": "По точному совпадению","question":"Введите слово : " ,
                     "action": "search_exact_word","data_type":"string","input_method": "one"},
                    {"text": "По частичному совпадению","question":"Введите часть слова : " ,
                     "action": "search_partial_word","data_type":"string","input_method": "two"},
                    {"question": f"{frequently_question }","data_type":"int","input_method": "one" }

                ]
            },
            {
                "text": "Поиск по жанру и году",
                "sub_menu": [
                    {"text": "По жанру", "question": "Выберите жанр : ", "choice": "choice_genres",
                     "action": "search_by_genre","data_type":"all","input_method": "two"},
                    {"text": "По году", "question": "Введите год : ","choice": "choice_years",
                     "action": "search_by_year","data_type":"int","input_method": "two"},
                    {"text": "По жанру и году", "question": "Введите жанр и год : ", "choice": "choice_genres_years",
                     "action": "search_by_genres_years","data_type":"all","input_method": "two"},
                    {"question": f"{frequently_question }","data_type": "int" ,"input_method": "one" }
                ]
            },
            {
                "text": "Вывод популярных запросов",
                "action": "show_popular_queries",
                "data_type":"int"
            },
                {"question": f"{frequently_question }" ,"data_type":"int","input_method": "one" }
        ]
    }


menu_genres_years = { "years": {"warning": "год","question": "года"},
                       "genre": {"warning": "жанр","question": "жанра"}
}


