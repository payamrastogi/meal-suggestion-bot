class FileHandler:
    def process_file(self, filename):
        dict = {}
        ingredient_dict = {}
        with open(filename) as file:
            for line in file:
                if line and line.strip():
                    line = line.strip().lower()
                    name = line.split(":")[0].strip().lower()
                    ingredients = line.split(":")[1].strip().split(",")
                    for ingredient in ingredients:
                        i = ingredient.strip().lower()
                        if i in ingredient_dict:
                            ingredient_dict[i].append(name)
                        else:
                            ingredient_dict[i] = [name]
                        if name in dict:
                            dict[name].append(i)
                        else:
                            dict[name] = [i]
        #print(dict)
        #print(ingredient_dict)
        return dict, ingredient_dict

if __name__ == "__main__":
    fileHandler = FileHandler()
    #fileHandler.process_file('dal.txt')
    #fileHandler.process_file('parantha.txt')
    fileHandler.process_file('sabji.txt')