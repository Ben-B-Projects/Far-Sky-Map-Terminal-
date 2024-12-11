import math, os


day = 0  
#Speeds assumed m/s atm  
shipSpeed = 5
planet_dict = {}
#Defines planet, with it's name, radius, days in a year, current day, extra info, and moons.
class planet:
    def __init__(self, name, radius, daysInYear, startOrbit, extraInfo, moonsStr):
        self.name = name
        self.radius = radius
        self.daysInYear = daysInYear
        self.startOrbit = startOrbit
        self.currentOrbit = startOrbit
        self.extraInfo = extraInfo
        self.moonsStr = moonsStr

    #Converts the current orbit day to degree
    def orbitToDegree(self):
        tempCurrentOrbit = 0
        #Checks if the current day is longer then a year, if it is gets the remainder.
        if (self.startOrbit+day) > self.daysInYear:
            tempCurrentOrbit = (self.startOrbit+day) % self.daysInYear
        else:
            tempCurrentOrbit = self.startOrbit+day

        degree = 360*(tempCurrentOrbit / self.daysInYear)
        return degree
    
    
    #Checks if the current day is over a year, then divides by a year.
    def currentDay(self):
        if self.currentOrbit + day > self.daysInYear:
            currentDay = (self.currentOrbit + day) % self.daysInYear
        else:
            currentDay = (self.currentOrbit + day)
        return currentDay        
        

#Gets the planets location based on the star as 0, 0.
def planetLocation(planetA):
    try:
        planetA = planet_dict[planetA]
    
        radius = planetA.radius
        degree = math.radians(planetA.orbitToDegree())
        testdegree = planetA.orbitToDegree()
        planetXY = [0, 0]
    
        if testdegree >= 0 and testdegree < 90:
            planetXY[0] = -(radius*math.cos(degree))
            planetXY[1] = radius*math.sin(degree)

        if testdegree >= 90 and testdegree < 180:
            degree -= math.radians(90)
            planetXY[0] = radius*math.sin(degree)
            planetXY[1] = radius*math.cos(degree)

        if testdegree >= 180 and testdegree < 270:
            degree -= math.radians(180)
            planetXY[0] = radius*math.cos(degree)
            planetXY[1] = -(radius*math.sin(degree))

        if testdegree >= 270 and testdegree < 360:
            degree -= math.radians(270)
            planetXY[0] = -(radius*math.sin(degree))
            planetXY[1] = -(radius*math.cos(degree))
    except KeyError:
        print("Invalid planet name. Use planet info to get a list of all of the planets.")
        return 
    return planetXY
    
    
#changeDay method
def changeDay(selectedDate):
    global day
    day = selectedDate
    print(f"The new date is: {day}")

#Commands: help, add planet, planet information, plan trip, set day
def commands(request):
    request = request.lower()
    if request == "help":
        os.system('cls')
        print("Help: Lists all available commands\nAdd Planet: Allows for creation of new planets on the map.\nPlanet Info: Returns all the available information on each planet.\nEdit Planet Info: Allows you to modify each aspect of a planets information.\nPlan Trip: Using two locations, either planets or specified coordinates, plot a route to see the distance and how long it will take you.\nSet Day: Sets the systems day.")

    elif request == "add planet":
        os.system('cls')
        name = input("Enter the planet's name: ")
        radius = input("Enter the planet's radius in 'to be determined measurement' from the star: ")
        try: 
            radius = int(radius)
        except ValueError:
            print("Please input a valid number for the radius, for example '54'\nRestart with 'Add Planet'")
        year = input("Enter the length of a year for this planet: ")
        try:
            year = int(year)
        except ValueError:
            print("Please input a valid number for the length of a year, for example '364'\nRestart with 'Add Planet'")
        currentday = input("Enter the current day of the year for this planet: ")
        try:
            currentday = int(currentday)
        except ValueError:
            print("Please input a valid number for the current day of the year, for example '69'\nRestart with 'Add Planet'")
        moons = input("Please include the names of any moons this planet has: ")
        extraInfo = input("Include any additional details about the planet here: ")
        planet_object = planet(name, radius, year, currentday, extraInfo, moons)
        global planet_dict
        planet_dict[name] = planet_object
        print("Planet added, use 'Planet Info' to view it.")

    elif request == "planet info":
        os.system('cls')
        print("The current list of planets includes:")
        for planet in planet_dict.values():
            print(planet.name)
        planetName = input("Enter a planet's name for all the information on the planet: ")
        planetlocat = planetLocation(planetName)
        if planetlocat is None:
            print(f"No planets by the name {planetName} exists.")
        else:
            print(f"Planet {planet_dict[planetName].name} is {planet_dict[planetName].radius} 'to be determined measurement' away from the star, \
and is located at the coordinates X{planetlocat[0]},Y{planetlocat[1]}. \
\nIt's year is {planet_dict[planetName].daysInYear} days long, it's current day is: {planet_dict[planetName].currentDay()}, \
and it has the moon(s): {planet_dict[planetName].moonsStr}. \nadditional information: {planet_dict[planetName].extraInfo}.")
        
    elif request == "edit planet info":
        os.system('cls')
        print("The current list of planets includes:")
        for planet in planet_dict.values():
            print(planet.name)
        planetName = input("Enter the planet's name that you wish to edit: ")
        try:
            planetInfo = planet_dict[planetName]
        except KeyError:
            planetInfo = ""
        if planetInfo is None or planetInfo == "":
            print(f"No planets by the name {planetName} exists.")
        else: 
            editedSection = input("Enter the sector you wish to edit. The editable sectors are: \nName, Radius, DaysInYear, StartOrbit, ExtraInfo, MoonsStr: ")
            editedSection = editedSection.lower()
            editedInput = input("Enter the new value for the edited sector, ensure that Radius, DaysInYear, StartOrbit are all numbers: ")
            editedInput = editedInput.lower()
            if editedSection == "radius" or editedSection == "daysinyear" or editedSection == "startorbit":
                try:
                    editedInput = int(editedInput)
                except ValueError:
                    print("The input was not a number.")
                    editedInput = int(1)
            if editedSection == "name":
                planet_dict[planetName].name = editedInput
                planet_dict[editedInput] = planet_dict.pop(planetName)
            elif editedSection == "radius":
                planet_dict[planetName].radius = editedInput
            elif editedSection == "daysinyear":
                planet_dict[planetName].daysInYear = editedInput
            elif editedSection == "startorbit":
                planet_dict[planetName].startOrbit = editedInput
            elif editedSection == "extrainfo":
                planet_dict[planetName].extraInfo = editedInput
            elif editedSection == "moonsstr":
                planet_dict[planetName].moonsStr = editedInput
            else:
                print("The edited section you chose does not exist.")


        #Four variants, planet to planet/specific location to planet/planet to location/location to location
    elif request == "plan trip":
        os.system('cls')
        print("Using either a specific location, or a planet, see the distance between both locations.")
        tripTypeA = input("Choose either 'planet' or 'location' for point A: ")
        tripTypeA = tripTypeA.lower()
        if tripTypeA == "planet":
            planetA = input("Input the name of the planet: ")
            locationA = planetLocation(planetA)

        elif tripTypeA == "location":
            locationA = [0, 0]
            locationA[0] = int(input("Input the 'x' coordinate: "))
            locationA[1] = int(input("Input the 'y' coordinate: "))

        tripTypeB = input("Choose either 'planet' or 'location' for point B: ")
        tripTypeB = tripTypeB.lower()
        if tripTypeB == "planet":
            planetB = input("Input the name of the planet: ")
            locationB = planetLocation(planetB)

        elif tripTypeB == "location":
            locationB = [0, 0]
            locationB[0] = int(input("Input the 'x' coordinate: "))
            locationB[1] = int(input("Input the 'y' coordinate: "))
        
        xDist = locationA[0] - locationB[0]
        yDist = locationA[1] - locationB[1]
        xDist = xDist*xDist
        yDist = yDist*yDist
        hypoDist = math.sqrt(xDist+yDist)
        tripTime = hypoDist/shipSpeed
        print(f"The trip distance is {hypoDist}, and at a ship speed of {shipSpeed}, it will take {tripTime} seconds to reach at full speed.")
        #TRY using acceleration instead of a set speed to calculate travel time.


    elif request == "set day":
        os.system('cls')
        global day
        day = input("Enter a specific day: ")
        try:
            day = int(day)
        except ValueError:
            print("Invalid day, type in a number such as '543'.")
        print(f"The day is now {day}.")



def main():
    active = True
    print("Welcome to the planet map, type 'help' for commands.")
    while active == True:
        request = input()
        commands(request)
        
planetobject = planet("test1", 50, 360, 135, "harharhar", "Titan, Enceladus, Dione")
planet_dict["test1"] = planetobject

planetobject = planet("test2", 90, 360, 290, "harharharHARHAR", "")
planet_dict["test2"] = planetobject


main()