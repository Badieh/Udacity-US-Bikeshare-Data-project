import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    def city() :
        while True :
            city = str(input('would you like to explore chicago , new york or washington ? \n')).lower()
            cites = CITY_DATA.keys()
            if city in cites :
                return city
            else :
                print('wrong input , try again \n')
        return city

    def month() :
        while True :
            months =('january', 'february', 'march', 'april', 'may', 'june', 'all')
            month = str(input('\n\nTo filter data by a particular month, please type the month name or all for not filtering by month:\n-January\n-February\n-March\n-April\n-May\n-June\n-all\n\n:')).lower()
            if month in months :
                return month
            else :
               print('wrong input , try again \n')
        return month

    def day () :
        while True :
            days =('monday','tuesday','wednesday','thursday','friday','saturday', 'sunday', 'all')
            day =str(input('\n\nTo filter data by a particular day, please type the day name or all for not filtering by day :\n-saturday\n-sunday\n-monday\n-tuesday\n-wednesday\n-thursday\n-friday\n-all\n\n:')).lower()
            if day in days :
                return day
            else :
                print('wrong input , try again \n')
        return day

    print('Hello! Let\'s explore some US bikeshare data!')

    city = city()

    dayORmonth = str(input('woud you like to filter by day or month or not at all ? Type "none" for no time filter \n')).lower()

    if dayORmonth == 'month' :
        month = month()
        day = 'all'
    elif dayORmonth == 'day' :
        day = day()
        month = 'all'
    elif dayORmonth == 'none':
        month = 'all'
        day = 'all'

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.weekday_name
    df['Start hour'] = df['Start Time'].dt.hour
    df['End hour'] = df['End Time'].dt.hour

    # filter by month
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february','march', 'april','may','june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    # filter by day of week
    if day != 'all':
        df = df[df['day'] == day.title()]



    return df


def time_stats(df , month , day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all' :
        months = ['january', 'february','march', 'april','may','june']
        x = df['month'].mode()[0] - 1
        print('The most commen month : ',months[x])

    # display the most common day of week
    if day == 'all' :
        print('The most commen day : ',df['day'].mode()[0])

    # display the most common start hour
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('The most commonly used start station :' , df['Start Station'].mode()[0])

    # display most commonly used end station
    print('The most commonly used end station :' , df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df["combine"] = df["Start Station"] + "-" + df["End Station"]
    print('The most frequent combination of start station and end station trip : {}'.format( df["combine"].mode()[0] ))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()


    df['Trip Duration'] = df['End hour']  - df['Start hour']
    # display total travel time
    print('The total travel time : {}'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('The mean travel time : {}'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df , city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #  Display counts of user types
    user_types = df['User Type'].value_counts()

    print(user_types)
    if city =='chicago' or city == 'new york':
        # Display counts of gender
        gender = df['Gender'].value_counts()

        print(gender)

        # Display earliest, most recent, and most common year of birth
        print('The earliest year : {}'.format(df['Birth Year'].min()))
        print('The most recent year : {}'.format(df['Birth Year'].max()))
        print('The most common year : {}'.format(df['Birth Year'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(city):
    """ ask user if he wants to check the Raw Data 
    Returns 5 rows of Raw Data """
    
    display_raw = str(input('would you like to take a look at the Raw Data ? Type yes or no \n')).lower()
    while display_raw == 'yes':
        try:
            for chunk in pd.read_csv(CITY_DATA[city] , chunksize = 5):
                print(chunk)
            # repeating the question
                display_raw = str(input('Do you want to have a look on more raw data? Type yes or no\n')).lower()

                if display_raw != 'yes':
                    break
            break  

        except KeyboardInterrupt:
            print('Thank you.')

def main():
    while True:

        city, month, day = get_filters()

        df = load_data(city, month, day)

        time_stats(df , month ,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
