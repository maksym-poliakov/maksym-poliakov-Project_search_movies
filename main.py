from user_iinterface import UserInterface
from unknownexception import UnknownException
import menu as m


user = None
try:
    user = UserInterface(3)
    while True :
        navigation = user.menu_navigation(m.menu_structure)
except ConnectionError as e :
    print(e)
except UnknownException as err:
    if str(err) == 'EXIT':
        print("Программа завершена.Возвращайтесь еще.")
    elif str(err) == 'request format error':
        print('что то пошло не так')
        while True:
            try:
                navigation = user.menu_navigation(m.menu_structure)
            except ConnectionError as e:
                print(e)
            except UnknownException as err:
                if str(err) == 'EXIT':
                    print("Программа завершена.Возвращайтесь еще.")
                    break
                elif str(err) == 'request format error':
                    print('что то пошло не так')
                    continue


