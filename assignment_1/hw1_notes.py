
# Homework 1


# question 1 - without slpitting at \n
import glob as glob

def read_calls(path_to_folder): 
  file_paths = glob.glob(path_to_folder)
  data = []

  for file_path in file_paths: 
    file_name = file_path.split("/")[-1]
    match = re.match(r"([a-z]+)_(q\d)_(\d{4})\.txt", file_name) 
    if match:
      ticker = match.group(1)
      quarter = match.group(2)
      year = match.group(3)
    else: 
      print("Skipping file {file_name} - invalid format.")
      continue # continue on to the next file name and check that one
    
    with open(file_path, "r", encoding="utf-8") as f: 
            content = f.read()  # reading content of the file 
            
    
    content = content.strip()
    data.append([ticker, quarter, year, content]) # add all the elements into the empty list 
  print(f"Number of rows collected: {len(data)}")
  if len(data) > 0:
    print(f"First row of data: {data[0]}")
    
  df = pd.DataFrame(data, columns=["ticker", "quarter", "year", "content"])
  return df


path_to_folder = "/Users/ruthiemontella/Desktop/uda_notes/assignment_1/calls/*.txt"

read_calls("/Users/ruthiemontella/Desktop/uda_notes/assignment_1/calls/*.txt")


glob.glob("/Users/ruthiemontella/Desktop/uda_notes/assignment_1/calls/*.txt")


# get rid of \n 



# question 2

import requests 
import pandas as pd
import plotly.express as px
from plotly.offline import plot

#alphavantage has the data for closing price for stocks 

av_key = "LHZYEPZLB5K2R01C"

#av_symbol = "WWE" 

tickers = ["WWE", "TKO", "DIS", "CMCSA", "FOX"] # WEE and related companies 

stock_data = []

for ticker in tickers:
  url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={av_key}&outputsize=full"
  response = requests.get(url)
  data = response.json()
    
  if 'Time Series (Daily)' not in data: 
    continue  
    
  df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index') # put the data into a dataframe 
  df['symbol'] = ticker # label each stocks data with appropriate ticker
  df.reset_index(inplace=True) # adjust the indecies
  df = df.rename(columns={'index': 'date'})
  df['date'] = pd.to_datetime(df['date']) # convert from string type to date type
  df['close'] = pd.to_numeric(df['4. close']) # convert from string to numeric 
    
  # now df has date, ticker symbol and closing price - append this data to the list
  stock_data.append(df[['date', 'symbol', 'close']])

# just do the last 5 years using pandas data frame 

# get all stock data into a single DataFrame
all_stock_data = pd.concat(stock_data) 

# filter for data between 2020 and 2025
all_stock_data = all_stock_data[(all_stock_data['date'].dt.year >= 2020) & (all_stock_data['date'].dt.year <= 2025)]

# plot
fig = px.line(all_stock_data, x="date", y="close", color="symbol", title="Stock Prices for WWE and Related Companies")
plot(fig)


# question 3

from bs4 import BeautifulSoup # for static
import requests  
from urllib.parse import parse_qs

# playwrite for dynamic 
# if link is changing it is static 
# navigating over a page - look to see if there is a pattern to a link 

link = 'https://www.cagematch.net/?id=111&view=statistics' # link to website 

top100_req = requests.get(link)

top100_soup = BeautifulSoup(top100_req.content, 'html.parser') # starts to parse out the html - gives us tags and other stuff we might


link1 = soup.select_one('.TRow1 .TCol-TColSeparator a')
if link:
    # Extract the href attribute (which contains the query string)
    href = link1.get('href')  # This will get '?id=111&amp;nr=8034'

    # Use urllib.parse.parse_qs to parse the query string
    query_params = parse_qs(href)  # Converts the query string to a dictionary

    # Extract 'id' value from the query string
    id_value = query_params.get('id', [None])[0]
    nr_value = query_params.get('nr', [None])[0]

    print(f"Extracted ID: {id_value}")
    print(f"Extracted nr: {nr_value}")
else:
    print("Link not found")




# select specifically what we want off the webpage via html format - 
#top100_matches = top100_soup.select('.TRow1 .TCol-TColSeparator #111') 

#len(top100_matches) 
