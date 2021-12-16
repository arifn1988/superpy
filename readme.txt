How to use the program

To add a product to the inventory:
	Running : python superpy/main.py buy --product-name [product] --expiration '%Y-%m-%d' --price [price]
	This will add a product to the inventory.

	Running : python superpy/main.py buy -p-name [product] -exp '%Y-%m-%d' --price [price]
	This will add a product to the inventory.

To sell a product from the inventory :
	Running: python sell --product-name [product] --price [sell-price]
	This will sell a product if it is present in the inventory. Will record the current time in the 
	program as the sell date 

	Running: python sell --p-name [product] --price [sell-price]
	This will sell a product if it is present in the inventory. Will record the current time in the 
	program as the sell date 

To view the inventory :
	Running: python superpy/main.py report inventory --now or python superpy/main.py report inventory
	Will give the inventory of today.

	Running: python superpy/main.py report inventory --yesterday
	Will give the inventory of yesterday

	Running: python superpy/main.py report inventory --date 2021-11-30
	Will give the revenue of the date 2021-11-30. Be careful not the input incorrect
	dates or else the program will give a error message.

To view the revenue:
	Running :python superpy/main.py report revenue --now
	This will give the revenue of the current day.

	Running :python superpy/main.py report revenue 
	This will also give the revenue of the current day.

	Running :python superpy/main.py report revenue --yesterday
	This will give the revenue of the current day.	

	Running :python superpy/main.py report revenue --date 2021-11
	This will give the revenue of the revenue of 2021-11. On must use 
	the time format %Y-%m where Y is the year and m is the month. Anything else 
	will not work. 

To view the profit:
	Running :python superpy/main.py report profit --now
	This will give the profit of the current day.

	Running :python superpy/main.py report profit 
	This will also give the profit of the current day.

	Running :python superpy/main.py report profit --yesterday
	This will give the profit of the current day.	

	Running :python superpy/main.py profit revenue --date 2021-11
	This will give the profit of the profit of 2021-11. On must use 
	the time format %Y-%m where Y is the year and m is the month. Anything else 
	will not work. 	
