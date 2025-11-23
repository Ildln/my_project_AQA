import requests

from requester.requester import CustomRequester
from utils.endpoints import CREATE_PET_ENDPOINT, GET_PET_ID


class PetApi(CustomRequester):
    """
    Класс для удобной работы с Питомцами API
    """
    def __init__(self, session: requests.Session, base_url: str):
        super().__init__(session=session, base_url=base_url)

    def add_pet(self, pet_data, expected_status=None):
        """
        Создание нового питомца. "POST /pet"
        """
        return self.send_request(
            method="POST",
            endpoint=CREATE_PET_ENDPOINT,
            data=pet_data,
            expected_status=expected_status
        )

    def update_pet(self, pet_data, expected_status=None):
        """
        Обновление существующего питомца. "UPDATE /pet"
        """
        return self.send_request(
            method="PUT",
            endpoint=CREATE_PET_ENDPOINT,
            data=pet_data,
            expected_status=expected_status
        )

    def create_to_pet(self, pet_data, expected_status=None):
        """Создание питомца, передадим в фикстуру и потом получим питомца"""
        return self.send_request(
            method="POST",
            endpoint=CREATE_PET_ENDPOINT,
            data=pet_data,
            expected_status=expected_status
        )

    def get_pet_id(self, pet_id, expected_status=None):
        """
        Получение питомца по id
        """
        return self.send_request(
            method="GET",
            endpoint=GET_PET_ID.format(pet_id=pet_id),
            expected_status=expected_status
        )

    def delete_pet_id(self, pet_id, expected_status=None):
        """
        Удаление питомца по id. "DELETE /pet/{pet_id}
        """
        return self.send_request(
            method="DELETE",
            endpoint=GET_PET_ID.format(pet_id=pet_id),
            expected_status=expected_status
        )