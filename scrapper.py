"""This module allows scraping and filtering information from Indeed.com URL"""

import requests
from bs4 import BeautifulSoup

class Query(object):
    """This class stores the results of a client query in a structured format
    
    Attributes:
        data: a dictionary with a string job_id as keys and a tuple storing
            (TITLE, EMPLOYER, LOCATION, LINK) as values.
        num_jobs: an int storing the total number of matches.
        soup: a BeautifulSoup object storing the current url's HTML content
    """
    def __init__(self, url):
        """Initializes the attributes of Query using the info of the given URL"""
        page = None
        while not page:
            page = requests.get(url)
        self.soup = BeautifulSoup(page.content, "html.parser")
        self.data = {}
        self.num_jobs = self.find_total_matches()
    
    def update_soup(self, url):
        """Updates the soup instance variable using the given URL
        
        Args:
            url: A string containing Indeed.com url with query parameters
        """
        page = None
        while not page:
            page = requests.get(url)
        self.soup = BeautifulSoup(page.content, "html.parser")
        
    def find_total_matches(self):
        """Find the total job matches of this query
        
        Returns:
            An int specifying the total job matches
        """
        html = self.soup.find(id='searchCountPages')
        if html is None:
            return 0
        words = html.text
        # words may look like this:
        #"\n                    Page 2 of 1,226 jobs"
        i = 0
        while words[i] != "f":
            i += 1
        i += 1
        j = i
        while words[j] != "j":
            j += 1
        j -= 1
        return int(words[i:j].strip(" ").replace(",", ""))
    
    def parse_soup(self):
        """Parses the soup instance variable to populate the data instance variable with job postings"""
        results = self.soup.find(id="resultsCol")
        job_elems = results.find_all("div", class_="jobsearch-SerpJobCard unifiedRow row result")
        for job_elem in job_elems:
            job_id = job_elem.get("data-jk")
            job_title = "'"+((job_elem.find("h2")).find("a")).get("title")+"'"
            job_link = ((job_elem.find("h2")).find("a")).get("href")
            job_link = "https://ca.indeed.com" + job_link
            job_employer = ((job_elem.find("div", attrs={"class":"sjcl"})).find("span", attrs={"class":"company"})).text.strip("\n")
            job_employer = "'" + job_employer + "'"
            job_location = ((job_elem.find("div", attrs={"class":"sjcl"})).find("div", attrs={"class":"recJobLoc"})).get("data-rc-loc")
            job_location = "'" + job_location + "'"
            self.data[job_id] = (job_title, job_employer, job_location, job_link)
        
    def __str__(self):
        """Converts the data of the Query into a csv format
        
        Returns:
            A string specifying the query data in csv format
        """
        CSV ="\n".join([k+','+','.join(v) for k,v in self.data.items()])
        return CSV
    
def main():
    """A client test"""
    url1 = "https://ca.indeed.com/jobs?q=Software%20Developer&l=Toronto,%20ON&jt=fulltime&start=10"
    query = Query(url1)
    query.parse_soup()
    query.update_soup("https://ca.indeed.com/jobs?q=Software%20Developer&l=Toronto,%20ON&jt=fulltime&start=20")
    query.parse_soup()
    query.update_soup("https://ca.indeed.com/jobs?q=Software%20Developer&l=Toronto,%20ON&jt=fulltime&start=0")
    query.parse_soup()
    print(query)
if __name__ == "__main__":
    main()
