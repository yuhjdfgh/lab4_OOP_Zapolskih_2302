class ObjectOfArt:
    def __init__(self, title, author):
        self.__title = title
        self.__author = author
        
    def get_title(self):
        return self.__title
        
    def set_title(self, title):
        self.__title = title

    def get_author(self):
        return self.__author
        
    def set_author(self, author):
        self.__author = author

    def watch(self):
        return "Вы смотрите на произведение искусства " + self.get_title() + " от автора " + self.get_author() + "."
    
    def buy(self):
        return "Вы купили произведение искусства " + self.get_title() + " от автора " + self.get_author() + "."
    
    def transport(self):
        return "Вы транспортировали произведение искусства " + self.get_title() + " от автора " + self.get_author() + "."
    
    def restore(self):
        return "Вы реставрировали произведение искусства " + self.get_title() + " от автора " + self.get_author() + "."


class Painting(ObjectOfArt):
    def __init__(self, title, author, size, type_color):
        super().__init__(title, author)
        self.__size = size
        self.__type_color = type_color
    
    def get_size(self):
        return self.__size
        
    def set_size(self, size):
        self.__size = size
    
    def get_type_color(self):
        return self.__type_color
        
    def set_type_color(self, type_color):
        self.__type_color = type_color
    
    def transport(self):
        return "Вы транспортировали картину " + self.get_title() + " от автора " + self.get_author() + "."
    
    def restore(self):
        return "Вы реставрировали картину " + self.get_title() + " от автора " + self.get_author() + "."
    
    def varnish(self):
        return "Вы нанесли лак на картину " + self.get_title() + " от автора " + self.get_author() + "."
    
    def clean(self):
        return "Вы почистиили картину " + self.get_title() + " от автора " + self.get_author()+ "."


class Sculpture(ObjectOfArt):
    def __init__(self, title, author, weight, material):
        super().__init__(title, author)
        self.__weight = weight
        self.__material = material
    
    def get_weight(self):
        return self.__weight
        
    def set_weight(self, weight):
        self.__weight = weight
    
    def get_material(self):
        return self.__material
        
    def set_material(self, material):
        self.__material = material
    
    def transport(self):
        return "Вы транспортировали скульптуру " + self.get_title() + " от автора " + self.get_author() + "."
    
    def restore(self):
        return "Вы реставрировали скульптуру " + self.get_title() + " от автора " + self.get_author() + "."
    
    def fix(self):
        return "Вы отремонтировали скульптуру" + self.get_title() + " от автора " + self.get_author() + "."
    
    def drop(self):
        return "Вы выбросили скульптуру " + self.get_title() + " от автора " + self.get_author() + "."
