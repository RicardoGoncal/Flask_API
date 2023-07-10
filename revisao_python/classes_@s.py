"""
Revisao:

@classmethod
"""

class Book:
    TYPES = ("capa dura", "capa normal") # Para uso do @classmethod

    def __init__(self, name, book_type,weight):
        self.name = name
        self.book_type = book_type
        self.weight = weight

    def __repr__(self):
        return f"<Book {self.name}, {self.book_type}, weight {self.weight}g"
    
    @classmethod
    def capa_dura(cls, name,weight):
        return cls(name, Book.TYPES[0],weight + 100)
    
    @classmethod
    def capa_normal(cls, name,weight):
        return cls(name, Book.TYPES[1],weight)
    

# exemplos
book = Book.capa_dura('Harry potter', 1500)
light = Book.capa_normal('Cabelo azul', 600)

print(book)
print(light)