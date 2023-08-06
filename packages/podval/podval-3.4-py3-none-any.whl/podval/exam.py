#1
def fchyaks():
    print('''#Используя лямбда-функцию, найдите все числа в заданном списке, которые являются числами Фибоначчи.

is_fibo = (lambda a: lambda v,fib=0,n=1: a(a,v,fib,n))(lambda f,value,fib,n: f(f,value,fib+n,fib) if fib < value else fib==value)

# Заданный список чисел
numbers = list(range(100))

# Использование лямбда-функции для фильтрации чисел Фибоначчи из списка
fibonacci_numbers = list(filter(is_fibo, numbers))

# Вывод результатов
print(fibonacci_numbers)''')
    
def kkemi():
    print('''#Напишите программу для сортировки заданного списка кортежей по разности между максимальным и минимальным элементами каждого кортежа.

# Заданный список кортежей
tuples = [(3, 8, 2), (1, 5, 10), (4, 7, 6), (2, 9, 1)]

# Функция для получения разности между максимальным и минимальным элементами кортежа
get_diff = lambda tuple: max(tuple) - min(tuple)

# Сортировка списка кортежей по разности между максимальным и минимальным элементами
sorted_tuples = sorted(tuples, key=get_diff)

# Вывод отсортированного списка кортежей
print(sorted_tuples)''')
    
def bstsk():
    print('''#Используя лямбда-функцию, найдите все строки в заданном списке строк, которые содержат только согласные буквы.

# Заданный список строк
strings = ['hll', 'wrld', 'bye', 'peace', 'aisd', 'sht']

# Функция для проверки строки на наличие только согласных букв
is_consonant = lambda s: all(letter.lower() not in 'aeiou' for letter in s)

# Фильтрация списка строк с помощью лямбда-функции
consonant_strings = list(filter(is_consonant, strings))

# Вывод результатов
print(consonant_strings)''')
    
def sieui():
    print('''#Реализовать функцию, которая находит максимальный элемент в двусвязном списке и удаляет его из списка. 

#реализация двусвязного списка
class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            new_node.prev = current

    def delete_node(self, data):
        if self.head is None:
            return
        elif self.head.data == data:
            if self.head.next is not None:
                self.head = self.head.next
                self.head.prev = None
            else:
                self.head = None
        else:
            current = self.head
            while current.next is not None and current.next.data != data:
                current = current.next
            if current.next is None:
                return
            else:
                current.next = current.next.next
                if current.next is not None:
                    current.next.prev = current

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        if self.head == None:
            return f"Двусвязный список пустой"
        current = self.head
        dllist_str = ""
        while current:
            dllist_str += " ⇄ " + str(current.data)
            current = current.next
        return dllist_str.lstrip(" ⇄ ") 
    
#программа

def find_and_remove_max(dllist):
    if dllist.head is None:
        return None

    current = dllist.head
    max_node = current

    # Находим узел с максимальным значением
    while current.next:
        current = current.next
        if current.data > max_node.data:
            max_node = current

    # Удаляем узел с максимальным значением
    if max_node.prev:
        max_node.prev.next = max_node.next
    else:
        dllist.head = max_node.next

    if max_node.next:
        max_node.next.prev = max_node.prev

    return max_node.data

#проверка
dllist = DoublyLinkedList()
dllist.add_node(5)
dllist.add_node(10)
dllist.add_node(8)
dllist.add_node(3)

print("Изначальный список:", dllist)
max_value = find_and_remove_max(dllist)
print("Максимальное значение:", max_value)
print("Список после удаления максимального элемента:", dllist)''')

#2    
def lpschs():
    print('''#Отфильтровать список целых чисел на простые и составные числа с помощью лямбда-функции.

# Заданный список целых чисел
numbers = [2, 3, 4, 5, 6, 7, 8, 9, 10]

# Лямбда-функция для проверки числа на простоту
is_prime = lambda num: all(num % i != 0 for i in range(2, int(num**0.5) + 1)) and num > 1

# Фильтрация списка на простые числа
prime_numbers = list(filter(is_prime, numbers))

# Фильтрация списка на составные числа
composite_numbers = list(filter(lambda num: not is_prime(num), numbers))

prime_numbers, composite_numbers''')
    
def susdp():
    print('''#Для удаления определённых символов из заданной строки используйте лямбда-функцию. Пример: дана строка 'hello world', удалить символы 'l' и 'o' → 'he wrd'.

string = 'hello world'
characters_to_remove = ['l', 'o']

# Функция для удаления символов из строки
remove_characters = lambda s: ''.join([char for char in s if char not in characters_to_remove])

# Применение лямбда-функции к строке
result = remove_characters(string)

# Вывод результата
print(result)''')
    
def nipsu():
    print('''#Используя лямбда-функцию, проверить, является ли указанный список палиндромом или нет

is_pal = lambda x: (x == (x[::-1]))

lst1 = [1,2,1]
lst2 = [1,2,3]
lst3 = ['a','b','a']
lst4 = ['a','b','c']

is_pal(lst1), is_pal(lst2), is_pal(lst3), is_pal(lst4)''')

def nsitn():
    print('''#Реализовать функцию, которая проверяет, является ли двусвязный список палиндромом (элементы списка читаются одинаково как слева направо, так и справа налево)

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            new_node.prev = current

    def delete_node(self, data):
        if self.head is None:
            return
        elif self.head.data == data:
            if self.head.next is not None:
                self.head = self.head.next
                self.head.prev = None
            else:
                self.head = None
        else:
            current = self.head
            while current.next is not None and current.next.data != data:
                current = current.next
            if current.next is None:
                return
            else:
                current.next = current.next.next
                if current.next is not None:
                    current.next.prev = current

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        if self.head == None:
            return f"Двусвязный список пустой"
        current = self.head
        dllist_str = ""
        while current:
            dllist_str += " ⇄ " + str(current.data)
            current = current.next
        return dllist_str.lstrip(" ⇄ ")   
    
#программа

def is_palindrome(dllist):
    if dllist.head is None:
        return True

    # Получаем длину списка
    length = len(dllist)

    # Объявляем два указателя, один идет с начала списка, другой - с конца
    front = dllist.head
    back = dllist.head

    # Перемещаем указатель back к последнему элементу списка
    while back.next:
        back = back.next

    # Проверяем значения элементов, двигая указатели front и back
    while front != back and front.prev != back:
        if front.data != back.data:
            return False
        front = front.next
        back = back.prev

    return True

dllist = DoublyLinkedList()
dllist.add_node(1)
dllist.add_node(2)
dllist.add_node(3)
dllist.add_node(2)
dllist.add_node(1)

print(dllist)
print(is_palindrome(dllist))  # Вывод: True

dllist.add_node(4)
print('\n', dllist)
print(is_palindrome(dllist))  # Вывод: False''')

#3    
def fuvko():
    print('''#Создайте класс «Банк» с атрибутами название, адрес и список клиентов.
Каждый клиент представлен классом «Клиент» с атрибутами имя,
фамилия, номер счета и баланс. Напишите методы для добавления
клиента в банк, удаления клиента из банка и вывода информации
о банке в виде «Банк '{название}', адрес - {адрес}, клиенты - {список
клиентов}». Используйте магический метод __str__ для вывода
информации о клиенте в удобном формате.

class Bank:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.clients = []
    
    def add_client(self, client):
        self.clients.append(client)
    
    def remove_client(self, client):
        if client in self.clients:
            self.clients.remove(client)
        else:
            print('Клиента нет в базе')
    
    def __str__(self):
        client_info = '\n'.join(str(client) for client in self.clients)
        return f"Банк '{self.name}', адрес - {self.address}, клиенты:\n{client_info}"  

class Client:
    def __init__(self, name, surname, account, balance):
        self.name = name
        self.surname = surname
        self.account = account
        self.balance = balance 
    def __str__(self):
        return f"Клиент: {self.name} {self.surname}, Номер счета: {self.account}, Баланс: {self.balance}"
    
bank = Bank("MFBank", "123 Ryasansky Avenue")

client1 = Client("Russell", "Westbrook", "8954792453", 10000)
client2 = Client("Busta", "Rhimes", "4472933908", 99999)

bank.add_client(client1)
bank.add_client(client2)

print(bank)''')
    
def sedkya():
    print('''# Дан стек. Необходимо проверить, содержит ли он хотя бы один элемент,
# который является квадратом другого элемента стека.

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if self.is_empty():
            return None
        else:
            popped_item = self.head.data
            self.head = self.head.next
            return popped_item

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.head.data

    def __str__(self):
        current = self.head
        stack_str = ""
        while current:
            stack_str += str(current.data) + " → "
            current = current.next
        return stack_str.rstrip(" → ")

#программа

def square(stack):
    if stack.is_empty():
        return False

    # Создаем множество для хранения уникальных элементов стека
    unique_elements = set()

    # Проходим по всем элементам стека
    current = stack.head
    while current:
        # Проверяем, является ли текущий элемент квадратом другого элемента
        if current.data ** 2 in unique_elements:
            return True

        # Добавляем текущий элемент в множество уникальных элементов
        unique_elements.add(current.data)

        current = current.next

    return False

lst1 = [1,2,3,5,9,25]
lst2 = [1,3,5,7,11,13,17]

stack1 = Stack()
stack2 = Stack()

for item in lst1:
    stack1.push(item)

for item in lst2:
    stack2.push(item)

print(f'Стек 1: {stack1}, {square(stack1)}')
print(f'Стек 2: {stack2}, {square(stack2)}')''')

#4    
def hzsap():
    print('''# Создайте класс АВТОМОБИЛЬ с методами, позволяющими вывести на
# экран информацию об автомобиле, а также определить, подходит ли
# данный автомобиль для заданных условий. Создайте дочерние классы
# ЛЕГКОВОЙ (марка, модель, год выпуска, объем двигателя, тип
# топлива), ГРУЗОВОЙ (марка, модель, год выпуска, грузоподъемность),
# ПАССАЖИРСКИЙ (марка, модель, год выпуска, количество мест) со
# своими методами вывода информации на экран и определения
# соответствия заданным условиям. Создайте список автомобилей,
# выведите полную информацию из базы на экран, а также организуйте
# поиск автомобилей с заданными характеристиками.

class Car:
    def __init__(self, brand, model, year, engine_capacity):
        self.brand = brand
        self.model = model
        self.year = year
        self.engine_capacity = engine_capacity

    def display_info(self):
        print(f"Марка: {self.brand}")
        print(f"Модель: {self.model}")
        print(f"Год выпуска: {self.year}")
        print(f"Объем двигателя: {self.engine_capacity} л")

    def is_matching(self, conditions):
        for key, value in conditions.items():
            if getattr(self, key) != value:
                return False
        return True


class PassengerCar(Car):
    def __init__(self, brand, model, year, engine_capacity, fuel_type, seats):
        super().__init__(brand, model, year, engine_capacity)
        self.fuel_type = fuel_type
        self.seats = seats

    def display_info(self):
        super().display_info()
        print(f"Тип топлива: {self.fuel_type}")
        print(f"Количество мест: {self.seats}")

    def is_matching(self, conditions):
        if not super().is_matching(conditions):
            return False
        if 'fuel_type' in conditions and self.fuel_type != conditions['fuel_type']:
            return False
        if 'seats' in conditions and self.seats < conditions['seats']:
            return False
        return True


class FreightCar(Car):
    def __init__(self, brand, model, year, engine_capacity, load_capacity):
        super().__init__(brand, model, year, engine_capacity)
        self.load_capacity = load_capacity

    def display_info(self):
        super().display_info()
        print(f"Грузоподъемность: {self.load_capacity} т")

    def is_matching(self, conditions):
        if not super().is_matching(conditions):
            return False
        if 'load_capacity' in conditions and self.load_capacity < conditions['load_capacity']:
            return False
        return True


class PassengerVan(Car):
    def __init__(self, brand, model, year, engine_capacity, seats):
        super().__init__(brand, model, year, engine_capacity)
        self.seats = seats

    def display_info(self):
        super().display_info()
        print(f"Количество мест: {self.seats}")

    def is_matching(self, conditions):
        if not super().is_matching(conditions):
            return False
        if 'seats' in conditions and self.seats < conditions['seats']:
            return False
        return True
    
cars = [
    PassengerCar("Toyota", "Camry", 2020, 2.5, "бензин", 5),
    FreightCar("Volvo", "FH16", 2018, 13.0, 30),
    PassengerVan("Mercedes-Benz", "Sprinter", 2019, 2.2, 9)
]

# Вывод полной информации о всех автомобилях
for car in cars:
    car.display_info()
    print()

# Поиск автомобилей по заданным характеристикам
search_conditions = {
    'brand': "Toyota",
    'engine_capacity': 2.5
}

matching_cars = [car for car in cars if car.is_matching(search_conditions)]

if matching_cars:
    print("Результаты поиска:")
    for car in matching_cars:
        car.display_info()
else:
    print("Нет автомобилей, удовлетворяющих заданным характеристикам.")
''')


def sdvev():
    print('''# Реализовать функцию, которая находит произведение квадратов всех
# элементов в двусвязном списке.

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            new_node.prev = current

    def delete_node(self, data):
        if self.head is None:
            return
        elif self.head.data == data:
            if self.head.next is not None:
                self.head = self.head.next
                self.head.prev = None
            else:
                self.head = None
        else:
            current = self.head
            while current.next is not None and current.next.data != data:
                current = current.next
            if current.next is None:
                return
            else:
                current.next = current.next.next
                if current.next is not None:
                    current.next.prev = current

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    def calculate_square_product(self):
        if self.head is None:
            return 1  # Если список пустой, возвращаем 1

        product = 1
        current = self.head
        while current:
            product *= current.data ** 2
            current = current.next

        return product
    
    def __str__(self):
        if self.head == None:
            return f"Двусвязный список пустой"
        current = self.head
        dllist_str = ""
        while current:
            dllist_str += " ⇄ " + str(current.data)
            current = current.next
        return dllist_str.lstrip(" ⇄ ")  
    
dllist = DoublyLinkedList()
dllist.add_node(2)
dllist.add_node(3)
dllist.add_node(4)
dllist.add_node(5)

square_product = dllist.calculate_square_product()
print(dllist)
print("Произведение квадратов элементов в списке:", square_product)''')

#5    
def rivgz():
    print('''# Создайте класс ФИЛЬМ с методами, позволяющими вывести на экран
# информацию о фильме, а также определить, подходит ли данный фильм
# для заданных условий. Создайте дочерние классы КОМЕДИЯ
# (название, год выпуска, режиссер, актеры), ДРАМА (название, год
# выпуска, режиссер, актеры), ФАНТАСТИКА (название, год выпуска,
# режиссер, актеры) со своими методами вывода информации на экран и
# определения соответствия заданным условиям. Создайте список
# фильмов, выведите полную информацию из базы на экран, а также
# организуйте поиск фильмов с заданным годом выпуска или режиссером.

class Film:
    def __init__(self, title, year, director, actors):
        self.title = title
        self.year = year
        self.director = director
        self.actors = actors

    def display_info(self):
        print("Фильм:", self.title)
        print("Год выпуска:", self.year)
        print("Режиссер:", self.director)
        print("Актеры:", ', '.join(self.actors))

    def matches_condition(self, year=None, director=None):
        if year and self.year != year:
            return False
        if director and self.director != director:
            return False
        return True


class Comedy(Film):
    def display_info(self):
        print("Комедия:")
        super().display_info()


class Drama(Film):
    def display_info(self):
        print("Драма:")
        super().display_info()


class Fantasy(Film):
    def display_info(self):
        print("Фантастика:")
        super().display_info()


# Создание списка фильмов
films = [
    Comedy("Комедия 1", 2000, "Режиссер 1", ["Актер 1", "Актер 2"]),
    Drama("Драма 1", 2005, "Режиссер 2", ["Актер 3", "Актер 4"]),
    Fantasy("Фантастика 1", 2010, "Режиссер 3", ["Актер 5", "Актер 6"]),
    Comedy("Комедия 2", 2000, "Режиссер 1", ["Актер 7", "Актер 8"]),
]

# Вывод полной информации о фильмах
for film in films:
    film.display_info()
    print()

# Поиск фильмов по заданным условиям
print("Фильмы, выпущенные в 2000 году:")
for film in films:
    if film.matches_condition(year=2000):
        film.display_info()
        print()

print("Фильмы режиссера 'Режиссер 1':")
for film in films:
    if film.matches_condition(director="Режиссер 1"):
        film.display_info()
        print()
''')
    
def pdbvn():
    print('''#Найти высоту бинарного дерева поиска

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None        

class BinaryTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        new_node = Node(data)
        if self.root is None:
            self.root = new_node
        else:
            current = self.root
            while True:
                if data < current.data:
                    if current.left is None:
                        current.left = new_node
                        break
                    else:
                        current = current.left
                else:
                    if current.right is None:
                        current.right = new_node
                        break
                    else:
                        current = current.right

    def search(self, data):
        current = self.root
        while current is not None:
            if data == current.data:
                return True
            elif data < current.data:
                current = current.left
            else:
                current = current.right
        return False

    def delete(self, data):
        if self.root is not None:
            self.root = self._delete(data, self.root)

    def _delete(self, data, node):
        if node is None:
            return node

        if data < node.data:
            node.left = self._delete(data, node.left)
        elif data > node.data:
            node.right = self._delete(data, node.right)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self._find_min_node(node.right)
            node.data = temp.data
            node.right = self._delete(temp.data, node.right)

        return node

    def _find_min_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def __str__(self):
        return '\n'.join(self._display(self.root)[0])

    def height(self):
        return self._height(self.root)

    def _height(self, node):
        if node is None:
            return 0
        else:
            left_height = self._height(node.left)
            right_height = self._height(node.right)
            return max(left_height, right_height) + 1


    def _display(self, node):
        if node.right is None and node.left is None:
            line = str(node.data)
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        if node.right is None:
            lines, n, p, x = self._display(node.left)
            s = str(node.data)
            u = len(s)
            first_line = (x + 1)*' ' + (n - x - 1)*'_' + s
            second_line = x*' ' + '/' + (n - x - 1 + u)*' '
            shifted_lines = [line + u*' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        if node.left is None:
            lines, n, p, x = self._display(node.right)
            s = str(node.data)
            u = len(s)
            first_line = s + x*'_' + (n - x)*' '
            second_line = (u + x)*' ' + '\\' + (n - x - 1)*' '
            shifted_lines = [u*' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        left, n, p, x = self._display(node.left)
        right, m, q, y = self._display(node.right)
        s = str(node.data)
        u = len(s)
        first_line = (x + 1)*' ' + (n - x - 1)*'_' + s + y*'_' + (m - y)*' '
        second_line = x*' ' + '/' + (n - x - 1 + u + y)*' ' + '\\' + (m - y - 1)*' '
        if p < q:
            left += [n*' ']*(q - p)
        elif q < p:
            right += [m*' ']*(p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u*' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2
    
from random import shuffle

# создание объекта класса BinaryTree
tree = BinaryTree()

# создание списка элементов
items = list(range(1,11))
shuffle(items)

# добавление элементов в бинарное дерево
for item in items:
    tree.insert(item)

# вывод бинарного дерева на экран
print(items)
print(tree)
tree.height()''')
    
#13
def chpyaks():
    print('''# а) Используя лямбда-функцию, найдите все числа в заданном списке, которые являются простыми числами.
import numpy as np
lst = np.random.randint(1, 100, 30)
A = list(filter(lambda a: np.sum([i for i in range (2, a) if a % i == 0]) == 0, lst))
print(A)''')
    
def skdup():
    print('''# б) Напишите программу для сортировки заданного списка строк по убыванию длины каждой строки.
st = ['twewgre', 'ewgregerh', 'rehr', 'rgrehreh', 'wqgre', 'qwergjb', 'et']
def sorting(lst):
    return sorted(lst, key=lambda a: len(a), reverse=True)
sorting(st)''')
    
def rvbts():
    print('''# в) Используя лямбда-функцию, найдите все строки в заданном списке строк, которые содержат только буквы верхнего регистра
st = ['RHGR', 'EGHTYHegF', 'rehGr', 'GETG', 'wqgre', 'qwergjb', 'eGt']
C = list(filter(lambda a: a.isupper(), st))
print(C)''')
    
def tyaovkh():
    print('''#Реализовать класс хеш-таблицы для хранения объектов класса «Книга». 
#Хеш-функция должна основываться на поле «автор книги». Если две
#книги имеют одного и того же автора, они должны храниться в одной
#ячейке таблицы

# реализация хеш-таблицы методом цепочек
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, book):
        index = self.hash_function(book.author)
        self.table[index].append(book.name)

    def find(self, author):
        index = self.hash_function(author)
        return self.table[index]
        
class Book:
    def __init__(self, author, name):
        self.author = author
        self.name = name

    def __str__(self):
        return f"Автор: {self.author}, название: {self.name}"
        
books = HashTable(6)
books_list = [Book('Pushkin', 'Boris Godunov'), Book('Dostoevskiy', 'Prestuplenie i nakazanie'),
              Book('Pushkin', 'Evgeniy Onegin')]
for b in books_list:
    books.insert(b)
    print(b)

print(books.find('Pushkin'))''')

#14    
def ndnin():
    print('''#а) Используя лямбда-функцию, найдите все числа в заданном списке, которые делятся на 3 и не делятся на 5.
import numpy as np
lst = np.random.randint(1, 100, 30)
A = list(filter(lambda a: (a % 3 == 0)*(a % 5 != 0), lst))
print(A)''')
    
def kkevv():
    print('''#б) Напишите программу для сортировки заданного списка кортежей по возрастанию второго элемента каждого кортежа.
def sort_tuples(tup):
    return sorted(tup, key=lambda a: a[1])

# Пример использования
st = [(7, 3), (4, 5), (2, 7), (4, 2), (1, 1)]
sort_tuples(st)''')
    
def tstsks():
    print('''#в) Используя лямбда-функцию, найдите все строки в заданном списке строк, которые содержат только цифры
st = ['67875', 'EGHT4YHegF', 'rehGr', 'GETG', '5478', 'qwer3gjb', 'e4Gt']
C = list(filter(lambda a: a.isdigit(), st))
print(C)''')
    
def ddnot():
    print('''#Создать класс очереди, который будет хранить только уникальные
#элементы. При добавлении элемента, если он уже есть в очереди, то он
#не должен добавляться

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return not bool(self.head)

    def enqueue(self, data):
        new_node = Node(data)
        current = self.head
        k = 0
        while current:
            if current.data == new_node.data:
                k = 1
                break
            current = current.next
        if k == 0:
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                self.tail = new_node

    def dequeue(self):
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ")  
    
import random
q = Queue()
for i in range(10):
    c = random.randint(-10,10)
    q.enqueue(c)
print(q)''')

#15    
def sitszs():
    print('''# Создайте класс ПРОДУКТ с методами, позволяющими вывести на экран
# информацию о продукте, а также определить, подходит ли данный
# продукт для заданных условий. Создайте дочерние классы МЯСО
# (название, цена, производитель, срок годности), ОВОЩИ (название,
# цена, производитель, сезонность), ФРУКТЫ (название, цена,
# производитель, сезонность) со своими методами вывода информации на
# экран и определения соответствия заданным условиям. Создайте список
# продуктов, выведите полную информацию из базы на экран, а также
# организуйте поиск продуктов с заданной ценой или сезонностью. 


class Product():
    def __init__(self, name, price, manufacturer):
        self.name = name
        self.price = price
        self.manufacturer = manufacturer
    def info(self):
        return self.__dict__
    def find_conditions(self):
        return True
    
class Meat(Product):
    def __init__(self, name, price, manufacturer, exp_date):
        super().__init__(name, price, manufacturer)
        self.exp_date = exp_date
    def find_conditions(self, a):
        return self.price <= a
    
class Vegetables(Product):
    def __init__(self, name, price, manufacturer, season):
        super().__init__(name, price, manufacturer)
        self.season = season
    def find_conditions(self, a):
        return self.season == a
    
class Fruits(Product):
    def __init__(self, name, price, manufacturer, season):
        super().__init__(name, price, manufacturer)
        self.season = season
    def find_conditions(self, a):
        return self.season == a
        
pr1 = Product('Сметана', 75, 'Простоквашино')
pr2 = Product('Молоко', 70, 'Молочный знак')
m1 = Meat('Говядина', 200, 'Волков', 15)
m2 = Meat('Свинина', 150, 'Волков', 10)
m3 = Meat('Курятина', 130, 'Мираторг', 20)

v1 = Vegetables('Помидор', 50, 'Овощной мастер', 'лето')
v2 = Vegetables('Капуста', 60, 'Супер-овощи', 'лето')
v3 = Vegetables('Морковь', 40, 'Мега-овощи', 'осень')

f1 = Fruits('Яблоко', 70, 'Apple', 'весна')
f2 = Fruits('Груша', 60, 'Фруктики', 'лето')
f3 = Fruits('Банан', 80, 'Фруктос', 'лето')

lst = [pr1,pr2,m1,m2,m3,v1,v2,v3,f1,f2,f3]
for p in lst:
    print(p.info())

print('_________')  
for p in lst:
    if p.price < 80:
        print(p.info())
print('_________')     
for p in lst:
    try:
        if p.find_conditions('лето'):
            print(p.info())
    except:
        pass''')
    
def chchyank():
    print('''#Дан стек. Необходимо удалить из него все элементы, которые не являются четными числами
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def push(self, item):
        new_node = Node(item)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if self.is_empty():
            return None
        else:
            popped_item = self.head.data
            self.head = self.head.next
            return popped_item

    def peek(self):
        if self.is_empty():
            return None
        else:
            return self.head.data

    def __str__(self):
        current = self.head
        stack_str = ""
        while current:
            stack_str += str(current.data) + " → "
            current = current.next
        return stack_str.rstrip(" → ")
    
import random
stack = Stack()
for i in range(10):
    stack.push(random.randint(-10,10))
print(stack)

def del_chet(stack):
    val = stack.head
    basket = []
    while val:
        if val.data % 2 == 0:
            pp = stack.pop()
            while pp != val.data:
                basket.append(pp)
                pp = stack.pop()
        val = val.next
    for i in reversed(basket):
        stack.push(i)
    return stack
print(del_chet(stack))''')

#16    
def oipzs():
    print('''# Создайте класс ЖИВОТНОЕ с методами, позволяющими вывести на
# экран информацию о животном, а также определить, подходит ли
# данное животное для заданных условий. Создайте дочерние классы
# КОШКА (кличка, порода, возраст, окрас), СОБАКА (кличка, порода,
# возраст, размер), ПТИЦА (вид, возраст, окрас) со своими методами
# вывода информации на экран и определения соответствия заданным
# условиям. Создайте список животных, выведите полную информацию
# из базы на экран, а также организуйте поиск животных с заданной
# породой или окрасом

class Animal():
    def __init__(self, species, age):
        self.species = species
        self.age = age
    def info(self):
        return self.__dict__
    def find_conditions(self):
        return True
    
class Cat(Animal):
    def __init__(self, name, species, age, color):
        super().__init__(species, age)
        self.name = name
        self.color = color
    def find_conditions(self, a):
        return self.color == a
    
class Dog(Animal):
    def __init__(self, name, species, age, size):
        super().__init__(species, age)
        self.name = name
        self.size = size
    def find_conditions(self, a):
        return self.species == a
    
class Bird(Animal):
    def __init__(self, species, age, color):
        super().__init__(species, age)
        self.color = color
    def find_conditions(self, a):
        return self.color == a
        
c1 = Cat('Муся', 'Обычная', 10, 'Серый')
c2 = Cat('Пуся', 'Британская', 5, 'Рыжий')

d1 = Dog('Хан', 'Овчарка', 7, 15)
d2 = Dog('Моджо', 'Чихуахуа', 2, 3)

b1 = Bird('Пингвин', 4, 'Черно-белый')
b2 = Bird('Голубь', 1, 'Серый')

lst = [c1,c2,d1,d2,b1,b2]

for a in lst:
    print(a.info())

print('_______')
for a in lst:
    try:
        if a.species == 'Овчарка':
            print(a.info())
    except:
        pass
    
print('_______')
for a in lst:
    try:
        if a.find_conditions('Серый'):
            print(a.info())
    except:
        pass''')
    
def sivii():
    print('''# Написать функцию, которая принимает на вход двусвязный список и индекс элемента, который нужно удалить. Функция должна удалить
# элемент с указанным индексом и вернуть измененный список

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None

    def add_node(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            new_node.prev = current

    def delete_node(self, data):
        if self.head is None:
            return
        elif self.head.data == data:
            if self.head.next is not None:
                self.head = self.head.next
                self.head.prev = None
            else:
                self.head = None
        else:
            current = self.head
            while current.next is not None and current.next.data != data:
                current = current.next
            if current.next is None:
                return
            else:
                current.next = current.next.next
                if current.next is not None:
                    current.next.prev = current

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def __str__(self):
        if self.head == None:
            return f"Двусвязный список пустой"
        current = self.head
        dllist_str = ""
        while current:
            dllist_str += " ⇄ " + str(current.data)
            current = current.next
        return dllist_str.lstrip(" ⇄ ")
        
lst1 = DoublyLinkedList()

for i in range(10):
    lst1.add_node(random.randint(0,9))

print(lst1)

def delete_element(lst, i):
    l = len(lst)
    cur = lst.head
    lst_new = DoublyLinkedList()
    for _ in range(i):
        lst_new.add_node(cur.data)
        cur = cur.next
    for _ in range(i+1, l):
        cur = cur.next
        lst_new.add_node(cur.data)
    return lst_new
print(delete_element(lst1, 8))''')

#17    
def dtibs():
    print('''# Создайте класс СТУДЕНТ с методами, позволяющими вывести на экран
# информацию о студенте, а также определить, соответствует ли данный
# студент заданным критериям. Создайте дочерние классы БАКАЛАВР
# (фамилия, имя, отчество, группа, курс, средний балл), МАГИСТР
# (фамилия, имя, отчество, группа, курс, средний балл, тема диссертации)
# со своими методами вывода информации на экран и определения
# соответствия заданным критериям. Создайте список студентов,
# выведите полную информацию из базы на экран, а также организуйте
# поиск студентов с заданным средним баллом или темой диссертации. 

class Student():
    def __init__(self, surname, name, patronymic, group, course, average_grade):
        self.surname = surname
        self.name = name
        self.patronymic = patronymic
        self.group = group
        self.course = course
        self.average_grade = average_grade
    def info(self):
        return self.__dict__
    def find_conditions(self):
        return True
    
class Bachelor(Student):
    def __init__(self, surname, name, patronymic, group, course, average_grade):
        super().__init__(surname, name, patronymic, group, course, average_grade)
    def find_conditions(self, a):
        return self.average_grade == a
    
class Master(Student):
    def __init__(self, surname, name, patronymic, group, course, average_grade, topic):
        super().__init__(surname, name, patronymic, group, course, average_grade)
        self.topic = topic
    def find_conditions(self, a):
        return self.topic == a
        
b1 = Bachelor('Иванов','Иван','Иванович',1,1,5)
b2 = Bachelor('Петров','Петр','Петрович',2,3,4)

m1 = Master('Николаев','Иван','Николаевич',3,6,5,'Математика')
m2 = Master('Андреева','Алина','Андреевна',3,6,4,'Физика')

lst = [b1,b2,m1,m2]

for s in lst:
    print(s.info())
    
print('_______')
for s in lst:
    if s.average_grade == 5:
        print(s.info())

print('_______')
for s in lst:
    try:
        if s.find_conditions('Математика'):
            print(s.info())
    except:
        pass''')
    
def siidm():
    print('''# Написать метод класса «Клиент», который сортирует список клиентов по возрасту с помощью алгоритма сортировки пузырьком. Метод должен изменять исходный список
class Client():
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def __str__(self):
        return f"Имя: {self.name}, Возраст: {self.age}"
    @staticmethod
    def sorting(clients):
        n = len(clients)
        for i in range(n):
            for j in range(n - i - 1):
                if clients[j].age > clients[j + 1].age:
                    clients[j], clients[j + 1] = clients[j + 1], clients[j]
                    
clients = [Client("Ivan", 25),Client("Elena", 18),Client("Alex", 37),Client("Petr", 64)]
Client.sorting(clients)
for i in clients:
    print(i)''')

#18    
def chspvch():
    print('''# а) Используя лямбда-функцию, найдите все числа в заданном списке,
# которые являются числами Кармайкла (для любого числа a, взаимно
# простого с числом n, a^(n-1) mod n = 1).

import numpy as np
import math
lst = [561, 346, 256, 4246, 56, 2821, 578, 1105]
print(lst)
A = list(filter(lambda n: np.sum([1 for a in range(2,n) if (math.gcd(a,n) == 1) and (a**(n-1)%n != 1)]) == 0, lst))
print(A)''')
    
def skvzi():
    print('''# б) Напишите программу для сортировки заданного списка строк по
# количеству символов-разделителей (пробелов или запятых) в каждой
# строке.

def sorting(strings):
    return sorted(strings, key=lambda a: a.count(" ") + a.count(","))

strings = ['RGEG, E   TEH,', 'WETRETER ', 'WTEY , EW', 'WETWT', 'EQERWT,,, ']
sorting(strings)''')
    
def tnzks():
    print('''# в) Используя лямбда-функцию, найдите все строки в заданном списке
# строк, которые заканчиваются на точку.
strings = ['RGEG, E   TEH,', 'WETRETER ','twter.', 'wrert.ehrth', 'wetwrytre.', 'WTEY , EW', 'WETWT', 'EQERWT,,, ']
C = list(filter(lambda s: s[-1] == '.', strings))
print(C)''')
    
def upobd():
    print('''# Создать класс очереди, который будет хранить только элементы типа int
# и отсортированные по убыванию. При добавлении элемента, если он не
# является целым числом, то он не должен добавляться. При получении
# элементов из очереди они должны быть отсортированы по убыванию. 

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, data):
        new_node = Node(data)
        if isinstance(new_node.data , int):
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                self.tail = new_node

    def dequeue(self):
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data
    
    def get_queue(self):
        q = []
        cur = self.head
        while cur:
            q.append(cur.data)
            cur = cur.next
        return sorted(q, reverse = True)

    def __str__(self):
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ") 
    
import random
q = Queue()
for i in range(10):
    c = random.randint(-10,10)
    q.enqueue(c)
print(q)

q.enqueue(0.6)
print(q)

q.enqueue(6)
print(q)

print(q.get_queue())''')