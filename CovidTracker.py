import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

class CovidTracker:
    def __init__(self):
        self.base_url = "https://disease.sh/v3/covid-19"
        
    ###############################################################################  
    ### Fetching Data for Global and Country and Historical COVID-19 Statistics ###
    ###############################################################################

    def get_global_data(self):

        try:
            response = requests.get(f"{self.base_url}/all")  #Making HTTP Get request to the API
            response.raise_for_status()         #Checking if the request was successful
            return response.json()      #parsing the JSON response from the API
        except requests.RequestException as e:
            print(f"Error fetcing global data: {e}")
            return None
    
    def get_country_data(self, country):

        try:
            response = requests.get(f"{self.base_url}/countries/{country}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data for {country}: {e}")
            return None
        
    def get_historical_data(self, country, days=30):

        try:
            response = requests.get(f"{self.base_url}/historical/{country}?lastdays={days}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching historical data for {country}: {e}")
            return None

        
    #################################################################################   
    ### Displaying Data for Global and Country and Historical COVID-19 Statistics ###
    #################################################################################
        
    def display_global_data(self):

        global_data = self.get_global_data()
        if global_data:
            print("\n--- GLOBAL COVID-19 STATISTICS ---")
            print(f"\nTotal Cases: {global_data['cases']:,}")
            print(f"Total Deaths: {global_data['deaths']:,}")
            print(f"Total Recovered: {global_data['recovered']:,}")
            print(f"Active Cases: {global_data['active']:,}")
            print(f"Critical Cases: {global_data['critical']:,}")
            print(f"Cases Per Million: {global_data['casesPerOneMillion']:,}")
            print(f"Deaths Per Million: {global_data['deathsPerOneMillion']:,}")

    def display_country_data(self, country):

        country_data = self.get_country_data(country)
        if country_data:
            print(f"\n--- COVID-19 STATISTICS FOR {country.upper()} ---")
            print(f"\nTotal Cases: {country_data['cases']:,}")
            print(f"Total Deaths: {country_data['deaths']:,}")
            print(f"Total Recovered: {country_data['recovered']:,}")
            print(f"Active Cases: {country_data['active']:,}")
            print(f"Critical Cases: {country_data['critical']:,}")

    def plot_historical_data(self, country, days=30):

        historical_data = self.get_historical_data(country, days)
        if historical_data:
            cases = historical_data['timeline']['cases']

            ### Converting dictionary to pandas DataFrame and setting index to datetime format ###
            df = pd.DataFrame.from_dict(cases, orient='index', columns=['Cases'])
            df.index = pd.to_datetime(df.index)

            ### Plot Customization ###
            plt.figure(figsize=(12,6))
            plt.plot(df.index, df['Cases'], 
                     marker='o',
                     linestyle='-',
                     linewidth=2,
                     color='black')
            plt.title(f'COVID-19 Cases in {country.upper()} (Last {days} Days)')
            plt.xlabel('Date', 
                    fontsize=14)
            plt.ylabel('Cumulative Cases',
                    fontsize=14)
            plt.xticks(rotation=45)   #Rotating x-axis labels
            plt.tight_layout()     #Adjusting layout to prevent label cutoff
            plt.show()


    #################################
    ### Calling the main function ###
    #################################

def main():
    tracker = CovidTracker()

    while True:
        print("\n--- COVID-19 TRACKER ---")
        print("1. Global Statistics")
        print("2. Country Statistics")
        print("3. Historical Country Statistics")
        print("4. Exit")

        choice = input("\nEnter your option (1-4): ")

        if choice == '1':
            tracker.display_global_data()
        elif choice == '2':
            country = input("\nEnter country name: ")
            tracker.display_country_data(country)
        elif choice == '3':
            country = input("Enter country name: ")
            days = int(input("Enter number of days for historical data (max 30): "))
            tracker.plot_historical_data(country, min(days, 30))
        elif choice == '4':
            print("\nExiting COVID-19 Tracker....")
            break
        else:
            print("\nInvalid choice. Please try again.")
            continue

        again = input("\nDo you want to continue? (yes/no): ").strip().lower()
        if again != "yes":
            print("\nExiting COVID-19 Tracker....")
            break


if __name__ == "__main__":
    main()