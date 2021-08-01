#!/usr/bin/python3
import calendar
import sys
from datetime import datetime as dt

import requests
import bs4

url = "https://student.unsw.edu.au/calendar"
terms = ["Summer", "1", "2", "3", "4"]

def main():

    # Check requirements
    if len(sys.argv) != 2:
        print("Usage: unsw-term.py <DD/MM>")
        sys.exit(1)
    
    # Extract the date
    [day, month] = sys.argv[1].split('/')
    year = dt.now().year
    date = dt(int(year), int(month), int(day))

    # Get the data from UNSW website
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "html.parser")

    # Extract the list of tables for each term
    calendar_details = soup.find(id="node-1334")
    term_tables = calendar_details.find_all("table", class_="table-striped")

    # Find the date
    for i, term_table in enumerate(term_tables):

        # If we found the date, end the program
        if within_term(date, i, term_table):
            return
    
    # Else we did not find it
    print("Outside current term's calendar")


def within_term(date: dt, term: int, term_table: bs4.element.Tag) -> bool:
    """
    Check if the date is within the term, or term break
    If the date is inside the term, return True
    """
    # Extract the string in the format "<date> <month> - <date> <month>"
    term_duration = term_table.find_all("tr")[1].find_all("td")[1].text

    # Get the starting date and end date
    start, end = get_start_end_date(term_duration)
    if within_duration(date, start, end, False, term):
        return True
    
    # If there is a term break
    if (term_table.find_all("tr")[-1].find_all("td")[0].text == "Term break"):

        term_break = term_table.find_all("tr")[-1].find_all("td")[1].text

        # Get the starting date and end date of the break
        break_start, break_end = get_start_end_date(term_break)
        if within_duration(date, break_start, break_end, True, term):
            return True
    
    return False


def get_start_end_date(term_duration: str) -> tuple:
    """
    Get the start and end days as datetime objects from the term duration string
    """
    start, end = term_duration.split("-")
    year = dt.now().year

    # Get starting date
    start_day = int(start.split()[0])
    start_month = list(calendar.month_abbr).index(start.split()[1])
    start_date = dt(year, start_month, start_day)

    # Get the ending date
    end_day = int(end.split()[0])
    end_month = list(calendar.month_abbr).index(end.split()[1])
    end_date = dt(year, end_month, end_day)
    return (start_date, end_date)


def within_duration(date: dt, start: dt, end: dt, is_break: bool, term: int) -> bool:
    """
    Check if the date is within the current duration
    If it is, print out the date as what week of the term or break it is
    and return True
    """
    if not start <= date <= end:
        return False

    week = ((date - start).days // 7) + 1
    day_name = calendar.day_abbr[date.weekday()]
    if is_break:
        print(day_name, "| Week", week, "| Term", terms[term] + "-" + terms[term + 1], "Break")
    else:
        print(day_name, "| Week", week, "| Term", terms[term])
    return True


if __name__ == "__main__":
    main()
