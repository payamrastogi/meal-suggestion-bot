class User:
    def __init__(self, id=""):
        self.id = id
        self.first_name = ""
        self.last_name = ""
        self.lang = ""

    def get_full_name_and_lang(self):
        return f"{self.first_name} {self.last_name} ({self.lang})"

    def __str__(self):
        return f"id:{self.id} first_name:{self.first_name} last_name:{self.last_name} lang:{self.lang}"


class MealSuggestion:
    def __init__(self, meal="", meal_type="", ingredients=[]):
        self.meal = meal
        self.meal_type = meal_type
        self.ingredients = ingredients
        self.accept_action = "accept"
        self.accept_position = len(self.ingredients)-1

    def __str__(self):
        return f"meal:{self.meal} ingredients:{self.ingredients} accept_action:{self.accept_action} accept_position:{self.accept_position}"