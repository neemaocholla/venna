# Add the following methods to the Account class
class Account:
    def __init__(self, owner, initial_deposit=0):
        self.owner = owner
        self.deposits = []
        self.withdrawals = []
        self.loan = 0
        self.is_frozen = False
        self.min_balance = 0
        if initial_deposit > 0:
            self.deposits.append(initial_deposit)


# Deposit: method to deposit funds, store the deposit and return a message with the new balance to the customer. It should only accept positive amounts.
    def deposit(self, amount):
        """Deposit funds if account is not frozen and amount is positive."""
        if self.is_frozen:
            return "Account is frozen. Cannot deposit funds."
        if amount <= 0:
            return "Deposit amount must be positive."
        self.deposits.append(amount)
        return f"Deposit successful. New balance: {self.get_balance():.2f}"


# Withdraw: method to withdraw funds, store the withdrawal and return a message with the new balance to the customer. An account cannot be overdrawn.
    def withdraw(self, amount):
        """Withdraw funds if account is not frozen, amount is positive, and balance after withdrawal respects min balance."""
        if self.is_frozen:
            return "Account is frozen. Cannot withdraw funds."
        if amount <= 0:
            return "Withdrawal amount must be positive."
        current_balance = self.get_balance()
        if current_balance - amount < self.min_balance:
            return f"Cannot withdraw. Balance cannot go below minimum balance of {self.min_balance:.2f}."
        if amount > current_balance:
            return "Insufficient funds. Cannot overdraw account."
        self.withdrawals.append(amount)
        return f"Withdrawal successful. New balance: {self.get_balance():.2f}"

# Transfer Funds: Method to transfer funds from one account to an instance of another account.
    def transfer_funds(self, amount, target_account):
        """Transfer funds to another Account instance."""
        if self.is_frozen:
            return "Account is frozen. Cannot transfer funds."
        if not isinstance(target_account, Account):
            return "Target account must be a valid Account instance."
        if amount <= 0:
            return "Transfer amount must be positive."
        if self.get_balance() - amount < self.min_balance:
            return f"Cannot transfer. Balance cannot go below minimum balance of {self.min_balance:.2f}."
        if amount > self.get_balance():
            return "Insufficient funds to transfer."
      
        self.withdrawals.append(amount)

        target_account.deposits.append(amount)
        return (f"Transfer successful. New balance: {self.get_balance():.2f} "
                f"Transferred {amount:.2f} to {target_account.owner}.")

 # Get Balance: Method to calculate an account balance from deposits and withdrawals.               
    def get_balance(self):
        """Calculate balance from deposits, withdrawals, and loan."""
        total_deposits = sum(self.deposits)
        total_withdrawals = sum(self.withdrawals)
        return total_deposits - total_withdrawals - self.loan


# Request Loan: Method to request a loan amount.
    def request_loan(self, amount):
        """Request a loan amount."""
        if amount <= 0:
            return "Loan amount must be positive."

        self.loan += amount
        return f"Loan approved for {amount:.2f}. Total loan balance: {self.loan:.2f}"


# Repay Loan: Method to repay a loan with a given amount.
    def repay_loan(self, amount):
        """Repay a loan with a given amount."""
        if amount <= 0:
            return "Repayment amount must be positive."
        if amount > self.loan:
            return f"Repayment amount exceeds loan balance of {self.loan:.2f}."
        if amount > self.get_balance():
            return "Insufficient funds to repay loan."
        self.withdrawals.append(amount)
        self.loan -= amount
        return f"Loan repayment successful. Remaining loan balance: {self.loan:.2f}"

# View Account Details: Method to display the account owner's details and current balance.
    def view_account_details(self):
        """Display account owner and current balance."""
        return f"Account Owner: {self.owner}\nCurrent Balance: {self.get_balance():.2f}"

# Change Account Owner: Method to update the account owner's name.
    def change_account_owner(self, new_owner):
        """Update the account owner's name."""
        if not new_owner:
            return "New owner name cannot be empty."
        self.owner = new_owner
        return f"Account owner changed to {self.owner}."

# Account Statement: Method to generate a statement of all transactions in an account. (Print using a for loop).
    def account_statement(self):
        """Generate a statement of all transactions."""
        print(f"Account Statement for {self.owner}:")
        print("Deposits:")
        for i, amount in enumerate(self.deposits, 1):
            print(f"  {i}. +{amount:.2f}")
        print("Withdrawals:")
        for i, amount in enumerate(self.withdrawals, 1):
            print(f"  {i}. -{amount:.2f}")
        print(f"Loan Balance: {self.loan:.2f}")
        print(f"Current Balance: {self.get_balance():.2f}")


# Interest Calculation: Method to calculate and apply an interest to the balance. Use 5% interest. 
    def calculate_interest(self):
        """Calculate and apply 5% interest to the balance."""
        if self.is_frozen:
            return "Account is frozen. Cannot apply interest."
        interest = self.get_balance() * 0.05
        if interest <= 0:
            return "No interest applied due to non-positive balance."
        self.deposits.append(interest)
        return f"Interest of {interest:.2f} applied. New balance: {self.get_balance():.2f}"


# Freeze/Unfreeze Account: Methods to freeze and unfreeze the account for security reasons.
    def freeze_account(self):
        """Freeze the account."""
        self.is_frozen = True
        return "Account has been frozen."

    def unfreeze_account(self):
        """Unfreeze the account."""
        self.is_frozen = False
        return "Account has been unfrozen."

# Set Minimum Balance: Method to enforce a minimum balance requirement. You cannot withdraw if your balance is less than this amount.Close Account: Method to close the account and set all balances to zero and empty all transactions.
    def set_minimum_balance(self, amount):
        """Set minimum balance requirement."""
        if amount < 0:
            return "Minimum balance cannot be negative."
        self.min_balance = amount
        return f"Minimum balance set to {self.min_balance:.2f}."

    def close_account(self):
        """Close account by resetting balances and transactions."""
        self.deposits.clear()
        self.withdrawals.clear()
        self.loan = 0
        self.min_balance = 0
        self.is_frozen = False
        return f"Account for {self.owner} has been closed. All balances reset."

if __name__ == "__main__":
    acc1 = Account("Jeremy", 1000)
    acc2 = Account("Barbara", 500)

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
