from pprint import pprint
import csv
import re

def format_list():
    with open("phonebook_raw.csv", encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    contacts_list2 = []
    check_in = []
    for cl in contacts_list:
        if cl == contacts_list[0]:
            contacts_list2.append(["lastname","firstname","surname","organization","position","phone","email"])
            continue
        full_name = cl[0] + ' ' + cl[1] + ' ' + cl[2]
        list_full_name = re.findall("\w+", full_name)
        phone = re.findall(r'(\+?\d+)\s*\(*(\d{3})\)*[\-\s]?(\d{3})[\-\s]?(\d{2})[\-\s]?(\d{2})\s*(?:доб\.\s*(\d+))*',
                           cl[5])
        name = list_full_name[0] + list_full_name[1]
        if name in check_in:
            for people in contacts_list2:
                if list_full_name[0] == people[0] and list_full_name[1] == people[1]:
                    if len(people[2]) < 1:
                        if len(list_full_name) == 3:
                            people[2] = list_full_name[2]
                    if len(people[3]) < 1:
                        people[3] = cl[3]
                    if len(people[4]) < 1:
                        people[4] = cl[4]
                    if len(people[5]) < 1:
                        people[5] = phone
                    if len(people[6]) < 1:
                        people[6] = cl[6]
        else:
            if len(list_full_name) == 3:
                contacts_list2.append([list_full_name[0],
                                       list_full_name[1],
                                       list_full_name[2],
                                       cl[3],
                                       cl[4],
                                       phone,
                                       cl[6]])
                check_in.append(name)
            else:
                contacts_list2.append([list_full_name[0],
                                       list_full_name[1],
                                       '',
                                       cl[3],
                                       cl[4],
                                       phone,
                                       cl[6]])
                check_in.append(name)
    return contacts_list2


def phone_format(contacts_list):
    for contact in contacts_list:
        if contact == contacts_list[0]:
            continue
        if contact[5]:
            phone = contact[5][0]
            contact[5] = f"+7({phone[1]}){phone[2]}-{phone[3]}-{phone[4]}"
            if phone[5] != "":
                contact[5] += f" доб.{phone[5]}"
    return contacts_list

def output(contact_list):
    with open("phonebook_result.csv", "w", encoding='UTF-8', newline="") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contact_list)

if __name__ == "__main__":
    text1 = format_list()
    text2 = phone_format(text1)
    pprint(text2)
    output(text2)