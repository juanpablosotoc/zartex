TEST_CLIENT_ID = 1
# TEST_ADDRESS_ID = 1
TEST_EMAIL = "test@example.com"
TEST_FIRST_NAME = "Test"
TEST_LAST_NAME = "User"
TEST_PASSWORD = "secret"

class DummyResult:
    def __init__(self, val):
        self._val = val

    # SQLAlchemy 1.4-style
    def scalars(self):
        return self

    def one_or_none(self):
        return self._val

    # you can still offer the convenience if you like:
    def scalar_one_or_none(self):
        return self._val

    # for list endpoint (if you ever want to use DummyResult there)
    def all(self):
        return self._val