import requests
import time
import sqlite3

def get_weather_info(city):

    # Initialize the API key 
    API_KEY = "d5adcfc572b44b40adf72923240304"

    # Define the Weather API URL
    url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"

    # Make the API request
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
            data = response.json()
            # Displaying the weather data in a user-friendly format
            time.sleep(1)
            print(f"\n\nWeather in {data['location']['name']}, {data['location']['region']} ({data['location']['country']})")
            print(f"\nLocal Time: {data['location']['localtime']}")
            print(f"\nCurrent Condition: {data['current']['condition']['text']}")
            print(f"\nTemperature: {data['current']['temp_c']}°C (Feels like {data['current']['feelslike_c']}°C)")
            print(f"\nWind: {data['current']['wind_kph']} km/h, Direction: {data['current']['wind_dir']}")
            print(f"\nHumidity: {data['current']['humidity']}%")
            print(f"\nVisibility: {data['current']['vis_km']} km")
            print(f"\nUV Index: {data['current']['uv']}\n")
    else:
        print("\nFailed to retrieve information.\n")
        print("Check if your connected to the internet or not")

def auto_refresh(city):
    a = 0
    while a != 10:
        try:
            # Print a message indicating that the latest information is being fetched for the 'city'
            print(f"\nFetching the latest information for {city}...")
            # Call the function to get weather information for the 'city'
            get_weather_info(city) 
        except Exception as e:
            # If an exception occurs, handle it by printing an error message
            print("An error occurred while fetching data:", e)
            print("\nPlease try again.\n")
        a += 1
        if a == 10:
            # If 'a' is 10, prompt the user to continue the auto-refresh process
            user_input = input("Type 'exit' if you want to quit the process of auto-refresh or \nType 'continue' if you want to continue the process of auto-refresh=")
            if user_input == "continue":
                # If 'user_input' is "continue", reset 'a' to 0 to continue the auto-refresh process
                a = 0
            else:
                # If 'user_input' is "exit", exit the loop and return from the function
                return
        # Wait for 15 second
        time.sleep(15)

def add_favorite_city(city):
    try:
        cursor.execute("INSERT INTO favorite_cities (city) VALUES (?)", (city,))
        conn.commit()
    except:
        print()
        time.sleep(1)
        print(city," is already present in the list of favorite cities")

def get_favorite_cities():
    print()
    time.sleep(1)
    cursor.execute("SELECT * FROM favorite_cities")
    favorite_cities = cursor.fetchall()
    print("City_id","City_name",sep="\t")
    for city in favorite_cities:
        print(city[0],city[1],sep="\t")
    print()

def update_favorite_city(city_id, city):
    try:
        cursor.execute("UPDATE favorite_cities SET city=? WHERE id=?",(city, city_id))     
        conn.commit()
    except:
        print("Invalid Input\nPlease try again")
        return
def delete_favorite_city(city_id):
    try:
        cursor.execute("DELETE FROM favorite_cities WHERE id=?", (city_id,))
        conn.commit()
    except:
        print("Invalid Input/nPlease try again")
        return

def main():
    while True:
        city = input("\nEnter the name of the city you want to get information for: ")

        # Check if city is empty
        if not city:
            print("City name cannot be empty. Please try again.")
            continue

        # Check if city contains only alphabetic characters and spaces
        if not city.replace(' ', '').isalpha():
            print("City name should contain only letters and spaces. Please try again.")
            continue

        try:
            print(f"\nFetching information for {city}...")
            get_weather_info(city)
            break  # Exit the loop since we got the information

        except Exception as e:
            # Handle specific exceptions if needed
            print("An error occurred while fetching data:", e)
            print("Please try again.")
    
    time.sleep(1)
    while True:
        # Take user input for further operations
        print("1.Get the weather information of another city",
            "2.Auto-refresh for every 15 seconds",
            "3.Add this city to the list of favorite cities",
            "4.End the program",sep="\n")
        c1=int(input("Enter Your Choice="))
        match c1:
            case 1:
                return 1
            
            # Initiate Auto-refresh
            case 2:
                auto_refresh(city)

            # Add the city to the list of favorite cities
            case 3:
                # Check if the table already exists
                cursor.execute('''CREATE TABLE IF NOT EXISTS favorite_cities (
                                    id INTEGER PRIMARY KEY,
                                    city TEXT NOT NULL UNIQUE 
                                )''')
                
                add_favorite_city(city)
                get_favorite_cities()
                while True:
                    time.sleep(1)
                    print("1.Get the weather information of another city",
                        "2.Add another city in the list of favorite cities",
                        "3.Update an existing city in the list of favorite cities",
                        "4.Delete an existing city in the list of favorite cities",
                        "5.End the program",sep="\n")
                    c2=int(input("Enter your choice="))
                    match c2:
                        case 1:
                            return 1
                        case 2:
                            c3=input(("\nEnter the name of the city="))
                            add_favorite_city(c3)
                            get_favorite_cities()
                        case 3:
                            c4=int(input("\nEnter the City_id of the city which you want to update="))
                            n=input("\nEnter the new city=")
                            update_favorite_city(c4,n)
                            get_favorite_cities()
                        case 4:
                            c5=int(input("\nEnter the City_id of the city which you want to delete="))
                            delete_favorite_city(c5)
                            get_favorite_cities() 
                        case 5:
                            return 0
                        case _:
                            print("\nInvalid Input\nTry again\n")

            # End the Program
            case 4:
                return 0
            
            case _:
                print("\nInvalid Input\nTry again\n")
            
if __name__ == "__main__":
    # Connect to a database (will create it if it doesn't exist)
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    while True:
        a=main()
        if a==0:
            break
    conn.commit()
    cursor.close()
    conn.close()