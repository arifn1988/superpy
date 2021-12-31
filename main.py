from datetime import date
from datetime import timedelta
import csv
import argparse
from collections import Counter
from matplotlib import pyplot as plt
import numpy
import program
from pathlib import Path
from rich.console import Console
from rich.table import Table

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'

def main():
    args =get_arguments()
    start = args.pop('start')

    if len(start)>2:
        print('Too many arguments for start')
        return False
    elif 'report' in start:
        if 'inventory' in start:
            report_inventory(args)
        elif 'profit' in start:
            date =args['date'] if args['date'] else str(program.get_time(args))
            profit =  revenue='[red]The profit for[red] [green]'+date+'[green][red] for is [red] [blue]'+str(get_profit(args))+'[blue]'
            program.create_Console(profit)
        elif 'revenue' in start:
            date =args['date'] if args['date'] else str(program.get_time(args))
            revenue='[red]The revenue for[red] [green]'+date+'[green][red] for is [red] [blue]'+str(get_revenue(args))+'[blue]'
            program.create_Console(revenue)
        else :
            print('1:Select the right combination of command')
    elif 'plot' in start: 
        if'inventory' in start:
            plot_inventory(args)
    elif 'buy' in start and len(start)==1:
        print(buy_product(args))
    elif 'sell' in start and len(start)==1:
        print(sell_product(args))
    elif 'set' in start and 'time' in args :
        program.change_days(args['time'])
    elif 'advance' in start and 'time' in args:
        program.advance_time(args['time'])
    elif 'clear' in start and len(start)==1:
        clear_inventory()
    elif 'export-sales' in start:
        export_sales(args)
    else:
        print('2:Select the right combination of commands')

def export_sales(args):
    bought = list(csv.DictReader(open(program.file_bought)))
    sold = list(csv.DictReader(open(program.file_sold)))
    data=[]
    time=[]

    if ':' in args['date']:
        time = args['date'].split(':')
        time = [program.format_time(x) for x in time]
        if time[0]>time[1]:
            program.create_Console('[red]Start time[red] [green]greater than [green] [red]the end time [red]')
            quit()
    elif args['date'].count('-')==2:
        time=[program.format_time(args['date'])]*2
    elif args['date'].count('-')==1:
        time.append(program.format_time(args['date'],'%Y-%m'))
        time.append(time[0]+timedelta(days=31))
        time[1]=program.format_time(str(time[1])[0:7],'%Y-%m')
        time[1]=time[1]+timedelta(days=-1)
    else:
        print('Enter a date format that is correct')
        quit()

    for row in bought:
        status=row['status'].split('/')
        if status[0]=='sold':
            sell_date = program.format_time(status[1])
            if time[0]<=sell_date<=time[1]:
                for line in sold:
                    if row['id'] == line['bought_id']:
                        data.append([row['product_name'],row['buy_price'],line['sell_price'],line['sell_date']])

    header=['product_name','buy_price','sell_price','sell_date']

    program.write_to_csv('csv/sales.csv',header,'w+')

    for line in data:
        program.write_csv('csv/sales.csv',line)

    if len(data)==0: 
        program.create_Console('[green] No sales for the time period:[green] [red]'+str(args['date'])+'[red]')
    elif args['view']=='y':
        file = open('csv/sales.csv','r')
        sales = sorted(list(csv.DictReader(file)),key=lambda k :k['sell_date'])
        header=list(sales[0].keys())
        console = Console()

        table = Table(show_header=True, header_style='bold #2070b2',title='[green]sales overview[green]:[bold][red]'+str(args['date'])+'[red][bold]')
        for column in header:
            table.add_column(column)

        for item in sales:
            table.add_row(item['product_name'],item['buy_price'],str(item['sell_price']),item['sell_date'])

        console.print(table)
    else:
        program.create_Console('[green]Succesfully created and exported the file :[green][red]sales.csv[red]')

def sell_product(args):
    product=program.get_product('product_name',args['product_name'])

    if product:
        sale =[program.product_id(program.file_sold), product['id'],program.get_date(program.get_days()),args['price']]
        program.write_csv(program.file_sold,sale)
        program.change_row(program.file_bought,product['id'],'inventory','sold/'+str(program.get_date(program.get_days())))
        return 'Product sold'
    else:
        return 'Product is not in inventory'

def buy_product(args):
    if args['product_name'] and args['expiration_date'] and args['price']:
        exp_date= args['expiration_date']
        buy_date=program.get_date(program.get_days())
        if program.format_time(exp_date)>= buy_date:
            product=[program.product_id(program.file_bought),args['product_name'],buy_date,args['price'],exp_date,'inventory']
            program.write_csv(program.file_bought,product)
            return 'Product bought!!!'
        else:
            return 'Expiration date is lesser than buy date'
    else:
        return 'Add all the correct arguments to buy product'

def get_profit(args):
    costs =0
    csv = program.csv_to_dict(program.file_bought)
    
    if args['now'] or args['yesterday']:
        time = program.get_time(args)
        for line in csv:
            buy_date = program.format_time(line['buy_date'])
            exp_date = program.format_time(line['expiration_date'])
            if 'inventory' in line['status']:
                if buy_date==time:
                    costs+=float(line['buy_price'])
            elif 'sold' in line['status']:
                sold_date = program.format_time(line['status'].split('/')[1])
                if buy_date==time and sold_date<= time:
                    costs+=float(line['buy_price'])
    elif args['date']:
        date = program.format_time(args['date'],'%Y-%m')
        for line in csv:
            buy_date = program.format_time(line['buy_date'])
            if 'inventory' in line['status']:
                exp_date = program.format_time(line['expiration_date'])
                if buy_date.year == date.year and buy_date.month== date.month:
                    costs+=float(line['buy_price'])
            elif 'sold' in line['status']:
                sold_date = program.format_time(line['status'].split('/')[1])
                if buy_date.year == date.year and buy_date.month== date.month:
                    costs+=float(line['buy_price'])
    else:
        program.create_Console('[green]Enter the[green] [red]correct arguments[red] [green] for the program [green]')
        quit()

    return get_revenue(args)-costs

def get_revenue(args):
    revenue =0
    csv = program.csv_to_dict(program.file_sold)

    if args['now'] or args['yesterday']:
        time = program.get_time(args)
        for line in csv:
            sold_date =program.format_time(line['sell_date'])
            if sold_date ==time:
                revenue+=float(line['sell_price'])
        return revenue
    elif args['date']:
        time= program.format_time(args['date'],'%Y-%m')
        for line in csv:
            sold_date= program.format_time(line['sell_date'])
            if time.year == sold_date.year and time.month == sold_date.month:
                revenue+=float(line['sell_price'])
        return revenue
    else:
        program.create_Console('[green]Enter the[green] [red]correct arguments[red] [green] for the program [green]')
        quit()
    
    return 0

"""
    Gets the inventory from the buy-date and or expiration-date. If the parameters
    of the arguments are are null are passed as parameters it prints the entire inventory
"""
def report_inventory(args):
    products = program.csv_to_dict(program.file_bought)
    time =program.get_time(args)
    inventory=[]

    while len(products)!=0:
        product = products.pop(0)
        buy_date=program.format_time(product['buy_date']) 
        exp_date=program.format_time(product['expiration_date'])
        if product['status']=='inventory':
            if time>= buy_date and exp_date>=time:
                item='/'.join([product['product_name'],product['buy_price'],product['expiration_date']])
                inventory.append(item)
        elif 'sold' in product['status']:
            sold_date =program.format_time(product['status'].split('/')[1])
            if time >=buy_date and time<=sold_date:
                item='/'.join([product['product_name'],product['buy_price'],product['expiration_date']])
                inventory.append(item)
     
    table=[]
    counter =Counter(inventory)

    header = ['product_name','price','num','expiration_date']
    for count in counter:
        item =count.split('/')
        item.insert(2,counter[count])
        d_item=dict(zip(header,item))
        table.append(d_item)

    program.create_Table(header,table,'Inventory:'+str(program.get_time(args)))
    program.create_Console('[blue]Price[blue] : [green]Represents price per piece[green]')

def plot_inventory(args):
    csv_file= open(program.file_bought)
    csv_reader = list(csv.DictReader(csv_file))

    inventory={}
    start_time = program.format_time(args['date'],'%Y-%m') 
   
    month= start_time.month+1 if start_time.month!=12 else 1
    year= start_time.year+1 if start_time.month ==12 else start_time.year
    end_time=program.format_time('-'.join([str(year),str(month)]),'%Y-%m')

    while start_time<=end_time:
        products=[]

        for product in csv_reader:
            buy_date = program.format_time(product['buy_date'])
            p_str= '/'.join([product['product_name'],product['buy_price'],product['expiration_date']])
            if product['status'] =='inventory' :
                exp_date= program.format_time(product['expiration_date'])
                if buy_date<=start_time and start_time<=exp_date:
                    products.append(p_str)
            elif 'sold' in product['status'] :
                sold_date =program.format_time(product['status'].split('/')[1])
                if buy_date<=start_time and start_time<=sold_date:
                    products.append(p_str)
        if len(products)!=0:
            inventory[start_time]=products
    
        start_time=start_time+timedelta(days=1)

    x_axis=inventory.keys()
    y_coordinates={}    
    end = len(x_axis)
    index = 0

    for item in inventory:
        counter = Counter(inventory[item])
        for count in counter:
            if count not in y_coordinates:
                y_coordinates[count]=[0]*end
                y_coordinates[count][index]=counter[count]
            else:
                y_coordinates[count][index]=counter[count]

        index+=1

    M=program.format_time(args['date'],'%Y-%m')
    plt.title('Inventory :'+str(M.year)+'-'+str(M.month))
    plt.ylabel('dates')
    plt.xlabel('number in inventory')
    x_indexes = numpy.arange(len(x_axis))
    index_offset=-1
    width=0.25

    for y in y_coordinates:
        plt.barh(x_indexes+width*index_offset,y_coordinates[y],height=width,label=y)
        index_offset+=1

    plt.yticks(x_indexes,labels=x_axis)
    plt.legend()
    plt.show()

"""
Clears the inventory of the program and returns everything
back the beginning 
"""

def clear_inventory():
    csv_inventory = program.read_csv(program.file_bought)
    header=next(csv_inventory)
    program.write_to_csv(program.file_bought,header,'w')
    csv_sales = program.read_csv(program.file_sold)
    header = next(csv_sales)
    program.write_to_csv(program.file_sold,header,'w')


"""
    Parse args and returns them in the form of 
    a dictionary
""" 
def get_arguments():
    parser =argparse.ArgumentParser()
    commands='report inventory profit revenue buy sell set advance plot clear export-sales'
    parser.add_argument('start',nargs='+',choices=commands,help='')
    parser.add_argument('--time',type=int,help='use in combination with the command set or advance')
    parser.add_argument('--product-name', help = 'Use when you want to sell or buy a product')
    parser.add_argument('--price',help='Use when you want to buy or sell a product.')
    parser.add_argument('--expiration-date','-exp',help='Use when you want to buy a product ')
    parser.add_argument('--view')
    time = parser.add_mutually_exclusive_group()
    time.add_argument('--date',help='Use when you want to view the inventory,revenue or profit')
    time.add_argument('--now',action='store_true', help='Use when you want to view the inventory,revenue or profit of the current program time')
    time.add_argument('--yesterday',action='store_true',help='Use when you want to view the inventory,revenue or profit of yesterday')
    args = parser.parse_args()

    return vars(args)

if __name__=='__main__':
   main()