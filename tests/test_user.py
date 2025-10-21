from services.user_service import UserService

user_service = UserService()

def test_add_funds():
    user_id = 1
    old_balance = user_service.get_balance(user_id)
    user_service.add_funds(user_id, 200)
    new_balance = user_service.get_balance(user_id)
    assert new_balance == old_balance + 200

def test_get_balance():
    user_id = 2
    balance = user_service.get_balance(user_id)
    assert balance == 300