import argparse
import csv
from datetime import date
from datetime import timedelta
from datetime import datetime
from rich.console import Console
from rich.table import Table

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

settings= 'txt/settings.txt'

# Your code below this line.
def main(): 
   create_Console('Hello [blue]world[blue]')

"""
    Creates a console and prints the line 
    that is passed as a parameter
"""
def create_Console(line):
    console = Console()
    console.print(line)
 
"""
    Returns a list with each line
    of the csv file as a dictionary with
    the header as a keys
""" 
def csv_to_dict(file):
    csv = read_csv(file)
    header= next(csv)
    products=[]

    for line in csv:
        csv_dict = {x:[] for x in header}
        counter = 0
        for key in csv_dict:
            if len(line)!=0:
                csv_dict[key]=line[counter]
                counter+=1
        products.append(csv_dict)

    return products

def change_row(file,row_id,old_val,new_val):    
    csv = read_csv(file)
    rows=[]
    
    for line in csv:
        if row_id == line[0] :
            line[line.index(old_val)]=new_val

        rows.append(line)

    write_to_csv(file,rows.pop(0),'w')
    for row in rows:
        write_csv(file,row)

def get_days():
    file = open(settings,'r')
    lines = file.readlines()

    for line in lines:
        if 'days' in line:
            return int(line.split('=')[1])

    return 0

def advance_time(num):
    days = get_days()
    change_days(days+num)


def change_days(num):
    file= open(settings,'w')
    line ='days='+(str(num))
    file.write(line)

"""
    Gets the current date and adds num days to it
    and returns the date
"""
def get_date(num):
    return date.today()+timedelta(days=num)

"""
    Turn time_str,which is a string, into a datetime object
    and return it. The variable format is the format to which you would
    want to format the time
"""
def format_time(time_str,format='%Y-%m-%d'):
    return datetime.strptime(time_str,format).date()

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

def create_Table(header,arr,table_title):
    console = Console()
    table = Table(show_header=True, header_style='bold #2070b2',title=table_title)
    for column in header:
        table.add_column(column)

    for item in arr:
        table.add_row(item['product_name'],item['price'],str(item['num']),item['expiration_date'])

    console.print(table)

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
    file= open(file_path,action,newline= '')   
    csv_file= csv.writer(file)
    csv_file.writerow(data)
    return read_csv(file_path)

if __name__ == '__main__':
    main()