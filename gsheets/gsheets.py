import pygsheets
import pandas as pd
import xlrd

#authorization
gc = pygsheets.authorize(service_file='.\Tableau with GSheets-11b441e80281.json')

#open the google spreadsheet (where 'Tableau with GSpreadsheet' is the name of my sheet)
sh = gc.open('Tableau with GSpreadsheet')

# Load Data from xls file
workbook = xlrd.open_workbook('.\TEST_DATA.xls')

# Clear current Gsheets workbook to update with most recent Test_Data xsl dataset
if len(sh.worksheets()) > 1:
    sh.add_worksheet('Sheet1')
    for x in range(len(sh.worksheets())-1):
        sh.del_worksheet(sh[x])

# Creates an empty array variable to be filled with the values on each column 
record = list()

for x in range(workbook.nsheets):
    # Select the sheet from the xls file to be loaded into GSheets 
    worksheet = workbook.sheet_by_index(x)

    # The first sheet has the peculiarity that is automatically created by GSheets with the name Sheet1 
    # so it has a sightly different behavior on the first run

    if x == 0:
        # Creates empty dataframe
        df = pd.DataFrame()

        # Iterate through the worksheet to fill the DataFrame
        for z in range(worksheet.ncols):
            for k in range(worksheet.nrows-1):
                record.append(worksheet.cell(k+1,z).value)
            df[worksheet.cell(0,z).value] = record
            record = []

        sh[x].title = workbook.sheet_names()[x]

        # Update the first sheet with df, starting at cell A1. 
        sh[x].set_dataframe(df,(1,1))

    # Every sheet after the first one needs to be created before filling it

    else:
        # Creates empty dataframe
        df = pd.DataFrame()

        # Iterate through the worksheet to fill the DataFrame
        for z in range(worksheet.ncols):
            for k in range(worksheet.nrows-1):
                record.append(worksheet.cell(k+1,z).value)
            df[worksheet.cell(0,z).value] = record
            record = []

        sh.add_worksheet(workbook.sheet_names()[x], rows = worksheet.nrows, cols = worksheet.ncols)

        #update the created sheet with df, starting at cell A1. 
        sh[x].set_dataframe(df,(1,1))