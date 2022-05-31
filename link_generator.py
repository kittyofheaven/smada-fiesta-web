import random

used_number_link = []

def used_number_delete(number):
    # print(used_number_link)
    used_number_link.remove(number)
    # print(used_number_link)

def randint_wo_duplicate():   
    rand_num = random.randint(1000000, 9999999)
    if rand_num not in used_number_link:
        used_number_link.append(rand_num)
        return rand_num
    else:
        link_generator()

def link_generator(email):
    email_cut = email.lower()[0:3]
    rand_num = randint_wo_duplicate()
    return str(email_cut) + str(rand_num)


