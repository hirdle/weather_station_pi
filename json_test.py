import json

filename = 'data.json'

with open(filename, "r") as file:
    data = json.load(file)

def delete_time(time):
    for i in range(len(data[0]['times'])):
        if data[0]['times'][i] == time:
            data[0]['times'].pop(i)
            break

def add_time(time):
    element_is = False
    for i in range(len(data[0]['times'])):
        if data[0]['times'][i] == time:
            element_is = True
            break

    if(element_is == False):
        data[0]['times'].append(time)

add_time('19:00')

with open(filename, "w") as file:
    json.dump(data, file)