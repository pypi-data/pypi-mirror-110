import csv
from random import choice
import os


class Names:
    def __init__(self):
        self.names = self.get_all()

    def get_names(self):
        path = os.path.join(os.path.dirname(__file__), "baby-names.csv")
        f = open(path, 'r', encoding='utf-8')
        reader = csv.DictReader(f)
        return reader

    def get_all(self):
        """
        take in consideration that this is 10s of thousands of names
        :return: list
        """
        return [name['name'] for name in list(self.get_names())]

    def get_single(self):
        """
        returns a single random name of any sex
        :return: str
        """

        return choice(self.get_all())

    def boy_names(self, n=None):
        """
        returns a list a given amount of boy designated names
        :param n: int
        :return: list
        """
        boys = [name['name'] for name in list(self.get_names())
                if name['sex'] == 'boy']
        # Check if no number was passed
        if n is None:
            return boys
        else:
            # Return a a given amount of random boy names
            return self.get_random(n, boys)

    def girl_names(self, n=None):
        """
        returns a list a given amount of girl designated names
        :param n: int
        :return: list
        """

        girls = [name['name'] for name in list(self.get_names())
                 if name['sex'] == 'girl']

        # Check if no number was passed
        if n is None:
            return girls
        else:
            # Return a given amount of random girl names
            return self.get_random(n, girls)

    def get_by_letter(self, letter, n=None):
        """
        returns a list of names starting with a given letter, user can
        optionally choose how many
        :param n: int
        :param letter: chr
        :return: list
        """
        names_of_letter = [name for name in self.get_all()
                           if name[0].lower() == letter.lower()]
        if n is None:
            return names_of_letter
        else:
            return self.get_random(n, names_of_letter)

    def get_random(self, n, name_dir=None):
        """
        returns a list of random names based on a given amount
        :param name_dir:
        :param n: int
        :return:
        """
        if name_dir is None:
            name_dir = self.get_all()
        name_list = list()

        # Iterate through the given number
        for _ in range(n):
            name = choice(name_dir)
            # Make sure there are no repeat names in the final list
            while name in name_list:
                name = choice(name_dir)

            name_list.append(name)

        return name_list
