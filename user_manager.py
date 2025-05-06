class UserManager:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def register_user(self, user_id, name):
        self.cursor.execute("SELECT user_id FROM Users WHERE user_id = ?", (user_id,))
        if self.cursor.fetchone():
            print(f"User ID {user_id} already exists.")
            return False
        self.cursor.execute('''
            INSERT INTO Users (user_id, name) VALUES (?, ?)
        ''', (user_id, name))
        self.conn.commit()
        print(f"User '{name}' registered successfully.")
        return True

    def display_users(self):
        self.cursor.execute("SELECT * FROM Users")
        users = self.cursor.fetchall()
        if not users:
            print("No users registered.")
            return
        print("\nRegistered Users:")
        for user in users:
            print(f"User ID: {user[0]}, Name: {user[1]}")