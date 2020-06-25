#!/home/oosifo/anaconda3/bin/python
import time
import pandas as pd
from statistics import mode
from prettytable import PrettyTable
import numpy as np



CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
        

class data_frame_manger():
    def __init__(self, all_df):
        self.all_df = all_df
        self.filtered_df = None
    
    def __filter_df_for_all_months_and_selected_day(self, day):
        df = self.all_df[(self.all_df['Start Day'] == day) & \
                         (self.all_df['End Day'] == day)]
        return df
    
    def __filter_df_for_all_days_in_selected_month(self, month):
        df = self.all_df[(self.all_df['Start Month'] == month) \
                         & (self.all_df['End Month'] == month)]
        return df
    
    def __filter_df_for_selected_month_and_selected_day(self, month, day):
        df = self.all_df[((self.all_df['Start Month'] == month) \
                         & (self.all_df['End Month'] == month)) &\
                         ((self.all_df['Start Day'] == day) \
                         & (self.all_df['End Day'] == day))]
        return df
    
    def get_filtered_df(self, month, day):
        if month.find('all') != -1 and day.find('all') != -1:
            self.filtered_df = self.all_df
        elif month.find('all') != -1 and day.find('all') == -1:
            self.filtered_df = self.__filter_df_for_all_months_and_selected_day(day)
        elif month.find('all') == -1 and day.find('all') != -1:
            self.filtered_df = self.__filter_df_for_all_days_in_selected_month(month)
        elif month.find('all') == -1 and day.find('all') == -1:
            self.filtered_df = self.__filter_df_for_selected_month_and_selected_day(month, day)

class month_checker:
    def __init__(self):
        self.months = 'all' + ' ' + 'january' + ' ' + 'february' + ' ' +  'march' + ' ' + \
                      'april' + ' ' +  'may' + ' ' +  'june' + ' ' +  'july' + ' ' + \
                      'august' + ' ' +  'september' + ' ' + 'october' + ' ' +  'november' + \
                      ' ' +  'december'
    
    def check_input_month(self, month):
        if month == None:
            return False
        
        month_loc = month.strip('\n')
        if month_loc in self.months:
            return True
        return False
    
class day_checker:
    def __init__(self):
        self.days = 'all'  + ' ' + 'monday' + ' ' + 'tuesday' + ' ' \
                    +  'wednesday' 'thursday' + ' ' +  'friday' + ' ' \
                    +  'saturday' + ' ' +  'sunday'
    
    def check_input_day(self, day):
        if day == None:
            return False
        
        day_loc = day.strip('\n')
        if day_loc in self.days:
            return True
        return False

class city_checker:
    def check_input_city(self, city):
        if city == None:
            return False
        
        city_loc = city.strip('\n')
        city_loc = city.strip()
        for key in CITY_DATA.keys():
            if city_loc == key:
                return True
        return False

class input_checker:
    def __init__(self):
        self.city_check = False
        self.month_check = False
        self.day_check = False
        
    def check_inputs(self, city, month, day):
        city_checker_ = city_checker()
        month_checker_ = month_checker()
        day_checker_ = day_checker()
        
        self.city_check = city_checker_.check_input_city(city)
        self.month_check = month_checker_.check_input_month(month)
        self.day_check = day_checker_.check_input_day(day)
        if  self.city_check == True and \
            self.month_check == True and \
           day_checker_.check_input_day(day) == True:
               return True
        return False
        
class input_data:
    def __init__(self, city, month, day):
        self.city = city
        self.month = month
        self.day = day
    
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (input_data) object which contains the followings
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = None
    month = None
    day = None
    cnt = 0
    max_n_trials = 6 #highest value of two error inputs for each of city, day and month
    input_checker_ = input_checker()
    correct_inputs = False 
    while correct_inputs == False:
        if input_checker_.city_check == False:
            city = input('Enter city of interest [chicago, new york city, washington]: ')
        elif input_checker_.month_check == False:
            month = input('Enter month of interest: [all, january, february, ... , december] where all is for all months in the year: ')
        elif input_checker_.day_check == False:
            day = input('Enter day of interest: [all,  monday, tuesday, ... sunday] where all is for all days in the month: ') 
                  
        cnt = cnt + 1
        if cnt > max_n_trials: #highet two error inputs for each of city, day and month
            print('Two many trials to get correct input from user')
            return None

        correct_inputs = input_checker_.check_inputs(city, month, day)
    print('-'*40)
    return input_data(city, month, day)

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - DataFrame manager which contains a pandas DataFrame containing city data filtered by month and day
    """
    file_name = CITY_DATA[city]

    df_tmp = pd.read_csv(file_name)
    df_tmp['Start Time'] = pd.to_datetime(df_tmp['Start Time'])
    df_tmp['End Time'] = pd.to_datetime(df_tmp['End Time'])
    
    df_tmp['Start Day'] = df_tmp['Start Time'].map(lambda x: x.strftime('%A').lower().strip())
    df_tmp['Start Month'] = df_tmp['Start Time'].map(lambda x: x.strftime('%B').lower().strip())
    df_tmp['End Day'] = df_tmp['End Time'].map(lambda x: x.strftime('%A').lower().strip())
    df_tmp['End Month'] = df_tmp['End Time'].map(lambda x: x.strftime('%B').lower().strip())
    df_tmp['Start Hour'] = df_tmp['Start Time'].map(lambda x: x.strftime('%H'))
    df_tmp['StartStopStations'] = 'Start Station: ' + df_tmp['Start Station'] + '; End Station: ' + df_tmp['End Station']
    
    data_frame_manger_ = data_frame_manger(df_tmp)
    data_frame_manger_.get_filtered_df(month, day)
    
    return data_frame_manger_


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = mode(df['Start Month'])
    print('The most common start month is: ', most_common_month)
    
    most_common_day = mode(df['Start Day'])
    print('The most common day of week is: ', most_common_day)

    most_frquent_start_hour = mode(df['Start Hour'])
    print('The most common start hour is: ', most_frquent_start_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    most_commonly_used_start_station = mode(df['Start Station'])
    print('The most commonly used start station is: ', most_commonly_used_start_station)
    
    most_commonly_used_end_station = mode(df['End Station'])
    print('The most commonly used end station is: ', most_commonly_used_end_station)

    most_frequent_combination_of_start_and_end_stations = mode(df['StartStopStations'])
    print('The most frequent combination of start station and end station trip is: ',  most_frequent_combination_of_start_and_end_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df_loc = df[['Start Time', 'End Time', 'Trip Duration']]
    
    print(df_loc.head())
    total_time_for_all_durations = df_loc['Trip Duration'].sum()
    print('\n')
    print('Total travel time for all trip durations is: ', total_time_for_all_durations)
   
    mean_travle_time = df_loc['Trip Duration'].mean()
    print('\n')
    print('The mean travel travel time for all trip durations is: ', mean_travle_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type_count = df['User Type'].value_counts()
    print('User Type Count:')
    user_type_table = PrettyTable(['User Type', 'Counts'])
    user_type_count_dict = user_type_count.to_dict()
    for key in user_type_count_dict.keys():
         counts = user_type_count_dict[key]
         user_type_table.add_row([key, counts])   
    print(user_type_table)
    
    print('\n')
    if'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('Gender Count: ')
        gender_counts_dict = gender_counts.to_dict()
        gender_count_table = PrettyTable(['Gender', 'Counts'])
        for key in gender_counts_dict.keys():
            counts = gender_counts_dict[key]
            gender_count_table.add_row([key, counts])
        print(gender_count_table)
        
    else:
        print('The dataset does not contain a gender column')
 
    print('\n')
    print('Age information: \n')
    if'Birth Year' in df.columns:
        commonest_year_of_birth = mode(df['Birth Year'])
        if np.isnan(commonest_year_of_birth) == False:
            commonest_year_of_birth = int(commonest_year_of_birth)
        
        most_recent_year_of_birth = max(df['Birth Year'])
        if np.isnan(most_recent_year_of_birth) == False:
            most_recent_year_of_birth = int(most_recent_year_of_birth)
        
        earliest_year_of_birth = min(df['Birth Year'])
        if np.isnan(earliest_year_of_birth) == False:
            earliest_year_of_birth = int(earliest_year_of_birth)
            
        print('Earliest: ', earliest_year_of_birth, ' ', 'Commonest: ', \
              commonest_year_of_birth, ' ', 'Most recent: ', most_recent_year_of_birth )
    else:
        print('The dataset does not contain a column for birth year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        input_data_ = get_filters()
        data_frame_manger_ = load_data(input_data_.city, input_data_.month, input_data_.day)
        print(data_frame_manger_.filtered_df.head())
        print(data_frame_manger_.filtered_df.tail())
        time_stats(data_frame_manger_.filtered_df)
        station_stats(data_frame_manger_.filtered_df)
        trip_duration_stats(data_frame_manger_.filtered_df)
        user_stats(data_frame_manger_.filtered_df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
