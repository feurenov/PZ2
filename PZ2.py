import hashlib
from datetime import datetime

# Базовий клас користувача
class User:
    def __init__(self, username, password, is_active=True):
        self.username = username
        self.password_hash = self._hash_password(password)
        self.is_active = is_active

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        return self._hash_password(password) == self.password_hash

# Адміністратор
class Administrator(User):
    def __init__(self, username, password, permissions=None):
        super().__init__(username, password)
        self.permissions = permissions if permissions else []

    def add_permission(self, perm):
        self.permissions.append(perm)

# Звичайний користувач
class RegularUser(User):
    def __init__(self, username, password, last_login=None):
        super().__init__(username, password)
        self.last_login = last_login or datetime.now()

    def update_login_time(self):
        self.last_login = datetime.now()

# Гість
class GuestUser(User):
    def __init__(self, username="guest", password="guest"):
        super().__init__(username, password)
        self.is_active = False  # зазвичай гість обмежений

# Контроль доступу
class AccessControl:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.username] = user

    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user.verify_password(password):
            return user
        return None

# --- Демонстрація ---

# Створюємо об'єкти користувачів
admin = Administrator("admin", "admin123", permissions=["manage_users", "view_logs"])
regular = RegularUser("john_doe", "password123")
guest = GuestUser()

# Контроль доступу
access_control = AccessControl()
access_control.add_user(admin)
access_control.add_user(regular)
access_control.add_user(guest)

# Тест аутентифікації
print("=== Аутентифікація ===")
user = access_control.authenticate_user("john_doe", "password123")
if user:
    print(f"Успішний вхід: {user.username}")
    if isinstance(user, RegularUser):
        user.update_login_time()
        print(f"Останній вхід: {user.last_login}")
else:
    print("Невірний логін або пароль")

# Тест адміністраторських прав
print("\n=== Адмінські дозволи ===")
admin.add_permission("edit_settings")
print(f"Дозволи {admin.username}: {admin.permissions}")