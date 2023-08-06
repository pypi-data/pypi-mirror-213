#get what we need
import urllib.request
import os

#set up new working directory && create folders
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)
os.system(r"python makem.py")

os.system('cls' if os.name == 'nt' else 'clear')

def get_proton():
    # Set up the URL for the text file
    url = "https://services.swpc.noaa.gov/text/ace-swepam.txt"
    
    # Download the text file
    response = urllib.request.urlopen(url)
    data = response.read().decode()
    
    # Split the text file into lines
    lines = data.split("\n")

    # Extract the most recent solar wind data from the second-to-last line
    last_line = lines[-2]
    fields = last_line.split()

    # Extract the solar wind speed, density, and temperature from the fields
    s = float(fields[6])
    density = float(fields[7])
    speed = float(fields[8])
    temperature = (fields[9])
    
    #returning values
    return s, speed, density, temperature
    
def get_gsm():
    # Set up the URL for the text file
    url = "https://services.swpc.noaa.gov/text/ace-magnetometer.txt"
    
    # Download the text file
    response = urllib.request.urlopen(url)
    data = response.read().decode()
    
    # Split the text file into lines
    lines = data.split("\n")
    
    # Extract the most recent Interplanetary Magnetic Field data from the second-to-last line
    last_line = lines[-2]
    fields = last_line.split()
    
    # Extract the Bx, By, Bz, Bt data from the fields
    S =  float(fields[6])
    Bx = float(fields[7])
    By = float(fields[8])
    Bz = float(fields[9])
    Bt = float(fields[10])
    
    #return all collected values
    return S, Bx, By, Bz, Bt
   
def get_report():
    # Set up the URL for the text file
    url = "https://services.swpc.noaa.gov/text/discussion.txt"
    
    # Download the text file
    response = urllib.request.urlopen(url)
    report = response.read().decode()
    return(report)
    

def main():
    
    os.system(r"python makem.py")

    #Present Options
    print("Welcome to the Interplanetary Space Weather Interface, \nThis data is collected by the Advanced Composition Explorer (ACE). \n\nYou have the following options: \n")
    print("1.) Space Weather Prediction Center Forecast Report")
    print("2.) 1-Minute Averaged Real-time Interplanetary Solar Wind Plasma Data")
    print("3.) 1-Minute Averaged Real-time Interplanetary Magnetic Field Data")
    print("4.) Download Today's 193 Angstrom Images from NASA Solar Dynamics Observatory")
    print("5.) Donwload Today's SOHO Coronograph Imagery")
    
    #Get User Choice
    choice = input("Enter a number corresponding to an option above: ")
    
    #printing values
    
    if choice == "1":
    
        #clean up screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        report = get_report()
        print("\n")
        print(report)
        print("\n")
        
        #prepare for follow on mission
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        main()
    
    elif choice == "2":
    
        #clean up screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        #update values
        s, speed, density, temperature = get_proton()
        
        #Print Information
        print("\nLatest data on Solar Wind Plasma (Protons) at the L1 Lagrange is below \n")
        
        #Account for Errors
        if s != 0:
            print("ERROR EITHER BAD DATA OR NO DATA \nTRY AGAIN IN 1 MINUTE")
        
        #print data
        else:
            print("Speed: ", speed, "km/s")
            print("Density: ", density, "protons/cm^3")
            print("Temperature: ", temperature, "K")
        
        #prepare for follow on mission
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        main()
        
    
    elif choice == "3":
        
        #clean up screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("\nLatest Data on Interplanetary Magnetic Field Values (GSM Coordinates): \n")
        S, Bx, By, Bz, Bt = get_gsm()
        
        if S != 0:
            print("ERROR EITHER BAD DATA OR NO DATA \nTRY AGAIN IN 1 MINUTE")
        
        else:
            print("Magnetic Field Strength in the X direction: ", Bx, "nT")
            print("Magnetic Field Strength in the Y direction: ", By, "nT")
            print("Magnetic Field Strength in the Z direction: ", Bz, "nT")
            print("Total Magnetic Field Magnitude: ", Bt, "nT \n")
        
        #prepare for follow on mission
        input("Press Enter to continue...")
        os.system('cls' if os.name == 'nt' else 'clear')
        main()
        
    elif choice == "4":
        
        #clean up screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        #call the sdo image getter
        os.system(r"python sdo_image_getter.py")
        
        print("You have successfully downloaded the images, would you like to generate an AVI from them?")
        movie = input("Enter \"y\" for Yes and \"n\" for No:  ")
        if movie == "y":
            print("The movie is now being generated. Please be Patient \n")
            os.system(r"python sdo_movie.py")
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
            
        elif movie == "n":
            os.system('cls' if os.name == 'nt' else 'clear')
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
            
    elif choice == "5":
        
        #clean up screen
        os.system('cls' if os.name == 'nt' else 'clear')
        
        #call the SOHO image gettter
        os.system(r"python soho_image_getter.py")
        
        print("You have successfully downloaded the images, would you like to generate an AVI from them?")
        movie = input("Enter \"y\" for Yes and \"n\" for No:  ")
        if movie == "y":
            print("The movie is now being generated. Please be Patient \n")
            os.system(r"python soho_movie.py")
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
            
        elif movie == "n":
            os.system('cls' if os.name == 'nt' else 'clear')
            os.system('cls' if os.name == 'nt' else 'clear')
            main()
    
    
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Please try again")
        main()
