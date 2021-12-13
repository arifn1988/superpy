from datetime import date
from datetime import datetime
import argparse
import program

file_bought= 'csv/bought.csv'
file_sold='csv/sold.csv'
settings='superpy/settings.txt'
days = 0

def main():
    args =get_arguments()
    start = args.pop('start')
    
    if len(start)>2:
        print('Too many arguments for start')
        return False

    if 'report' in start:
        if 'inventory' in start:
            report_inventory(args)
        elif 'profit' in start:
            print(get_profit())
        elif 'revenue' in start:
            print(get_revenue())
        else :
            print('1:Select the right combination of command')
    elif 'buy' in start and len(start)==1:
        print(buy_product(args))
    elif 'sell' in start and len(start)==1:
        print(sell_product(args))
    elif 'set' in start:
        if -1>=args['time'] or args['time']>=0:
            print('changing time')
            change_days(args['time'])
        else:
            print('Set command must be paired with the command --time {#days}!')
    else:
        print('2:Select the right combination of commands')

def sell_product(args):
    product= get_product(file_bought,'product_name',args['product_name'])
    if product:
        sale = [product_id(file_sold),product['id'],get_today(),args['price'],product['buy_price']]
        product['status']='sold:'+str(get_today())
        program.write_csv(file_sold,sale)
        program.change_row(file_bought,product['id'],'inventory','sold/'+str(get_today()))
        return product['product_name']+' sold.' 
    else:
        return 'This product is not in stock!!!'

def buy_product(args):
    if args['product_name'] and args['expiration_date'] and args['price']:
        pname= args['product_name']
        exp = program.format_to_iso(args['expiration_date'])
        price = args['price']
        product=[product_id(file_bought),pname,get_today(),price,exp,'inventory']
        program.write_csv(file_bought,product)
        return 'Product bought!!!'
    else:
        return 'Can\'t by product'

def get_profit():
    csv= program.read_csv(file_sold)
    header = next(csv)
    buy_index= header.index('buy_price')
    sell_index = header.index('sell_price')
    sales = 0 

    for line in csv:
        sales+=int(line[sell_index])

    csv_inventory = program.read_csv(file_bought)
    header= next(csv_inventory)
    buy_index= header.index('buy_price')
    cost= 0 

    for line in csv_inventory:
        cost+=int(line[buy_index])

    return sales-cost

def get_revenue():
    revenue =0
    csv = program.read_csv(file_sold)
    header= next(csv)
    p_index = header.index('sell_price')
    
    for line in csv:
        revenue+=int(line[p_index])
    
    return revenue 

"""
    Gets the inventory from the buy-date and or expiration-date. If the parameters
    of the arguments are are null are passed as parameters it prints the entire inventory
"""
def report_inventory(args):
    product_list = program.csv_to_dict(file_bought)
    time =get_time(args)

    if not time:
        return 'No time passed through as args'

    inventory=[]
    inventory.append(['Product','num','expiration date'])

    while len(product_list)!=0:
        product = product_list.pop(0)
        buy_date=format_time(product['buy_date']) 
        exp_date=format_time(product['expiration_date'])
        if product['status']=='inventory':
            if time>= buy_date and exp_date>=time:
                inventory.append([product['id'],product['product_name'],product['buy_price'],product['expiration_date']])
        elif 'sold' in product['status']:
            sold_date =format_time(product['status'].split('/')[1])
            if time >=buy_date and time<=sold_date:
                inventory.append([product['id'],product['product_name'],product['buy_price'],product['expiration_date']])

    for item in inventory:
        print(item)

    return inventory

"""
 Creates a new product id for a product
"""
def product_id(file):
    csv= program.read_csv(file)
    count =0

    for line in csv:
        count+=1

    return count

def get_product(file,pname,pval):
    products = program.csv_to_dict(file)

    for product in products:
        if product[pname]== pval and product['status']=='inventory':
            return product

    return None

def compare_time(a_time,b_time,c_time):
    return True if c_time>= a_time and a_time >= b_time else False

"""
    Returns datetime object from the args that
    are passed through 
"""
def get_time(args):
    if args['yesterday']:
        return program.set_days(days-1)
    elif args['date']:
        return format_time(program.format_to_iso(args['date']))
    else:
        return program.set_days(days)

def format_time(time_str):
    return datetime.strptime(time_str,'%Y-%m-%d').date()

"""
    Returns the number of days in the 
    stored in the setting.txt
"""
def return_days():
    file = open(settings,'r')
    lines = file.readlines()
    days= 0

    for line in lines:
        if 'days' in line:
            days = line.split('=')
            return int(days.pop(1))

    return days

"""
    Changes the number of days in the 
    setting.txt
"""
def change_days(num):
    file = open(settings,'r')
    lines = file.readlines()
    file.close()

    new_lines=[]

    for line in lines:
        day = ''
        if 'days' in line:
            day = line.split('=')
            day[1]=str(num)
        
        new_lines.append('='.join(day))


    file= open(settings,'w')

    for line in new_lines:
        file.write(line)

    return "Time advanced by : "+str(num)+' days'
    
"""
    Returns the current day stored in 
    the program
"""
def get_today():
    days= return_days()
    return program.set_days(days)

"""
    Parse args and returns them in the form of 
    a dictionary
"""
def get_arguments():
    parser =argparse.ArgumentParser()
    parser.add_argument('start',nargs='+',choices='report inventory profit revenue buy sell set')
    parser.add_argument('--product-name','-p-name')
    parser.add_argument('--time', type= int)
    parser.add_argument('--price','--sell-price','--buy-price')
    parser.add_argument('--expiration-date','-exp')
    time = parser.add_mutually_exclusive_group()
    time.add_argument('--date')
    time.add_argument('--now',action='store_true')
    time.add_argument('--yesterday',action='store_true')
    args = parser.parse_args()

    return vars(args)

if __name__=='__main__':
   main()