import csv
tab = [['mesto', 'tocke'], [1, 100], [2, 80], [3, 60], [4, 50], [5, 45], [6, 40], [7, 36], [8, 32], 
[9, 29], [10, 26], [11, 24], [12, 22], [13, 20], [14, 18], [15, 16], [16, 15], 
[17, 14], [18, 13], [19, 12], [20, 11], [21, 10], [22, 9], [23, 8], [24, 7], 
[25, 6], [26, 5], [27, 4], [28, 3], [29, 2], [30, 1]]

with open('tockovanje.csv', 'w', encoding='UTF8', newline='') as file:
    writer = csv.writer(file)
    for elt in tab:
       writer.writerow(elt)