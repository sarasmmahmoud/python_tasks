import psycopg2
import hashlib
from getpass import getpass
from decimal import Decimal


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="loan_project",
            user="iti",
            password="123456",
            host="localhost"
        )
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None, fetch=False):
        self.cursor.execute(query, params or [])
        if fetch:
            return self.cursor.fetchall()
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()


class LoanApp:
    def __init__(self):
        self.db = Database()
        self.user_id = None

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self):
        username = input("Enter a new username: ")
        password = getpass("Enter password: ")
        hashed = self.hash_password(password)
        try:
            self.db.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed))
            print("✅ Registration successful!")
        except Exception as e:
            print("❌ Username already exists.")

    def login(self):
        username = input("Enter username: ")
        password = getpass("Enter password: ")
        hashed = self.hash_password(password)
        result = self.db.execute(
            "SELECT id FROM users WHERE username = %s AND password = %s",
            (username, hashed), fetch=True
        )
        if result:
            self.user_id = result[0][0]
            print("✅ Login successful!")
            return True
        else:
            print("❌ Invalid credentials.")
            return False

    def apply_loan(self):
        try:
            amount = float(input("Enter loan amount: "))
            self.db.execute("INSERT INTO loans (user_id, amount, balance) VALUES (%s, %s, %s)",
                            (self.user_id, amount, amount))
            print("✅ Loan application submitted.")
        except ValueError:
            print("❌ Invalid amount.")

    def make_payment(self):
        loan = self.get_user_loan()
        if not loan:
            print("❌ No loan found.")
            return
        try:
            amount = Decimal(input("Enter payment amount: "))
            if amount <= 0:
                print("❌ Amount must be positive.")
                return
            if amount > loan[3]:
                print("❌ Payment exceeds balance.")
                return
            new_balance = loan[3] - amount
            self.db.execute("UPDATE loans SET balance = %s WHERE id = %s", (new_balance, loan[0]))
            self.db.execute("INSERT INTO payments (loan_id, amount) VALUES (%s, %s)", (loan[0], amount))
            print("✅ Payment recorded.")
        except ValueError:
            print("❌ Invalid amount.")

    def check_balance(self):
        loan = self.get_user_loan()
        if loan:
            print(f"💰 Current loan balance: {loan[3]}")
        else:
            print("❌ No active loan.")

    def payment_history(self):
        loan = self.get_user_loan()
        if loan:
            payments = self.db.execute(
                "SELECT amount, payment_date FROM payments WHERE loan_id = %s",
                (loan[0],), fetch=True
            )
            print("📜 Payment History:")
            for amount, date in payments:
                print(f"- {date.date()} : {amount}")
        else:
            print("❌ No payment history found.")

    def get_user_loan(self):
        result = self.db.execute("SELECT * FROM loans WHERE user_id = %s", (self.user_id,), fetch=True)
        return result[0] if result else None

    def close(self):
        self.db.close()

    def menu(self):
        while True:
            print("\n1. Apply for a loan\n2. Make a payment\n3. Check balance\n4. View payment history\n5. Logout")
            choice = input("Choose an option: ")
            if choice == '1':
                self.apply_loan()
            elif choice == '2':
                self.make_payment()
            elif choice == '3':
                self.check_balance()
            elif choice == '4':
                self.payment_history()
            elif choice == '5':
                self.close()
                break
            else:
                print("❌ Invalid choice.")


def main():
    app = LoanApp()
    while True:
        print("\n--- Loan Application System ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == '1':
            if app.login():
                app.menu()
        elif choice == '2':
            app.register()
        elif choice == '3':
            app.close()
            break
        else:
            print("❌ Invalid choice.")

if __name__ == "__main__":
    main()