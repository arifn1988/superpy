import argparse
import csv
from datetime import date
from datetime import timedelta

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

# Your code below this line.
def main(): 
    print(csv_to_dict('csv/bought.csv'))
 
def csv_to_dict(file):
    csv = read_csv(file)
    header= next(csv)
    products=[]

    for line in csv:
        csv_dict = {x:[] for x in header}
        counter = 0
        for key in csv_dict:
            csv_dict[key]=line[counter]
            counter+=1
        products.append(csv_dict)


    return products


def change_row(file,row_id,old_val,new_val):    
    csv = read_csv(file)
    rows=[]
    
    for line in csv:
        if row_id == line[0]:
            line[line.index(old_val)] = new_val

        rows.append(line)

    write_to_csv('csv/bought.csv',rows.pop(0),'w')
    for row in rows:
        write_csv('csv/bought.csv',row)

def set_days(num):
    return date.today()+timedelta(days=num)

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
    return write_to_csv(file_path,data,'a')

def write_to_csv(file_path,data,action):
    file= open(file_path,action)   
    csv_file= csv.writer(file)
    csv_file.writerow(data)
    return read_csv(file_path)

if __name__ == '__main__':
    main()