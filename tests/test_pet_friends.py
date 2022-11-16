from api import PetFriends
from settings import *
import os

pf = PetFriends()

# Эти тесты повторил из курса. Ниже будут те, которые писал сам


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result


def test_get_all_pets_with_valid_key(filter=""):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0


def test_add_new_pet_with_valid_data(name="Вася", animal_type="Кошак", age="4", pet_photo="images/cat.jpg"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result["name"] == name


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "Пушок", "Кот", "2", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets["pets"][0]["id"]
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_information_about_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


# Эти тесты писал сам


def test_get_api_key_with_invalid_email(email=invalid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "found in database" in result


def test_get_api_key_with_invalid_password(email=valid_email, password=invalid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "found in database" in result


def test_adding_new_pet_simple_with_invalid_auth_key(name="Петрович", animal_type="Трактор", age=15):
    status, result = pf.add_new_pet_simple(invalid_auth_key, name, animal_type, age)
    assert status == 403
    assert "provide" in result


def test_get_all_my_pets_with_valid_key(filter="my_pets"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0


def test_delete_self_pet_with_invalid_auth_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets["pets"]) == 0:
        pf.add_new_pet(auth_key, "Пушок", "Кот", "2", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets["pets"][0]["id"]
    status, result = pf.delete_pet(invalid_auth_key, pet_id)
    assert status == 403
    assert "provide" in result


def test_add_wrong_photo_format_for_self_pet(pet_photo="images/giphy.gif"):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets["pets"][0]["id"]
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 500  # Должна быть 400
    assert "server" in result


def test_adding_new_pet_simple_with_invalid_data(name=123, anymal_type=321, age='3'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_simple(auth_key, name, anymal_type, age)
    assert status == 200  # Должна быть 400
    assert "name" in result


def test_update_pet_of_other_user(name="Копатыч", animal_type="Медведь", age=8):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    pet_id = all_pets["pets"][0]["id"]
    staus, result = pf.update_information_about_pet(auth_key, pet_id, name, animal_type, age)
    assert staus == 200  # Должна быть 403
    assert "age" in result


def test_delete_pet_of_other_user():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    pet_id = all_pets["pets"][0]["id"]
    status, result = pf.delete_pet(auth_key, pet_id)
    assert status == 200  # Должна быть 403


def test_adding_new_pet_with_blank_name(name="", animal_type="Cat", age="4", pet_photo="images/cat.jpg"):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200  # Должна быть 400
    print(result)
    assert "name" in result
