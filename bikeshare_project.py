import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please Enter the city(chicago, new york city, washington)!\n').lower()
    while city not in CITY_DATA.keys():
        city = input('Please Enter the city(chicago, new york city, washington)!\n').lower()
    if city in CITY_DATA:
        print('You choosed city : {}'.format(city))

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('please Enter the month from January to june!\n').lower()
    while month not in months:
        month = input('please Enter the month from January to june!\n').lower()
    if month in months:
        print('You choosed month : {}'.format(month))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('please Enter the day!\n').lower()
    while day not in weekdays:
        day = input('please Enter the day!\n').lower()
    if day in weekdays:
        print('You choosed day: {}'.format(day))


    print('-'*40)

    return city, month, day



def load_data(city, month, day):
    df = pd.read_csv(CITY_DATA[city])
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    print("\nThe program is loading the data for the filters of your choice.")
    start_time = time.time()

	# filter the data according to the selected city filters
    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),
                       sort=True)
        # reorganize DataFrame columns after a city concat
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])

    # create columns to display statistics
    df['Start Time'] = pd.to_datetime( df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour

    # filter the data according to month and weekday into two new DataFrames
    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] ==
                           (months.index(month)+1)], month))
    else:
        df = df[df['Month'] == (months.index(month)+1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Weekday'] ==
                           (day.title())], day))
    else:
        df = df[df['Weekday'] == day.title()]

    print("\nThis took {} seconds.".format((time.time() - start_time)))
    print('-'*40)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print(df.head())
    most_common_month = df['Month'].mode()[0]
    print('the month with the most travels is: ' + str(months[most_common_month-1]).title() + '.')

    # TO DO: display the most common day of week
    most_common_day = df['Weekday'].mode()[0]
    print('the most common day of the week is: ' + str(most_common_day) + '.')

    # TO DO: display the most common start hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('the most common start hour is: ' + str(most_common_hour) + '.')

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print(" the most common start station is: " + most_common_start_station)
    # TO DO: display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print(" the most common start end is: " + most_common_end_station)
    # TO DO: display most frequent combination of start station and end station trip
    df['combination_start_end'] = (df['Start Station'] + ' - ' + df['End Station'])
    most_common_combination = df['combination_start_end'].mode()[0]
    print('most frequent combination of start station and end station trip' + most_common_combination )
    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = (str(int(total_travel_time//86400)) + 'd ' + str(int((total_travel_time % 86400)//3600)) +'h '+str(int(((total_travel_time % 86400) % 3600)//60)) +'m ' + str(int(((total_travel_time % 86400) % 3600) % 60)) +'s')
    print('the total travel time is : ' +  total_travel_time + '.')

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = (str(int(mean_travel_time//60)) + 'm ' + str(int(mean_travel_time % 60)) + 's')
    print("the mean travel time is : " + mean_travel_time + ".")
    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User type distribution:', user_types)
    try:
   # TO DO: Display counts of gender
        genders = df['Gender'].value_counts()
        print('Gender distribution' , genders)
    except KeyError:
        print ("there is no data about gender distridution for this City")

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earliest_birth = df['Birth Year'].min()
        print('the oldest person: ' , earliest_birth)
        most_recent_birth = df['Birth Year'].max()
        print('the youngest person:' , most_recent_birth)
        common_birth = df['Birth Year'].mode()
        print('common birthday:', common_birth)
    except KeyError:
        print("There is no birth year data for this city")


    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)



def slicing (df):

    """Display 5 lines of sorted raw data each time."""

    print("\nYou wanted to display 5 lines of raw data.")

    # each loop displays 5 lines of raw data
    global from_offset
	
    from_offset = 0

    raw_data = df.iloc[from_offset:from_offset+5]

    while True:
        raw_data = df.iloc[from_offset:from_offset+5]
        print(raw_data)
        user_input = input("Do you want to keep printing raw data?\n\n[y]Yes\n[n]No\n\n>")
        if user_input in ['y','yes','YES','Yes']:
            from_offset = from_offset + 5
            continue
        else:
            break

    return raw_data
	

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data = slicing(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart not in ['yes','YES','Yes'] or restart in ['no', 'No', 'NO']:
            break


if __name__ == "__main__":
	main()
