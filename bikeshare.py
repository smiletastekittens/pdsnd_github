import time
import pandas as pd
import numpy as np

# Add new .csv files to this CITY_DATA dictionary if you want them to be usable
CITY_DATA = { 'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv' }

AVAILABLE_MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
AVAILABLE_DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

RAW_DATA_CHUNK_SIZE = 5


def handle_raw_data_request(df):
    '''
    Fields user input to determine if successive chunks of raw data should be printed
    Arguments:
        (pandas.DataFrame) df - The raw data that should be chunked
    '''
    # keep track of the total count of rows in the dataframe
    row_count = len(df.index)

    # use this as an offset for the chunks
    offset = 0

    # use this to store the subset of the dataframe
    sub = df

    # use this to store a bool that determines when we break the loop
    exit_loop = False

    while exit_loop == False:
        # Calculate offsets
        start_row = offset * RAW_DATA_CHUNK_SIZE
        end_row = (offset + 1) * RAW_DATA_CHUNK_SIZE

        # we need to do a check here to ensure that the next range of rows is still within the bounds of the dataframe
        if end_row + 1 >= row_count:
            # update the slice stop value to the last row in the dataframe
            end_row = count - 1

            # set our exit loop value to True so that we break out of the loop after printing our remaining values below
            exit_loop = True

        # solicit user input
        user_input = input("Would you like to see rows {} to {} of raw data?  Please answser 'yes' or 'no'".format(start_row, end_row - 1))
        if len(user_input) > 0 and user_input == 'yes':
            # show the raw chunk of data
            sub = df[start_row:end_row]
            print(sub)
            offset += 1
        else:
            exit_loop = True

def wait_for_input(next_step):
    '''
    Prints text notifying the user that their input is required to move forward and ensures that each section of information can be easily reviewed
    Arguments:
        (str) next_step - arbitrary text that informs that user which section of information will be printed next
    Returns:
        (bool) True or False value that indicates whether we should break out of the main loop
    '''
    r = True
    user_input = input("Press enter to continue to {} section, or type 'quit' to exit the program\n".format(next_step))
    if len(user_input) > 0 and user_input == 'quit':
        r = False
    return r

def print_separator():
    ''' Prints a string of dashes sandwiched between two newline characters -- this is used to visually segment information for the user '''
    print("\n{}\n".format('-' * 40))

def validate_city(city):
    '''
    Validates user input for the 'city' field and ensures that there is a corresponding data set available for it
    Arguments:
        (str) city - The city name
    Returns:
        (bool) True or False value indicating whether the city is valid
    '''
    if len(city) < 1 or city not in CITY_DATA:
        print("Invalid city supplied.  Please supply value 'Chicago', 'New York City', or 'Washington'")
        return False
    else:
        return True

def validate_month(month):
    '''
    Validates user input for the 'month' field
    Arguments:
        (str) month - the name of the month (eg. "May")
    Returns:
        (bool) True or False value indicating whether the city is valid
    '''
    if len(month) < 1 or month not in AVAILABLE_MONTHS:
        print("Invalid month supplied.  Please supply a valid month name (eg. 'April') from 'January' to 'June' or 'all' for all available months")
        return False
    else:
        return True

def validate_day(day):
    '''
    Validates user input for the 'day' field
    Arguments:
        (str) day - the name of the day (eg. "Monday")
    Returns:
        (bool) True or False value indicating whether the day is valid
    '''
    if len(day) < 1 or day not in AVAILABLE_DAYS:
        print("Invalid day supplied. Please supply a valid day name (eg. 'Monday') or 'all' for all days")
        return False
    else:
        return True

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        input_success = False
        while input_success is False:
            # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
            city = input("Enter the desired city ('Chicago', 'New York City', 'Washington'): ")
            city = city.lower()
            input_success = validate_city(city)

        input_success = False
        while input_success is False:
            # get user input for month (all, january, february, ... , june)
            month = input("Enter the of the desired month ('January' through 'June' only), or 'all' for all available months: ")
            month = month.lower()
            input_success = validate_month(month)

        input_success = False
        while input_success is False:
            # get user input for day of week (all, monday, tuesday, ... sunday)
            day = input("Enter the name of the desired day (eg. 'Monday') or 'all' for all available days: ")
            day = day.lower()
            input_success = validate_day(day)
        break

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
    df = pd.read_csv(CITY_DATA[city], parse_dates=['Start Time', 'End Time'])

    if month != "all":
        # Filter by a specific month
        df = df[df['Start Time'].dt.month == AVAILABLE_MONTHS.index(month)]

    if day != "all":
        # Filter by day
        df = df[df['Start Time'].dt.day == AVAILABLE_DAYS.index(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = AVAILABLE_MONTHS[df['Start Time'].dt.month.mode()[0]].capitalize()
    print("Most Common Month: {}".format(most_common_month))

    # display the most common day of week
    most_common_day = AVAILABLE_DAYS[df['Start Time'].dt.dayofweek.mode()[0] + 1].capitalize()
    print("Most Common Day: {}".format(most_common_day))

    # display the most common start hour
    most_common_start_hour = df['Start Time'].dt.hour.mode()[0]
    print("Most Common Start Hour: {}".format(most_common_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("Most Common Start Station: {}".format(most_common_start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("Most Common End Station: {}".format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    # break out the 'Start Station' and 'End Station' columns, zip them together, convert to a List, and then to a Panda Series
    most_common_station_combination = pd.Series(list(zip(df['Start Station'], df['End Station']))).mode()[0]
    print("Most Common Station Combination: {} to {}".format(most_common_station_combination[0], most_common_station_combination[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # NOTE: travel time is in seconds, not minutes

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    ttt_minutes = total_travel_time / 60
    ttt_hours = ttt_minutes / 60
    print("Total Travel Time: {:.2f} seconds, or {:.2f} minutes, or {:.2f} hours".format(total_travel_time, ttt_minutes, ttt_hours))

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    att_minutes = average_travel_time / 60
    att_hours = att_minutes / 60
    print("Average travel time: {:.2f} seconds, or {:.2f} minutes, or {:.2f} hours".format(average_travel_time, att_minutes, att_hours))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    s_user_types = df['User Type']
    s_user_types = s_user_types.groupby(s_user_types)

    print("Count by User Type\n")

    for key, values in s_user_types:
        print("\t{}: {}".format(key, values.count()))

    print("\n")

    # Display counts of gender
    # NOTE: 'washington.csv' does not have a Gender column or Birth Year column
    if 'Gender' in df.columns:
        genders = df['Gender']
        genders = genders.groupby(genders)

        print("Count By Gender\n")

        for key, values in genders:
            print("\t{}: {}".format(key, values.count()))
    else:
        print("Gender data does not exist in this data set")

    print("\n")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        b_years = df['Birth Year'][df['Birth Year'] > 0]

        print("Earliest Birth Year: {}".format(b_years.min()))
        print("Most Recent Birth Year: {}".format(b_years.max()))
        print("Most Common Birth Year: {}".format(b_years.mode()[0]))
    else:
        print("Birth Year data does not exist in this data set")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    while True:

        try:

            city, month, day = get_filters()

            city_readable = city.capitalize()
            month_readable = ("all months", "the month of {}".format(month.capitalize()))[month != 'all']
            day_readable = ("all days", "{}s".format(day.capitalize()))[day != 'all']

            df = load_data(city, month, day)

            print_separator()

            print("Loading data for {} in {} for the city of {}".format(day_readable, month_readable, city_readable))

            print_separator()

            time_stats(df)

            if wait_for_input("Station Stats") == False:
                break;

        except Exception as e:
            print("Unable to load time stats: {}".format(e))
            break

        print_separator()

        station_stats(df)

        if wait_for_input("Trip Duration Stats") == False:
            break;

        print_separator()

        trip_duration_stats(df)

        if wait_for_input("User Stats") == False:
            break;

        print_separator()

        user_stats(df)

        print_separator()

        handle_raw_data_request(df)

        print_separator()

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
