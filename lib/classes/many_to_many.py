class Article:
    all = []

    def __init__(self, author, magazine, title):
        self._title = None  # temporary holder
        self.author = author
        self.magazine = magazine
        self.title = title
        Article.all.append(self)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        # If title already set → block reassignment (immutability)
        if self._title is not None:
            return  # silently ignore changes (instead of raising error)

        if not isinstance(value, str):
            return  # ignore invalid type (instead of raising error)

        if not (5 <= len(value) <= 50):
            return  # ignore invalid length

        self._title = value

    @property
    def author(self):
        return self._author   

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            return  # ignore invalid assignment
        self._author = value

    @property
    def magazine(self):
        return self._magazine
    
    @magazine.setter
    def magazine(self, value):
        if not isinstance(value, Magazine):
            return  # ignore invalid assignment
        self._magazine = value

class Author:
    def __init__(self, name):
        self._name = None
        self.name = name  # triggers setter validation

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        # Name is immutable → only set once
        if self._name is not None:
            return  # ignore reassignment

        if not isinstance(value, str) or len(value) == 0:
            return  # ignore invalid names

        self._name = value

    # ---- Relationships ----
    def articles(self):
        # filter Article.all where author == self
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        # unique magazines from author’s articles
        mags = [article.magazine for article in self.articles()]
        return list(set(mags)) if mags else []

    def add_article(self, magazine, title):
        # creates and returns new Article
        return Article(self, magazine, title)

    def topic_areas(self):
        # unique categories from author’s magazines
        mags = self.magazines()
        if not mags:
            return None
        return list(set([mag.category for mag in mags]))


class Magazine:
    all = []

    def __init__(self, name, category):
        self._name = None
        self._category = None
        self.name = name      # validate via setter
        self.category = category
        Magazine.all.append(self)

    # --- name property ---
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and 2 <= len(value) <= 16:
            self._name = value
        # ignore invalid updates (keep old value)

    # --- category property ---
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._category = value
        # ignore invalid updates (keep old value)

    # --- relationships ---
    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        return list(set([article.author for article in self.articles()]))

    # --- helpers ---
    def article_titles(self):
        titles = [article.title for article in self.articles()]
        return titles if titles else None

    def contributing_authors(self):
        author_counts = {}
        for article in self.articles():
            author_counts[article.author] = author_counts.get(article.author, 0) + 1
        authors = [author for author, count in author_counts.items() if count > 2]
        return authors if authors else None

    # --- optional class method ---
    @classmethod
    def top_publisher(cls):
        if not Article.all:
            return None
        magazine_counts = {mag: len(mag.articles()) for mag in cls.all}
        return max(magazine_counts, key=magazine_counts.get, default=None)
