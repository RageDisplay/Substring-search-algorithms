from substring import *

text = "abracadabra"
pattern = "cadabra"

print("-------------------------------------")
bm_search = BoyerMooreSearch(pattern)
index = bm_search.search(text)
if index != -1:
    print("Подстрока найдена в позиции", index)
else:
    print("Подстрока не найдена")
print("-------------------------------------")
rk_search = RabinKarpSearch(pattern)
index = rk_search.search(text)
if index != -1:
    print("Подстрока найдена в позиции", index)
else:
    print("Подстрока не найдена")
print("-------------------------------------")
rk_search = Knut(pattern)
index = rk_search.search(text)
if index != -1:
    print("Подстрока найдена в позиции", index)
else:
    print("Подстрока не найдена")
print(rk_search.find_all(text))  #все индексы 
print("-------------------------------------")
search = FiniteAutomaton()
matches = FiniteAutomaton.search_fsm(pattern, text)
if matches != -1:
    for match in matches:
        print("Подстрока найдена в позиции", match)
print("-------------------------------------")