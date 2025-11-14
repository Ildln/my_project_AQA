from pydantic import BaseModel, Field
from typing import Optional, Union

class User(BaseModel):
    full_name: str

data = {'FullName': "Irina Smornova"}

user = User(**data)
print(repr(user))

# from pydantic import BaseModel, Field, EmailStr, ConfigDict
#
# data = {
#     "email": "abc@mail.ru",
#     "bio": None,
#     "age": 12,
# }
#
# data_wo_age = {
#     "email": "abc@mail.ru",
#     "bio": None,
#     "gender": "male",
#     "birthday": "2022"
# }
#
# class UserSchema(BaseModel):
#     email: EmailStr
#     bio: str | None = Field(max_length=100)
#
#     model_config = ConfigDict(extra='forbid')
#
# class UserAgeSchema(UserSchema):
#     age: int = Field(ge=0, le=130)
#
# print(repr(UserSchema(**data_wo_age)))
# # print(repr(UserAgeSchema(**data)))

