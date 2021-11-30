from datetime import date
import argparse
import program

file_bought= 'csv/bought.csv'
file_sold='csv/sold.csv'

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
            print(get_profit(args))
        elif 'revenue' in start:
            print(get_revenue(args))
        else :
            print('1:Select the right combination of command')
    elif 'buy' in start and len(start)==1:
        print(buy_product(args))
    elif 'sell' in start and len(start)==1:
        print(sell_product(args))
    elif 'set' in start and 'time' in args :
        program.change_days(args['time'])
    else:
        print('2:Select the right combination of commands')

def sell_product(args):
    product=get_product('product_name',args['product_name'])

    if product:
        sale =[product_id(file_sold), product['id'],program.get_date(program.get_days()),args['price'],product['buy_price']]
        program.write_csv(file_sold,sale)
        program.change_row(file_bought,product['id'],'inventory','sold/'+str(program.get_date(program.get_days())))
        return 'Product sold'
    else:
        return 'Product is not in inventory'

def buy_product(args):
    if args['product_name'] and args['expiration_date'] and args['price']:
        exp_date= reverse_date(args['expiration_date'])
        buy_date=program.get_date(program.get_days())
        if program.format_time(exp_date)>= buy_date:
            product=[product_id(file_bought),args['product_name'],buy_date,args['price'],exp_date,'inventory']
            program.write_csv(file_bought,product)
            return 'Product bought!!!'
        else:
            return 'Expiration date is greater than buy date'
    else:
        return 'Add all the correct arguments to buy product'

def get_profit(args):
    costs =0
    csv = program.csv_to_dict(file_bought)
    
    if args['now'] or args['yesterday']:
        time = get_time(args)
        for line in csv:
            buy_date = program.format_time(line['buy_date'])
            exp_date = program.format_time(line['expiration_date'])
            if 'inventory' in line['status']:
                if buy_date<= time and exp_date>= time:
                    costs+=float(line['buy_price'])
            elif 'sold' in line['status']:
                sold_date = program.format_time(line['status'].split('/')[1])
                if buy_date>=time and sold_date<= time:
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

    return 'The profit is:'+str(get_revenue(args)-costs)

def get_revenue(args):
    revenue =0
    csv = program.csv_to_dict(file_sold)

    if args['now'] or args['yesterday']:
        time = get_time(args)
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

    return 0

"""
    Gets the inventory from the buy-date and or expiration-date. If the parameters
    of the arguments are are null are passed as parameters it prints the entire inventory
"""
def report_inventory(args):
    products = program.csv_to_dict(file_bought)
    time =get_time(args)
    inventory=[['id','product_name','price','expiration_date']]

    while len(products)!=0:
        product = products.pop(0)
        buy_date=program.format_time(product['buy_date']) 
        exp_date=program.format_time(product['expiration_date'])
        if product['status']=='inventory':
            if time>= buy_date and exp_date>=time:
                inventory.append([product['id'],product['product_name'],product['buy_price'],product['expiration_date']])
        elif 'sold' in product['status']:
            sold_date =program.format_time(product['status'].split('/')[1])
            if time >=buy_date and time<=sold_date:
                inventory.append([product['id'],product['product_name'],product['buy_price'],product['expiration_date']])
    
    program.create_Table(inventory.pop(0),inventory,'Inventory:'+str(program.get_date(program.get_days())))
    return inventory

"""
    Gets the time that is passed through to 
    argparse module and returns the datetime object
"""
def get_time(args):
    if args['yesterday']:
        return program.get_date(program.get_days()-1)
    elif args['date']:
        return program.format_time(reverse_date(args['date']))
    else:
        return program.get_date(program.get_days())

"""
    Reverses the date of date to match 
    iso format
"""
def reverse_date(date):
    arr=date.split('-')
    arr.reverse()
    return '-'.join(arr)

"""
 Creates a new product id for a product
 and returns the value of the id
"""
def product_id(file):
    csv= program.read_csv(file)
    count =0

    for line in csv: 
        count+=1

    return count

""""
    Returns a product with the pname and pval 
"""
def get_product(key_name,key_val):
    products=program.csv_to_dict(file_bought)

    for product in products:
        exp_date = program.format_time(product['expiration_date'])
        if product[key_name]==key_val and product['status']=='inventory' and exp_date>=program.get_date(program.get_days()):
                return product

    return None
"""
    Parse args and returns them in the form of 
    a dictionary
""" 
def get_arguments():
    parser =argparse.ArgumentParser()
    parser.add_argument('start',nargs='+',choices='report inventory profit revenue buy sell set')
    parser.add_argument('--time',type=int)
    parser.add_argument('--product-name','-p-name')
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