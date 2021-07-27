#!/usr/bin/python3
import calendar
import sys
from datetime import datetime

import requests
from bs4 import BeautifulSoup

url = "https://student.unsw.edu.au/calendar"

def main():

    # Check requirements
    if len(sys.argv) != 2:
        print("Usage: unsw-term.py <DD/MM>")
        sys.exit(1)
    
    # Extract the date
    [day, month] = sys.argv[1].split('/')
    year = datetime.now().year
    date = datetime(int(year), int(month), int(day))

    # Get the data from UNSW website
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    calendar_details = soup.find(id="node-1334")
    term_tables = calendar_details.find_all("table", class_="table-striped")

    # Find the date
    terms = ["Summer", "One", "Two", "Three"]
    for term, term_table in zip(terms, term_tables):

        # Extract the string in the format "<date> <month> - <date> <month>"
        term_duration = term_table.find_all("tr")[1].find_all("td")[1].text

        # Get the starting date and end date
        start_date, end_date = get_start_end_date(term_duration)

        # Check if the date is in the range
        if date >= start_date and date <= end_date:

            # Find number of days since the start of term and day of week
            week = (date - start_date).days // 7
            day_name = calendar.day_name[date.weekday()]

            print(day_name, "Week", week, "Term", term)
            return
    
    print("Outside current term's calendar")


def get_start_end_date(term_duration):
    start, end = term_duration.split("-")
    year = datetime.now().year

    # Get starting date
    start_day = int(start.split()[0])
    start_month = list(calendar.month_abbr).index(start.split()[1])
    start_date = datetime(year, start_month, start_day)

    # Get the ending date
    end_day = int(end.split()[0])
    end_month = list(calendar.month_abbr).index(end.split()[1])
    end_date = datetime(year, end_month, end_day)
    return start_date, end_date


if __name__ == "__main__":
    main()
