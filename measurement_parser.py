import inflect 


word_to_int = {'one': '1', 'two': '2', 'three' : '3', 'four' : '4', 'five' : '5', 'six' : '6', 'seven' : '7', 'eight' : '8', 'nine' : '9', 'ten' : '10'}

measurements = set(x.strip().lower() for x in open('raw_data/foodnetwork_measurements.txt', 'r+').readlines())
word_numbers = set(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'])

## Convert all plural nouns to singular, reduces ingredients that need to be entered into food names
def plural_to_singular(ingredient):
    p = inflect.engine()
    ## Certain characters that need to get filtered out from ingredient
    ingredient = ingredient.strip().replace(',', '').replace('- ', ' ').replace('\xa0', ' ').replace(';', '').replace('"', '').replace('(', '').replace(')', '').replace('%', '').replace(' to ', '-').replace('½', ' 1/2').replace('¼', ' 1/4').replace('¾', ' 3/4').replace('*', '')
    ## Handle parentheses later
    singular_phrase = []
    for word in ingredient.split(' '):
        word = word.strip().lower()
        if '-' in word and len(word) > 1:
            first, second = word.split('-')[0], word.split('-')[1]
            ## Some recipes list amounts as 1-2, 3-4, etc., we decided for this that we will take the smaller of the two numbers
            if first.isnumeric() and second.isnumeric():
                word = first
            ## Other case would be a situation such as 8-ounce, for this we just need to split the two apart
            elif first.isnumeric():
                singular_phrase.append(first)
                word = second
            else:
                word = word.replace('-', ' ')
            ## Handles if amount is a decimal ex. .01 ounce
        if '.' in word:
            if word.endswith('.'):
                word = word.replace('.', '')
            ##else:
                ##with open('raw_data/unknown_ingredients.txt', 'a+') as f:
                    ##f.write('unknown' + ingredient + '\n')
        if '/' in word:
            if word.endswith('/'):
                word = word.replace('/', '')
            ## Weird edgecase when recipe author has terrible formating, wrote ingredient is 14/-inch
            if len(word.split(' ')) > 1:
                if word.split(' ')[0].endswith('/'):
                    word = word.replace('/', '')

        if word != '' and word != 'tbs':
            singular = p.singular_noun(word)
        else:
            singular = False

        if singular is not False:
            singular_phrase.append(singular)
        else:
            if word in word_numbers:
                singular_phrase.append(word_to_int[word])
            else:
                singular_phrase.append(word)

    return " ".join(singular_phrase).lower()

def get_measurements(ingredient):
    matches = []

    ## Handles case where ingredient specifies cutting into a certain quantity ex. 1/2 inch cube, do not want to accidently link this quantity to an ingredient
    if 'cut into' in ingredient:
        ingredient_split = ingredient.split('cut into')[0]

    ingredient_split = ingredient.split(' ')
    ## Remove extra spaces
    while '' in ingredient_split:
        ingredient_split.remove('')

    counter = 0

    while counter < len(ingredient_split):
        current_ingredient = ingredient_split[counter]
        if (current_ingredient.isnumeric() or (current_ingredient[0].isnumeric() and '/' in current_ingredient and len(current_ingredient) == 3)) and counter < len(ingredient_split) - 1:
            ingredient_amount = eval(current_ingredient)
            counter += 1
            
            if (current_ingredient.isnumeric() or (current_ingredient[0].isnumeric() and '/' in current_ingredient and len(current_ingredient) == 3)):
                if len(current_ingredient) > 2:
                    ingredient_amount += eval(current_ingredient)
                    counter += 1
                else:
                    ingredient_amount *= float(current_ingredient)
                    counter += 1

            if counter < len(ingredient_split) and current_ingredient in measurements:
                matches.append(str(ingredient_amount) + ' ' + current_ingredient)
                counter += 1
                continue
            elif counter + 1 < len(ingredient_split) and ingredient_split[counter + 1] in measurements:
                counter += 1
                current_ingredient = ingredient_split[counter]
                matches.append(str(ingredient_amount) + ' ' + current_ingredient)
                counter += 1
                continue
            else:
                ## Add whole label to ingredient if measurement type cannot be found unless previous measurement has been found Ex. 6 pounds about 2 tomatoes should just be 6 pounds tomatoes, not (6 pound tomatoes, 2 whole tomatoes)
                if len(matches) == 0:
                    matches.append(str(ingredient_amount) + ' whole')
        else:
            counter += 1         

    return matches