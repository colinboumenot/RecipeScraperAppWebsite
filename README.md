# RecipeScraperAppWebsite

## **Overview**

The goal of our project is to create an application, where you can enter and save what ingridients you have, and the application will provide you with a list of detailed recipies that you can do. The provided recipies can be sorted by origin, time of preppaaration, spicieness and whether they contain meat or not.

### **Main Features**

- The project will include at least two scappers - first being the one that scapes the URLs of all recipies on the website and the secon done being the one that scrapes the details of the actual recipies.
- The project will induced a database where all the recipies and their details will be stored.
- There will be an App interface, which will allow the user to switch in between recipies, add and delete available ingridients and sort and filter recipies by taste.
- The language for the project will be Python, with a possible inclusion of a database language.

### **Goals:**

**Initial goals**

1) Get the 2 scrappers done - or at least ready to test
2) Choose and prepare the Database
3) Fill in and Create the Database
4) Sort and Double check all the data before transferring focus to making the App

**Sprint 1 Goals**
1) Finish coding in the Database Interaction Class
2) Create a working UI that takes User Input
3)  Clean up the Ingridients
4)  Cleaning and figuring out how to dealn with recipe Exceptions

**Sprint 2 Goals**
1) Finished cleaning up ingredients
2) Enter cleaned ingredients into database
3) Create workable UI

**Sprint 3 Goals**
1) Take user input and find recipes
2) Finish UI

### **Running the Game:**

To run the app first download the following libraries.

-	PyAutoGUI - `pip install pyautogui`
  
-	PyGame – `pip install pygame`

## **Architecture**

&nbsp;&nbsp;&nbsp;&nbsp;The architecture of the program is divided into two main components, processing recipes into a database and a UI for the user to find desired recipes. To create easily filterable recipes for the user the recipe dictionary database was created by using a 3 step process to filter individual recipes, scraping the raw data, parsing the data for desired components, and lastly converting the found componenets to a more user friendly format. The UI is split into several different screens to allow the user to enter ingredients, find recipes based on their ingredients, and view selected recipes.

### **Scrapers:**

- **'url_scraper.py':** The intital pass through foodnetwork.com, this scraper retrieves all urls for the recipes, these urls are then passed along to the next scraper to get further processed.
  
- **'recipe_scraper.py':** This scraper takes the urls previously scraped and goes through each url to find the title, time, servings, level, ingredients, steps, and tags for each recipe, this data is then used to create a Recipe object, once all recipes are scraped they are dumped into a file for user later.

### **Parsers:**

&nbsp;&nbsp;&nbsp;&nbsp;Parsers serve as the second pass through the data, all parsers first unpluralize the strings of the recipe objects in order to ensure continuity between the same ingredients (Ex. strawberry and strawberries should be the same thing).

- **'ingredient_parser.py':** The first parser, it runs through the ingredients of the previously stored recipe objects to find keywords matching our created list of possible ingredients, returns a list of ingredients sorted by first appearance in the string.
  
- **'measurement_parser.py':** The second parsers, it runs through the ingredients of the recipe searching for units in the recipe, it only returns a found unit if it finds an accompanied quantity, when returning data it sends back a list of the unit quantity pairs in order of appearance.

- **'object_parser.py':** The final parser, serves as a way to combine the data from the previous two parsers, for each recipe it runs ingredient and measurement parser, depending on what is returned it creates pairs of ingredients and measurements that are then added back to the Recipe objects as an additional field, the resulting recipes are then stored in a file for later use with the converters.

### **Converters:**
&nbsp;&nbsp;&nbsp;&nbsp;Converters serve as the final process of cleaning the data, these converters standardize units and create dictionaries to allow us to quickly provide recipes to users depending on their ingredients

- **'id_converter.py':** Assigns each recipe a unique ID number, this ID later serves as the key to the dictionary of recipes, unique ID is needed since many recipes have duplicate names


### **Recipe Finder:**

### **UI:**
## **User Experience**

## **Retrospective**
