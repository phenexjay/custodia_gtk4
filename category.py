
class Category:
    def __init__(self, title, created):
        self.ident = title.replace(" ", "_").lower()
        self.title = title
        self.created = created

    def __repr__(self):
        return f"category-class-object: {self.ident}"


    @property
    def category_ident(self):
        return self.ident
    
    @property
    def category_title(self):
        return self.title

    @property
    def category_created(self):
        return self.created


    @category_title.setter
    def category_title(self, title):
        self.title = title
        print(f'SET: Titel wurde auf "{self.title}" gesetzt...')

    @category_created.setter
    def category_created(self, created):
        self.created = created
        print(f'SET: Erstellungsdatum wurde auf "{created}" gesetzt...')

