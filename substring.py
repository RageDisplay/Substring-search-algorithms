class BoyerMooreSearch:
    def __init__(self, pattern):
        self.pattern = pattern
        self.table = self.make_table(pattern)

    def search(self, text):
        # Начальное смещение
        offset = 0
        # Пока остались символы для сравнения
        while offset <= len(text) - len(self.pattern):
            # Сравниваем символы с конца подстроки
            j = len(self.pattern) - 1
            while j >= 0 and self.pattern[j] == text[offset + j]:
                j -= 1
            # Если все символы совпали, то мы нашли подстроку
            if j == -1:
                return offset
            else:
                # Иначе смещаемся на максимальное из двух значений:
                # 1. Смещение, которое соответствует текущему символу в таблице смещений
                # 2. Разность между текущим символом в тексте и последним вхождением этого символа в подстроке
                offset += max(1, j - self.table.get(text[offset + j], -1))
        return -1

    def make_table(self, pattern):
        table = {}
        # Заполняем таблицу смещений для каждого символа в подстроке
        for i in range(len(pattern)):
            table[pattern[i]] = i
        return table
    
class RabinKarpSearch:
    def __init__(self, pattern):
        self.pattern = pattern
        self.table = self.make_table(pattern)
        self.prime = 101

    def search(self, text):
        # Вычисляем хеш для подстроки и первого фрагмента текста
        pattern_hash = self.hash(self.pattern)
        text_hash = self.hash(text[:len(self.pattern)])
        # Начальное смещение
        offset = 0
        # Пока остались символы для сравнения
        while offset <= len(text) - len(self.pattern):
            # Если хеши совпали, то проверяем символы по одному
            if pattern_hash == text_hash:
                j = 0
                while j < len(self.pattern) and self.pattern[j] == text[offset + j]:
                    j += 1
                # Если все символы совпали, то мы нашли подстроку
                if j == len(self.pattern):
                    return offset
            # Иначе вычисляем хеш для следующего фрагмента текста
            if offset < len(text) - len(self.pattern):
                text_hash = self.rehash(text, text_hash, offset)
            offset += 1
        return -1

    def make_table(self, pattern):
        table = {}
        # Заполняем таблицу смещений для каждого символа в подстроке
        for i in range(len(pattern)):
            table[pattern[i]] = i
        return table

    def hash(self, string):
        # Вычисляем хеш для строки
        h = 0
        for c in string:
            h = (h * self.prime + ord(c)) % 101
        return h

    def rehash(self, string, old_hash, index):
        # Вычисляем хеш для следующего фрагмента текста
        new_hash = old_hash - ord(string[index]) * pow(self.prime, len(self.pattern) - 1)
        new_hash = new_hash * self.prime + ord(string[index + len(self.pattern)])
        new_hash = new_hash % 101
        return new_hash
    
class Knut:
    def __init__(self, pattern):
        self.pattern = pattern
        self.prime = 101
        self.base = 256
        self.pattern_hash = self.hash(pattern)

    def hash(self, string):
        hash_value = 0
        for char in string:
            hash_value = (hash_value * self.base + ord(char)) % self.prime
        return hash_value

    def rehash(self, old_hash, old_char, new_char, length):
        old_hash -= (ord(old_char) * pow(self.base, length-1)) % self.prime
        old_hash = (old_hash * self.base + ord(new_char)) % self.prime
        return old_hash

    def compute_prefix_function(self, pattern):
        prefix = [0] * len(pattern)
        j = 0
        for i in range(1, len(pattern)):
            while j > 0 and pattern[j] != pattern[i]:
                j = prefix[j-1]
            if pattern[j] == pattern[i]:
                j += 1
            prefix[i] = j
        return prefix

    def search(self, text):
        n = len(text)
        m = len(self.pattern)
        prefix = self.compute_prefix_function(self.pattern)
        j = 0
        for i in range(n):
            while j > 0 and text[i] != self.pattern[j]:
                j = prefix[j-1]
            if text[i] == self.pattern[j]:
                j += 1
            if j == m:
                return i - m + 1
        return -1

    def find_all(self, text):
        n = len(text)
        m = len(self.pattern)
        prefix = self.compute_prefix_function(self.pattern)
        j = 0
        positions = []
        for i in range(n):
            while j > 0 and text[i] != self.pattern[j]:
                j = prefix[j-1]
            if text[i] == self.pattern[j]:
                j += 1
            if j == m:
                positions.append(i - m + 1)
                j = prefix[j-1]
        return positions

class FiniteAutomaton:    
    def search_fsm(pattern, text):
        m = len(pattern) # длина образца
        n = len(text) # длина текста

    # Словарь transition, содержащий состояния конечного автомата
    # Ключи - это пары (состояние, символ), а значения - это номер следующего состояния.
    # Каждое состояние определяется позицией в образце, которое указывает на текущий префикс,
    # который соответствует текущему состоянию.
        transition = {}
        for q in range(m+1):
            for c in set(text):
                prefix = pattern[:q] + c # формируем префикс для нового состояния
                k = min(m+1, q+2) # уменьшаем k до q+2, если префикс не является суффиксом
                while True:
                    k = k - 1
                    if prefix.endswith(pattern[:k]):
                        transition[q, c] = k
                        break
# Переменная matches для хранения найденных вхождений подстроки.
        matches = []
        q = 0 # начальное состояние
        for i, c in enumerate(text):
            if (q, c) in transition:
                q = transition[q, c] # переход в следующее состояние
            else:
                q = 0 # возвращаемся в начальное состояние, если символ не найден в словаре transition
            if q == m: # если достигнуто последнее состояние (завершающее)
                matches.append(i-m+1) # добавляем индекс начала вхождения в список matches
        return matches