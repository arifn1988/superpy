# Imports
import argparse
import csv
from datetime import date
from datetime import timedelta

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

# Your code below this line.
def main(): 
    csv = read_csv('csv/bought.csv')
    d_file = csv_Dict(csv)

    for key in d_file:
        print(key+' :'+str(d_file[key]))
    
"""
    Turns a csv file to a dictionary file
"""
def csv_Dict(file):
    arr= create_dict(next(file))

    for line in file:
        for key in arr:
            arr[key].append(line.pop(0))

    return arr  

def get_today():
    return date.today()

def set_days(num):
    return get_today()+timedelta(days=num)


def create_dict(arr):
    d_arr ={}

    for a in arr:
        d_arr[a] = []
    return d_arr

def delete_row(file_path,product,num):
    reader= read_csv(file_path)
    rows=[]

    for line in reader:
        rows.append(line)

    file = open(file_path,'w')
    writer = csv.writer(file)
    counter =0

    for row in rows:
        if product in row and num!=counter:
            counter+=1
        else:
            writer.writerow(row)

    return read_csv(file_path)

"""
    Formats an array
"""
def get_formatted_string(arr):
    s =""
    for x in range(len(arr)):
        s+="{}      "    
    return s

#returns a readable csv file from 
def read_csv(file_path):
    file =open(file_path,'r')
    csv_file = csv.reader(file)
    return csv_file

"""
    Append a new row of the data to the file file_path
"""
def write_csv(file_path,data):
    file= open(file_path,'a')   
    csv_file= csv.writer(file)
    csv_file.writerow(data)
    return read_csv(file_path)

if __name__ == '__main__':
    main()