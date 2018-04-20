# final_project_yay

# SOURCE INFO:
#The data sources I used were the OMDB API, plotly and the DeviantArt API.

#OMDB documentation can be found here: http://www.omdbapi.com/
#OMDB requires an API key which can be retrieved at: http://www.omdbapi.com/apikey.aspx

#plotly also requires an api key which can be found in the API Keys tab on the profile screen
#to access that, you will have to make an account here: https://plot.ly/accounts/login/?next=%2Fsettings
#this does not need to be imported but needs to be imputted in the git credentials file
#to do this, first, you need to make a plotly account (visit https://plot.ly/)
#Second, make sure you have installed plotly on your machine 
#pip install plotly
#or 
#pip3 install plotly
#Next, grab your api key (Click your account name in the upper right > settings > navigate to API keys). From here, click regenerate key #and copy the key.
#Now, you will need to setup your plotly credentials file.  To do this, go to your terminal and enter the python shell (type 'python' or #'python3' depending on what you normally use).  You will see something like this:
#First, type in 
#import plotly
#And hit enter.  Next, type the following line in (NOTE: You need to put in your username and API key)
#plotly.tools.set_credentials_file(username='myusername', api_key='lr1c37zw8asdfasdf') 

#DeviantArt documentation can be found here: https://www.deviantart.com/developers/http/v1/20160316
#To get a client id and client secret, you must first make an account, then create and publish an app. To do so, go to 
#https://www.deviantart.com/join/ then once you are set up, to to the developers link above and click on the 
#Applications & Keys tab on the bottom left hand side and follow the instructions to make and publish the app.

#put the keys and secrets in a secrets file which should be in a .gitignore file
#each key or secret should be named with a different variable as a string then imported into the 
#main file using:
#from secrets import client_id
#from secrets import client_secret
#from secrets import OMDB_API_KEY
#the variables should be named as stated in the three lines above

# CODE STRUCTURE 
#The code first imports relevant modules and files, then it sets up a cache and cache function.
#The next four functions initialize then insert data into the two database tables which are connected
#through a primary/foreign key. These functions are init_first_db(), init_table3(), insert_data(), and insert_data2().
#My class sets up the 'more information' portion of the interactive function to print info easily.
#The interactive() function contains a while loop to get input from the user to accomplish the tasks
#in the user guide below.
#The other functions get data from their respective APIS

# USER GUIDE:
#To run and interact with the code, run it in the terminal and follow the command prompts, if you
#enter invalid commands, you will be taken back to the beginning to re-enter it properly
#You have the options of adding movie titles and information to the database (which starts with 100),
#you can also see more information about each movie, you can see 4 different types of graphs, or you 
#can exit the program.

# Additional INFO
#All info is cached but the DevaintArt API has a very short period of time where it is valid.
#The auth() function gets a new API for this every time the DeviantArt api is needed because it would otherwise have to be
#manually changed every few minutes.
