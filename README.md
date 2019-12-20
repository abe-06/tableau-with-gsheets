# tableau-with-gsheets
Tableau with Gsheets
# Tableau with Live Data from a Gsheets Document and automatic update
As requested by the original e-mail, the following guide will apply the concepts shown on this link http://www.irarickman.com/blog/Auto-Refreshing-Tableau-Public/ with some minor changes since the author is working on a Unix environment and is feeding data through a csv file, while in our case, we are working on a ***Windows DOM*** with data being provided through a **TEST_DATA.xsl** file.

Constraints:
* There are size limitations in Rows x Columns in Google Sheets, on default the system accepts a maximum of 50.000 records to load on each sheet at once, it might be possible to push further segmenting the data on load, though this might be a attributable to hardware and not the app.
* The code ran on the file **gsheets.py** has the particularity that it deletes the entire data on the Google Sheets table each time it loads new data through the **xls** file, this is to prevent error when Tableau access the data since any change on sheets' names might cause issues
* If data is fed through a **.csv** file, then the python code would need changes

## Automatic Data Updating in Tableau Public:

These are the steps we will over for applying this concept:
- Get Tableau Public to Refresh Automatically
  - Create a Google Sheets Table
  - Create a Google APIs project 
  - Connect to Google Sheets API
  - Write a Python code to connect the xls file with Google Sheets' Table
  - Include a function to update the data
  - Create Tableau's Dashboard
  - Create Tableau's Vizze
  - Add Vizze to the webpage or app
- Scheduling the process so it updates the data periodically
  - Set Windows Task Scheduller to run the update when specified

## [ ] Create a Google Sheets Table
With a Google account, either directly through **Google Drive or Google Sheets**, create a new table and give it a name, said name will be used by the Google API to connect to the table.
## [ ] Create a Google APIs project
Once the Google Sheet is created, you will need a Google Drive API account to be able to access it through an url fetch. Follow the next steps to do so:
- Go to **https://console.developers.google.com/**
- If you have a Google account just use it to access the Google Drive API
- Once on the page, next to the Google APIs logo there will be a dropdown arrow, click on that to open a window
- On that window, at the top right corner is a folder with a plus sign, click on it to create a new project
- Next Search Google Apps for **Google Drive API** and enable it
- Now with the project created, on the left menu click on **credentials** and then select Service Account Key
- You will see a simple form on screen, make sure the option **JSON** is selected and the user is Owner.
- This will download a JSON file with all the information you will need to connect to the Google Sheet you created before
- Open said file, you will see a line starting with **"client_email"** that has something like this: **xxxxxx@tableau-with-gsheets.iam.gserviceaccount.com**
- Now go to the table you created on Google Sheets, on the top menu click on **file** then **share**, on the windows that opens, paste the client email. and submit.
- With this, you have access to the Google Sheets to be manipulated outside the web app.
## [ ] Connect the xls file with Google Sheets' Table with Python
- To make this process as simple as possible, just use the files on this repository as base
- You will need **Python** to make it work, the current version is **3.80**, get it from **https://www.python.org/downloads/release/python-380/** at the end of the page there is a link named: **Windows x86-64 executable installer**, download said file and follow the installation process.
- Then through cmd you will need to install some libraries needed to run the code, just copy and paste these commands:
```
pip install pandas
then
pip install https://github.com/nithinmurali/pygsheets/archive/master.zip
then
pip install xlrd
```
- That will install pandas, pygsheets and xlrd, three libraries to manage the xls data and the connection between python and Google Sheets
- Next on the gsheets.py file change the service_file with the location of yor JSON file
```
#authorization
gc = pygsheets.authorize(service_file='HERE_GOES_YOUR_PATH')
```
- Then change the name of the spreadsheet to match the name you gave it to yout Google Sheets Table
```
#open the google spreadsheet (where 'Tableau with GSpreadsheet' is the name of my sheet)
sh = gc.open('HERE_GOES_THE_NAME_OF_YOUR_GOOGLE_SHEETS_TABLE')
```
- And make sre the path of your xls file is correct
```
# Load Data from xls file
workbook = xlrd.open_workbook('TEST_DATA_PATH')
```
## [ ] Create Tableau's Dashboard
- On Tableau's Public Desktop app, go to the menu on the left and select **"Google Drive"** on the server options, if it does not show on the list, click on **"More..."** and look for **"Google Drive"** on the options.
- Once you select **Google Drive**, a browser window will open and will ask you for permission to access your Google Account.
- After approving access, you can close the window and on Tableau you will see your Drive's files, just select the Table you created
- Once you do, Tableau will have access to all sheets on your Table. Once you sellected how yu want to manage your sheets, subsets, joins or merges, on the bottom tags select Sheet1 and manage how you want to see your data displayed.
## [ ] Create Tableau's Vizze
- With the graphs created, save the file and it will prompt open a window to sellect the server to upload the data to, on that windows make sure the checkbox on the bottom right corner is checked, **inlude user credentials**, this will allow Tableau to aces your Google Sheet's data without having to ask permission each time it does.
## [ ] Add Vizze to the webpage or app
Go to Tableau's page at **https://public.tableau.com/** and on your profile look for the Vizze you uploaded and open it, on the bottom of the view you will have the **share** icon which will give you two choices: a link or an html line. Whichever you prefer, add to your webpage or the place you want to show the graph on. Since we are working with all the characteristics of the free version of Tableau, the system is limited to 1 automatic update every 24 hours, so Tableau's data will refresh every day at the exact time the Vizze was uploaded to the system.
## [ ] Set Windows Task Scheduller to run the update when specified
- In the previous point, Tableau refresh the data, but originally, the data is being pulled from an **xsl** file into Gsheets, so that is the data update we need to automatize. For that we will use **Windows Task Scheduller**.
- In Windows Task create a new task, with any name. Then click on **Actions**, for Program/script first go to cmd and type: 
```
python -c "import sys; print(sys.executable)"
```
- This will give you the exact path where python is on that machine, it will look something like this: **C:\Users\USER\AppData\Local\Programs\Python\Python38-32\python.exe**
- Copy that path and paste it under Programe/script
- Then on the option **Add arguments (optional)** add the name of the python file **gsheets.py**
- Next on the option **Start in (optional)** paste the path of the **folder** where python file is, it will vary depending on your file distribution but it will look soething like this: **C:\Users\USER\Documents\Tableau with Gsheets**, and click **OK**
- Now go into **Triggers** and crate a new one. Here you can schedulle when and how often you want the program to update Google Sheets, sellect the best options for your program and click OK. Take into account that this will run only when the computer is ON, there are options to do it on a python cloud server as well, if that's what you need
