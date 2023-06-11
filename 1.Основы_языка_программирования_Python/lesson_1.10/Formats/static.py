import csv
with open('D:/Фулстек/Progi/Formats/neprer3.csv', 'r') as f:
    reader = csv.DictReader(f)
    count = 0
    for row in reader:
        print('Координата X:' + row['X'] +' '+'Координата Y:' + row['Y'] +' '+'Координата Z:' + row['Z'])
        count += 1
        fw = open('D:/Фулстек/Progi/Formats/xyz.txt', 'a')
        fw.write(row['X']+', '+ row['Y'] +', '+ row['Z']+'\n')
    fw.close()
    
print(f'в файле {count} записи(-ей)')