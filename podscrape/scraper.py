from bs4 import BeautifulSoup

class Scraper(object):

    def __init__(self, filename):
        self.soup = make_soup_from_file(filename)

    def get_itunes_podcast_urls(self):
        podcast_soup = self.soup.find("div", id="selectedcontent")
        a_list = podcast_soup.find_all("a")
        urls = []
        for tag in a_list:
            urls.append(tag.get('href'))
        return urls

    def get_top_level_genre_tags(self):
        genre_soup = self.soup.find("div", id="genre-nav")
        a_list = genre_soup.find_all("a", class_="top-level-genre")
        return a_list

    def get_top_level_genre_urls(self):
        a_list = self.get_top_level_genre_tags()
        urls = []
        for tag in a_list:
            urls.append(tag.get('href'))
        return urls

    def get_currently_selected_genre(self):
        """
        Return the Tag for the current genre

        If the current genre element with a "selected" css class is a
        subgenre, this will return the subgenre's parent genre.

        """
        selected = None
        genres = self.get_top_level_genre_tags()
        if genres:
            for tag in genres:
                if "selected" in tag['class']:
                    selected = tag
                    break
            #No hits in genres means a subgenre is currently selected
            else:
                subgenre = self.get_currently_selected_subgenre()
                if subgenre:
                    parent_li = subgenre.parent.parent.parent
                    selected = parent_li.find("a", class_="top-level-genre")
        return selected

    def get_subgenre_tags(self):
        genre_soup = self.soup.find("div", id="genre-nav")
        subgenre_soup = genre_soup.find(class_="list top-level-subgenres")
        if subgenre_soup:
            a_list = subgenre_soup.find_all("a")
        else:
            a_list = None
        return a_list

    def get_subgenre_urls(self):
        a_list = self.get_subgenre_tags()
        if a_list:
            urls = []
            for tag in a_list:
                urls.append(tag.get('href'))
            return urls
        else:
            return None

    def get_currently_selected_subgenre(self):
        """Return the Tag of the currently selected subgenre"""
        selected = None
        subgenres = self.get_subgenre_tags()
        if subgenres:
            parent_list = subgenres[0].parent.parent
            selected = parent_list.find("a", class_="selected")
        return selected

    def get_number_of_pages(self):
        page_soup = self.soup.find("ul", class_="list paginate")

        if (page_soup is None):
            return 0
        else:
            # I know this will find the numbers plus the next link
            # But due to an off by one error on the site, there's
            # always one link left on an unlisted page.
            a_list = page_soup.find_all("a")
            return len(a_list)

    def get_letter_tags(self):
        letter_soup = self.soup.find("ul", class_="list alpha")
        if letter_soup:
            a_list = letter_soup.find_all("a")
        else:
            a_list = None
        return a_list

    def get_currently_selected_letter(self):
        """Returns the Tag for the current letter"""
        selected = None
        letters = self.get_letter_tags()
        if letters:
            parent_list = letters[0].parent.parent
            selected = parent_list.find("a", class_="selected")
        return selected

    def get_page_tags(self):
        page_soup = self.soup.find("ul", class_="list paginate")
        a_list = None
        if page_soup:
            # I know this will find the numbers plus the next link
            # But due to an off by one error on the site, there's
            # always one link left on an unlisted page.
            a_list = page_soup.find_all("a")
            last_href = a_list[-1]['href']
            last_page_number = len(a_list)
            last_page_string = "page=" + str(last_page_number)
            last_href = last_href.replace("page=2", last_page_string)
            a_list[-1]['href'] = last_href
            a_list[-1].string = str(last_page_number)
            a_list.pop(0)
        return a_list

def make_soup_from_file(filename):
    handle = open(filename)
    text = handle.read()
    handle.close()
    soup = BeautifulSoup(text)
    return soup
