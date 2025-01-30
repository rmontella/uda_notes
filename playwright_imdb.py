import pandas as pd

# The following get ran in the terminal
# pip install playwright
# python3 -m playwright install
from playwright.sync_api import sync_playwright, Playwright # allows you to scrape stuff dynamically
# scrape things where there is user input, things change upon clicks, etc. 
# if a link doesn't change upon reloding a page then the stuff is dynamically loading from somewhere else 
import re

# The following lines will activate a playwright
# browser, open a new page, and then go to the
# desired page.

pw = sync_playwright().start() # start a playwright story


chrome = pw.chromium.launch(headless=False) # telling playright to launch a chrome browser (chromium)
# headless = False means it will open a browser that we can see, touch and interact with (probably want this now so we can see what we're doing)
# headless = True means it won't open anything (takes less time)

page = chrome.new_page() # the thing that actually opens the browser

page.goto('https://www.imdb.com/title/tt0290988/reviews/?ref_=tt_ov_ql_2') # opens this link 

# page.locator('css=.ipc-see-more__text').click()

# Display all reviews

page.get_by_test_id("tturv-pagination").get_by_role("button", name="All").click()

# find all elements, get what I want (a button in this case) and its named "All", then we want to click that button 
# "tturv-pagination" - look for the names in the html 
# playwright opens a new world of functions we can use to access stuff on a page
# get_by_test_id - function that looks for test_ids and gathers them - always want to target the test_id bc it will always be there 

# The class below will grab the entire review block
# and the class can change on a whim. You'l have to
# inspect the page to find the correct class.

reviews = page.locator('css=.sc-d59f276d-1') 

# this is unique and only works right now, otherwise its constantly changing 
# the css is the class for the item we want 


# You'l always count your objects, for the sake
# of iterating over them.

reviews_count = reviews.count() # count how many reviews we have - important to know this 

# You'll make constant use of the nth() function!

reviews.nth(0).hover() # 0 index of the list - the first thing 
reviews.nth(3).click()
reviews.nth(0).locator('css=.ipc-rating-star--rating').inner_text() # get the inner text of first thing 

# The is_visible function is very useful when you have 
# include something condition (i.e., if no star is visible,
# then return None in your DataFrame).

reviews.locator('css=.ipc-list-card--border-speech').nth(3).locator('css=.ipc-rating-star').is_visible()
# not eveery text has a star rating, so if we try to pull something that isn't there you will get an error
# is_visible askes the question "is this thing there?" and if the answer is no it does something else instead 

# Lots of flexibility with how you find elements!
# Most of the time you are looking for the inner text.

review = reviews.nth(0).get_by_test_id('review-overflow').inner_text()

# You'll always have to create a list to your data!

review_list = []

for i in range(0, reviews_count):
    # A fun surprise! Some reviews have a spoiler button!
    if reviews.nth(i).get_by_role("button", name="Spoiler").is_visible():# .nth(i) for the nth thing - if you find a button that says spoiler...
        reviews.nth(i).get_by_role("button", name="Spoiler").click() #... click it! 
    # This pulls out the information from every individual review   
    review_text = reviews.locator('css=.ipc-list-card__content').nth(i).locator('css=.ipc-html-content').inner_text() # for each one, get the locator and then get the inner text 
    #review_text = reviews.nth(i).locator('css=.ipc-list-card__content').inner_text()
    # Hitting some cleanup!
    review_text = re.sub(r'\n', ' ', review_text)
    # You'll usually have to create a DataFrame for each review
    review_df = pd.DataFrame({'review': [review_text]})
    review_list.append(review_df)
    
pd.concat(review_list)

page.get_by_placeholder('Search IMDb').fill('Barbie') # placeholder search bar 'search imdb' is a placeholder 

page.locator('css=#suggestion-search-button').click()

page.locator('css=.ipc-metadata-list-summary-item__t').nth(0).click()

page.get_by_text('User reviews').click()

page.close()

chrome.close()

pw.stop()