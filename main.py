import json
from random import randint
import os.path


# Helper function to determine the type of an object {Хлам/Оружие/Провизия/...}
def type_obj(obj): # Определение какого типа объект (Хлам, оружие...)
    for k, v in tech["all_invent"].items():
        if obj in v:
            return k
    return False


# Output text (story) of vertex
def output_text_vert():
    # Change text with replaced {Хлам/Оружие/Провизия/...} to missed object from inventory
    if "flag_change_text_mis_obj_from_invent" in vert_now["Flag"]:
        # Cycle of all types of items and check the item for belonging to this type
        for i in tech["all_invent"].keys():     
            # Selecting elements from "all_invent" if they are not in "my_invent"
            vert_now["Text"] = vert_now["Text"].replace("{" + i + "}", list(filter(lambda x: x not in tech["my_invent"][i], tech["all_invent"][i]))[0].lower())

    # Change text with replaced {Хлам/Оружие/Провизия/...} to available  object from inventory
    if "flag_change_text_available_obj_from_invent" in vert_now["Flag"]:
        # Cycle of all types of items and check the item for belonging to this type 
        for i in tech["all_invent"].keys():
            # Selecting elements from "all_invent" if they are in "my_invent"
            vert_now["Text"] = vert_now["Text"].replace("{" + i + "}", list(filter(lambda x: x in tech["my_invent"][i], tech["all_invent"][i]))[0])

    # Output text
    if "flag_change_text_only_input"  not in vert_now["Flag"]:  #Не вывод текста, а запрос
        print(vert_now["Text"])
    # Output only input, without text
    else:
        input("Введите вопрос:    ")


# Output show (options for next steps)
def output_show_vert():
    # Does the person have these items and change the show with a postscript (yes / no)
    if "flag_change_show_do_item_exist_in_my_invent" in vert_now["Flag"]: 
        vert_now["Show"] = [vert_now["Show"][i] + " (есть)" if vert_now["use_items"][i] in tech["my_invent"][type_obj(vert_now["use_items"][i])] else vert_now["Show"][i] + " (отсутствует)" for i in range(len(vert_now["Show"]))]
        
    # Output show
    print(*vert_now["Show"], sep="    ")

    
# Automatically jump (without showing the player that there is another option) to the vertex
# Changing the list of destinations associated with flags is not displaye
def change_next():
    # Injury has a 50% chance of getting worse
    if "flag_change_next_random_worse_injury" in vert_now["Flag"]:
        vert_now["Next"][randint(0, 1)]

    # Jump to the vertex, where there "flag_use_injury"
    if "flag_change_next_change_injury" in vert_now["Flag"]:
        if "injury" in tech["all_need_state_flag_atc"]:
            vert_now["Next"] = list(filter(lambda z: "flag_use_injury" in vert_now[z]["Flag"], vert_now["Next"]))
        else:
            vert_now["Next"] = list(filter(lambda z: "flag_use_injury" not in data[z]["Flag"], vert_now["Next"]))

    # Jump to the vertex, where there "flag_change_next_letter_to_mars"
    if "flag_change_next_letter_to_mars" in vert_now["Flag"]:
        if "want_to_mars" in tech["all_need_state_flag_atc"]: 
            vert_now["Next"] = list(filter(lambda z: "flag_consent_mars" in data[z]["Flag"], vert_now["Next"]))
        else:
            vert_now["Next"] = list(filter(lambda z: "flag_consent_mars" not in data[z]["Flag"], vert_now["Next"]))

            
# Check what my_input is correct
def correct(ind):
    # Commands
    if ind in tech["Commands"]:
        if ind == "/инвентарь":
            print(tech["my_invent"])
            
        if ind == "/состояние":
            print(tech["my_state"])
        return False
    
    # Empty string, check for 1 path
    if 1 == len(vert_now["Next"]):
        return ind == ""

    # !int
    if not (ind.isdigit()):  
        return False
        
    # choice of direction with an available item
    if "flag_change_show_do_item_exist_in_my_invent" in vert_now["Flag"]:  
        return "есть" in vert_now["Show"][int(ind) - 1]

    # Defolt
    return int(ind) - 1 < len(vert_now["Show"])

    

# Direction input
def my_input():
    ind = input() # First input
    # Loop until selection is entered correctly
    while vert_now["Next"] != [] and not correct(ind):
        if ind not in tech["Commands"]:
            print("Такого варианта нет")
        print(*vert_now["Show"],sep="    ")
        # Reentry
        ind = input()
        
    # if vert_now["Next"] == [] --> End
    if vert_now["Next"] == []:
        ind = -1
        
    # if Empty string, choise first way
    if ind == "":
        ind = 1
        
    # Output
    return ind


# Changing variables that are not displayed
def change_var(ind):

    # Consent to fly to Mars
    if "flag_change_var_want_to_mars" in vert_now["Flag"]:
        tech["all_need_state_flag_atc"].append("want_to_mars")

    # Append to my_invent
    if "flag_add_inv" in vert_now["Flag"]:
        tech["my_invent"][type_obj(vert_now["add_obj"][ind - 1])].append(vert_now["add_obj"][ind - 1])
        tech["all_need_state_flag_atc"].append(vert_now["add_obj"][ind - 1])

    #Del from my_invent
    if "flag_del_inv" in vert_now["Flag"]:
        tech["my_invent"][type_obj(vert_now["add_obj"][ind - 1])].remove(vert_now["add_obj"][ind - 1])
        tech["all_need_state_flag_atc"].remove(vert_now["del_obj"][ind - 1])

    # Append to state
    if "flag_add_stat" in vert_now["Flag"]:
        tech["my_state"].append(vert_now["add_state"][ind - 1])
        tech["all_need_state_flag_atc"].append(vert_now["add_state"][ind - 1])

    # Del from state
    if "flag_del_stat" in vert_now["Flag"]:
        tech["my_state"].remove(vert_now["del_state"][ind - 1])
        tech["all_need_state_flag_atc"].remove(vert_now["del_state"][ind - 1])


# Move to next vert
def new_vert(ind):
    with open('Saving.json', 'w') as file:
        json.dump(tech, file, ensure_ascii=False, indent=4)
    tech["vert_now"] = vert_now["Next"][int(ind) - 1]
    return data[tech["vert_now"]]


# Helper func, check what input wos 1 or 2
def easy_corr_check():
    x = input("1. Да    2. Нет\n")
    while x != "1" and x != "2":
        print("Такого варинта нет")
        x = input("1. Да    2. Нет\n")
    return x


# main cycle
while True: 
    
    # Open file 
    with open('Project.json') as file:
        tech = json.load(file) # Tech - Technical information
        tech, data = tech["Tech"], tech["Out"] 
    
    vert_now = data[tech["vert_now"]]  # Vertex now
    
    # Do u have saving?
    if os.path.exists("Saving.json"):
        print("Хотите ли вы продолжить с последнего сохранения?")
        
        if easy_corr_check() == "1":
            with open('Saving.json') as Saving:
                Saving = json.load(Saving)
                vert_now = data[Saving["vert_now"]]
                tech = Saving
                
        else:
            os.remove("Saving.json")
        
        
    # cycle of one iteration    
    while True: 
        
        # Output text (story) of vertex
        output_text_vert()
    
        # Output show (options for next steps)
        output_show_vert()
    
        # Changing the list of destinations associated with flags (not displayed)
        change_next()
    
        # Direction input
        ind = int(my_input())
        if ind == -1: # -->End
            break
    
        # Сhanging variables that are not displayed
        change_var(ind)
        
        # Move to next vert
        vert_now = new_vert(ind) 
        
    # End?
    print("Конец?")
    
    # Do u want play again
    print("Хотите сыграть еще раз?")
    if easy_corr_check() == "2":
        break

print("Спасибо за игру!")
