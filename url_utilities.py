"""This module allows the creation and parsing of Indeed.com URLs"""

class urlMaker(object):
    """
    Turns a client query into a valid URL
    
    A client provides a dictionary of query parameters. An object of this class
    performs the necessary parsing to generate a URL compatible with Indeed.com.
    
    Attributes:
        job_title: A string to describe the job to search for.
        location: A string of a city, or a province (Default is unspecified).
        radius: An int minimum radius of search in km (Default is unspecified).
        job_type: A string specifying whether the job is full-time, part-time, etc. 
            (Default is unspecified). Accepts one of {fulltime, parttime, internship}.
        
    """


    def __init__(self, **params):
        """Initialize the query parameters"""
        self.job_title = params["job_title"]
        self.location = params["location"]
        self.radius = params["radius"]
        self.job_type = job_type_tokenizer(params["job_type"])
        self.url = ""
        
    def build_url(self):
        """Builds a URL using the existing urlMaker attributes"""
        link = ["https://ca.indeed.com/jobs?"]
        link.append("q="+token_producer(self.job_title))
        if self.location != "":
            link.append("&l="+token_producer(self.location))
        if self.radius != 0:
            link.append("&radius="+str(self.radius))
        if self.job_type != "":
            link.append("&jt="+self.job_type)
        link.append("&start=0")
        self.url = "".join(link)
        
    def next_page(self):
        """Changes the url so that it directs to the next page"""
        i = 0
        while self.url[i-1] != "=":
            i -= 1
        page_num = int(self.url[i:])
        page_num += 10
        self.url = self.url[:i]
        self.url += str(page_num)
    
    def prev_page(self):
        """Changes the url so that it directs to the previous page"""
        i = 0
        while self.url[i-1] != "=":
            i -= 1
        page_num = int(self.url[i:])
        page_num -= 10
        self.url = self.url[:i]
        self.url += str(page_num)
        
def job_type_tokenizer(raw_job_type):
    """Standradizes a spelling variant of the job type string given by the client.
    
    Args:
        raw_job_type: A string describing the job type, i.e. full-time, part-time, etc.
        
    Returns:
        A string spelled in a form that a urlMaker object expects.
    """
    if "full" in raw_job_type.lower():
        return "fulltime"
    elif "part" in raw_job_type.lower():
        return "parttime"
    elif "intern" in raw_job_type.lower():
        return "internship"
    else:
        return ""
    
def token_producer(raw_string):
    """Turns a client string into a valid URL token
    
    Args:
        raw_string: A string of English words and punctuation marks.
        
    Returns:
        A string with punctuation marks encoded so as to be included in a URL.
    """
    char_map = {
    " ": "%20", "!": "%21", "\"": "%22", "#": "%23", "$": "%24",
     "%": "%25", "&": "%26", "'": "%27", "(": "%28", ")": "%29",
    "*": "%2A", "+": "%2B", ",": "%2C", "-": "%2D", ".": "%2E",
    "/": "%2F", ":": "%3A", ";": "%3B", "<": "%3C", "=": "%3D",
    ">": "%3E", "?": "%3F", "@": "%40", "[": "%5B", "\\": "%5C",
     "]": "%5D", "^": "%5E", "_": "%5F", "`": "%60", "{": "%7B",
     "|": "%7C", "}": "%7D", "~": "%7E",
                }
    token = []
    for char in raw_string:
        if char not in char_map:
            token.append(char)
        else:
            token.append(char_map[char])
    return "".join(token)

def main():
    """A client test"""
    title = input("Enter job title: ")
    place = input("Enter a location: ")
    rad = int(input("Enter a search radius in km: "))
    j_type = input("Enter the job-type, i.e. full-time, part-time, or internship: ")
    
    query = urlMaker(job_title = title, location = place, radius = rad, job_type = j_type)
    query.build_url()
    print(f"Your URL is {query.url}")
    query.next_page()
    print(f"Your next page URL is {query.url}")
    query.next_page()
    print(f"Your next page URL is {query.url}")
    query.prev_page()
    print(f"Your previous page URL is {query.url}")
    
if __name__ == "__main__":
    main()
    