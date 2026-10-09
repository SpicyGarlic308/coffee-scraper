import matplotlib.pyplot as plt
import sqlite3
from matplotlib.ticker import MultipleLocator
import pandas as pd
import streamlit as st
import datetime as dt

# pull data from github file
url = 'https://raw.githubusercontent.com/SpicyGarlic308/coffee-scraper/main/Coffee.csv'

# pull the data from sql database and preprocess the data for analysis
coffee_df = pd.read_csv(url, encoding="utf-8")
coffee_df['Coffee'] = coffee_df.Coffee.astype(str)
coffee_df = coffee_df[coffee_df.Cost != 'price:']
coffee_df['Cost'] = coffee_df.Cost.astype(float)
c = coffee_df.Coffee.str.split(':', expand = True)
# separate Coffee by country and type
coffee_df['country']= c[0].str.replace(':',"")
coffee_df['coffee_type'] = c[1]
# drop na values as these are likely mistakes from earlier iteration of the scraper
coffee_df.dropna(inplace = True)

# uncomment below to see df and if the preprocessing works
# print(coffee_df)

dataframe_length = len(coffee_df)
countries = coffee_df.country.unique()
country_length = len(countries)
unique_coffees = len(coffee_df.coffee_type.unique())
todays_date = dt.date.today()
formatted_date = todays_date.strftime("%d %b %Y")

#average price by country
date_df, country_list, average_price = [],[],[]

for country in countries:
    data = coffee_df[coffee_df.country == country]
    date_list = data.Date.unique().tolist()
    for date in date_list:
        date_data = data[data.Date == date]
        # print(date_data)       
        average_cost = date_data.Cost.mean()
        date_df.append(date)
        country_list.append(country)
        average_price.append(average_cost)
        
average_df = pd.DataFrame({'Date' : date_df,
                          'country' : country_list,
                          'average_cost' : average_price})

# Lots of talking and display the data
######################################
st.title('Welcome to my coffee tracker!')
st.caption(f"Last updated: {formatted_date}")

st.write(
    "Hello, and welcome to my coffee tracker! This is a project that I began in 2024 because I was curious how changes in " \
    "global politics, economics, and general shenanigans would affect the price of coffee. I am an avid coffee drinker (as " \
    "I'd imagine many of you also are) and was concerned how much or little the price of my daily motivation would change." \
    "I began this project in the middle of my degree when I had some time off. While my skills have improved somewhat, this is" \
    "still an early version of my inital program. I know there are ways that I could improve it, but honestly, it works well " \
    "enough for what I want it to do."
)

st.header('The details')
st.write(
    "This project began as a learning tool for data analysis from beginning to end. This covers the data collection, data storage (databasing)," \
    "extraction from a database, cleaning the data, and making it into something to be analyzed. Lets begin with the data collection."
)

st.subheader('Data collection')
st.write(
    "   This part was the most interesting and had the steepest learning curve. In 2024, I delved into the world of web scraping with beautifulsoup4 (bs4). I " \
    "built several rudimentry scrapers, mostly pulling news articles, speeches, or updates for policies. From these, I would summarize the data" \
    " using summarization techniques that I learned while pursuing my degree. I liked bs4 because it parsed the html data from the sites instead" \
    " of opening the webpages themselves like with Selinum or pyautogui (also pyautogui would involve MUCH more work). " \
    "Compared to the other scrapers that I have made this is really no different except that I have stayed " \
    "with this one the longest. Before understanding cron jobs, I would run this twice a month manually. Then, due to several life events, I stopped" \
    "running this bimonthly, which explains the gap from late 2025 to late 2026. I now have this running on a raspberry pi zero 2w, so as long as" \
    "I have internet, I will be collecting data and updating this dataset."
)
st.write(
    "   In the other file on my github, there will be the webscraper that I wrote. It scrapes from Coffee Bean Corral," \
    " a vendor that I have used many times. I think that they are a good metric as they sell unroasted and roasted coffee beans." \
    "Since coffee needs to be roasted to be served, understanding the sourcing of coffee really puts the final price of a cup" \
    " into a clearer picture. The scraper itself is simple. It tackles pagination well and the webpages tags" \
    " are clean and simple to run through. Later iterations needed the headers function as the webpage would block" \
    " scraping at some point in 2026. I was able to use the find_all functions with the only issue being that some" \
    " more obscure coffees would return a 'price:' value. Since there were so few in the dataset, I dropped them for " \
    "ease of use and how little they would affect the overall dataset. Overall, the scraper is a low cost option and can scale easily" \
    " as long as the web page does not change much. The tags are hardcoded, so that affects the agility and interoperablity" \
    "of the overall."
)

st.subheader('Storing and Extracting the data')
st.write(
    f"""Some would call this a big data set. This dataset has {dataframe_length} entries and is growing. Once the
    scraper has finished its scraping for the day, it saves the entries to a sqlite database that is stored on the 
    pi itself. For the analysis, it pulls the file off of the database to conduct its analysis (this program here).
    Having an sqlite database is safer, especially during a power outage or sudden shutdown of the pi during the saving
    process. It can be queried much more easily and since I am having this pi run several scrapers and saving to multiple databases on this pi, if 
    something happens concurrently, the data will be safe. Hence, this is why I am using an sqlite database to save 
    and extract the data for analysis."""
)

st.subheader('What can this be used for?')
st.write(
    """ In its current form, this data only acts as a time series to show the change of coffee prices over time.
    With some additional information and more time to see price fluctuations, an acutal analysis could be conducted.
    Basic information such as grow and harvest times, supply shortages/blockages, and other political pressure could
    be used in statisical and ML models to predict future prices. For the general population, this could inform people
    if your daily coffee with cost more or not. However, for businesses that rely fully or paritally on coffee sales,
    this could be used for business descisions. Changes could include highlighting harvest times for each region to 
    see if there is a correlation between price and time."""
)

# plotting the data

st.header('The final data!')
st.caption(f'There are a total of {unique_coffees} coffees from {country_length} countries and blends. Countries with only one coffee type were removed for space.')

for country in countries:
    data = coffee_df[coffee_df.country == country]
    average_data = average_df[average_df.country == country]
    special_coffee = list(data.coffee_type.unique())
    if len(special_coffee) == 1:
        pass
    else:
        fig, ax = plt.subplots()
        plt.figure(country + 'coffee', figsize = (10,10))
        ax.plot(average_data.Date, average_data.average_cost,
                'r',
                linestyle = 'dashed',
                label = 'Average cost for ' + country
                )
        ax.set_title(str(country) + ' ' + ' coffee cost')
        
        ax.set_ylabel('Cost')
        ax.yaxis.set_major_locator(MultipleLocator(2))
        ax.yaxis.set_minor_locator(MultipleLocator(0.5))

        ax.set_xlabel('Date')
        ax.xaxis.set_major_locator(MultipleLocator(12))
        ax.xaxis.set_minor_locator(MultipleLocator(6))
        ax.tick_params(axis="x", rotation=45)

        for special in special_coffee:
            plant_data = data[data.coffee_type == special]
            plt.figure(country + 'coffee', figsize = (10,10))
            ax.plot(plant_data.Date, plant_data.Cost, label = special)

        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray')
        ax.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))

        st.pyplot(fig)
        plt.close(fig)