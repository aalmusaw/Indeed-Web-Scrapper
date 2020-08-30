"""This module contains the user interface"""
import os
import pathlib

import scrapper
import url_utilities


def main():
    print("Welcome to Indeed Job Search Tool")
    print("To skip a search field, hit Enter on blank input")
    print("Invalid input will be ignored")
    job_title = input("Job Title: ")
    job_location = input("Job Location: ")
    job_radius = input("Radius of Search in km: ")
    try:
        job_radius = int(job_radius)
    except ValueError:
        job_radius = 0
    job_type = input("Job Type [Full-time, Part-time, Internship]: ")
    url_maker = url_utilities.urlMaker(job_title = job_title, location = job_location, radius = job_radius, job_type = job_type)
    url_maker.build_url()
    print(url_maker.url)
    query = scrapper.Query(url_maker.url)
    num_matches = query.num_jobs
    num_pages = (num_matches // 11)
    print(f"A total of {num_matches} matches have been found")
    for i in range(num_pages):
        print(f"Extracting data: page ({i+1}/{num_pages})")
        query.parse_soup()
        url_maker.next_page()
        query.update_soup(url_maker.url)
    print("Displaying results:")
    for key, value in query.data.items():
        print(f"Job Title: {value[0][1:-1]}") # ignore quote marks
        print(f"Job Location: {value[2][1:-1]}") # ignore quote marks
        print(f"Employer: {value[1][1:-1]}") # ignore quote marks
        print(f"Apply here: {value[3]}")
        print("\n")
    response = input("Would you like to save the results in a .csv file [Y/n]? : ")
    if "y" in response.lower():
        response = input("Provide a directory path to write to: ")
        try:
            f = open(str(os.join(pathlib.Path(response), pathlib.Path("job_query.csv"))), "w")
            f.write(str(query))
            f.close()
            print("File written successfully.")
        except Exception:
            print("An error has occurred in writing the file. ")
            print("Make sure the directory you provided is correct.")
            print("If you are using Windows, please ensure you are escaping the slashes.")
        finally:
            if f:
                f.close()
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()

