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

    if 'report' in start:
        if 'inventory' in start:
            report_inventory()
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
    else:
        print('2:Select the right combination of commands')

def sell_product(args):
    product=[]

    if args['price'] ==None:
        return 'Pass price as argument'
    elif get_product_val(args['product_name'],'id')!=0 :
        csv = program.read_csv(file_bought)
        header = next(csv)   
        buy_price=header.index('buy_price')
        product=[product_id(file_sold),get_product_val(args['product_name'],'id'),program.get_today(),args['price'],get_product_val(args['product_name'],'buy_price')]
        print(product)
        program.delete_row(file_bought,args['product_name'],1)
        program.write_csv(file_sold,product)
        return 'Product sold'
    else:
        return 'Product is not in inventory'

def buy_product(args):
    if args['product_name'] and args['expiration_date'] and args['price']:
        product=[product_id(file_bought),args['product_name'],program.get_today(),args['price'],args['expiration_date']]
        program.write_csv(file_bought,product)
        return 'Product bought!!!'
    else:
        return 'Cant do anything'

def get_profit():
    csv= program.read_csv(file_sold)
    header = next(csv)
    buy_index= header.index('buy_price')
    sell_index = header.index('sell_price')
    profit = 0 

    for line in csv:
        profit+=(int(line[sell_index])-int(line[buy_index]))

    csv_inventory = program.read_csv(file_bought)
    header= next(csv_inventory)
    buy_index= header.index('buy_price')
    cost= 0 

    for line in csv_inventory:
        cost+=int(line[buy_index])

    return profit-cost

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
def report_inventory():
    csv = program.read_csv(file_bought)

    for line in csv:
        print(line)

"""
 Creates a new product id for a product
"""
def product_id(file):
    csv= program.read_csv(file)
    count =0

    for line in csv:
        count+=1

    return count

def get_product_val(pname,pval):
    csv=program.read_csv(file_bought)
    header=next(csv)
    id_index= header.index(pval)
    product_id=0

    for line in csv:
        if pname in line:
            product_id = line[id_index]
            return product_id

    return product_id

"""
    Parse args and returns them in the form of 
    a dictionary
"""
def get_arguments():
    parser =argparse.ArgumentParser()
    parser.add_argument('start',nargs='+',choices='report inventory profit revenue buy sell')
    parser.add_argument('--product-name','-p-name')
    parser.add_argument('--price','--sell-price','--buy-price')
    parser.add_argument('--expiration-date','-exp')
    time = parser.add_mutually_exclusive_group()
    time.add_argument('--date')
    time.add_argument('--now',nargs='?')
    time.add_argument('--today',nargs='?')
    args = parser.parse_args()

    return vars(args)

if __name__=='__main__':
   main()