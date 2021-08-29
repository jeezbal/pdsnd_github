import time
import pandas as pd
import numpy as np

"""
The following are static data structures based on available data and
granulation of data analysis.
"""

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
# Note: jan=1
VALID_MONTHS = ['all','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec',
               'january','february','march','april','may','june','july','august','september',
               'october','november','december']
# Note: mon=0
VALID_DAYS = ['mon','tue','wed','thu','fri','sat','sun','all',
             'monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) dow - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city
    
    city = "None"
    while city not in CITY_DATA:
        city = input('\nChoose a city (chicago, new york city, washington): ').lower()

    # get user input for month

    month = "None"
    while month not in VALID_MONTHS:
        month = input('Choose month (all, jan, feb, ..., dec): ').lower()
    month = month[:3]
    
    # get user input for day of week

    dow = "None"
    while dow not in VALID_DAYS:
        dow = input('Choose day (all, mon, tue, ..., sun): ').lower()
    dow = dow[:3]
        
    print('-'*40)
    print('You chose {} for {} month/s and {} day/s.\n'.format(city,month,dow))
    print('-'*40)

    return city, month, dow


def load_data(city, month, dow):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) dow - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # read file using dict list
    
    df = pd.read_csv(CITY_DATA[city])
    #print(df.dtypes)
    
    # rename unnamed column
    
    df.rename(columns={'Unnamed: 0':'rowid'}, inplace=True)
    #print(df.dtypes)
    
    # add columns for filter values
    
    df['Month'] = pd.DatetimeIndex(df['Start Time']).month
    df['DOW'] = pd.DatetimeIndex(df['Start Time']).dayofweek
    #print(df.head)
    
    # filter rows by month, if applicable
    
    if month != 'all':
        df = df.loc[df['Month'] == VALID_MONTHS.index(month)]

    # filter rows by day of week, if applicable
    
    if dow != 'all':
        df = df.loc[df['DOW'] == VALID_DAYS.index(dow)]

    print(df.dtypes)
    print(df.head(5))
    return df

def display_result(result, title):
    """Interactively displays tabular outcomes"""
    
    response = input('\nDo you want to view {} resuls?  Type yes to view.'.format(title)).lower()
    
    print('You typed {}.'.format(response))
    if response in ['yes','y']:
        
        response = "None"
        while not response.isnumeric():
            response = input('How many records at a time?  Enter a number: ')
        n = int(response)
        #print('Displaying {} records at a time.  Type stop to abort display.'.format(n))
    
        x = len(result)
        i = 0
        while i < x:
            if i+n < x:
                print('Records {} to {}'.format(i+1,i+n))
                print(result.iloc[i:i+n, :])
            else:
                print('Records {} to {}'.format(i+1,x))
                print(result.iloc[i:x, :])
            response = input('Type stop to abort, or enter for next records: ').lower()
            if response == "stop":
                break
            else:
                i += n
        print('Display complete.  Enter to continue: ')
        response = input('')
        
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    
    common = df.groupby(['Month'])['rowid'].count().sort_values(ascending=False).reset_index()
    common.rename(columns={'rowid':'Month Count'}, inplace=True)
    print(common.head(1))
    
    # display the most common day of week
    
    common = df.groupby(['DOW'])['rowid'].count().sort_values(ascending=False).reset_index()
    common.rename(columns={'rowid':'DOW Count'}, inplace=True)
    print(common.head(1))    

    # TO DO: display the most common start hour

    common = df.copy()
    common['Start Hour'] = pd.DatetimeIndex(common['Start Time']).hour
    common = common.groupby(['Start Hour'])['rowid'].count().sort_values(ascending=False).reset_index()
    common.rename(columns={'rowid':'Hour Count'}, inplace=True)
    print(common.head(1))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    common = df.groupby(['Start Station'])['rowid'].count().sort_values(ascending=False).reset_index()
    common.rename(columns={'rowid':'Station Count'}, inplace=True)
    display_result(common, 'Commonly Used Start Station')

    # display most commonly used end station

    common = df.groupby(['End Station'])['rowid'].count().sort_values(ascending=False).reset_index()
    common.rename(columns={'rowid':'Station Count'}, inplace=True)
    display_result(common, 'Commonly Used End Station')

    # display most frequent combination of start station and end station trip

    common = df.groupby(['Start Station','End Station'])['rowid'].count().sort_values(ascending=False).reset_index()
    common.rename(columns={'rowid':'Combination Count'}, inplace=True)
    display_result(common, 'Most Frequent Station Combination')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    print('Total travel time:')
    print(df['Trip Duration'].sum(axis=0))

    # display mean travel time

    print('Mean travel time:')
    print(df['Trip Duration'].mean(axis=0))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    common = df.groupby(['User Type'])['rowid'].count().sort_values(ascending=False).reset_index()
    common.rename(columns={'rowid':'Type Count'}, inplace=True)
    print(common)

    # Display counts of gender

    if 'Gender' in df.columns:
        common = df.groupby(['Gender'])['rowid'].count().sort_values(ascending=False).reset_index()
        common.rename(columns={'rowid':'Gender Count'}, inplace=True)
        print(common)

    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df.columns:
        print('Earliest year of birth: ')
        print(df['Birth Year'].min(axis=0))
        
        print('Most recent year of birth: ')
        print(df['Birth Year'].max(axis=0))
        
        print('Most common year of birth: ')
        print(df['Birth Year'].mode())
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # display most commonly used windows of time
        
        time_stats(df)
        
        # display most commonly used stations
        
        station_stats(df)
        
        # display trip duration statistics
        
        trip_duration_stats(df)
        
        # display user statistics
        
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
