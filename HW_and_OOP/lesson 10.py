# Задание 1 =================================================
import copy
from functools import total_ordering


class Soda:
    def __init__(self, additive: str = None):
        self.additive = additive

    def show_my_drink(self):
        return f"Газировка и {self.additive}" if self.additive else f"Обычная газировка"

soda_1 = Soda()
soda_2 = Soda("Ваниль")
print(soda_1.show_my_drink())
print(soda_2.show_my_drink())

# Задание 2 =================================================
class TriangleChecker:
    def __init__(self, a: int | float, b: int | float, c: int | float):
        self.a = a
        self.b = b
        self.c = c

    def is_triangle(self):
        if not (isinstance(self.a, (int, float)) and isinstance(self.b, (int, float)) and isinstance(self.c, (int, float))):
            return f"Нужно вводить только числа!"
        elif self.a <= 0 or self.b <= 0 or self.c <= 0:
            return f"С отрицательными числами ничего не выйдет!"
        elif self.a + self.b > self.c and self.a + self.c > self.b and self.b + self.c > self.a:
            return f"Ура, можно построить треугольник!"
        else:
            return f"Жаль, но из этого треугольник не сделать."

tr = TriangleChecker(9, 5, 7)
print(tr.is_triangle())

# Задание 3 =================================================
class KgToPounds:
    def __init__(self, __kg: int | float):
        self.__kg = __kg
        if not isinstance(self.__kg, (int, float)):
            raise ValueError

    @property
    def kg(self):
        return self.__kg

    @kg.setter
    def kg(self, value):
        self.__kg = value

    def to_pounds(self):
        return self.__kg*2.205

    # def get_kg(self):
    #     return self.__kg
    #
    # def set_kg(self, value):
    #     self.__kg = value


weight = KgToPounds(10)
print(weight.kg)
weight.kg=12
print(weight.kg)
print(weight.to_pounds())

# Задание 4 =================================================
@total_ordering
class RealString:
    def __init__(self, string: str):
        self.string = string

    def __len__(self):
        return len(self.string)

    def __eq__(self, other):
        return len(self) == len(other)

    def __gt__(self, other):
        return len(self) > len(other)

rs1 = RealString('Apple')
rs2 = RealString('Яблоко')
print(rs2 > rs1)
print('Яблоко' == rs2)

# Задание 5 =================================================
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __str__(self):
        return f"Прямоугольник шириной {self.width} и высотой {self.height}"

    def get_area(self):
        return self.width * self.height

    def get_perimeter(self):
        return 2 * (self.width + self.height)

    @property
    def is_square(self):
        return self.width == self.height

re1 = Rectangle(5, 8)
print(re1)
print(re1.get_area())
print(re1.get_perimeter())
print(re1.is_square)

# Задание 6 =================================================
class Person:
    def __init__(self, _name, age, gender):
        self._name = _name
        self.age = age
        self.gender = gender

    def __str__(self):
        return f"Имя: {self.name}, Возраст: {self.age}, Пол: {self.gender}"

    def get_name(self):
        return self.name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @staticmethod
    def is_adult(age):
        return age >= 18

    @classmethod
    def create_from_string(cls, s: str):
        s = s.split("-")
        name = s[0]
        age = int(s[1])
        gender = s[2]
        return cls(name, age, gender)

p1 = Person("Алексей", 28, "М")
print(p1)
print(p1.get_name())
p1.name = "Alexey"
print(p1.name)
print(Person.is_adult(p1.age))
p2 = Person.create_from_string("Alexey-27-M")
print(p2)

# Задание Matrix =================================================
class Matrix:
    def __init__(self, matrix: list[list[int | float]]):
        self.matrix = matrix

    def __str__(self):
        max_elem = len(str(max([max(row) for row in self.matrix])))+1
        text = ""
        for row in self.matrix:
            text += "|"
            for i in row:
                text += f" {i:<{max_elem}}"
            text += "|\n"
        return text

    def __len__(self):
        return len(self.matrix)

    def __iter__(self):
        return iter(self.matrix)

    def __dict__(self):
        return list(self.matrix)

    def __add__(self, other) -> 'Matrix':
        if len(self.matrix) == len(other.matrix) and len(self.matrix[0]) == len(other.matrix[0]):
            new_matrix = copy.deepcopy(self.matrix)
            for i in range(len(new_matrix)):
                for j in range(len(new_matrix[i])):
                    new_matrix[i][j] += other.matrix[i][j]
        else:
            raise ValueError("Матрицы разных размерностей")
        return Matrix(new_matrix)

    def __sub__(self, other) -> 'Matrix':
        if len(self.matrix) == len(other.matrix) and len(self.matrix[0]) == len(other.matrix[0]):
            new_matrix = copy.deepcopy(self.matrix)
            for i in range(len(new_matrix)):
                for j in range(len(new_matrix[i])):
                    new_matrix[i][j] -= other.matrix[i][j]
        else:
            raise ValueError("Матрицы разных размерностей")
        return Matrix(new_matrix)

    def __mul__(self, number) -> 'Matrix':
        new_matrix = copy.deepcopy(self.matrix)
        for i in range(len(new_matrix)):
            for j in range(len(new_matrix[i])):
                new_matrix[i][j] *= number
        return Matrix(new_matrix)

    @classmethod
    def transposition(cls, matrix: list[list[int | float]]) -> 'Matrix':
        new_matrix = []
        for i in range(len(list(matrix)[0])):
            list_new = []
            for j in matrix:
                list_new.append(j[i])
            new_matrix.append(list_new)
        return cls(new_matrix)

    @classmethod
    def ones_matrix(cls, n: int) -> 'Matrix':
        new_matrix = []
        for i in range(n):
            list_new = [0] * (n - 1)
            list_new.insert(i, 1)
            new_matrix.append(list_new)
        return cls(new_matrix)

    @classmethod
    def zero_matrix(cls, m: int, n: int) -> 'Matrix':
        return cls([[0] * n] * m)

    @classmethod
    def diagonal_matrix(cls, numbers: list[int | float]) -> 'Matrix':
        new_matrix = []
        for i in range(len(numbers)):
            list_new = [0] * (len(numbers) - 1)
            list_new.insert(i,numbers[i])
            new_matrix.append(list_new)
        return cls(new_matrix)

    def size(self) -> tuple[int, int]:
        """Размерность матрицы"""
        return (len(self.matrix), len(self.matrix[0]))

    def quantity(self) -> int:
        """Количество элементов"""
        return len(self.matrix) * len(self.matrix[0])

    def summ_all(self) -> int | float:
        """Сумма всех элементов"""
        sum = 0
        for i in self.matrix:
            for j in i:
                sum += j
        return sum

    def no_negative (self) -> 'Matrix':
        """Заменяет отрицательные значения нулями"""
        new_matrix = copy.deepcopy(self.matrix)
        for i in range(len(new_matrix)):
            for j in range(len(new_matrix[i])):
                if new_matrix[i][j] < 0:
                    new_matrix[i][j] = 0
        return Matrix(new_matrix)

    def __eq__(self, other) -> bool:
        if len(self.matrix) != len(other.matrix) or len(self.matrix[0]) != len(other.matrix[0]):
            return False
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != other.matrix[i][j]:
                    return False
        return True



m_1 = Matrix([[1, 2], [4, 5], [7, 8]])
m_2 = Matrix([[2, 3], [5, 6], [8, 9]])
m_3 = Matrix([[1, 2, -3], [4, 5, 6], [-7, 8, 9]])
print(f"Сумма:\n{m_1+m_2}")
# print(m_3+m_2)
m_sub = m_1-m_2
print(f"Разность:\n{m_sub}")
# print(m_3-m_2)
m_mul = m_3*20
print(f"Умножение:\n{m_mul}")
m_of_ones = Matrix.ones_matrix(5)
print(f"Единичная:\n{m_of_ones}")
m_of_zeros = Matrix.zero_matrix(6, 2)
print(f"Нулевая:\n{m_of_zeros}")
m_1_tr = Matrix.transposition(m_1)
print(m_1_tr)
m_3_tr = Matrix.transposition(m_3)
print(m_3_tr)
m_diag = Matrix.diagonal_matrix([1,3,4,6])
print(m_diag)
print(m_2.size())
print(m_2.quantity())
print(m_2.summ_all())
print(m_3.no_negative())
m_1_1 = Matrix([[1, 2], [4, 5], [7, 8]])
print(m_1 == m_1_1)
print(m_1 == m_2)