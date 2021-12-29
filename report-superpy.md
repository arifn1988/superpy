Report on Superpy 

This program consist of two python files, superpy.py and program.py and two csv files bought.csv and sold.csv.The structure of the program is as follows:
	superpy:
		txt:
			readme.txt
			report-superpy.md
		csv:
			bought.csv
			sold.csv
		main.py
		program.py

The main.py is the file where the user should start if he wants to run the program. In program.py there are mostly helper functions for to make the code in main.py perform its work.In program.py there is the code that performs the writing data and reading data from the csv files, and main.py will call the functions from program.py the perform all the necessary work to with the csv files.
The main.py has the code that handles the user input with the argparse module.And it also contains most of the functions needed with respect to the performing the tasks of reporting the inventory,profit and revenue.

The program stores products bought by the store in bought.csv, and all products  that are sold by the store are recorded in sold.csv. The program does not delete the record of the sale from bought.csv.When a product is sold the program creates a new record in sold.csv
with a sold-id and the sell-date and the price which it was sold for. 
If a product is sold the product-id of the product will be changed to sold/[sold-date] 
One can export all the sales one has done in a given period to a csv file called sales. File sales will be made in the directory called csv.

The program-time of the program is determined by the number of days recorded in settings.txt. The program adds the number of days to the current date of the computer.If the user buys or sells a product then the buy-date or sell-date recorded will be the program-time.

To see how to use the program read the readme.txt.In it are written the commands needed to run the program.