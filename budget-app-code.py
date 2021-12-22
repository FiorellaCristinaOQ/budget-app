def create_spend_chart(categories):
    output = 'Percentage spent by category\n'
    output_lst = []
    categories_spent = []
    total_spent = 0
    previous_total_spent = 0
    names_lst = []
    for i in categories: # Cada i es un objeto
        for j in i.ledger: # Cada j es un dict en la lista ledger
            if j["amount"] < 0:
                total_spent += -j["amount"]
        categories_spent.append(total_spent - previous_total_spent)
        previous_total_spent = total_spent
        names_lst.append(i.element)
    # En este punto ya tenemos el total_spent y los gastos por cada categoría en una lista
    for i in range(len(categories)):
        percentage_spent = categories_spent[i]*100/total_spent
        output_lst.append({"name":categories[i].element, "%":round(percentage_spent,-1)})
    n = 100
    while n >= 0:
        for i in output_lst:
            if i["%"] >= n and i == output_lst[0]:
                output += ' '*(3 - len(str(n))) + str(n) + '|' + ' ' + 'o' + ' '
            elif i["%"] < n and i == output_lst[0]:
                output += ' '*(3 - len(str(n))) + str(n) + '|' + ' '*3
            elif i["%"] >= n and i != output_lst[0]:
                output += ' ' + 'o' + ' '
            else:
                output += '   '
        output += ' ' + '\n'
        n = n - 10
    output += '    ' + '-'*3*len(output_lst) + '-\n'
    longest_name =  max(names_lst, key=len) # Encuentra la palabra más larga de una lista de strings
    for i in range(len(longest_name)):
        for j in names_lst:
            if j == names_lst[0]:
                output += '    '
            if i < len(j):
                output += ' ' + j[i] + ' '
            else:
                output += '   '
        output += '\n'
    return output
class Category:
    def __init__(self, element):
        self.element = element
        self.ledger = []
    def deposit(self, amount, description = ''):
        self.ledger.append({"amount": amount, "description": description})
    def withdraw(self, amount, description = ''):
        if(self.check_funds(amount) == True):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False
    def get_balance(self): # It's never gonna be negative
        balance = 0
        for i in self.ledger:
            # Cada elemento en ledger es un dict -> usar la clave
            balance += i["amount"]
        return balance
    def transfer(self, amount, category):
        if(self.check_funds(amount) == True):
            self.withdraw(amount, 'Transfer to ' + category.element)
            category.deposit(amount, "Transfer from " + self.element)
            return True
        return False
    def check_funds(self, amount):
        if(self.get_balance() >= amount):
            return True
        return False
    def __str__(self): # Este método se llama cuando se escribe print(obj), no necesita obj.__str__()
        title_length = len(self.element)
        if(title_length % 2 == 0):
            string_length = (30 - title_length)/2
            string = '*'*int(string_length) + self.element + '*'*int(string_length) + '\n'
        else:
            string_length = (30 - title_length)/2 + 0.5
            string = '*'*int(string_length) + self.element + '*'*int(string_length - 1) + '\n'
        withdraw_total = 0
        for i in self.ledger:
            count = 0
            withdraw_total += i["amount"]
            for j in i["description"]: # Por cada letra en la descripción
                if count < 23:
                    string += j
                else:
                    break
                count += 1
            spaces_amount = 7 - (len(str(int(i["amount"]))) + 3)
            string += ' '*(23 - count) + ' '*spaces_amount + f'{float(i["amount"]):.2f}' + '\n'
        string += 'Total: ' + f'{float(withdraw_total):.2f}'
        return string
# Crear objetos    
food = Category("Food")
entertainment = Category("Entertainment")
business = Category("Business")
# Test deposit
food.deposit(900, "deposit")
food.deposit(45.56)
# Test withdraw
food.withdraw(45.67, "milk, cereal, eggs, bacon, bread")
food.withdraw(45.67)
food.withdraw(1000)
# Test get balance
print(food.get_balance())
print(entertainment.get_balance())
# Test transfer
food.transfer(20, entertainment)
print("Transferencia de 20 de food a entertainment")
print(food.get_balance())
print(entertainment.get_balance())
print("Transferencia de 200 de entertainment a food")
entertainment.transfer(200, food)
print(food.get_balance())
print(entertainment.get_balance())
# Test check_funds
food.deposit(10, "deposit")
print('Entertainment check funds (10): ',entertainment.check_funds(10))
print('Business check funds (10): ',business.check_funds(10))
# Test str method
print(food)
# Test create a spend chart
print(create_spend_chart([business, food, entertainment]))