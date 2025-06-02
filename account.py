
from datetime import datetime

class Account:
    def __init__(self, owner, account_number, initial_balance=0.0):
        self.__owner = owner
        self.__account_number = account_number
        self.__loan = 0.0
        self.__is_frozen = False
        self.__min_balance = 0.0
        self.transactions = []

        if initial_balance > 0:
            self.transactions.append(Transaction(
                datetime.now(), "Initial deposit", initial_balance, 'credit'
            ))
class Transaction:
    def __init__(self, date_time, narration, amount, transaction_type):
        self.date_time = date_time
        self.narration = narration
        self.amount = amount
        if transaction_type.lower() not in ('credit', 'debit'):
            raise ValueError("Transaction type must be 'credit' or 'debit'")
        self.transaction_type = transaction_type.lower()

    def __repr__(self):
        sign = "+" if self.transaction_type == 'credit' else "-"
        return f"{self.date_time} | {self.narration} | {sign}{self.amount}"

    # Encapsulated access
    def get_account_number(self):
        return self.__account_number

    def get_owner(self):
        return self.__owner

    def get_balance(self):
        balance = sum(t.amount if t.transaction_type == 'credit' else -t.amount
                      for t in self.transactions)
        return balance - self.__loan

    # Core functionality
    def deposit(self, amount, narration="Deposit"):
        if self.__is_frozen:
            return "Account is frozen. Cannot deposit funds."
        if amount <= 0:
            return "Deposit amount must be positive."
        self.transactions.append(Transaction(datetime.now(), narration, amount, 'credit'))
        return f"Deposit successful. New balance: {self.get_balance()}"

    def withdraw(self, amount, narration="Withdrawal"):
        if self.__is_frozen:
            return "Account is frozen. Cannot withdraw funds."
        if amount <= 0:
            return "Withdrawal amount must be positive."
        if self.get_balance() - amount < self.__min_balance:
            return f"Cannot withdraw. Balance cannot go below minimum of {self.__min_balance}."
        self.transactions.append(Transaction(datetime.now(), narration, amount, 'debit'))
        return f"Withdrawal successful. New balance: {self.get_balance()}"

    def transfer_funds(self, amount, target_account):
        if self.__is_frozen:
            return "Account is frozen. Cannot transfer funds."
        if not isinstance(target_account, Account):
            return "Target must be an Account instance."
        if amount <= 0:
            return "Transfer amount must be positive."
        if self.get_balance() - amount < self.__min_balance:
            return "Cannot transfer. Insufficient balance."
        self.transactions.append(Transaction(datetime.now(), f"Transfer to {target_account.get_owner()}", amount, 'debit'))
        target_account.transactions.append(Transaction(datetime.now(), f"Transfer from {self.__owner}", amount, 'credit'))
        return f"Transfer successful. New balance: {self.get_balance()}"

    def request_loan(self, amount):
        if amount <= 0:
            return "Loan amount must be positive."
        self.__loan += amount
        return f"Loan approved for {amount}. Total loan balance: {self.__loan}"

    def repay_loan(self, amount):
        if amount <= 0:
            return "Repayment amount must be positive."
        if amount > self.__loan:
            return f"Repayment amount exceeds loan balance of {self.__loan}."
        if self.get_balance() < amount:
            return "Insufficient funds to repay loan."
        self.transactions.append(Transaction(datetime.now(), "Loan repayment", amount, 'debit'))
        self.__loan -= amount
        return f"Loan repayment successful. Remaining loan balance: {self.__loan}"

    def view_account_details(self):
        return f"Account Owner: {self.__owner}\nAccount Number: {self.__account_number}\nCurrent Balance: {self.get_balance()}"

    def change_account_owner(self, new_owner):
        if not new_owner:
            return "New owner name cannot be empty."
        self.__owner = new_owner
        return f"Account owner changed to {self.__owner}."

    def account_statement(self):
        print(f"\n--- Account Statement for {self.__owner} ---")
        for txn in self.transactions:
            print(txn)
        print(f"Loan Balance: {self.__loan}")
        print(f"Current Balance: {self.get_balance()}")
      

    def calculate_interest(self):
        if self.__is_frozen:
            return "Account is frozen. Cannot apply interest."
        interest = self.get_balance() * 0.05
        if interest <= 0:
            return "No interest applied."
        self.transactions.append(Transaction(datetime.now(), "Interest", interest, 'credit'))
        return f"Interest of {interest} applied. New balance: {self.get_balance()}"

    def freeze_account(self):
        self.__is_frozen = True
        return "Account has been frozen."

    def unfreeze_account(self):
        self.__is_frozen = False
        return "Account has been unfrozen."

    def set_minimum_balance(self, amount):
        if amount < 0:
            return "Minimum balance cannot be negative."
        self.__min_balance = amount
        return f"Minimum balance set to {self.__min_balance}"

    def close_account(self):
        self.transactions.clear()
        self.__loan = 0.0
        self.__is_frozen = False
        self.__min_balance = 0.0
        return f"Account for {self.__owner} has been closed. All balances reset."


# Example usage
if __name__ == "__main__":
    acc1 = Account("Jeremy", "123456789", 1000)
    acc2 = Account("Barbara", "987654321", 500)

    print(acc1.deposit(200))
    print(acc1.withdraw(150))
    print(acc1.transfer_funds(300, acc2))
    print(acc1.request_loan(500))
    print(acc1.repay_loan(200))
    print(acc1.view_account_details())
    acc1.account_statement()
    print(acc1.calculate_interest())
    print(acc1.freeze_account())
    print(acc1.deposit(100))
    print(acc1.unfreeze_account())
    print(acc1.deposit(100))
    print(acc1.set_minimum_balance(100))
    print(acc1.withdraw(950))
    print(acc1.close_account())
    acc1.account_statement()
