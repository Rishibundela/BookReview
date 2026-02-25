from src.auth.schema import UserCreate
from src import API_ROUTE_VERSION

auth_prefix = f"/api/{API_ROUTE_VERSION}/auth/"

def test_user_creation(fake_session, fake_user_service, test_client):

  signup_data = {
    "first_name": "John",
    "last_name": "Doe",
    "username": "john_doe",
    "email": "john.doe@example.com",
    "password": "P@ssw0rd"
  }

  response = test_client.post(
    url = f"{auth_prefix}/signup",
    json = signup_data,
  )

  user_data = UserCreate(**signup_data)


  assert fake_user_service.user_exists_called_once()
  assert fake_user_service.user_exists_called_once_with(signup_data['email'],fake_session)
  assert fake_user_service.create_user_called_once()
  assert fake_user_service. create_user_called_once_with(user_data, fake_session)