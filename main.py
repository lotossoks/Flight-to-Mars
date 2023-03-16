import json
from random import randint
"""with open('Project.json') as pro:
    proj = json.load(pro)
with open('Test.json') as test:
    tech = json.load(test)["Tech"]

    
data = {"Tech": tech}
data["Out"] = {}
for k, v in proj.items():
    print(k,v)
    data["Out"][k] = {
        "Text": v["Text"],
        "Next": v["Go_to"],
        "Show": v["To_show"],
        "Flag": []
    }

with open('file.json', 'w') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)"""


def output_text_vert():  # Вывод Text на экран
    if "flag_change_text_mis_obj" in vert_now["Flag"]: #Вывод с заменой {хлам/оружие/провизия/...} на отсутствующие элементы из инвентаря
       for i in tech["all_invent"].keys():
            vert_now["Text"] = vert_now["Text"].replace(
                "{" + i + "}",
                list(filter(lambda x: x not in tech["my_invent"][i], tech["all_invent"][i]))[0].lower())
           
    if "flag_change_text_have_obj" in vert_now["Flag"]: #Вывод с заменой {хлам/оружие/провизия/...} на присутствующие элементы из инвентаря
       for i in tech["all_invent"].keys():
            vert_now["Text"] = vert_now["Text"].replace(
                "{" + i + "}",
                list(filter(lambda x: x in tech["my_invent"][i], tech["all_invent"][i]))[0])
           
    if "flag_input" in vert_now["Flag"]:  #Не вывод текста, а запрос
        input("Введите вопрос:    ")
        
    else:
        print(vert_now["Text"])  # Дефолт вывод


def type_obj(obj): # Определение какого типа объект (Хлам, оружие...)
    for k, v in tech["all_invent"].items():
        if obj in v:
            return k
    return False

def output_show_vert():  # Вывод Show (куда идти дальше)
    if "flag_choise" in vert_now["Flag"]:  #Вывод преобразованный Show (есть/нет)
        for i in range(len(vert_now["Show"])):
            if vert_now["use_items"][i] in tech["my_invent"][type_obj(vert_now["use_items"][i])]:
                vert_now["Show"][i] = vert_now["Show"][i] + " (есть)"
            else:
                vert_now["Show"][i] = vert_now["Show"][i] + " (отсутствует)"

    print(*vert_now["Show"], sep="    ")  # Дефолт вывод


def change_next():  # Изменение списка направлений, связанных с флагами
    if "flag_random_injury" in vert_now["Flag"]:
        vert_now["Next"][randint(0, 1)]
        
    if "flag_choise_injury" in vert_now["Flag"] and "injury" in tech["all_need_state_flag_atc"]:  # Ранение в состояниях
        vert_now["Next"] = list(filter(lambda z: "flag_use_injury" in vert_now[z]["Flag"], vert_now["Next"]))  # Та вершина в к-й есть флаг ранения flag_use_injury
    
    if "flag_choise_injury" in vert_now["Flag"] and "injury" not in tech["all_need_state_flag_atc"]:  # Ранение в состояниях
        vert_now["Next"] = list(filter(lambda z: "flag_use_injury" not in data[z]["Flag"], vert_now["Next"]))  # Та вершина в к-й нет флаг ранения flag_use_injury
    
    if "flag_choise_mars" in vert_now["Flag"] and "toMars" in tech["all_need_state_flag_atc"]:  #  В зависимости от выбора в вершине выбора, полет на марс - да
         vert_now["Next"] = list(filter(lambda z: "flag_consent_mars" in data[z]["Flag"], vert_now["Next"]))
        
    if "flag_choise_mars" in vert_now["Flag"] and "toMars" not in tech["all_need_state_flag_atc"]:  #  В зависимости от выбора в вершине выбора, полет на марс - нет
         vert_now["Next"] = list(filter(lambda z: "flag_consent_mars" not in data[z]["Flag"], vert_now["Next"]))


def my_input():  # Ввод направления
    ind = input()  # Ввод числа
    
    while vert_now["Next"] != [] and not correct(ind):  # Фильтрация
        if ind not in tech["Commands"]:
            print("Такого варианта нет")
        print(*vert_now["Show"],sep="    ")
        ind = input()  #Повторный ввод
    if vert_now["Next"] == []:
        ind = -1
    if ind == "":
        ind = 1
        
    return ind # Дефолт вывод


def correct(ind):  # Фильтрация my_input()
    if 1 == len(vert_now["Next"]):  # Пустая строка, проверка на 1 путь
        return ind == ""
        
    if ind in tech["Commands"]:  #Команды
        
        if ind == "/инвентарь":
            print(tech["my_invent"])
            
        if ind == "/состояние":
            print(tech["my_state"])
            
        return False
    if not (ind.isdigit()):  # !Число, отбрасываем
        return False
        
    if "flag_choise" in vert_now["Flag"]:  # Есть/Нет
        return "есть" in vert_now["Show"][int(ind) - 1]
        
    return int(ind) - 1 < len(vert_now["Show"])  #Дефолтный случай.
    
            
def change_var(ind):  # Изменение разных переменных к-х мы не показываем.
    if "flag_consent_mars_beg" in vert_now["Flag"]: # Первый выбор согласие/отказ, я соглаш
        tech["all_need_state_flag_atc"].append("toMars")
        
    if "flag_add_inv" in vert_now["Flag"]:  # Добавление в инвентарь
        tech["my_invent"][type_obj(vert_now["add_obj"][ind - 1])].append(vert_now["add_obj"][ind - 1])
        tech["all_need_state_flag_atc"].append(vert_now["add_obj"][ind - 1])
        
    if "flag_del_inv" in vert_now["Flag"]:  # Удаление из  инвентаря
        tech["my_invent"][type_obj(vert_now["add_obj"][ind - 1])].remove(vert_now["add_obj"][ind - 1])
        tech["all_need_state_flag_atc"].remove(vert_now["del_obj"][ind - 1])
        
    if "flag_add_stat" in vert_now["Flag"]:  # Добавление в состояние
        tech["my_state"].append(vert_now["add_state"][ind - 1])
        tech["all_need_state_flag_atc"].append(vert_now["add_state"][ind - 1])
        
    if "flag_del_stat" in vert_now["Flag"]:  # Удаление из состояния
        tech["my_state"].remove(vert_now["del_state"][ind - 1])
        tech["all_need_state_flag_atc"].remove(vert_now["del_state"][ind - 1])

def new_vert(ind):  # Переход на новую вершину
    return data[vert_now["Next"][int(ind) - 1]]


with open('Project.json') as file:
    tech = json.load(file)
    tech, data = tech["Tech"], tech["Out"]

vert_now = data["0/Предыстория"]  #На какой вершине сейчас

while True:  #Основной цикл
    output_text_vert()  # Вывод Text на экран
    
    output_show_vert()  # Вывод Show (куда идти дальше)
    
    change_next()  # Изменение списка направлений, связанных с флагами
    
    ind = int(my_input())  # Изменение разных переменных к-х мы не показываем.
    if ind == -1:
        break
    
    change_var(ind)
    
    vert_now = new_vert(ind)  # Переход на новую вершину
        
print("Конец?")
