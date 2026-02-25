from src import API_ROUTE_VERSION

book_prefix = f"/api/{API_ROUTE_VERSION}/books/"

def test_get_all_books(fake_session, fake_book_service, test_client):
  response = test_client.get(
    url=f"{book_prefix}"
  )

  assert fake_book_service.get_all_books_called_once()
  assert fake_book_service.get_all_books_called_once_with(fake_session) 