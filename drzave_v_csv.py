import csv
prva_vrstica = ['ime_drzave', 'kratica', 'populacija', 'bdp']
drzave_in_podatki = [['Avstrija', 'AUT', 8935112, 446.315],
 ['Kanada', 'CAN', 38436447, 2016],
 ['Kitajska', 'CHN', 1411778724, 18500],
 ['Češka', 'CZE', 10701777, 276.109],
 ['Finska', 'FIN', 5536146, 277],
 ['Francija', 'FRA', 67413000, 2938],
 ['Nemčija', 'GER', 83190556, 4319],
 ['Madžarska', 'HUN', 9730000, 180.959],
 ['Italija', 'ITA', 60317116, 2106],
 ['Japonska', 'JPN', 125360000, 5378],
 ['Kazakstan', 'KAZ', 19082467, 179.813],
 ['Južna Koreja', 'KOR', 51709098, 1806],
 ['Nizozemska', 'NED', 17677800, 1012],
 ['Norveška', 'NOR', 5402171, 366],
 ['Poljska', 'POL', 38268000, 720],
 ['Romunija', 'ROU', 19186201, 289.130],
 ['Rusija', 'RUS', 146171015, 1710],
 ['Slovenija', 'SLO', 2107126, 60.9],
 ['Švica', 'SUI', 8570146, 749],
 ['Slovaška', 'SVK', 5449270, 117.664],
 ['Švedska', 'SWE', 10402070, 528.929],
 ['Ukrajina', 'UKR', 41167336, 181],
 ['Združene države Amerike', 'USA', 331893745, 22940]]

with open('drzave.csv', 'w', encoding='UTF8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(prva_vrstica)
    for i in range(len(drzave_in_podatki)):
        writer.writerow(drzave_in_podatki[i])
