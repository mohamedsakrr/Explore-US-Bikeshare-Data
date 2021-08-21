import time
import pandas as pd
import numpy as np




CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }
month_list = [
     "January" ,
     "February", 
     "March"   ,
     "April"   ,
     "May"     ,
     "June"    ,
     "All"    
]
day_list = [
     
    "Monday"    ,
    "Tuesday"   ,
    "Wednesday" ,
    "Thursday"  ,
    "Friday"    ,
    "Saturday"  ,
    "Sunday"    ,
    "All"          
]



    
def get_filters():
    print('Hello! Let\'s explore some US bikeshare data!')


    city = input('Would you like to see analsys about chicago,new york or washington.').title()
    while city not in (CITY_DATA.keys()):
        print('Unfortunately, You selected wrong choice. Recheck the needed city, please!')
        city = input('Clarify needed city like to see analsys about it. chicago,new york or washington!').title()

    print("\n")


    month = input('Select month you want to see analsys about it, such January,till June, or all  for all six months.').title()
    #while month not in (month_list.keys()):
    while month not in month_list:
        print('Unfortunately, You selected wrong month.recheck the needed month, please!')
        month = input('Clarify the needed month from January,February, March, April,May, June or all  of them!').title()

    print("\n") 

    day = input('Would you like to see analsys about Sat,Sun,Mon...etc or all the week.').title()
    while day not in day_list:
    #while day not in (day_list.keys()):
        print('Unfortunately, You selected wrong month.recheck the needed day, please!')
        day = input('Clarify the needed day from week Sat,Sun,Mon...etc or all the week!').title()
    print("\n")

    print('-'*40)
    
    return city, month, day
    




def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """


    start_time = time.time()
    df = pd.read_csv(CITY_DATA.get(city), parse_dates = ["Start Time","End Time"])

    #Creation 3 new columns
    df["Start Month"],df["Start Day"],df["Start Hour"] = df["Start Time"].dt.month_name(), df["Start Time"].dt.day_name(), df["Start Time"].dt.strftime('%H:%M:%S')
    

    #Select specific month
    if month != "All":
        df = df.loc[df["Start Month"] == month]
        
    
    #Select specific day
    if day != "All":
        df = df.loc[df["Start Day"] == day]
        
    print("Done!")
    print("\nIt took {} seconds.".format(round(time.time()-start_time,2)))
    return df



def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    print('Needed data loaded.')
    # TO DO: display the most common month
    if month == "All":
        popular_month = df["Start Month"].dropna()
        if popular_month.empty:
            print("No popular month found, please recheck your data again.")
        else:
            popular_month = popular_month.mode()[0]
            print(f"Most popular month is : {popular_month}")
    
 
    
    # Display the most common day of week
    if day == "All":
        popular_day = df["Start Day"].dropna()
        if popular_day.empty:
            print("No popular day found, please rechec your data again.")
        else:
            popular_day = popular_day.mode()[0]
            print(f"Most popular day is : {popular_day}")

    # Display the most common start hour
    
        popular_hour = df["Start Hour"].dropna()
        if popular_hour.empty:
            print("No popular hour found, please recheck your data again.")
        else:
            popular_hour = popular_hour.mode()[0]
            print(f"Most popular hour is : {popular_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df["Start Station"].mode()[0]
    print(f"Most popular start station is : {popular_start_station}")

    # Display most commonly used end station
    popular_end_station = df["End Station"].mode()[0]
    print(f"Most popular end station is : {popular_end_station}")


    #Display most frequent combination of start station and end station trip   
    group_field=df.groupby(['Start Station','End Station'])
    popular_combination_station = group_field.size().sort_values(ascending=False).head(1)
    print('Most frequent combination of Start Station and End Station trip:\n', popular_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    
    total_travel_duration = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).sum()
    days =  total_travel_duration.days
    hours = total_travel_duration.seconds // (60*60)
    minutes = total_travel_duration.seconds % (60*60) // 60
    seconds = total_travel_duration.seconds % (60*60) % 60
    print(f'Total travel time is: {days} days {hours} hours {minutes} minutes {seconds} seconds')

    # Display mean travel time
    average_travel_duration = (pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])).mean()
    days =  average_travel_duration.days
    hours = average_travel_duration.seconds // (60*60)
    minutes = average_travel_duration.seconds % (60*60) // 60
    seconds = average_travel_duration.seconds % (60*60) % 60
    print(f'Average travel time is: {days} days {hours} hours {minutes} minutes {seconds} seconds')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print(df["User Type"].value_counts())
    print("\n\n")

    # Display counts of gender
    if "Gender" in (df.columns):
        gender_counts = df["Gender"].value_counts()
        print(f"Gender counts is : {gender_counts}")
        

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in (df.columns):
        year = df["Birth Year"].dropna().astype("int64")

        print(f"""
        The earliest birth year is :{year.min()}
        The most resent birth year is: {year.max()}
        The most common year of birth is:{year.mode()[0]}""")        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    """ Print 5 rows from raw data every time"""
    choice = input("Would you like to see 5 raws from data raw? [Y / N]:").upper()
    
    count = 0
    if choice == "Y" :
        for row in df.iterrows():
            print(row)
            count +=1
            if count !=0 and count% 5 == 0 :
                choice = input("Would you like to see raw data?  [Y / N] :").upper()
                if choice != "Y":
                    break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city,month,day)
        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)
        
        restart = input('\nWould you like to restart??  [Y / N] : \n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()

