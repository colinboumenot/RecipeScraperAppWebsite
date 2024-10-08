# RecipeScraperAppWebsite

## **Overview**

The goal of our project is to create an application, where you can enter and save what ingridients you have, and the application will provide you with a list of detailed recipies that you can do. The provided recipies can be sorted by origin, time of preppaaration, spicieness and whether they contain meat or not.

### **Main Features**

- The project will include at least two scrapers - first being the one that scapes the URLs of all recipies on the website and the secon done being the one that scrapes the details of the actual recipies.
- The project will induced a database where all the recipies and their details will be stored.
- There will be an App interface, which will allow the user to switch in between recipies, add and delete available ingridients and sort and filter recipies by taste.
- The language for the project will be Python, with a possible inclusion of a database language.

### **Goals:**

**Initial goals**

1) Get the 2 scrapers done - or at least ready to test
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

-	PyGame GUI - `pip install pygame_gui`
  
-	PyGame – `pip install pygame`

## **Architecture**

&nbsp;&nbsp;&nbsp;&nbsp;The architecture of the program is divided into two main components, processing recipes into a database and a UI for the user to find desired recipes. To create easily filterable recipes for the user the recipe dictionary database was created by using a 3 step process to filter individual recipes, scraping the raw data, parsing the data for desired components, and lastly converting the found componenets to a more user friendly format. The UI is split into several different screens to allow the user to enter ingredients, find recipes based on their ingredients, and view selected recipes.

### **Scrapers:**

- **url_scraper.py**: The intital pass through foodnetwork.com, this scraper retrieves all urls for the recipes, these urls are then passed along to the next scraper to get further processed.
  
- **recipe_scraper.py:** This scraper takes the urls previously scraped and goes through each url to find the title, time, servings, level, ingredients, steps, and tags for each recipe, this data is then used to create a Recipe object, once all recipes are scraped they are dumped into a file for user later.

### **Parsers:**

&nbsp;&nbsp;&nbsp;&nbsp;Parsers serve as the second pass through the data, all parsers first unpluralize the strings of the recipe objects in order to ensure continuity between the same ingredients (Ex. strawberry and strawberries should be the same thing).

- **ingredient_parser.py:** The first parser, it runs through the ingredients of the previously stored recipe objects to find keywords matching our created list of possible ingredients, returns a list of ingredients sorted by first appearance in the string.
  
- **measurement_parser.py:** The second parsers, it runs through the ingredients of the recipe searching for units in the recipe, it only returns a found unit if it finds an accompanied quantity, when returning data it sends back a list of the unit quantity pairs in order of appearance.

- **object_parser.py:** The final parser, serves as a way to combine the data from the previous two parsers, for each recipe it runs ingredient and measurement parser, depending on what is returned it creates pairs of ingredients and measurements that are then added back to the Recipe objects as an additional field, the resulting recipes are then stored in a file for later use with the converters.

### **Converters:**
&nbsp;&nbsp;&nbsp;&nbsp;Converters serve as the final process of cleaning the data, these converters standardize units and create dictionaries to allow us to quickly provide recipes to users depending on their ingredients

- **id_converter.py:** Assigns each recipe a unique ID number, this ID later serves as the key to the dictionary of recipes, unique ID is needed since many recipes have duplicate names.

- **measurement_converter.py:** Standardizes measurements, for volume ingredients measurements are converted to cups, for mass ingredients measurements are converted to grams. For simplicity ambiguous units such as tubes, cans, bottles, etc. were assumed to be a certain amount based on research.

- **recipe_dictionary_converter.py:** Every recipe is added as values to a dictionary with ingredients as the keys, makes it easier later on to find recipes based on users ingredients.

- **recipeobject_dictionary_converter.py:** Turns each recipe object into a dictionary, for each recipe the key is one of the ingredients and the value is a empty list of [0, 0, 0, 0] the first item represents how many grams of the ingredient, the second item the amount of cups, the third the amount of packages, and the last the amount of wholes.

- **input_converter.py:** Takes user input of ingredients and splits each entry into a quantity unit and ingredients, allows for dictionaries to be parsed for recipes.

### **Recipe Finder:**
&nbsp;&nbsp;&nbsp;&nbsp;For finding recipes the user has 4 options

1. Recipes no quantities
   - For this option the user provides a list of ingredients they want to use, and recipe that contains all these ingredients is initially selected, each of these recipes are then checked to see if the user has all ingredients required for the recipe
    
2. Recipes no quantities exclusive
   - Similar to recipes no quantities, with user provided list of ingredients all recipes containing all the ingredients are returned, we do not check to see if the user has enough of the non pre-selected ingredients in the recipe, useful if user wants to use up certain ingredients

3. Recipes quantities
   - Same functionality as recipes no quantities, except each ingredient is also checked to see if the user has enough of the ingredient

4. Recipes quantities exclusive
   - Same functionality as recipes no quantities exclusive, except quantities are taken into account

### **UI:**

### **Diagram:**

![image000000 (01E)](https://github.com/SofiyaChubich/RecipeScraperAppWebsite/assets/90056323/a773320f-6227-4c23-9ae1-63d532555993)

## **User Experience**

&nbsp;&nbsp;&nbsp;&nbsp;Overall, this app is meant to be a useful tool for home cooks looking for recipe ideas, the use of the app is meant to be as straightforward as possible.

### **First Time User:** 

&nbsp;&nbsp;&nbsp;&nbsp;The app intially loads onto a screen providing a user the option to search for recipes or enter ingredients into their database. For a first time user they will liekly need to add ingredients to their database (unless they want a recipe with 0 ingredients), to add ingredients users are then instructed to give an ingredient name, and if they choose a unit with a quantity (ex. 2 tablespoons). After entering their ingredients users then can return to the homescreen and move to the tab allowing them to search for recipes, to search for recipes they provide at least 1 ingredient that they want to be used in the recipe, they then select which of the 4 recipe finder functionalities they want to use. After doing so they are provided with a list of recipes which they can click on to see the full step by step instructions.

&nbsp;&nbsp;&nbsp;&nbsp;By taking a smaller step by step approach to the process of finding recipes, it makes it easy for new users to get a feel of how the application works.

### **Returning User:** 

&nbsp;&nbsp;&nbsp;&nbsp;As with the first time user the app intially loads to the homescreen, however for the returning user the app loads the database of ingredients that they previously provided. So the returning user could immediately begin searching for recipes, which has the same flow previously described for beginning users. Returning users may also need to enter updates to their ingredient database, for adding ingredients recently purchased, or for subtracting ingredients that may have expired. 

## **Retrospective**

### **Sindhura:**

### **Nikil:**

### **Camila:**
**Summary:** I believe that our project was pretty good since early on we had cut parts of our project and save them for later in the event that we finished early - we didn't so doing so was definetly a good idea. We also had defined work for people to work on so we generally had work for people to do. I feel like the code reviews and PR's definetly helped us get a better understanding of git and transition to a process more similar to something that might be found in an actual workforce which was pretty cool.

**Communication:** I think communication was pretty good, but I do think it could have been a bit better since sometimes it would feel like people would only talk to me, so then I'd have to pass them along to the person that they should have been talking to, but we were always aware of what others were doing with the standups (or quick sitting down conversations) at the start of class. 

**Surprises:** While moving away from the database was a bit of a surprise considering how commited we were to it earlier, I also feel like it was a good thing because I have a tendency to sometimes get stuck doing mindless but long tasks that while a little helpful can drag me down so it helped me stop categorizing all the ingredients since our current sorting method wouldn't be able to utilize umbrella terms and transition to more helpful work like storing data, connecting UI and backend, and a spell checker.

**Takeaways:** I feel like this project was a great expirence to get better at communication, and having the expirence of a long project, because while I've had some similar moments in robotics, they're both unique in their own ways and help me grow differently. Something else that I did in this project that I don't do much was a bit of testing after I kept running into bugs on my spell-checker and I felt like it was a great start since testing is a really important thing, and I felt like it was a start to get more used to creating and using testing methods.

### **Sofiya:**

### **Colin:**

**Summary:** Overall I thought that the project went fairly well, we did a good job of establishing what tasks each person was going to be doing intially, however after this is became clear that certain tasks were going to take far longer than expected (cleaning the data, creating UI), and I think it may have been better if at this point we stopped to reevaluate what tasks needed to be prioritized in order to ensure the project would finish on time.

**Communication:** For the most part our communication in class as a group was fairly good, with our daily standups we were able to stay up to date on what everyone was doing. Additionally our code reviews for each other were very strong, each of our pull requests was fully evaluated by a member of the group to ensure the best quality, rather than just quickly passing it along, personally I think this allowed me to grow as a coder, by being forced to think in a bigger picture sense with small commits.

**Suprises:** The main thing that suprised me was how hard it was to clean the data. Initially I assumed that I would quickly be able to scrape the data and parse for ingredients, but after seeing how diverse the formats of recipes were, I realized that the process was going to be far more complicated than that. This setback forced me to find a different way to comb through the data, leading me to use the Scrape - Parse - Convert format that I did.

**Takeaways:** After completing this project one of the main takeaways I had was the degree of difficulty that goes into creating a large project that you do not have a framework for. For all other projects I have done I had some idea how to complete the task, whether it be from past experience or examples that I had seen. For this project none of that applied, it forced me to think more about each small detail, and how it would connect to the overarching framework. The other main takeaway I had was learning more about the functionality of github, I had never before used branches or pull requests, but this project allowed me to see how they work, and the value in them, and over time it became more ingrained in my coding practices, allowing me to become a more effective programmer.

