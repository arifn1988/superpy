How to use the program

Enter into the directory superpy where the file main.py is located then run the following commands

To add a product to the inventory:
	Running : python main.py buy --product-name [product] --expiration '%Y-%m-%d' --price [price]
	This will add a product to the inventory.

	Running : python main.py buy -p-name [product] -exp '%Y-%m-%d' --price [price]
	This will add a product to the inventory.

To sell a product from the inventory :
	Running: python main.py sell --product-name [product] --price [sell-price]
	This will sell a product if it is present in the inventory. Will record the current time in the 
	program as the sell date 

	Running: python main.py sell -p-name [product] --price [sell-price]
	This will sell a product if it is present in the inventory. Will record the current time in the 
	program as the sell date 

To view the inventory :
	Running: python main.py report inventory --now or python superpy/main.py report inventory
	Will give the inventory of today.

	Running: python main.py report inventory --yesterday
	Will give the inventory of yesterday

	Running: python main.py report inventory --date 2021-11-30
	Will give the revenue of the date 2021-11-30. Be careful not the input incorrect
	dates or else the program will give a error message.

To view the revenue:
	Running :python main.py report revenue --now
	This will give the revenue of the current day.

	Running :python main.py report revenue 
	This will also give the revenue of the current day.

	Running :python main.py report revenue --yesterday
	This will give the revenue of the current day.	

	Running :python main.py report revenue --date 2021-11
	This will give the revenue of the revenue of 2021-11. On must use 
	the time format %Y-%m where Y is the year and m is the month. Anything else 
	will not work. 

To view the profit:
	Running :python main.py report profit --now
	This will give the profit of the current day.

	Running :python main.py report profit 
	This will also give the profit of the current day.

	Running :python main.py report profit --yesterday
	This will give the profit of the current day.	

	Running :python main.py profit revenue --date 2021-11
	This will give the profit of the profit of 2021-11. On must use 
	the time format %Y-%m where Y is the year and m is the month. Anything else 
	will not work. 	
	
To plot the inventory :
	Running: python main.py report inventory --date 2021-11
	Will plot the revenue of the month 2021-11. Be careful not the input incorrect
	date formats or else the program will give a error message.
To set time : 
	Running python main.py set --time [days] 
	This will add a number of days to the current time of the year. For example if today is 
	17-12-2021, then adding two days means the program time is 19-12-2021. 
	
	Running python main.py advance --time [days]
	Will advance the program time by the amount of days. For example if program time is 25-12-2021,
	then adding  three days to the program time will mean the program time will become 28-12-2021

To clear the inventory:
	Run : python main.py clear
	Which deletes all entries in bought.csv and sold.csv

To get export a overview of the sales
	Run : python main.py export-sales --date 2021-12
	Which will export all sales in the month december to a csv file called sales in the folder csv

	Run : python main.py export-sales --date 2021-12-30
	Which will export all sales for the date 2021-12-30 to a csv file called sales in the folder csv

	Run : python main.py export-sales --date 2021-12-06:2021-12-28
	Which will export all sales between the given time period (2021-12-06:2021-12-28) to a csv file called sales in the folder csv
	The first time period has to be smaller then the second one

	If one adds the command --view y to the argument then the program will print out the content of the csv file sales to 
	the console. For example running: python main.py export-sales --date 2021-12-06:2021-12-28 --view y
