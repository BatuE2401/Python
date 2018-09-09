import wikipedia #Module to get the information from a certain wikipedia page

class WikiSearch:
    def __init__(self):
        self.baseURL = 'https://en.wikipedia.org/wiki/' #The base url for wikipedia

    def create_article_url(self, names): #Creates the url for the wiki page
        url = self.baseURL
        for name in names:
            if names.index(name) != len(names) - 1:
                url += name + '_'
            else:
                url += name

        return url

    def create_article_name(self, names): #Creates the name for the wiki page based on the proper nouns
        article_name = ''
        for name in names:
            if names.index(name) != len(names) - 1:
                article_name += name + ' '
            else:
                article_name += name

        return article_name

    def get_summary(self, names): #Gets the summary from the wiki page using the create_article_name function
        article_name = self.create_article_name(names)
        wikipedia.set_lang('en') #Sets the language
        summary = wikipedia.summary(article_name, redirect = True, auto_suggest = True)
        return summary
