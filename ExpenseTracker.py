import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QMessageBox
from PyQt5.QtGui import QDoubleValidator

class ExpenseTracker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Expense Tracker")

        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Load data
        self.load_data()

        # Calculate total expenses
        self.total_expenses = sum(sum(amount for _, amount in expenses) for expenses in self.expenses.values())

        # Money input
        self.money_input = QLineEdit()
        self.money_input.setPlaceholderText("Enter money amount")
        self.money_input.setValidator(QDoubleValidator(0, 1000000000, 2))
        self.layout.addWidget(self.money_input)

        # Add money button
        self.add_money_button = QPushButton("Add Money")
        self.add_money_button.clicked.connect(self.add_money)
        self.layout.addWidget(self.add_money_button)

        # Expense name input
        self.expense_name_input = QLineEdit()
        self.expense_name_input.setPlaceholderText("Enter expense name")
        self.layout.addWidget(self.expense_name_input)

        # Expense amount input
        self.expense_amount_input = QLineEdit()
        self.expense_amount_input.setPlaceholderText("Enter expense amount")
        self.expense_amount_input.setValidator(QDoubleValidator(0, 1000000000, 2))
        self.layout.addWidget(self.expense_amount_input)

        # Category input
        self.category_input = QComboBox()
        self.category_input.addItems(["Single", "Weekly", "Monthly", "Yearly"])
        self.category_input.currentIndexChanged.connect(self.update_category_expenses)
        self.layout.addWidget(self.category_input)

        # Add expense button
        self.add_expense_button = QPushButton("Add Expense")
        self.add_expense_button.clicked.connect(self.add_expense)
        self.layout.addWidget(self.add_expense_button)

        # Remove expense button
        self.remove_expense_button = QPushButton("Remove Last Expense")
        self.remove_expense_button.clicked.connect(self.remove_expense)
        self.layout.addWidget(self.remove_expense_button)

        # View all expenses button
        self.view_all_expenses_button = QPushButton("View All Expenses")
        self.view_all_expenses_button.clicked.connect(self.view_all_expenses)
        self.layout.addWidget(self.view_all_expenses_button)

        # Total money label
        self.total_money_label = QLabel(f"Total Money: ${format(self.money, '.2f')}")
        self.layout.addWidget(self.total_money_label)

        # Total expenses label
        self.total_expenses_label = QLabel(f"Total Expenses: ${format(self.total_expenses, '.2f')}")
        self.layout.addWidget(self.total_expenses_label)

        # Category expenses label
        self.category_expenses_label = QLabel("Category Expenses: $0.00")
        self.layout.addWidget(self.category_expenses_label)

    def load_data(self):
        try:
            with open('data.json', 'r') as f:
                data = json.load(f)
                self.money = data.get('money', 0.00)
                self.expenses = data.get('expenses', {
                                        "Single": [],
                    "Weekly": [],
                    "Monthly": [],
                    "Yearly": []
                })
        except Exception as e:
            self.money = 0.00
            self.expenses = {
                "Single": [],
                "Weekly": [],
                "Monthly": [],
                "Yearly": []
            }

    def save_data(self):
        data = {
            'money': self.money,
            'expenses': self.expenses
        }
        with open('data.json', 'w') as f:
            json.dump(data, f)

    def add_money(self):
        money = float(self.money_input.text())
        self.money += money

        # Reset input
        self.money_input.setText("")

        # Update total money
        self.total_money_label.setText(f"Total Money: ${format(self.money, '.2f')}")

        # Save data
        self.save_data()

    def add_expense(self):
        expense_name = self.expense_name_input.text()
        expense_amount_text = self.expense_amount_input.text()

        if not expense_name:
            QMessageBox.warning(self, "Input Error", "Please enter an expense name.")
            return

        if not expense_amount_text:
            QMessageBox.warning(self, "Input Error", "Please enter an expense amount.")
            return

        expense_amount = float(expense_amount_text)
        category = self.category_input.currentText()
        self.expenses[category].append((expense_name, expense_amount))

        # Add to total expenses
        self.total_expenses += expense_amount

        # Subtract expense from total money
        self.money -= expense_amount

        # Reset input
        self.expense_name_input.setText("")
        self.expense_amount_input.setText("")

        # Update total money
        self.total_money_label.setText(f"Total Money: ${format(self.money, '.2f')}")

        # Update total expenses
        self.total_expenses_label.setText(f"Total Expenses: ${format(self.total_expenses, '.2f')}")

        # Update category expenses
        self.update_category_expenses()

        # Save data
        self.save_data()


    def remove_expense(self):
        category = self.category_input.currentText()
        if self.expenses[category]:
            _, expense_amount = self.expenses[category].pop()

            # Subtract from total expenses
            self.total_expenses -= expense_amount

            # Add expense back to total money
            self.money += expense_amount

            # Update total money
            self.total_money_label.setText(f"Total Money: ${format(self.money, '.2f')}")

            # Update total expenses
            self.total_expenses_label.setText(f"Total Expenses: ${format(self.total_expenses, '.2f')}")

            # Update category expenses
            self.update_category_expenses()

            # Save data
            self.save_data()

    def update_category_expenses(self):
        category = self.category_input.currentText()
        total = sum(amount for _, amount in self.expenses[category])
        self.category_expenses_label.setText(f"{category} Expenses: ${format(total, '.2f')}")

    def view_all_expenses(self):
        category = self.category_input.currentText()
        expenses = self.expenses[category]

        message = "\n".join([f"{name}: ${format(amount, '.2f')}" for name, amount in expenses])

        QMessageBox.information(self, f"{category} Expenses", message)

if __name__ == "__main__":
    app = QApplication([])

    window = ExpenseTracker()
    window.show()

    app.exec_()

