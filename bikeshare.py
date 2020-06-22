import time
import pandas as pd
import numpy as np
from datetime import datetime

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
        

class data_frame_manger():
    def __init__(self, all_df):
        self.all_df = all_df
        self.filtered_df = None
    
    def __get_row_as_list(self, row):
        row_list = list()
        for val in row:
            row_list.append(val)
        return row_list
    
    def __filter_df_for_all_months_and_selected_day(self, day):
        df = pd.DataFrame(columns =  self.all_df.columns)
        cnt = 1
        #df = self.all_df[datetime.fromisoformat(self.all_df['Start Time'].valuesnew).strftime("%A").lower().strip().find(day) != -1]
        #for index, row in self.all_df.iterrows():
        for index in range(len(self.all_df)):
            start_time = datetime.fromisoformat(self.all_df['Start Time'].iloc[index])
            end_time = datetime.fromisoformat(self.all_df['End Time'].iloc[index])
            start_day = start_time.strftime("%A")
            end_day = end_time.strftime("%A")
            start_day = start_day.lower().strip()
            end_day = end_day.lower().strip()
            if start_day.find(day) != -1 and end_day.find(day) != -1:
                df.loc[cnt] = self.all_df.loc[index]
                cnt = cnt + 1
            
        return df
    
    def __filter_df_for_all_days_in_selected_month(self, month):
        month_converter_ = month_converter()
        df = pd.DataFrame(columns =  self.all_df.columns)
        return df
    
    def __filter_df_for_selected_month_and_selected_day(self, month, day):
        df = pd.DataFrame(columns =  self.all_df.columns)
        return df
    
    def get_filtered_df(self, month, day):
        if month.find('all') != -1 and day.find('all') != -1:
            self.filtered_df = self.all_df
        elif month.find('all') != -1 and day.find('all') == -1:
            self.filtered_df = self.__filter_df_for_all_months_and_selected_day(day)
        elif month.find('all') == -1 and day.find('all') != -1:
            self.filtered_df = self.__filter_df_for_all_days_in_selected_month(day)
        elif month.find('all') == -1 and day.find('all') == -1:
            self.filtered_df = self.__filter_df_for_selected_month_and_selected_day(month, day)

class month_checker:
    def __init__(self):
        self.months = 'all' + ' ' + 'january' + ' ' + 'february' + ' ' +  'march' + ' ' +  'april' + ' ' +  'may' + ' ' +  \
                      'june' + ' ' +  'july' + ' ' + 'august' + ' ' +  'september' + ' ' + 'october' + ' ' +  'november' + ' ' +  'december'
    
    def check_input_month(self, month):
        if month == None:
            return False
        
        month_loc = month.strip('\n')
        if month_loc in self.months:
            return True
        return False
    
class day_checker:
    def __init__(self):
        self.days = 'all'  + ' ' + 'monday' + ' ' + 'tuesday' + ' ' +  'wednesday' 'thursday' + ' ' +  'friday' + ' ' +  'saturday' + ' ' +  'sunday'
    
    def check_input_day(self, day):
        if day == None:
            return False
        
        day_loc = day.strip('\n')
        if day_loc in self.days:
            return True
        return False

class city_checker:
    def __init__(self):
        self.cities = 'chicago' + ' ' + 'new york city' + ' ' +  'washington'
    
    def check_input_city(self, city):
        if city == None:
            return False
        
        city_loc = city.strip('\n')
        if city_loc in self.cities:
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
        df - Pandas DataFrame manager with DataFrame containing city data filtered by month and day
    """
    file_name = CITY_DATA[city]
    
    
    df_tmp = pd.read_csv(file_name)
    data_frame_manger_ = data_frame_manger(df_tmp)
    data_frame_manger_.get_filtered_df(month, day)
    
    print(data_frame_manger_.filtered_df.shape)
    print(data_frame_manger_.all_df.shape)
    #print(len(data_frame_manger_.all_df))
    print(data_frame_manger_.filtered_df.head())
    return data_frame_manger_


#def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

 #   print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month


    # TO DO: display the most common day of week


    # TO DO: display the most common start hour


 #   print("\nThis took %s seconds." % (time.time() - start_time))
  #  print('-'*40)


#def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

 #   print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station


    # TO DO: display most commonly used end station


    # TO DO: display most frequent combination of start station and end station trip


 #   print("\nThis took %s seconds." % (time.time() - start_time))
 #   print('-'*40)


#def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

#    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time


    # TO DO: display mean travel time


#    print("\nThis took %s seconds." % (time.time() - start_time))
#    print('-'*40)


#def user_stats(df):
    """Displays statistics on bikeshare users."""

#    print('\nCalculating User Stats...\n')
#    start_time = time.time()

    # TO DO: Display counts of user types


    # TO DO: Display counts of gender


    # TO DO: Display earliest, most recent, and most common year of birth


 #   print("\nThis took %s seconds." % (time.time() - start_time))
 #   print('-'*40)


def main():
    #while True:
        input_data_ = get_filters()
        df = load_data(input_data_.city, input_data_.month, input_data_.day)

        #time_stats(df)
        #station_stats(df)
        #trip_duration_stats(df)
        #user_stats(df)

        #restart = input('\nWould you like to restart? Enter yes or no.\n')
        #if restart.lower() != 'yes':
        #    break


if __name__ == "__main__":
	main()
