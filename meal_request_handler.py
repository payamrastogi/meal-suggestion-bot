from file_handler import FileHandler
import random


class MealRequestHandler:

    def __init__(self):
        self.file_handler = FileHandler()
        self.na_ingredient_dict = []
        self.dal_dict, self.dal_ingredient_dict = self.file_handler.process_file('dal.txt')
        self.sabji_dict, self.sabji_ingredient_dict = self.file_handler.process_file('sabji.txt')
        self.parantha_dict, self.parantha_ingredient_dict = self.file_handler.process_file('parantha.txt')
        self.breakfast_dict, self.breakfast_ingredient_dict = self.file_handler.process_file('breakfast.txt')

    def get_random_meal(self, meal_type):
        if meal_type == 'D':
            copied_dict = self.dal_dict.copy()
            copied_ingredient_dict = self.dal_ingredient_dict.copy()
        elif meal_type == 'S':
            copied_dict = self.sabji_dict.copy()
            copied_ingredient_dict = self.sabji_ingredient_dict.copy()
        elif meal_type == 'B':
            copied_dict = self.breakfast_dict.copy()
            copied_ingredient_dict = self.breakfast_ingredient_dict.copy()
        else:
            copied_dict = self.parantha_dict.copy()
            copied_ingredient_dict = self.parantha_ingredient_dict.copy()
        self.filter_dishes(copied_dict, copied_ingredient_dict)
        entry_list = list(copied_dict.items())
        if entry_list:
            random_meal = random.choice(entry_list)
            return random_meal
        return None, None

    def filter_dishes(self, copied_dict, copied_ingredient_dict):
        for unavailable_ingredient in self.na_ingredient_dict:
            if unavailable_ingredient in copied_ingredient_dict:
                for item in copied_ingredient_dict[unavailable_ingredient]:
                    copied_dict.pop(item, 'No Key found')

    def add_unavailable_ingredients(self, na_ingredients):
        for ingredient in na_ingredients:
            self.na_ingredient_dict.append(ingredient)

    def reset_unavailable_ingredients(self):
        self.na_ingredient_dict = []


if __name__ == "__main__":
    mealRequestHandler = MealRequestHandler()
    meal = mealRequestHandler.get_random_meal('S')
    print(meal)
    mealRequestHandler.add_unavailable_ingredients(['onion'])
    meal = mealRequestHandler.get_random_meal('S')
    print(meal)
