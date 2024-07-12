import time
import pandas as pd
import numpy as np

"""
Purpose: Explore bike share data using Python, Pandas, and NumPy for three US cities (Chicago, New York, and Washington).

Author: Patrick Bloomingdale
Project: Explore US Bikeshare Data
Due Date: July 17, 2018
Cohort: June 2018 - Data Analyst Nanodegree from Udacity
"""

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}

cities = ['chicago', 'new york', 'washington']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']

def get_filters():
    """
    Prompts user to specify a city, month, and day to analyze.
    
    Returns:
        (str) city: name of the city to analyze
        (str) month: name of the month to filter by, or "all" for no filter
        (str) day: name of the day to filter by, or "all" for no filter
    """
    print("Hello! Let's explore some US bikeshare data!")

    while True:
        city = input("Enter the city you want to explore data for (Chicago, New York, Washington): ").lower()
        if city in cities:
            break
        else:
            print('Invalid city. Please enter again.')

    while True:
        filter_type = input("Would you like to filter the data by month, day, or not at all? Type 'none' for no filter: ").lower()
        if filter_type == 'month':
            month = input("Enter the month to filter by (January, February, March, April, May, June) or 'all': ").lower()
            day = 'all'
            if month in months:
                break
            else:
                print('Invalid month. Please enter again.')
        elif filter_type == 'day':
            day = input("Enter the day to filter by (Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday) or 'all': ").lower()
            month = 'all'
            if day in days:
                break
            else:
                print('Invalid day. Please enter again.')
        elif filter_type == 'none':
            month = 'all'
            day = 'all'
            break

    print('-' * 40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    
    Args:
        (str) city: name of the city to analyze
        (str) month: name of the month to filter by, or "all" for no filter
        (str) day: name of the day to filter by, or "all" for no filter
    
    Returns:
        df: Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Popular Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    popular_month = df['month'].mode()[0]
    popular_day = df['day_of_week'].mode()[0]
    popular_hour = df['hour'].mode()[0]

    month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June"}
    popular_month_name = month_names.get(popular_month, "Unknown")

    print(f'Most Common Month: {popular_month_name}')
    print(f'Most Common Day of the Week: {popular_day}')
    print(f'Most Common Start Hour: {popular_hour % 12 if popular_hour != 12 else 12} {"AM" if popular_hour < 12 else "PM"}')

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    popular_end_station = df['End Station'].mode()[0]
    combo_station = df['Start Station'] + " to " + df['End Station']
    popular_combo = combo_station.mode()[0]

    print(f'Most Common Start Station: {popular_start_station}')
    print(f'Most Common End Station: {popular_end_station}')
    print(f'Most Common Trip: {popular_combo}')

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_duration = df['Trip Duration'].sum()
    mean_duration = df['Trip Duration'].mean()

    total_hours, total_minutes = divmod(total_duration, 3600)
    total_minutes, total_seconds = divmod(total_minutes, 60)

    mean_minutes, mean_seconds = divmod(mean_duration, 60)

    print(f'Total Travel Time: {int(total_hours)} hours, {int(total_minutes)} minutes, and {int(total_seconds)} seconds')
    print(f'Mean Travel Time: {int(mean_minutes)} minutes and {int(mean_seconds)} seconds')

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print(f'Counts of User Types:\n{user_types}')

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f'\nCounts of Gender:\n{gender_counts}')
    else:
        print(f'\nNo gender data available for {city.title()}')

    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        recent_year = df['Birth Year'].max()
        common_year = df['Birth Year'].mode()[0]

        print(f'\nEarliest Birth Year: {int(earliest_year)}')
        print(f'Most Recent Birth Year: {int(recent_year)}')
        print(f'Most Common Birth Year: {int(common_year)}')
    else:
        print(f'\nNo birth year data available for {city.title()}')

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-' * 40)

def display_raw_data(df):
    """Displays individual trip data upon request."""
    start_loc = 0
    while True:
        view_data = input("\nWould you like to view individual trip data? Enter 'yes' or 'no': ").lower()
        if view_data != 'yes':
            break
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5

def main():
    while True:
        city, month, day = get_filters()
        print(f"You selected city: {city.title()}, month: {month.title()}, day: {day.title()}")

        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_raw_data(df)

        restart = input("\nWould you like to restart? Enter 'yes' or 'no': ").lower()
        if restart != 'yes':
            break

if __name__ == "__main__":
    main()
