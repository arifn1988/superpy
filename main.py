# Imports
import argparse
import csv
from datetime import date

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

# Your code below this line.
def main(): 
    args=get_arguments()
    if args.com=='inventory':
        csv= read_csv('csv/bought.csv')
        iterate_list(csv)
    elif args.com=='sold':
        csv = read_csv('csv/sold.csv')
        iterate_list(csv)
    elif args.com=='buy':
        product=[args.id,args.product,args.buy_date,args.price,args.expiration]
        write_csv('csv/bought.csv',product)
    elif args.com=='sell':
        product=[1,args.id,args.sell_date,args.price]
        csv = write_csv('csv/sold.csv',product)
        bought = read_csv('csv/bought.csv')
        iterate_list(bought)

def iterate_list(l_arr):
    row = next(l_arr)
    print(get_formatted_string(row).format(*row))
    for item in l_arr:
        print(get_formatted_string(item).format(*item))

def get_formatted_string(arr):
    s =""
    for x in range(len(arr)):
        s+="{}      "    
    return s

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--com')
    parser.add_argument('--id')
    parser.add_argument('--product')
    parser.add_argument('--price')
    parser.add_argument('--buy_date')
    parser.add_argument('--sell_date')
    parser.add_argument('--expiration')
    return parser.parse_args()

def count_val(products,product):
    val=0
    for item in products:
        if(product in item):
            val=val+int(item[-2])
    return val

#returns a readable csv file from 
def read_csv(file_path):
    file =open(file_path,'r')
    csv_file = csv.reader(file)
    return csv_file

def write_csv(file_path,data):
    file= open(file_path,'a')           #passing the argument 'a' to open means appending to instead of overwriting the existing data 
    csv_file= csv.writer(file)
    csv_file.writerow(data)
    return read_csv(file_path)

if __name__ == '__main__':
    main()