myDictionary = {'1.txt': 10, '2.txt': 2, '3.txt': 15}

sorted_values = sorted(myDictionary.values()) #Сортировка словаря Python по значению
new_sorted_dictionary = { }
for i in sorted_values:
    for k in myDictionary.keys():
        if myDictionary[k] == i:
            new_sorted_dictionary[k] = myDictionary[k]
            break

for k, sorted_values in new_sorted_dictionary.items():
    print(k,sorted_values, sep = '\n')
    print('strings')

# print(*list(new_sorted_dictionary.items()), sep = '\n')