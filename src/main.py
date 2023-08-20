import os

from phonebook_functions import phonebook_search, phonebook_edit, \
    phonebook_add, phonebook_show


def main():
    filename = os.path.abspath('phonebook.csv')

    def help_text():
        print('1 - посмотреть содержимое телефонной книги')
        print('2 - добавить контакт в телефонную книгу')
        print('3 - найти контакты с заданными характеристиками')
        print('4 - изменить контакт')
        print('5 - завершить работу программы')
        print('любой другой символ - вызвать эту подсказку')

    help_text()
    option = input('\nВыберите действие: ')

    while True:
        if option == '1':
            phonebook_show(filename)
        elif option == '2':
            phonebook_add(filename)
        elif option == '3':
            phonebook_search(filename)
        elif option == '4':
            phonebook_edit(filename)
        elif option == '5':
            break
        else:
            help_text()

        option = input('\nВыберите действие: ')


if __name__ == "__main__":
    main()