import time
import re


class Robot:
    def __init__(self, page):
        self.page = page
        self.url_icd9 = 'http://www.icd9data.com'
        self.url_main = 'http://www.icd9data.com/2014/Volume1/default.htm'

    def browser_categories(self, links):
        for link in links:
            link = f'{self.url_icd9}{link.get_attribute("href")}'
            self.page.goto(link)
            self.page.wait_for_url(link)
            self.page.locator('.definitionList').wait_for()

    def url_mapping(self):
        self.page.goto(self.url_main)
        self.page.wait_for_url(self.url_main)
        url_mapping = []
        for category in self.page.query_selector('.definitionList > ul').query_selector_all('li > .identifier'):
            url_mapping.append(
                dict(identifier=f'{category.inner_text()}', url=f'{self.url_icd9}{category.get_attribute("href")}',
                     subcategory=[]))
        for category in url_mapping:
            self.page.goto(category['url'])
            self.page.wait_for_url(category['url'])
            if 'den 408' in self.page.content():
                time.sleep(100)
            self.page.locator('.definitionList').wait_for()
            subcategories = []
            try:
                for subcategory in self.page.query_selector('.definitionList > ul').query_selector_all(
                        'li > .identifier'):
                    subcategories.append(dict(identifier=f'{subcategory.inner_text()}',
                                              url=f'{self.url_icd9}{subcategory.get_attribute("href")}'))
            except:
                for subcategory in self.page.query_selector('.definitionList').query_selector_all('li > .identifier'):
                    subcategories.append(dict(identifier=f'{subcategory.inner_text()}',
                                              url=f'{self.url_icd9}{subcategory.get_attribute("href")}'))
            category['subcategory'] = subcategories
        return url_mapping

    def illness_mapping(self, urls):
        illness_tuples = []
        for category in urls:
            for url in category['subcategory']:
                self.page.goto(url['url'])
                self.page.wait_for_url(url['url'])
                try:
                    try:
                        self.page.locator('.definitionList').wait_for(timeout=2000)
                    except:
                        full_text = self.page.query_selector('.codeIdentifier').inner_text()
                        identifier = re.search(r'\d+', full_text)[0]
                        name = full_text.replace(re.search(r'(?= \d+).*', full_text)[0], "")
                        illness_tuples.append((identifier, name))
                    else:
                        illnesses = self.page.query_selector('.definitionList').query_selector_all('li')
                        for illness in illnesses:
                            illness = illness.inner_text()
                            illness_tuples.append((illness.split(' ', 1)[0], illness.split(' ', 1)[-1]))
                except:
                    illness_tuples.append(('forbidden', {url["url"]}))
                    print(f'forbidden: {url["url"]}')
                    time.sleep(5)
        return illness_tuples
