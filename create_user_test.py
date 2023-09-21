import sender_stand_request
import data
def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body ['firstName'] = first_name
    return current_body

#Позитивные проверки
def positive_asser(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()['authToken'] != ''
    users_table_response = sender_stand_request.get_users_table()
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
           + user_body["address"] + ",,," + user_response.json()["authToken"]
    assert users_table_response.text.count(str_user) == 1
# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов

def test_create_user_2_letter_in_first_name_get_success_respons():
    positive_asser('Аа')
# Тест 2. Успешное создание пользователя
# Параметр fisrtName состоит из 15 символов
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_asser('Ааааааааааааааа')

#Негативные проверки

def negative_assert(first_name):
    user_body = get_user_body(first_name)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400
    assert response.json()['code'] == 400
    assert response.json()['message'] == "Имя пользователя введено некорректно. " \
                                             "Имя может содержать только русские или латинские буквы, " \
                                             "длина должна быть не менее 2 и не более 15 символов"

# тест 3.
# 1 символ
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert('А')
# тест 4.
# 16 символ
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert('Аааааааааааааааа')
# тест 5.
# Английские буквы
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_asser('QWErty')
# тест 6.
# Русские буквы
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_asser('Мария')
# тест 7.
# Запрещены пробелы
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert('Человек и Ко')
# тест 8.
# Запрещены спецсимволы
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert('"№%:,%')
# тест 9.
# Запрещены цифры
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert('65835')


# Функция для негативной проверки
# В ответе ошибка: "Не все необходимые параметры были переданы"
def negative_assert_no_first_name(user_body):
    # В переменную response сохрани результат вызова функции
    response = sender_stand_request.post_new_user(user_body)

    # Проверь, что код ответа — 400
    assert response.status_code == 400

    # Проверь, что в теле ответа атрибут "code" — 400
    assert response.json()["code"] == 400

    # Проверь текст в теле ответа в атрибуте "message"
    assert response.json()["message"] == "Не все необходимые параметры были переданы"


# Тест 10. Ошибка
# В запросе нет параметра firstName
def test_create_user_no_first_name_get_error_response():
    # Копируется словарь с телом запроса из файла data в переменную user_body
    # Иначе можно потерять данные из исходного словаря
    user_body = data.user_body.copy()
    # Удаление параметра firstName из запроса
    user_body.pop("firstName")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)

# Тест 11. Ошибка
# Параметр fisrtName состоит из пустой строки
def test_create_user_empty_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body("")
    # Проверка полученного ответа
    negative_assert_no_first_name(user_body)

    # Тест 12. Ошибка
    # Тип параметра firstName: число
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    response = sender_stand_request.post_new_user(user_body)
    assert response.status_code == 400

