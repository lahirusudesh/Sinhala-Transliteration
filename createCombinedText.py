import json
from glob import glob
import os
import io
from datetime import datetime

#filename = glob('\\Sinhala_News\\AdaDerana\\adaderana*.txt')
filenames = []
data = []
today = datetime.now().date()
if __name__ == '__main__':
    folders = ['AdaDerana','Citizen','HiruNews']

    for folder in folders:
        file_location = os.path.join('Sinhala_News', folder, '*.txt')
        print(file_location)
        filenames = glob('G:\\FYP\\FYP_Approches\\'+ file_location)

        for f in filenames:
            print(f)
            x = os.path.getctime(f)
            newsdate = datetime.fromtimestamp(x)
            if(newsdate.date() == today):
                with open(f, 'r',encoding='utf-8', errors='ignore') as outfile:
                    readfile = json.load(outfile)
                    data.append(readfile)
                outfile.close()
    with open('combined.txt', 'w', encoding='utf-8', errors='ignore') as a_file:
        json.dump(data,a_file)
    print(today)