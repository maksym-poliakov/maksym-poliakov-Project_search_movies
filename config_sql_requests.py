# Configuration file for dictionaries with indexes and SQL queries
from validation import Validator

base_query = """
            SELECT film.title, film.description,category.name,film.release_year  FROM film
            LEFT JOIN  film_category AS fc ON fc.film_id = film.film_id 
            LEFT JOIN category ON  category.category_id =  fc.category_id
            """


INDEXES= {
            'word': "CREATE INDEX idx_film_title_lower ON film((LOWER(title)))",
            'genre': "CREATE INDEX idx_category_name_lower ON category((LOWER(name)))",
            'year' : "CREATE INDEX idx_film_release_year ON film(release_year)"
        }

QUERY = {
            'search_exact_word': f"{base_query}" + "WHERE LOWER(title) REGEXP CONCAT ('(^| )',%s,'( |$)')",
            'search_partial_word': f"{base_query}" + "WHERE LOWER(title) LIKE CONCAT( '%',%s ,'%')" ,
            "search_by_genres_years":  f"{base_query}" ,
            "search_by_genre": f"{base_query}" + "WHERE LOWER(category.name) IN " ,
            'search_by_year': f"{base_query}" + "WHERE film.release_year IN ",
            'choice_genres': 'SELECT category_id ,name FROM category',
            'choice_years' :"""SELECT film_id,release_year FROM film
                            GROUP BY release_year 
                            ORDER BY release_year ASC""",
            'choice_genres_years': """SELECT DISTINCT category.name,film.release_year  FROM film
                                    JOIN  film_category AS fc ON fc.film_id = film.film_id 
                                    JOIN category ON  category.category_id = fc.category_id """ ,
            "show_popular_queries":"""SELECT query_type,query_text,query_count 
             FROM (
            SELECT query_type,query_text,query_count , RANK() OVER(partition by query_type order BY query_count DESC
                    ) as lim_10
            FROM search_queries) as popular
            WHERE  lim_10 <= 10
                                    """,
            'genre' : f"{base_query}" + "WHERE LOWER(category.name) = %s",
            'year' : f"{base_query}" + "WHERE film.release_year IN "
        }


def complex_query(key_query, data_tuple):
    new_query = QUERY.get(key_query)
    def creating_placeholders(data, part_query):
        placeholders = ', '.join(['%s'] * len(data))
        return f" {part_query} IN ({placeholders}) "

    if key_query == "search_by_genres_years":
        if Validator.is_tuple_numbers(data_tuple) and Validator.is_tuple_words(data_tuple):
            # Split the tuple into two for correct placeholder substitution
            two_tuple = Validator.split_tuple_by_type(data_tuple)
            new_query += " WHERE " + creating_placeholders(two_tuple[0], "film.release_year")
            new_query += " AND " + creating_placeholders(two_tuple[1], "LOWER(category.name)")
        else:
            if Validator.is_tuple_numbers(data_tuple):
                new_query += " WHERE " + creating_placeholders(data_tuple, "film.release_year")
            else:
                new_query += " WHERE " + creating_placeholders(data_tuple, "LOWER(category.name)")
    return new_query


def modify_query(key_query,len_values,data_tuple) :
    """
    Modifies SQL queries if the user input contains multiple values.

    :param key_query: Query key from the QUERY dictionary
    :param len_values: Number of values provided
    :param data_tuple: Tuple containing query data
    :return: Modified query if multiple values are provided, otherwise the standard query
    """

    string_query = ''
    new_query = QUERY.get(key_query)

    len_base_query = len(base_query)
    if len_values > 1 :
        for item in range(1,len_values) :
            if key_query == 'search_partial_word' :
                string_query += "OR LOWER(title) LIKE CONCAT( '%',%s ,'%')"
            elif key_query == 'genre' :
                string_query += "OR LOWER(category.name) = %s"
            elif QUERY.get(key_query)[len_base_query :].find('IN') >= 0 :
                placeholders = ', '.join(['%s'] * len_values )
                string_query = f"( {placeholders} )"
                break
            elif key_query == "search_by_genres_years":
                return complex_query(key_query, data_tuple)
            else :

                return new_query
        return new_query + string_query
    elif len_values == 1  :
        if len_values == 1 :
            if QUERY.get(key_query)[len_base_query :].find('IN') >= 0 :
                placeholders = ', '.join(['%s'] * len_values )
                string_query = f"( {placeholders} )"
                new_query += string_query
            if key_query == "search_by_genres_years":
                return complex_query(key_query, data_tuple)
        return new_query
    else :
        return  new_query


def add_limit_offset(query, offset,seize_request):
    """
    Adds LIMIT and OFFSET to an SQL query for pagination.

    :param query: SQL query (string)
    :param seize_request: Number of rows per page
    :param offset: Offset (starting row number)
    :return: Modified SQL query with LIMIT and OFFSET
    """
    if not query:
        print("Error: Empty query")
        return query
    # Check if LIMIT is already present
    if 'LIMIT' in query.upper():
        limit_index = query.upper().find('LIMIT')
        query = query[:limit_index]
    # Add LIMIT and OFFSET
    modified_query = f"{query} LIMIT {seize_request} OFFSET {offset}"
    return modified_query


