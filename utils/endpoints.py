# utils / endpoints.py


# Базовые эндпоинты для User API
CREATE_USER_ENDPOINT = "/user"          # POST /user
GET_USER_BY_NAME_ENDPOINT = "/user/{username}"  # GET /user/{username}
LOGIN_USER_ENDPOINT = "/user/login"     # GET /user/login?username&password
LOGOUT_USER_ENDPOINT = "/user/logout"   # GET /user/logout (если понадобиться)


# Базовые эндпоинты для Store API
CREATE_STORE_ORDER_ENDPOINT = "/store/order"     # POST /store/order
GET_STORE_INVENTORY_ENDPOINT = "/store/inventory"     # GET /store/inventory
GET_STORE_ORDER_ID_ENDPOINT = "/store/order/{order_id}"  # GET/DELETE  store/order/{orderId}


# Базовые эндпоинты для Pet API
CREATE_PET_ENDPOINT = "/pet"    # POST /pet
UPDATE_PET_ENDPOINT = "/pet"    # PUT /pet
GET_PET_ID = "/pet/{pet_id}"    # GET/DELETE  /pet/{petId}