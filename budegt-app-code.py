def create_spend_chart(categories):
    output = ''
    output_lst = []
    percentage = 100
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
            if i["%"] >= n:
                output += str(n) + '|' + ' ' + 'o' + ' '
            else:
                output += str(n) + '|' + ' '*3
        output += ' ' + '\n'
        n = n - 10
    output += '    ' + '-'*3*len(output_lst) + '-\n'
    longest_name =  max(names_lst, key=len) # Encuentra la palabra más larga de una lista de strings
    for i in range(len(longest_name)):
        for j in names_lst:
            if i < len(j):
                if j == names_lst[0]:
                    output += '   '
                output += ' ' + j[i] + ' '
    return output
class Category:
    def __init__(self, element):
        print("Creado")
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
        if(self.get_balance >= amount):
            return True
        return False
    def __str__(self): # Este método se llama cuando se escribe print(obj), no necesita obj.__str__()
        title_length = len(self.element)
        if(title_length % 2 == 0):
            string_length = (30 - title_length)/2
            string = '*'*string_length + self.element + '*'*string_length + '\n'
        else:
            string_length = (30 - title_length)/2 + 0.5
            string = '*'*string_length + self.element + '*'*(string_length - 1) + '\n'
        for i in self.ledger:
            count = 0
            for j in i["description"]: # Por cada letra en la descripción
                if count < 23:
                    string += j
                else:
                    break
            string += round(i["amount"],2) + '\n'
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
# Test get balance
food.get_balance()