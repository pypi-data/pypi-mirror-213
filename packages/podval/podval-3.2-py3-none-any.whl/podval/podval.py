def Stack_descr():
    print('''
Стек — это структура данных, которая представляет собой упорядоченный список элементов, где доступ к элементам осуществляется только с одного конца — вершины стека.

Стек работает по принципу «последний вошел, первый вышел» (Last-In-First-Out, LIFO). Это означает, что последний добавленный элемент находится на вершине стека и будет первым удаленным элементом.

Основные операции, которые можно выполнять со стеком, это добавление элемента в вершину (push) и удаление элемента из вершины (pop). Также можно выполнить операцию просмотра элемента на вершине стека без его удаления (peek).

Стек используется в различных областях программирования, например, для реализации обратной польской записи выражений, выполнения рекурсивных функций и управления вызовами в операционных системах

Класс Node представляет узел стека и имеет два атрибута:

data — для хранения данных,
next — для указания на следующий узел.
Класс Stack представляет сам стек и имеет атрибут head, который указывает на верхний узел стека.

Метод push(item) добавляет новый элемент в стек, создавая новый узел и помещая его в начало списка, т.е. делая его новой вершиной стека.

Метод pop() удаляет и возвращает верхний элемент стека, если он существует. Если стек пустой, метод возвращает None.

Метод peek() возвращает верхний элемент стека без его удаления. Если стек пустой, метод возвращает None.

Метод is_empty() проверяет, пустой ли стек, и возвращает True, если он пустой, и False в противном случае.

Метод __str__ предназначен для преобразования объекта класса Stack в строку, он возвращает строку, содержащую все элементы стека, разделенные символов «→».
    ''')
    
def Stack():
    print('''class Node:
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
        return stack_str.rstrip(" → ")''')
    
def Stack1():
    print('''#Дан стек и число  k . Необходимо найти  k -й по счету элемент в стеке.
    def find(s, i):
    current = s.head
    k=1
    while current and k<=i:
        if k==i:
            return f'Элемент под номером {i}: {current.data}'
        current = current.next
        k+=1
    return 'Элемента с таким номером в данном стеке нет'
    ''')
    
def Stack2():
    print('''#Дан стек и значение  A . Необходимо удалить из стека все элементы, которые больше  A .
    stack2 = Stack()

while not stack1.is_empty():
    temp = stack1.pop()
    if temp <= A:
        stack2.push(temp)

while not stack2.is_empty():
    stack1.push(stack2.pop())
''')

def Stack3():
    print('''#Дан стек и два элемента  A  и  B . Необходимо удалить из стека все элементы, которые находятся между  A  и  B  (включая сами  A  и  B
    A = int(input())
B = int(input())
bf_stack = Stack()
while not(stack.is_empty()):
  if stack.peek() == A:
    while stack.peek() != B:
      stack.pop()
    if stack.peek() == B:
      stack.pop()
  bf_stack.push(stack.peek())
  stack.pop()
while not(bf_stack.is_empty()):
  stack.push(bf_stack.peek())
  bf_stack.pop()
print(stack)''')
    
def Stack4():
    print('''#Дан стек. Необходимо найти среднее арифметическое всех его элементов.
    from random import randint

for i in range(10):
    a.push(randint(1,20))
cnt = 0
s = 0
while a.is_empty() ^ 1:
    cnt += 1
    s += a.peek()
    a.pop()
s/cnt''')
    
def Stack5():
    print('''#Дан стек. Необходимо проверить, есть ли в нем повторяющиеся элементы. Вывести повторяющиеся элементы, если они есть.
    def find_dup(stack):
    seen = set()
    dup = set()
    current = stack.top
    while current is not None:
        if current.data in seen:
            dup.add(current.data)
        else:
            seen.add(current.data)
        current = current.next
    return dup''')
    
def Stack6():
    print('''#Дан стек. Необходимо удалить из него все отрицательные элементы.
    stack = Stack()
for i in range(10):
    stack.add(random.randint(-10,10))
    def del_negative(stack):
    val = stack.head
    basket = []
    while val:
        if 0 > val.data:
            pp = stack.pop()
            while pp != val.data:
                basket.append(pp)
                pp = stack.pop()
        val = val.next
    for i in reversed(basket):
        stack.add(i)
    return stack
print(del_negative(stack)) ''')
    
def Queue_descr():
    print('''
Очередь — это структура данных, которая представляет собой список элементов, в котором новые элементы добавляются в конец очереди, а удаление элементов происходит из начала очереди.

Эта структура данных работает по принципу «первым пришел — первым ушел» (FIFO — First In First Out). Таким образом, элементы, добавленные раньше, имеют более высокий приоритет и должны быть удалены раньше элементов, добавленных позже.

Очередь широко используется в программировании для управления потоками данных и выполнения задач в порядке их поступления.


Класс Node представляет узел связного списка и имеет два атрибута:

data (данные, которые хранятся в узле),
next (ссылка на следующий узел списка).
Класс Queue реализует очередь и имеет два атрибута:

head (ссылка на первый элемент очереди),
tail (ссылка на последний элемент очереди).
Метод is_empty проверяет, пуста ли очередь.

Метод enqueue добавляет новый элемент в конец очереди. Если очередь пуста, то новый элемент становится и первым, и последним. Если очередь не пуста, то новый элемент добавляется в конец списка, и tail обновляется на новый элемент.

Метод dequeue удаляет первый элемент из очереди и возвращает его значение. Если очередь пуста, то возникает исключение. Если после удаления первого элемента очередь становится пустой, то tail обновляется на None.

Метод __len__ возвращает количество элементов в очереди.

Метод __str__ переопределяет стандартный метод __str__ для класса Queue и возвращает строковое представление элементов очереди в виде последовательности через стрелку «→».
''')
           
def Queue():
    print('''
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
        
        # создание объекта класса Queue
q = Queue()

# добавление элементов в очередь
for item in range(5):
    q.enqueue(item)''')

def Queue1():
    print('''# функция для нахождения первого нечетного элемента очереди
def find_first_odd(queue):
    current = queue.head
    while current:
        if current.data % 2 != 0:
            return current.data
        current = current.next
    return None''')

def Queue2():
    print('''# функция для добавления нового элемента в очередь перед первым четным элементом
def add_before_first_even(queue, item):
    new_node = Node(item)
    if not queue.head:
        queue.head = new_node
        queue.tail = new_node
    elif queue.head.data % 2 == 0:
        new_node.next = queue.head
        queue.head = new_node
    else:
        prev_node = queue.head
        current = prev_node.next
        while current:
            if current.data % 2 == 0:
                prev_node.next = new_node
                new_node.next = current
                return
            prev_node = current
            current = current.next
        queue.tail.next = new_node
        queue.tail = new_node''')

def Queue3():
    print('''# альтернативная функция для добавления нового элемента в очередь перед первым четным элементом
def add_before_first_even(queue, data):
    temp_queue = Queue()
    even_found = False

    while not queue.is_empty():
        item = queue.dequeue()
        if item % 2 == 0 and not even_found:
            temp_queue.enqueue(data)
            even_found = True
        temp_queue.enqueue(item)

    while not temp_queue.is_empty():
        queue.enqueue(temp_queue.dequeue())''')

def Queue4():
    print('''Создать класс очереди, который будет поддерживать операции добавления элемента в конец очереди и удаления всех элементов из очереди, которые меньше заданного значения.
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
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node


    def dequeue_less(self, par):
        current = self.head
        previous = None

        while current:
            if current.data < par:
                if previous:
                    previous.next = current.next
                else:
                    self.head = current.next

                if current == self.tail:
                    self.tail = previous
            else:
                previous = current
            current = current.next


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
        return queue_str.lstrip(" → ")''')

def Queue5():
    print('''Сортировка значений очереди по возрастанию
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
    
    def listed(self):
        current = self.head
        queue_str = []
        while current:
            queue_str.append(current.data)
            current = current.next
        return queue_str

    def sorting(queue):
      temp_queue = sorted(Queue.listed(queue))
      queue = Queue()
      for i in temp_queue:
          queue.enqueue(i)
      return queue                       

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
        return queue_str.lstrip(" → ")  ''')

def Queue6():
    print('''Создать класс очереди, который будет поддерживать операции добавления элемента в конец очереди и удаления всех повторяющихся элементов из очереди.
    class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return not bool(self.head)

    def enqueue(self, data):
        new_node = Node(data)
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
    
    def del_repeats(self):
        new_data = []
        while self.head:
            if self.head.data not in new_data:
                new_data.append(self.head.data)
            self.head = self.head.next
        self.tail = None
        for i in new_data:
            self.enqueue(i)

    def __str__(self):
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ")  ''')

def Queue7():
    print('''Создать класс очереди с ограниченной емкостью. Если при добавлении элемента очередь уже заполнена, то новый элемент должен заменить первый элемент в очереди.

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Queue5:
    def __init__(self, capacity):
        self.head = None
        self.tail = None
        self.capacity = capacity

    def is_empty(self):
        return not bool(self.head)

    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    def enqueue(self, data):
        new_node = Node(data)
        
        if self.__len__() < self.capacity:
            print('место в очереди еще есть')
            if not self.head:
                self.head = new_node
                self.tail = new_node
            else:
                self.tail.next = new_node
                self.tail = new_node
        else:
            print('места в очереди уже нет')
            self.head.data = new_node.data
            

    def dequeue(self):
        data = self.head.data
        self.head = self.head.next
        if not self.head:
            self.tail = None
        return data

    def __str__(self):
        current = self.head
        queue_str = ""
        while current:
            queue_str += " → " + str(current.data)
            current = current.next
        return queue_str.lstrip(" → ") ''')

def DoublyLinkedList_descr():
    print(''' 
Двусвязный список — это структура данных, которая состоит из узлов, каждый из которых содержит ссылки на предыдущий и следующий узел в списке. Таким образом, каждый узел имеет две связи: одну со своим предшественником и одну со своим последователем. Это позволяет эффективно добавлять и удалять элементы в середине списка, а также перемещаться в обоих направлениях по списку.


Класс Node определяет узел списка, который имеет три атрибута:

data (хранит данные),
prev (хранит ссылку на предыдущий узел),
next (хранит ссылку на следующий узел).
Класс DoublyLinkedList определяет сам список. Он имеет атрибут head (хранит ссылку на первый узел списка).

Метод add_node добавляет новый узел в конец списка. Если список пуст, то новый узел становится первым элементом.

Метод delete_node удаляет узел с заданным значением. Если узел, который нужно удалить, является первым элементом списка, то head изменяется на следующий элемент. Если удаляемый узел находится в середине или в конце списка, то ссылки на предыдущий и следующий узлы соединяются.

Метод __len__ возвращает количество элементов в списке.

Метод __str__ возвращает строковое представление списка в формате «data1 ⇄ data2 ⇄ ... ⇄ dataN».
''')
def DoublyLinkedList():
    print('''
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
        return dllist_str.lstrip(" ⇄ ") ''')

    
def DoublyLinkedList1():
    print('''
    # создание объекта класса DoublyLinkedList
dll = DoublyLinkedList()
from random import randint

# добавление элементов в двухсвязный список
for i in range(randint(5,10)):
    dll.add_node(randint(1,20))

# вывод двусвязного списка на экран
print(f'Двусвязный список: {dll}\nколичество элементов в двусвязном списке равно {len(dll)}')

# удаление элементов из двусвязного списка
dll.delete_node(18)
dll.delete_node(1)

# вывод двусвязного списка на экран
print(f'Двусвязный список: {dll}\nколичество элементов в двусвязном списке равно {len(dll)}')


# функция для удвоения каждого четного элемента двусвязного списка
def double_even_nodes(dllist):
    current_node = dllist.head
    while current_node:
        if current_node.data % 2 == 0:
            new_node = Node(current_node.data)
            new_node.next = current_node.next
            new_node.prev = current_node
            if current_node.next:
                current_node.next.prev = new_node
            current_node.next = new_node
            current_node = new_node.next
        else:
            current_node = current_node.next
            
# функция для удаления всех отрицательных элементов из двусвязного списка
def delete_negative_nodes(dllist):
    current_node = dllist.head
    while current_node:
        if current_node.data < 0:
            if current_node.prev:
                current_node.prev.next = current_node.next
            else:
                dllist.head = current_node.next
            if current_node.next:
                current_node.next.prev = current_node.prev
        current_node = current_node.next
    ''')
    
def DoublyLinkedList2():
    print('''#Создайте двусвязный список для хранения информации о посетителях музея. Каждый элемент списка должен содержать имя и фамилию посетителя, дату посещения, список экспонатов, которые он посмотрел, и оценку каждого из них.
    class Data:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoubleList:
    def __init__(self):
        self.head = None

    def add_info(self, data):
        new_node = Data(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next is not None:
                cur = cur.next
            cur.next = new_node
            new_node.prev = cur

    def del_info(self, data):
        if self.head is None:
            return
        elif self.head.__dict__ == data:
            self.head = self.head.next
            self.head.prev = None
        else:
            cur = self.head
            while cur.next is not None and cur.next.data != data:
                cur = cur.next
            if cur.next is None:
                return
            else:
                cur.next = cur.next.next
                if cur.next is not None:
                    cur.next.prev = cur
                    
    def __len__(self):
        count = 0
        cur = self.head
        while cur:
            count += 1
            cur = cur.next
        return count

    def __str__(self):
        cur = self.head
        dllist_str = ""
        while cur:
            dllist_str += "\n" + str(cur.data)
            cur = cur.next
        return dllist_str.lstrip("\n")
        
        class Visitors:
    def __init__(self, name, surname, date, ex_list, estimation):
        self.name = name
        self.surname = surname
        self.date = date
        self.ex_list = ex_list
        self.estimation = estimation
        
    def __str__(self):
        return f"Name: {self.name}, Surname: {self.surname}, Date: {self.date}, Exhibits_list: {self.ex_list}, Estimations: {self.estimation}"
        
        a_1 = Visitors('Stive','Ivanov','12.04.2023',['Raketa','Sputnik'],['5','4.5'])
a_2 = Visitors('Evgeniy','Petrov','16.04.2023',['Sputnik'],['5'])
a_3 = Visitors('Alexandr','Sidorov','16.04.2023',['Earth', 'Space'], ['5','5'])

a = DoubleList()
a.add_info(a_1)
a.add_info(a_2)
a.add_info(a_3)

a.del_info(a_2)


#Реализовать функцию, которая находит сумму двух чисел, представленных в виде двусвязных списков.
import random
lst1 = DoubleList()
lst2 = DoubleList()
for i in range(random.randint(1,8)):
    lst1.add_info(random.randint(0,9))
for i in range(random.randint(1,8)):
    lst2.add_info(random.randint(0,9))
print(lst1)

def summa(ls1, ls2):
    ch1 = ''
    ch2 = ''
    cur = ls1.head
    cur2 = ls2.head
    while cur:
        ch1 = ch1 + str(cur.data)
        cur = cur.next
    while cur2:
        ch2 = ch2 + str(cur2.data)
        cur2 = cur2.next
    return int(ch1) + int(ch2)

summa(lst1,lst2)''')
    
    
def CircularDoublyLinkedList_descr():
    print(''' 
Циклический двусвязный список — это структура данных, которая состоит из узлов, каждый из которых содержит ссылки на предыдущий и следующий узлы. При этом последний узел списка ссылается на первый, а первый — на последний, образуя тем самым замкнутую цепочку.

Преимуществом циклического двусвязного списка является возможность быстрого перемещения как вперед, так и назад по списку, а также возможность выполнения операций вставки и удаления элементов в начале и конце списка за постоянное время.

Класс Node представляет узел списка и имеет три атрибута: data, prev и next. Атрибут data хранит данные узла, а атрибуты prev и next указывают на предыдущий и следующий узлы соответственно.

Класс CircularDoublyLinkedList представляет сам список и имеет два атрибута: head и tail. Атрибут head указывает на первый узел списка, а атрибут tail указывает на последний узел списка.

Метод append добавляет новый узел в конец списка. Если список пустой, то новый узел становится и первым и последним, а его prev и next указывают на него самого. Если список не пустой, то новый узел становится последним, его prev указывает на текущий последний узел, а next на первый узел. Последний узел списка (tail) обновляется на новый узел.

Метод prepend добавляет новый узел в начало списка. Если список пустой, то новый узел становится и первым и последним, а его prev и next указывают на него самого. Если список не пустой, то новый узел становится первым, его next указывает на текущий первый узел, а prev на последний узел. Первый узел списка (head) обновляется на новый узел.

Метод delete удаляет узел со значением key из списка. Если удаляемый узел является первым, то head обновляется на следующий узел, tail.next указывает на новый первый узел, а новый первый узел.prev указывает на tail. Если удаляемый узел является последним, то tail обновляется на предыдущий узел, head.prev указывает на новый последний узел, а новый последний узел.next указывает на head. Если удаляемый узел находится где-то в середине списка, то prev и next соседних узлов переустанавливаются на соответствующие друг другу, чтобы пропустить удаляемый узел.

Метод __len__ возвращает количество узлов в списке путем прохода по всему списку и подсчета количества узлов.

Метод __str__ возвращает строковое представление списка путем прохода по всему списку и конкатенации значений всех узлов в одну строку.''')
    
def CircularDoublyLinkedList():
    print('''class Data:
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None

class CircularDoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, data):
        new_node = Data(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.prev = self.tail
            new_node.next = self.head
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.tail.next = new_node
            self.head.prev = new_node
            self.tail = new_node

    def prepend(self, data):
        new_node = Data(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            new_node.prev = self.tail
            new_node.next = self.head
        else:
            new_node.prev = self.tail
            new_node.next = self.head
            self.head.prev = new_node
            self.tail.next = new_node
            self.head = new_node

    def delete(self, key):
        current_node = self.head
        while current_node:
            if current_node.data == key:
                if current_node == self.head:
                    self.head = current_node.next
                    self.tail.next = self.head
                    self.head.prev = self.tail
                elif current_node == self.tail:
                    self.tail = current_node.prev
                    self.head.prev = self.tail
                    self.tail.next = self.head
                else:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                return
            current_node = current_node.next

    def __len__(self):
        count = 0
        current_node = self.head
        while current_node:
            count += 1
            current_node = current_node.next
            if current_node == self.head:
                break
        return count

    def __str__(self):
        cdllist_str = ""
        current_node = self.head
        while current_node:
            cdllist_str += str(current_node.data) + " ⇄ "
            current_node = current_node.next
            if current_node == self.head:
                break
        return " ⇄ " + cdllist_str''')
    
def CircularDoublyLinkedList1():
    print('''# создание объекта класса CircularDoublyLinkedList
cdll = CircularDoublyLinkedList()

from random import randint

# добавление элементов в циклический двухсвязный список
for i in range(randint(5,10)):
    cdll.append(randint(1,20))

# вывод циклического двусвязного списка на экран
print(f'Циклический двусвязный список: {cdll}\nКоличество элементов в циклическом двусвязном списке равно {len(cdll)}')

# добавление элементов в начало циклического двусвязного списка
cdll.prepend(5)
cdll.prepend(17)

# вывод циклического двусвязного списка на экран
print(f'Циклический двусвязный список (len = {len(cdll)}): {cdll}')

# удаление элемента с заданным значением из циклического двусвязного списка
cdll.delete(20)

# вывод циклического двусвязного списка на экран
print(f'Циклический двусвязный список (len = {len(cdll)}): {cdll}')
    ''')   
    
def CircularDoublyLinkedList2():
    print('''
    # функция, возводящая в квадрат все отрицательные элементы в циклическом двусвязном списке
def square_negative_values(cdllist):
    current_node = cdllist.head
    while current_node:
        if current_node.data < 0:
            current_node.data = current_node.data ** 2
        current_node = current_node.next
        if current_node == cdllist.head:
            break
# функция для удаления всех элементов из циклического двусвязного списка, кратных 5
def delete_multiples_of_5(cdllist):
    current_node = cdllist.head
    while current_node:
        if current_node.data % 5 == 0:
            cdllist.delete(current_node.data)
        current_node = current_node.next
        if current_node == cdllist.head:
            break''')
    
def CircularDoublyLinkedList3():
    print(''' 
#Реализовать функцию, которая удаляет все элементы циклического двусвязного списка, большие заданного значения.
import random
cy = CircularDoublyLinkedList()
for i in range(20):
    cy.append(random.randint(0,100))
print(cy)

def del_large_elem(cycle, a):
    cur = cycle.head
    l = len(cycle)
    count = 0
    while count <= l:
        if cur.data > a:
            cycle.delete(cur.data)
        count += 1
        cur = cur.next
    return cycle
print(del_large_elem(cy,30))''')
    
    
def Tree_descr():
    print(''' 
Дерево — это структура данных, состоящая из узлов, связанных между собой ребрами. Каждый узел может иметь несколько потомков (дочерних узлов), но только один предок (родительский узел), за исключением корневого узла, который не имеет предков.

Структура дерева включает в себя:

Корневой узел — это вершина дерева, которая не имеет предков и является начальной точкой для обхода дерева.

Дочерние узлы — это вершины, которые имеют одного родительского узла и могут иметь несколько дочерних узлов.

Листовые узлы — это вершины, которые не имеют дочерних узлов и являются конечными точками в дереве.

Уровень дерева — это расстояние от корневого узла до любого другого узла.

Высота дерева — это максимальное количество уровней в дереве.

Поддерево — это часть дерева, состоящая из узла и всех его потомков.

Родительский узел — это вершина, от которой исходит ребро к дочернему узлу.

Дочерний узел — это вершина, к которой идет ребро от родительского узла.

Класс Node представляет узел дерева и имеет два атрибута:

значение узла (value),
список дочерних узлов (children).
Класс Tree представляет собой само дерево и имеет один атрибут — корневой узел (root). Конструктор класса инициализирует корневой узел значением None.

Метод add_node(value, parent_value=None) добавляет новый узел в дерево. Если parent_value не указан, то новый узел становится корневым. Если parent_value указан, то новый узел добавляется в список дочерних узлов соответствующего родительского узла.

Метод find_node(value) ищет узел по его значению value. Для этого используется рекурсивный метод _find_node(value, node), который начинает поиск с корневого узла.

Метод _str_tree(node, indent=0) используется для вывода дерева на экран в виде строки. Он также рекурсивно обходит все узлы дерева, начиная с корневого, и добавляет их значения в строку с отступами, чтобы отображать иерархическую структуру дерева.
''')

def Tree():
    print('''
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

class Tree:
    def __init__(self):
        self.root = None

    def add_node(self, value, parent_value=None):
        node = Node(value)
        if parent_value is None:
            if self.root is not None:
                raise ValueError("У дерева уже есть корень")
            self.root = node
        else:
            parent_node = self.find_node(parent_value)
            if parent_node is None:
                raise ValueError("Родительский узел не найден")
            parent_node.children.append(node)

    def find_node(self, value):
        return self._find_node(value, self.root)

    def _find_node(self, value, node):
        if node is None:
            return None
        if node.value == value:
            return node
        for child in node.children:
            found = self._find_node(value, child)
            if found is not None:
                return found
        return None

    def __str__(self):
        return self._str_tree(self.root)

    def _str_tree(self, node, indent=0):
        result = "  " * indent + str(node.value) + "\n"
        for child in node.children:
            result += self._str_tree(child, indent + 2)
        return result''')
     
def Tree1():
    print('''
# функция для замены каждого числа в дереве на сумму чисел всех его потомков
def replace_with_sum_of_children(tree, node=None):
    if node is None:
        node = tree.root
    if not node.children:
        return node.value
    else:
        sum_of_children = 0
        for child in node.children:
            sum_of_children += replace_with_sum_of_children(tree, child)
        node.value = sum_of_children
        return sum_of_children''')
        
def Tree2():
    print('''
# функция, удваивающая каждое нечетное число в дереве
def double_odd_values(tree, node=None):
    if node is None:
        node = tree.root
    if node.value % 2 == 1:
        node.value *= 2
    for child in node.children:
        double_odd_values(tree, child)
    return tree''')
        
def Tree3():
    print('''
# функция для определения листьев дерева
def find_leaves(tree, node=None, leaves=None):
    if leaves is None:
        leaves = []
    if node is None:
        node = tree.root
    if len(node.children) == 0:
        leaves.append(node.value)
    else:
        for child in node.children:
            find_leaves(tree, child, leaves)
    return leaves''')  

    
def BinaryTree_descr():
    print('''
Бинарное дерево — это структура данных, которая состоит из узлов и связей между ними. Каждый узел содержит значение и ссылки на два дочерних узла — левый и правый. Левый дочерний узел содержит значение, которое меньше значения родительского узла, а правый — больше.

Пример бинарного дерева:

      7
    /   \
   4     9
  / \   / \
 2   5 8   10
 
Бинарные деревья могут быть сбалансированными и несбалансированными.

Сбалансированные деревья имеют такое расположение элементов, при котором высота дерева минимальна, что обеспечивает быстрый поиск и вставку элементов. Равное количество элементов в левой и правой ветвях не является необходимым условием для сбалансированности дерева.

Несбалансированные деревья характеризуются тем, что высота одной из ветвей значительно больше высоты другой ветви. Это может привести к тому, что операции поиска и вставки элементов будут выполняться медленнее.

Обход бинарного дерева — это процесс посещения каждого узла дерева в определенном порядке. Существуют три основных способа обхода бинарного дерева:

Прямой обход (pre-order traversal) — при этом способе сначала посещается корень дерева, затем левое поддерево и затем правое поддерево. То есть порядок обхода узлов следующий: корень — левый потомок — правый потомок.

Центрированный обход (in-order traversal) — при этом способе сначала посещается левое поддерево, затем корень дерева и затем правое поддерево. То есть порядок обхода узлов следующий: левый потомок — корень — правый потомок.

Обратный обход (post-order traversal) — при этом способе сначала посещается левое поддерево, затем правое поддерево и затем корень дерева. То есть порядок обхода узлов следующий: левый потомок — правый потомок — корень.

Каждый из способов обхода может быть реализован с помощью рекурсивных функций или с использованием стека. Выбор способа зависит от конкретной задачи и структуры данных, которые хранятся в узлах дерева.


Класс Node определяет узел дерева, который имеет атрибут data (данные, которые хранятся в узле), а также указатели на левый и правый подузлы.

Класс BinaryTree определяет само дерево. Он имеет атрибут root (корень дерева), которое изначально равно None.

Метод insert позволяет добавлять новые узлы в дерево. Он принимает данные для нового узла, создает новый узел и вставляет его в дерево в соответствии с правилами двоичного дерева поиска: если значение нового узла меньше значения корневого узла, он помещается в левое поддерево, иначе — в правое.

Метод search позволяет проверять, есть ли заданное значение в дереве. Он проходит по дереву от корня до листьев, сравнивая значения каждого узла с заданным значением. Если такое значение найдено, метод возвращает True, в противном случае — False.

Метод delete позволяет удалить элемент с заданным значением из дерева. Он использует вспомогательный метод _delete, который рекурсивно проходит по дереву и удаляет узел с заданным значением. Если удаляемый узел имеет только одного потомка, то этот потомок становится на его место. Если удаляемый узел имеет двух потомков, то его значение заменяется на значение наименьшего узла из правого поддерева, а этот узел удаляется.

Метод _find_min_node находит наименьший узел в дереве, начиная с заданного узла.

Метод __str__ используется для отображения дерева на экране. Он вызывает приватный метод _display, который рекурсивно обходит все узлы дерева и строит строковое представление дерева в виде ASCII-графики.

Метод _display получает на вход узел дерева и возвращает список строк, представляющих узлы этого поддерева в виде ASCII-графики. Каждая строка соответствует одному уровню дерева, а символы «_», «/» и «\» используются для отображения связей между узлами.''')

def BinaryTree():
    print('''class Node:
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
        return lines, n + m + u, max(p, q) + 2, n + u // 2''')
    
def BinaryTree1():
    print('''
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
print(tree)''')

def BinaryTree2():
    print('''
# функция для нахождения количества узлов в бинарном дереве
def count_nodes(node):
    if node is None:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)''')
    
def BinaryTree3():
    print('''class Node:
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
    
    def find_min(self):
        if self.root is None:
            return None
        current = self.root
        while current.left is not None:
            current = current.left
        return current.data

    def find_max(self):
        if self.root is None:
            return None
        current = self.root
        while current.right is not None:
            current = current.right
        return current.data


    def __str__(self):
        return '\n'.join(self._display(self.root)[0])

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
items = list(range(-11,11))
shuffle(items)

# добавление элементов в бинарное дерево
for item in items:
    tree.insert(item)

# вывод бинарного дерева на экран
print(tree)
tree.find_max(),tree.find_min()''')
    
def BinaryTree4():
    print('''
    def find(Tree, x):
        cur = Tree.root
        while True:
          if cur == None:
            return False
          if cur.data == x:
            return True
          elif cur.data < x:
            cur = cur.right
          else:
            cur = cur.left
        return False''')

def BinaryTree5():
    print('''
a = [] # глобальный список а для хранения входящих элементов

class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None        

class BinaryTree:
    
    def __init__(self):
        self.root = None
        
    def insert(self, data):
        
        global a # указываем функции, что переменную а следует считывать как глобальную
        
        new_node = Node(data)
        
        if self.root is None:
            a.append(data) # добавляем в список корень дерева
            self.root = new_node
        else:
            current = self.root
            while True:
                a.append(data) # добавляем в список последующие значения, входящие в дерево
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
                        
    def listed():
        return a # вспомогательная функция для визуализации получившегося списка (каждое значение встречается ровно столько раз, на какой глубине дерева находится)
    
    def max_leaf_deep():
        return max([BinaryTree.listed().count(i) for i in set(BinaryTree.listed())]) # с помощью генератора определяем максимальное количество вхождения в вспомогательный список
                                                                                     # => максимальное количество вхождений = максимальная глубина дерева. Считаем, что корень - нулевой уровень.
    

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
    
    def searching(self, data):
        a = []
        current = self.root
        while current is not None:
            if data == current.data:
                a.append(current.data)
                return a
            elif data < current.data:
                a.append(current.data)
                current = current.left
            else:
                a.append(current.data)
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
        return lines, n + m + u, max(p, q) + 2, n + u // 2''')
    
def BinaryTree6():
    print('''#проверить, является ли дерево полным
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
    
    def _find_minimal_level(self, current, levels):
        levels += 1
        if current is None:
            return levels
        return min(self._find_minimal_level(current.left, levels), self._find_minimal_level(current.right, levels))
    
    def _find_maximal_level(self, current, levels):
        levels += 1
        if current is None:
            return levels
        return max(self._find_maximal_level(current.left, levels), self._find_maximal_level(current.right, levels))
        
    def is_full_binary(self):
        current = self.root
        levels = 0
        minimimal_level = self._find_minimal_level(current, levels)
        maximal_level = self._find_maximal_level(current, levels)
        if (maximal_level - minimimal_level) > 1:
            return False
        else:
            return True''')

def BinaryTree7():
    print('''#найти узлы, которые имеют только одного потомка
    from random import shuffle

tree = BinaryTree()

items = list(range(1,15))
shuffle(items)

for item in items:
    tree.insert(item)
    def one_descendant(node):
    if node is None:
        return []
    result = []
    if ((node.right is None) and (node.left is not None)) or ((node.right is not None) and (node.left is None)):
        result.append(node.data)
    result += one_descendant(node.left)
    result += one_descendant(node.right)
    return result
    print(f'Узлы, которые имеют только одного потомка: {one_descendant(tree.root)}')''')
    
    
    
def HashTable_descr():
    print('''
Хеш-таблица — это структура данных, которая используется для хранения и быстрого поиска информации. Она работает на основе хеш-функции, которая преобразует входные данные (ключ) в уникальный номер (хеш), который затем используется для быстрого поиска соответствующего значения.

Хеш-таблицы обычно используются для реализации ассоциативных массивов, где ключи являются уникальными идентификаторами, а значения — связанными с ними данными. Они также широко применяются в базах данных, поисковых системах, кэшировании и других приложениях, где требуется быстрый доступ к данным.

Преимущества хеш-таблиц включают в себя быстрый поиск и вставку данных, а также возможность быстрого удаления элементов. Однако они могут быть неэффективными при большом количестве коллизий (когда два разных ключа имеют одинаковый хеш) и требуют дополнительных ресурсов для хранения хеш-таблицы.


Хеш-таблицы могут быть реализованы различными способами, включая метод цепочек (когда элементы с одинаковым хешом хранятся в связанных списках) и метод открытой адресации (когда элементы с одинаковым хешом ищутся в других ячейках таблицы).

Также стоит учитывать, что выбор хеш-функции может оказать значительное влияние на производительность хеш-таблицы. Хорошая хеш-функция должна равномерно распределять ключи по всей таблице и минимизировать количество коллизий.

Функция hash() — это встроенная функция в языке Python, которая принимает объект и возвращает его хеш-значение.

Хеш-значение — это целочисленное значение, которое вычисляется на основе содержимого объекта. Оно используется для быстрого поиска объектов в хеш-таблицах, множествах и других структурах данных. Если хеш-значение одинаково для разных объектов, но это называется коллизией и должно быть обработано соответствующим образом при реализации хеш-таблиц.


Метод цепочек — это один из способов реализации хеш-таблиц, при котором элементы с одинаковым хешем хранятся в связанных списках. Каждый элемент таблицы содержит пару «ключ–значение», где ключ — это уникальный идентификатор, а значение — это данные, связанные с этим ключом. Хеш-функция используется для вычисления индекса ячейки таблицы, где должен быть сохранен элемент.

При добавлении нового элемента с ключом  K  и значением  V , хеш-функция вычисляет индекс  i  ячейки таблицы, куда должен быть помещен элемент. Затем элемент добавляется в список, который хранится в  i -й ячейке. Если в этой ячейке уже есть элементы, то новый элемент просто добавляется в конец списка.

При поиске элемента с ключом  K , хеш-функция снова вычисляет индекс  i  ячейки таблицы, где может находиться элемент с этим ключом. Затем происходит поиск в связанном списке, который хранится в  i -й ячейке.

init(self, size): конструктор класса, который создает пустую хеш-таблицу заданного размера size.

hash_function(self, key): метод, который принимает ключ key и возвращает его хеш-значение, вычисленное с помощью встроенной функции hash(). Хеш-значение получается остатком от деления значения хеш-функции на размер таблицы, то есть приводится к диапазону от 0 до size–1.

insert(self, key, value): метод, который добавляет пару ключ-значение в хеш-таблицу. Сначала вычисляется хеш-значение ключа, затем происходит поиск пары с таким же ключом в списке элементов таблицы с этим индексом. Если такая пара уже есть, то ее значение заменяется на новое переданное значение value, и метод завершается. Если пары с таким ключом нет, то она добавляется в конец списка.

find(self, key): метод, который ищет значение по ключу в хеш-таблице. Сначала вычисляется хеш-значение ключа, затем происходит поиск пары с таким же ключом в списке элементов таблицы с этим индексом. Если такая пара найдена, то возвращается ее значение. Если пары с таким ключом нет, то метод возвращает None.


Метод открытой адресации — это другой способ реализации хеш-таблиц, при котором элементы с одинаковым хешем ищутся в других ячейках таблицы. Каждый элемент таблицы содержит пару «ключ–значение», как и в методе цепочек.

При добавлении нового элемента с ключом  K  и значением  V , хеш-функция вычисляет индекс  i  ячейки таблицы, куда должен быть помещен элемент. Если  i -я ячейка уже занята, то происходит поиск следующей свободной ячейки, используя специальную последовательность «хеш-функций открытой адресации». Эта последовательность определяет, какие ячейки должны быть проверены, чтобы найти следующую свободную ячейку.

При поиске элемента с ключом  K , хеш-функция также вычисляет индекс  i  ячейки таблицы. Если элемент с ключом  K  находится в  i -й ячейке, то поиск завершается. Если же  i -я ячейка пуста или содержит элемент с другим ключом, то происходит поиск следующей ячейки в последовательности хеш-функций открытой адресации. Если все ячейки в последовательности были проверены и элемент с ключом  K  не найден, то поиск завершается со значением «элемент не найден».

init(self, size): инициализация хеш-таблицы заданного размера size, создается список table, заполненный значениями None.

hash_function(self, key): вычисление хеша ключа key, используется простое хеширование по модулю размера таблицы.

insert(self, key, value): вставка пары «ключ–значение» в таблицу. Сначала вычисляется хеш ключа, затем производится поиск свободной ячейки с помощью цикла while. Если в ячейке уже есть элемент, то индекс ячейки увеличивается на 1 по модулю размера таблицы до тех пор, пока не будет найдена свободная ячейка. Если найдена ячейка с ключом key, то значение обновляется. В противном случае в свободную ячейку записывается пара «ключ–значение».

find(self, key): поиск значения по ключу key в таблице. Вычисляется хеш ключа, затем производится поиск значения с помощью цикла while. Если в ячейке есть элемент с ключом key, то возвращается его значение. Если ячейка свободна, значит элемента с таким ключом в таблице нет, и метод возвращает None.
''')
    
def HashTable():
    print('''
# реализация хеш-таблицы методом цепочек
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        slot = self.hash_function(key)
        for pair in self.table[slot]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[slot].append([key, value])

    def find(self, key):
        slot = self.hash_function(key)
        for pair in self.table[slot]:
            if pair[0] == key:
                return pair[1]
        return None''')

def HashTable1():
    print('''
# реализация хеш-таблицы методом открытой адресации
class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        while self.table[index]:
            if self.table[index][0] == key:
                break
            index = (index + 1) % self.size
        self.table[index] = (key, value)

    def find(self, key):
        index = self.hash_function(key)
        while self.table[index]:
            if self.table[index][0] == key:
                return self.table[index][1]
            index = (index + 1) % self.size
        return None''')
    
def HashTable2():
    print('''Создать класс «Животное» с полями «Вид», «Кличка», «Пол» и «Возраст». Создать хеш-таблицу для хранения объектов класса «Животное» по ключу — номеру чипа.
    
    # описание класса Animal
class Animal:
    def __init__(self, species, name, gender, age):
        self.species = species
        self.name = name
        self.gender = gender
        self.age = age

    def __str__(self):
        return f"Кличка: {self.name} ({self.species}), пол: {self.gender}, возраст: {self.age}"
        
# описание класса хеш-таблицы
class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash(self, chip_number):
        return hash(str(chip_number)) % self.size

    def add(self, chip_number, animal):
        index = self._hash(chip_number)
        for item in self.table[index]:
            if item[0] == chip_number:
                item[1] = animal
                return
        self.table[index].append([chip_number, animal])

    def remove(self, chip_number):
        index = self._hash(chip_number)
        for i, item in enumerate(self.table[index]):
            if item[0] == chip_number:
                del self.table[index][i]
                return

    def get(self, chip_number):
        index = self._hash(chip_number)
        for item in self.table[index]:
            if item[0] == chip_number:
                return item[1]
        return None
        
# создание хеш-таблицы
animals = HashTable()
# создание списка объектов класса Animal
list_of_animals = [Animal("собака", "Рекс", "муж.", 5), Animal("кошка", "Матильда", "жен.", 7), Animal("собака", "Белла", "жен.", 3), Animal("хомяк", "Кузьма", "муж.", 1), Animal("попугай", "Раджа", "муж.", 2)]

# вывод информации о животных
for animal in list_of_animals:
    print(animal)
    
    import random

# добавление элементов в хеш-таблицу
print('Номера чипов:')
for animal in list_of_animals:
    chip_number = random.randint(100000000, 999999999)
    print(f'{chip_number} — {animal.name}')
    animals.add(chip_number, animal)
    
    # получение объекта из хеш-таблицы по номеру чипа
print(animals.get(754416660))
print(animals.get(584617521))

# удаление объекта из хеш-таблицы по номеру чипа
animals.remove(584617521)

print(animals.get(584617521) if animals.get(584617521) else "Животного с данным номером чипа нет в хеш-таблице")

# функция для нахождения наиболее часто встречающегося значения в хеш-таблице (по полю species)
def most_common_species(hash_table):
    species_count = {}
    for slot in hash_table.table:
        for _, animal in slot:
            if animal.species in species_count:
                species_count[animal.species] += 1
            else:
                species_count[animal.species] = 1
    return max(species_count, key=species_count.get)
    
     #нахождение и вывод на экран наиболее часто встречающегося значения в хеш-таблице (по полю species)
print(f'Наиболее часто в хеш-таблице встречается значение "{most_common_species(animals)}"')
    ''')
    
def HashTable3():
    print('''
def average(table):
    count = 0
    common_sum = 0
    for slot in table.table:
        for _, value in slot:
            common_sum += int(value)
            count += 1
    return common_sum / count''')
    
def HashTable4():
    print('''
    class Country:
    def __init__(self, name, capital, population, area):
        self.name = name
        self.capital = capital
        self.population = population
        self.area = area

    def __str__(self):
        return f"Страна: {self.name}, столица: {self.capital}, население: {self.population}, площадь: {self.area}"
        
    countries = HashTable()
    
    countries_list = [Country('Россия', 'Москва', 146980061, 17098246), Country('Бразилия', 'Бразилиа', 215681045, 8515767), Country('Белоруссия', 'Минск', 9255524, 207595), Country('Бурунди', 'Гитега', 12574571, 27830)]
    
    for c in countries_list:
    countries.add(c.name, c)
    print(c)
    
#нахождение наименьшего значения в хеш-таблице
def min_count(hash_table, attr):
    mini = 10**9
    for slot in hash_table.table:
        for _, country in slot:
            if getattr(country, attr) < mini:
                mini = getattr(country, attr)
    return mini
print(f"Минимальное население {min_count(countries, 'population')}")
print(f"Минимальная площадь {min_count(countries, 'area')}")''')
    
def HashTable5():
    print('''
# описание класса хеш-таблицы
class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash(self, card_number):
        return hash(str(card_number)) % self.size

    def add(self, card_number, client):
        index = self._hash(card_number)
        for item in self.table[index]:
            if item[0] == card_number:
                item[1] = client
                return
        self.table[index].append([card_number, client])

    def remove(self, card_number):
        index = self._hash(card_number)
        for i, item in enumerate(self.table[index]):
            if item[0] == card_number:
                del self.table[index][i]
                return

    def get(self, card_number):
        index = self._hash(card_number)
        for item in self.table[index]:
            if item[0] == card_number:
                return item[1]
        return None
    
    def remove_condition(self, condition):
        for slot in self.table:
            for item in slot[:]:
                if not condition(item):
                    slot.remove(item)''')
    
    
def Sorting_descr():
    print('''
Простая обменная сортировка, также известная как сортировка пузырьком (Bubble Sort), является одним из наиболее простых алгоритмов сортировки. Этот алгоритм получил свое название из-за того, что наибольшие элементы массива «всплывают» на поверхность по мере прохода по массиву. Суть алгоритма заключается в том, что на каждом проходе сравниваются пары соседних элементов, и если они находятся в неправильном порядке, то они меняются местами. Процесс продолжается до тех пор, пока массив не будет отсортирован.

Алгоритм сортировки пузырьком состоит из следующих шагов:

Проходим по всем элементам массива данных, начиная с первого элемента.
Сравниваем текущий элемент со следующим элементом.
Если текущий элемент больше следующего элемента, меняем их местами.
Продолжаем проходить по массиву данных до тех пор, пока все элементы не будут отсортированы.


Шейкерная сортировка (Cocktail Shaker Sort) — это усовершенствованный алгоритм сортировки пузырьком. является усовершенствованным алгоритмом пузырьковой сортировки. Он работает следующим образом:

Задаем начальный и конечный индексы для массива, которые соответствуют первому и последнему элементам.

Создаем переменную (флаг), которая будет использоваться для определения того, были ли произведены какие-либо перестановки на данной итерации.

Пока начальный индекс меньше конечного индекса, повторяем следующие шаги:

a. Проходимся по массиву от начального до конечного индекса и сравниваем соседние элементы. Если текущий элемент больше следующего, меняем их местами и устанавливаем флаг в значение True.

b. Если флаг остался в значении False, то выходим из цикла, так как массив уже отсортирован.

c. Уменьшаем конечный индекс на 1 и повторяем шаги a и b.

Пока начальный индекс меньше конечного индекса, повторяем следующие шаги:

a. Проходимся по массиву от конечного до начального индекса и сравниваем соседние элементы. Если текущий элемент меньше предыдущего, меняем их местами и устанавливаем флаг в значение True.

b. Если флаг остался в значении False, то выходим из цикла, так как массив уже отсортирован.

c. Увеличиваем начальный индекс на 1 и повторяем шаги a и b.

Массив отсортирован.


Сортировка расческой (Comb Sort) — это алгоритм сортировки, который является улучшенной версией сортировки пузырьком. Он был разработан в 1980 году в команде сотрудников компании Hewlett-Packard.

Основная идея этого алгоритма заключается в том, что он использует большие промежутки для сравнения элементов массива, а затем постепенно уменьшает их до минимального значения (обычно 1). Это позволяет ему быстро перемещать большие элементы в конец массива и уменьшить количество обменов.

Алгоритм работает следующим образом:

Задаем начальный размер промежутка равный длине массива.
Сравниваем элементы на расстоянии равном заданному промежутку и меняем их местами, если необходимо.
Уменьшаем промежуток на определенный коэффициент (обычно 1.3).
Повторяем шаги 2–3 до тех пор, пока промежуток не станет равным 1.
Выполняем обычную сортировку пузырьком для окончательной сортировки.


Сортировка выбором или извлечением (Selection Sort) — это алгоритм сортировки, который на каждой итерации находит минимальный элемент в неотсортированной части массива и перемещает его в конец отсортированной части.

Алгоритм сортировки выбором можно реализовать следующим образом:

Найти наименьший элемент в неотсортированной части массива.
Обменять его с первым элементом в неотсортированной части массива.
Пометить первый элемент как отсортированный.
Повторять шаги 1–3 для оставшейся части массива, пока все элементы не будут отсортированы.


Сортировка включением или вставками (Insertion Sort) — это алгоритм сортировки, который работает путем постепенного построения отсортированного массива. На каждом шаге алгоритм берет очередной элемент массива и вставляет его в правильную позицию в уже отсортированном массиве.

Алгоритм сортировки включением имеет следующий шаги:

Начинаем с пустого массива, который считается отсортированным.

Берем первый элемент неотсортированного массива и вставляем его в правильную позицию в отсортированном массиве.

Берем следующий элемент неотсортированного массива и вставляем его в правильную позицию в отсортированном массиве.

Продолжаем этот процесс до тех пор, пока не все элементы неотсортированного массива не будут вставлены в отсортированный массив.


Быстрая сортировка (Quick Sort) — это алгоритм сортировки, основанный на принципе «разделяй и властвуй». Он был разработан Тони Хоаром в 1960 году и с тех пор стал одним из самых широко используемых алгоритмов сортировки.

Алгоритм быстрой сортировки можно разбить на несколько шагов:

Выбрать опорный элемент из массива.
Разделить массив на две части: элементы, меньшие опорного, и элементы, большие опорного.
Рекурсивно применить алгоритм быстрой сортировки к обеим частям массива.
Объединить отсортированные части массива в один отсортированный массив.


Сортировка Шелла (Shell Sort) — это алгоритм сортировки, который основан на идеи сравнения элементов, находящихся на определенном расстоянии друг от друга. Алгоритм был разработан Дональдом Шеллом в 1959 году.

Этот алгоритм является модификацией сортировки вставками, при которой сначала происходит сортировка элементов, находящихся на некотором расстоянии друг от друга, а затем это расстояние уменьшается и процесс повторяется до тех пор, пока расстояние не станет равным 1.

Принцип работы алгоритма:

Задается расстояние между элементами, которое будет изменяться на каждой итерации алгоритма.

Исходный массив разбивается на подмассивы длиной, равной заданному расстоянию.

В каждом подмассиве выполняется сортировка вставками.

Расстояние между элементами уменьшается на каждой итерации до тех пор, пока не будет достигнуто значение 1.

Наконец, выполняется полная сортировка вставками.


Сортировка слиянием (Merge Sort) — это алгоритм сортировки, который использует подход «разделяй и властвуй». Он разбивает список на две половины, рекурсивно сортирует каждую половину, а затем объединяет их в отсортированный список.

Процесс сортировки слиянием можно разбить на следующие шаги:

Разделение: Исходный массив делится пополам на две части.
Рекурсивная сортировка: Каждая половина массива сортируется рекурсивно по тому же алгоритму.
Слияние: Отсортированные половины массива сливаются в один отсортированный массив.
Повторение: Процесс повторяется до тех пор, пока весь массив не будет отсортирован.''')
    
def Sorting():
    print('''import time

class Sorting:

    # простая обменная сортировка
    @staticmethod
    def bubble_sort(arr, reverse=False):
        n = len(arr)
        for i in range(n):
            for j in range(n - i - 1):
                if not reverse:
                    if arr[j] > arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
                else:
                    if arr[j] < arr[j + 1]:
                        arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    # шейкерная сортировка
    @staticmethod
    def cocktail_sort(arr, reverse=False):
        n = len(arr)
        start = 0
        end = n - 1
        swapped = True
        while swapped:
            swapped = False
            for i in range(start, end):
                if (not reverse and arr[i] > arr[i + 1]) or (reverse and arr[i] < arr[i + 1]):
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    swapped = True
            if not swapped:
                break
            swapped = False
            end = end - 1
            for i in range(end - 1, start - 1, -1):
                if (not reverse and arr[i] > arr[i + 1]) or (reverse and arr[i] < arr[i + 1]):
                    arr[i], arr[i + 1] = arr[i + 1], arr[i]
                    swapped = True
            start = start + 1
        return arr

    # сортировка расчёской
    @staticmethod
    def comb_sort(arr, reverse=False):
        n = len(arr)
        gap = n
        shrink = 1.3
        swapped = True
        while swapped:
            gap = int(gap/shrink)
            if gap < 1:
                gap = 1
            i = 0
            swapped = False
            while i+gap < n:
                if (not reverse and arr[i] > arr[i+gap]) or (reverse and arr[i] < arr[i+gap]):
                    arr[i], arr[i+gap] = arr[i+gap], arr[i]
                    swapped = True
                i += 1
        return arr

    # сортировка выбором
    @staticmethod
    def selection_sort(arr, reverse=False):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if reverse:
                    if arr[j] > arr[min_idx]:
                        min_idx = j
                else:
                    if arr[j] < arr[min_idx]:
                        min_idx = j
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
        return arr

    # сортировка включением
    @staticmethod
    def insertion_sort(arr, reverse=False):
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and ((not reverse and arr[j] > key) or (reverse and arr[j] < key)):
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr

    # быстрая сортировка
    @staticmethod
    def quick_sort(arr, reverse=False):
        if len(arr) <= 1:
            return arr
        else:
            pivot = arr[0]
            left = []
            right = []
            for i in range(1, len(arr)):
                if arr[i] < pivot:
                    left.append(arr[i])
                else:
                    right.append(arr[i])
            if reverse:
                return Sorting.quick_sort(right, reverse=True) + [pivot] + Sorting.quick_sort(left, reverse=True)
            else:
                return Sorting.quick_sort(left) + [pivot] + Sorting.quick_sort(right)

    # сортировка Шелла
    @staticmethod
    def shell_sort(arr, reverse=False):
        gap = len(arr) // 2
        while gap > 0:
            for i in range(gap, len(arr)):
                temp = arr[i]
                j = i
                while j >= gap and ((not reverse and arr[j - gap] > temp) or (reverse and arr[j - gap] < temp)):
                    arr[j] = arr[j - gap]
                    j -= gap
                arr[j] = temp
            gap //= 2
        return arr

    # сортировка слиянием
    @staticmethod
    def merge_sort(arr, reverse=False):
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        
        left_half = Sorting.merge_sort(left_half, reverse=reverse)
        right_half = Sorting.merge_sort(right_half, reverse=reverse)
        
        return Sorting.merge(left_half, right_half, reverse=reverse)

    # вспомогательная функция для сортировки слиянием
    @staticmethod
    def merge(left_half, right_half, reverse=False):
        result = []
        i = 0
        j = 0
        while i < len(left_half) and j < len(right_half):
            if not reverse:
                if left_half[i] <= right_half[j]:
                    result.append(left_half[i])
                    i += 1
                else:
                    result.append(right_half[j])
                    j += 1
            elif reverse:
                if left_half[i] >= right_half[j]:
                    result.append(left_half[i])
                    i += 1
                else:
                    result.append(right_half[j])
                    j += 1
        result += left_half[i:]
        result += right_half[j:]
        return result

    # декоратор, вычисляющий время выполнения функции и выводящий его на экран
    def measure_time(func):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()            
            print(f"\nВремя выполнения {tuple(kwargs.items())[0][1]}_sort: {end - start:.6f} сек.")
            return result
        return wrapper

    @staticmethod
    @measure_time
    def sort(arr, method='bubble', reverse=False):
        if method == 'bubble':
            return Sorting.bubble_sort(arr, reverse)
        elif method == 'cocktail':
            return Sorting.cocktail_sort(arr, reverse)
        elif method == 'comb':
            return Sorting.comb_sort(arr, reverse)
        elif method == 'selection':
            return Sorting.selection_sort(arr, reverse)
        elif method == 'insertion':
            return Sorting.insertion_sort(arr, reverse)
        elif method == 'quick':
            return Sorting.quick_sort(arr, reverse)
        elif method == 'shell':
            return Sorting.shell_sort(arr, reverse)
        elif method == 'merge':
            return Sorting.merge_sort(arr, reverse)''')
    
def Sorting1():
    print('''from random import randint

# пример использования метода comb_sort из класса Sorting
arr = [randint(-100,100) for _ in range(40)]
print('Исходный список:\n\t', arr)
print('\nОтсортированный список:\n\t', Sorting.sort(arr, method='comb'))
import random

# создание исходного списка целых чисел
arr = random.sample(range(15000), 15000)

# вывод первых 10 элементов исходного списка
arr[:10]

import copy

# создание списка наименований алгоритмов сортировки
sorting_methods = ['bubble', 'cocktail', 'comb', 'selection','insertion', 'quick', 'shell', 'merge']

# применение каждого алгоритма сортировки для списка целых чисел
for sorting_method in sorting_methods:
    # создание глубокой копии исходного списка целых чисел
    arr_copy = copy.deepcopy(arr)
    # вызов очередного алгоритма сортировки
    sorted_arr = Sorting.sort(arr_copy, method=sorting_method)
''')
    
def Sorting2():
    print('''
#Необходимо отсортировать список слов по алфавиту и вывести результат на экран. В зависимости от переданного параметра отсортировать список слов по возрастанию или по убыванию алфавитного порядка, используя алгоритмы сортировки: сортировку вставками, сортировку выбором и быструю сортировку. Сравнить время выполнения алгоритмов сортировки с помощью декоратора. Текст хранится в файле
import csv
text = ['remains', 'primary', 'eligible', 'tab', 'ranges', 'bang', 'theme', 'exclusion', 'counseling', 'sao', 'updating', 'yale', 'registration', 'shed', 'surgery', 'affiliation', 'canvas', 'randy', 'score', 'disney', 'personally', 'agreements', 'discovery', 'binary', 'campaigns', 'arrest', 'tasks', 'features', 'everyone', 'fireplace', 'deals', 'postcards', 'inch', 'avatar', 'collectibles', 'paying', 'singapore', 'effects', 'distributor', 'eve', 'makers', 'tier', 'du', 'recent', 'meditation', 'producer', 'hope', 'assembled', 'crop', 'told', 'tons', 'posted', 'cleaner', 'peter', 'slight', 'ads', 'protocol', 'broadcast', 'hat', 'recruiting', 'tx', 'shipping', 'towards', 'refused', 'illustration', 'clouds', 'widescreen', 'ta', 'occurred', 'intend', 'lawyers', 'use', 'diagram', 'shopzilla', 'magazine', 'hewlett', 'excess', 'formal', 'meter', 'rating', 'computation', 'spy', 'particular', 'retirement', 'durable', 'independent', 'venice', 'harder', 'opened', 'taxi', 'canon', 'garbage', 'persons', 'posts', 'poster', 'costs', 'dash', 'dependent', 'airplane']
with open('text.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    for word in text:
        writer.writerow([word])
import copy

with open('text.csv') as f:
    words = f.read().splitlines()

print('Исходный список:\n\t', words)
sort_methods = ['quick', 'selection', 'insertion']
for sort_m in sort_methods:
    words_copy = copy.deepcopy(words)
    if sort_m == sort_methods[-1]:
        print('\nОтсортированный список:\n\t', Sorting.sort(words_copy, method=sort_m, reverse=False))
    else:
        sort_alg = Sorting.sort(words_copy, method=sort_m)
   
print('\nОтсортированный список:\n\t', Sorting.sort(words, method='quick', reverse=True))
 ''')