class Snippet:
    def __init__(self, category, title, created, changed="", content="", language="", description="", tags=[]):
        self.ident = (category + "_" + title).replace(" ", "_").lower()
        self.category = category
        self.title = title
        self.created = created
        self.changed = changed
        self.content = content
        self.language = language
        self.description = description
        self.tags = tags
        
    def __repr__(self):
        return f"snippet-class-object: {self.ident}"


    @property
    def snippet_ident(self):
        return self.ident
    
    @property
    def snippet_category(self):
        return self.category
        
    @property
    def snippet_title(self):
        return self.title
    
    @property
    def snippet_created(self):
        return self.created
    
    @property
    def snippet_changed(self):
        return self.changed
    
    @property
    def snippet_content(self):
        return self.content

    @property
    def snippet_language(self):
        return self.language

    @property
    def snippet_description(self):
        return self.description

    @property
    def snippet_tags(self):
        return self.tags
    
    
    
    @snippet_category.setter
    def snippet_category(self, category):
        self.category = category
        print(f'SET: Kategorie in wurde auf "{category}" gesetzt...')

    @snippet_title.setter
    def snippet_title(self, title):
        self.title = title
        print(f'SET: Titel wurde auf "{title}" gesetzt...')
        
    @snippet_created.setter
    def snippet_created(self, created):
        self.created = created
        print(f'SET: Erstellungsdatum wurde auf "{created}" gesetzt...')
    
    @snippet_changed.setter
    def snippet_changed(self, changed):
        self.changed = changed
        print(f'SET: Änderungsdatum wurde auf "{changed}" gesetzt...')
        
    @snippet_content.setter
    def snippet_content(self, content):
        self.content = content
        print(f'SET: Inhalt wurde auf "{content}" gesetzt...')

    @snippet_language.setter
    def snippet_language(self, language):
        self.language = language
        print(f'SET: Sprache wurde auf "{language}" gesetzt...')

    @snippet_description.setter
    def snippet_description(self, description):
        self.description = description
        print(f'SET: Beschreibung wurde auf "{description}" gesetzt...')

    @snippet_tags.setter
    def snippet_tags(self, tags):
        self.tags = tags
        print(f'SET: Tags wurde auf "{tags}" gesetzt...')
    

