from flask_login import UserMixin, AnonymousUserMixin


class User(UserMixin):
    def __init__(self, user_data) -> None:
        self.user_id = user_data['id']
        self.email = user_data['email']

    def get_id(self):
        return self.user_id

    def is_admin(self):
        return self.admin
