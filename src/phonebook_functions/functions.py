from csv import reader, writer
import pandas as pd


COLUMN_NAMES = ['lastname', 'name', 'middle_name', 'organisation',
                'work_phone', 'personal_phone']


def phonebook_show(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        csv_reader = list(reader(file))
    contacts = csv_reader
    rows = [' '.join(item) for item in contacts]
    rows = '\n'.join(rows)
    print(rows)


def phonebook_search(filename):
    print('Введите характеристики контактов, которые вы хотите '
          'посмотреть')
    search_parameters = get_search_parameters()

    result = find_contacts(filename, search_parameters)

    print('\nРезультат поиска:\n')
    if result.empty:
        print('Ваш поиск не дал результатов. Попробуйте задать другие '
              'характеристики для поиска\n')
    else:
        print(result.to_csv(sep=' ', index=False, header=False), '\n')


def phonebook_add(filename):
    print('Введите информацию о новом контакте')
    lastname = input('Введите фамилию: ')
    name = input('Введите имя: ')
    middle_name = input('Введите отчество: ')
    organisation = input('Введите название организации: ')
    work_phone = input('Введите рабочий телефон: ')
    personal_phone = input('Введите личный телефон (сотовый): ')

    new_contact = [lastname, name, middle_name, organisation, work_phone,
                   personal_phone]

    with open(filename, 'a', encoding='utf-8') as file:
        csv_reader = writer(file)
        csv_reader.writerow(new_contact)

        print('Контакт успешно добавлен!\n')


def phonebook_edit(filename):
    print('Введите характеристики контактов, которые вы хотите '
          'отредактировать')
    search_parameters = get_search_parameters()

    search_results = find_contacts(filename, search_parameters)

    if search_results.empty:
        print('\nКонтакта с такими характеристиками нет в телефонной книге. '
              'Попробуйте задать другие характеристики для поиска\n')
    else:
        data_for_edit = get_contacts(filename)
        print('\nНайденые контакты:\n')
        print(search_results.to_csv(sep=' ', index=False, header=False), '\n')
        columns = list(search_results.columns)

        for index, row in search_results.iterrows():
            contact = dict(row)
            print(' '.join(contact.values()))
            edit = input('Редактировать этот контакт? д/н: ')
            if edit == 'д' or edit == 'Д':
                print('\nВведите новые данные в формате '
                      'фамилия:имя:отчество:название_фирмы:рабочий_'
                      'телефон:личный_телефон')
                print('Если какую-то из характеристик не нужно менять, '
                      'оставьте значение пустым\n')
                new_values = input('Введите новые данные: ')
                while True:
                    if new_values.count(':') == 5:
                        break
                    print('Неверный формат ввода. Попробуйте еще раз')
                    print('Например, Иванов:Руслан:::78-90-56:')
                    new_values = input('Введите новые данные: ')

                new_values = new_values.split(':')

                new_contact = zip(columns, new_values)
                new_contact = {k: v for (k, v) in new_contact
                               if v != '' and v != ' '}
                for k, v in contact.items():
                    if k in new_contact.keys():
                        contact[k] = new_contact[k]
                data_for_edit.iloc[index] = list(contact.values())

        data_for_edit.to_csv(filename, index=False, encoding='utf-8',
                             header=False)
        print('Данные в телефонной книге обновлены!')


def find_contacts(filename, search_parameters):
    column_names = COLUMN_NAMES.copy()
    contacts = get_contacts(filename)
    search_parameters = zip(column_names, search_parameters)
    search_parameters = {k: v for (k, v) in search_parameters
                         if v != '' and v != ' '}

    if not search_parameters:
        return contacts

    key = list(search_parameters.keys())[0]
    val = search_parameters[key]
    result = contacts.loc[contacts[key] == val]

    for k, v in search_parameters.items():
        if k == key:
            continue
        result = result.loc[result[k] == v]

    return result


def get_contacts(filename):
    column_names = COLUMN_NAMES.copy()
    contacts = pd.read_csv(filename, encoding='utf-8', names=column_names,
                           header=None)
    return contacts


def get_search_parameters():
    print('Формат ввода: фамилия:имя:отчество:название_фирмы:рабочий_'
          'телефон:личный_телефон')
    print('Если какая-то из характеристик неизвестна, оставьте значение '
          'пустым')
    print('Примеры ввода: \nИванов:Иван:Иванович:Предприятие:123:456'
          '\nСидоров:::Предприятие::789\n')
    search_parameters = input('Введите характеристики для поиска: ')
    while True:
        if search_parameters.count(':') == 5:
            break
        print('Неверный формат ввода. Попробуйте еще раз')
        print('Например, Иванов:Руслан:::78-90-56:')
        search_parameters = input('Введите характеристики для поиска: ')

    return search_parameters.split(':')




