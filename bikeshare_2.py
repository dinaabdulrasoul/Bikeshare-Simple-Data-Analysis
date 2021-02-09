import pandas as pd
import numpy as np
import calendar
import time

# Creating a dictionary containing the CSV filenames
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ""
    print('Hello! Let\'s explore some US bikeshare data!')
    # Getting the user input for city (chicago, new york city, washington).
    while city not in CITY_DATA.keys():
        print("\nPlease choose your city:\n 1.New York City\n 2.Chicago \n 3.Washington")
        print("\nYou may enter the name of the city in either uppercase, lowercase or titlecase.")
              
        # Making sure the city is in lowercase like our dataset
        city = input().lower()
        
        # Checking if the user input is valid or not:
        if city not in CITY_DATA.keys():
            print("Your input is invalid, please check your input format and start over.")
              
    print("\nAwesome! You have chosen",city.title() ,"as your city.")

    # Getting the user's input for month (all, january, february, ... , june)
              
    #Creating a dictionary to store all the months including the 'all' option
    MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'all': 7}
    month = ''
    while month not in MONTH_DATA.keys():
        print("\nPlease enter the month in string format, for example January.\nOr type all to show data for all months.")
        print("\nPlease note that the data is available from January to June only.")
        print("\nYou may enter the month in either uppercase, lowercase or titlecase.")
        month = input().lower()

        if month not in MONTH_DATA.keys():
            print("Your input is invalid, please check your input format and start over.")

    print("\nAwesome! You have chosen", month.title() ,"as your month.")


    # Getting the user's input for day of week (all, monday, tuesday, ... sunday)
    #Creating a dictionary to store all the months including the 'all' option
    DAY_DATA = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    day = ''
    while day not in DAY_DATA:
        print("\nPlease enter the day in string format, for example Sunday.\nOr type all to show data for all days.")
        print("\nYou may enter the day in either uppercase, lowercase or titlecase.")
        day = input().lower()

        if day not in DAY_DATA:
            print("Your input is invalid, please check your input format and start over.")

    print("\nAwesome! You have chosen ", day.title() ," as your day.")
    print("\nYou have chosen to view data for city:",city.title(), ",for month/s:", month.title(), 
          "and day/s:" ,day.title())

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
    print("Loading data for city: ", city.title())
    df = pd.read_csv(CITY_DATA[city])
              
    # Converting all the start times into datetime objects to be able to sort it
    df['Start Time'] = pd.to_datetime(df['Start Time'])
              
    # Extracting month and day of the week from the data
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
              
    # Filtering by month:     
    if month!= 'all':
        # Using the index to get the corrosponding month from our data
        months_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months_list.index(month) + 1
        df = df[df['month']== month]
              
    # Filtering by day:         
    if day!= 'all':
        df = df[df['day_of_week'] == day.title()]
              
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month:        
    popular_month = df['month'].mode()[0]
    # Converting the month number to month name
    popular_month = calendar.month_name[popular_month]
    print('\nThe most common month is: ', popular_month)

    # display the most common day of the week:
    popular_day = df['day_of_week'].mode()[0]
    print('\nThe most common day is: ', popular_day)


    # Creating an hour column 
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
              
    # Displaying the most common start hour
    print('\nThe most common start hour is: ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("\nThe most common start station is ", popular_start)

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print("\nThe most common start station is ", popular_end)


    # display most frequent combination of start station and end station trip
    df['start_to_end'] = df['Start Station'].str.cat(df['End Station'], sep = ' to ')
    combination = df['start_to_end'].mode()[0]
    print("\nThe most common combination for the start to end stations is: ", combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("The total travel time is: ", total_time)


    # display mean travel time
    mean_time = np.mean(df['Trip Duration'])
    print("The average travel time is: ", mean_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nDisplaying the counts of different user types...")
    print(user_types.to_string())

    # Display counts of gender 
    # Note that not all files may have the 'Gender' column so we'll use an exception-try
    try:
        gender_types = df['Gender'].value_counts()
        print("\nDisplaying the counts of different user genders...")
        print(gender_types.to_string())
    except:
        print("\nThere is no 'Gender' column in this file.")

    # Display earliest, most recent, and most common year of birth
    # Note that not all files may have the 'Birth Year' column so we'll use an exception-try
    try:
        common_year = int(df['Birth Year'].mode()[0])
        early_year = int(df['Birth Year'].min())
        late_year = int(df['Birth Year'].max())
        print("\n The most common year of birh is: ", common_year)
        print("\n The most recent year of birh is: ", early_year)
        print("\n The earliest year of birh is: ", late_year)
    except:
        print("\nThere is no 'Birth Year' column in this file.")
        

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("Goodbye!")
            break


if __name__ == "__main__":
	main()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()