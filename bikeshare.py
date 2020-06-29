    import time
    import pandas as pd
    import numpy as np

    from utils import MethodTimer
    from utils import get_user_input

    CITY_DATA = { 'ch': 'chicago.csv',
                  'nyc': 'new_york_city.csv',
                  'wa': 'washington.csv'}

    AVAILABLE_MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']

    DAYS_OF_WEEK = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


    def get_filters():
        """
        Asks user to specify a city, month, and day to analyze.

        Returns:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        """

        city = get_user_input("Please enter the code for the city to analyse: CH (Chicago), NYC (New York City), WA (Washington ) ...", 
                              CITY_DATA.keys(), 'city')

        month = get_user_input("Please enter the month that you want to analyse: all, january, february, march, april, may, june ...",
                               AVAILABLE_MONTHS, 'month')

        day = get_user_input("Please enter the day you want to analyse: all, monday, tuesday, wednesday, thursday, friday, saturday, sunday ...",
                             DAYS_OF_WEEK, 'day')

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
        df = pd.read_csv(CITY_DATA[city])

        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])

        # extract month and day of week from Start Time to create new columns
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.weekday_name

        # filter by month if applicable
        if month != 'all':
            # use the index of the months list to get the corresponding int
            month = AVAILABLE_MONTHS.index(month)

            # filter by month to create the new dataframe
            df = df[df['month'] == month]

        # filter by day of week if applicable
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]     

        return df


    def time_stats(df):
        """Displays statistics on the most frequent times of travel."""

        print('\nCalculating The Most Frequent Times of Travel...\n')
        timer = MethodTimer()

        # Display the most frequent month
        most_frequent_month = AVAILABLE_MONTHS[df.month.mode()[0]].title()
        print("The Most Frequent Month of Travel is :: %s " % most_frequent_month)

        # Display the most common day of week
        most_common_day_of_week = df.day_of_week.mode()[0]
        print("The Most Common Day of Week is :: %s " % most_common_day_of_week)

        # Display the most common start hour
        most_common_start_hour = df['Start Time'].dt.hour.mode()[0]
        print("The Most Common Start Hour is :: %s " % most_common_start_hour)

        timer.print_duration()


    def station_stats(df):
        """Displays statistics on the most popular stations and trip."""

        print('\nCalculating The Most Popular Stations and Trip...\n')
        start_time = time.time()

        # Display most commonly used start station
        most_used_start_station = df["Start Station"].mode()[0]
        print("The Most Commonly Used Start Station is :: %s " % most_used_start_station)

        # Display most commonly used end station
        most_used_end_station = df["End Station"].mode()[0]
        print("The Most Commonly Used End Station is :: %s " % most_used_end_station)

        # Display the most frequent combination of start station and end station trip
        df['trip'] = df[['Start Station', 'End Station']].agg(' - '.join, axis=1)
        print("The Most Frequent Combination of Start Station and End Station Trip :: %s " % df['trip'].mode()[0])

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


    def trip_duration_stats(df):
        """Displays statistics on the total and average trip duration."""

        print('\nCalculating Trip Duration...\n')
        timer = MethodTimer()

        # Display the total travel time
        total_in_seconds = df['Trip Duration'].sum()
        print("The Total Travel Time is :: %s " % time.strftime('%H:%M:%S', time.gmtime(total_in_seconds))) 

        # Display the average travel time
        average_in_seconds = df['Trip Duration'].mean()
        print("The Average Traval Time is :: %s " % time.strftime('%H:%M:%S', time.gmtime(average_in_seconds)))

        timer.print_duration()


    def user_stats(df):
        """Displays statistics on bikeshare users."""

        print('\nCalculating User Stats...\n')
        timer = MethodTimer()

        # Display counts of user types
        print("The user type counts ::")
        print(df['User Type'].value_counts())

        try:
            # Display counts of gender
            print("\nThe gender counts ::")
            print(df['Gender'].value_counts())

            # Display earliest, most recent, and most common year of birth
            earliest_year_of_birth = df['Birth Year'].min()
            most_recent_year_of_birth = df['Birth Year'].max()
            most_common_year_of_birth = df['Birth Year'].mode()
            print("\nThe earliest year of birth :: %s " % int(earliest_year_of_birth))
            print("The most recent year of birth :: %s " % int(most_recent_year_of_birth))
            print("The most common year of birth :: %s " % int(most_common_year_of_birth[0]))
        except KeyError:
            print("Some statistics are not available ... ")

        timer.print_duration()


    def display_raw_data(df):
        """Displays the raw data in chunks of 5 rows."""

        while True:
            show = input("Would you like to view the first few lines of raw data? 'yes' to continue, any other key to ignore ... ")
            if show.lower() != 'yes':
                break
            else:
                print(df.head())
                df = df[5:]
                print('*'*40)

        print('-'*40)    

    def main():
        print('Hello! Let\'s explore some US bikeshare data!')

        while True:
            city, month, day = get_filters()
            print("You have selected --> city: %s, month: %s, day: %s" % (city, month, day))
            df = load_data(city, month, day)
            raw_df = df.copy()

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            display_raw_data(raw_df)

            restart = input("\nWould you like to restart? 'yes' to continue, any other key to abort ... ")
            if restart.lower() != 'yes':
                break

    if __name__ == "__main__":
        main()
