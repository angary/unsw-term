#!/usr/bin/python3
import calendar as cal
import sys
from datetime import datetime as dt

import requests
import bs4

URL = "https://student.unsw.edu.au/calendar"
TERMS = ["Summer", "1", "2", "3", "4"]


def main():
    if len(sys.argv) != 2:
        print("Usage: unsw-term.py <DD/MM>")
        sys.exit(1)

    # Extract the date and get data from UNSW website
    [day, month] = sys.argv[1].split('/')
    date = dt(int(dt.now().year), int(month), int(day))
    soup = bs4.BeautifulSoup(requests.get(URL).content, "html.parser")

    # Extract the list of tables for each term
    calendar_details = soup.find(about="/calendar")
    term_tables = calendar_details.find_all("table", class_="table-striped")
    for i, term_table in enumerate(term_tables):
        string = within_term(date, i, term_table)
        if string:
            print(string)
            return

    # Else we did not find it
    print("Outside current term's calendar")


def within_term(date: dt, term: int, term_table: bs4.element.Tag) -> str:
    """
    Check if the date is within the term, or term break
    If the date is inside the term, return the string to print out else an empty string
    """
    # Extract the string in the format "<date> <month> - <date> <month>"
    term_duration = term_table.find_all("tr")[1].find_all("td")[1].text
    day = cal.day_abbr[date.weekday()]

    start, end = get_start_end_date(term_duration)
    if start <= date <= end:
        week = ((date - start).days // 7) + 1
        return f"{day} | Week {week} | Term {TERMS[term]}"

    # If there is a term break
    if (term_table.find_all("tr")[-1].find_all("td")[0].text == "Term break"):
        term_break = term_table.find_all("tr")[-1].find_all("td")[1].text
        break_start, break_end = get_start_end_date(term_break)
        if break_start <= date <= break_end:
            week = ((date - break_start).days // 7) + 1
            return f"{day} | Week {week} | Term {TERMS[term]}-{TERMS[term + 1]} Break"
    return ""


def get_start_end_date(term_duration: str) -> tuple[dt, dt]:
    """
    Get the start and end days as datetime objects from the term duration string
    """
    start, end = term_duration.split("-")
    def day(s: str) -> int: return int(s.split()[0])
    def month(s: str) -> int: return list(cal.month_abbr).index(s.split()[1])
    def to_dt(s: str) -> dt: return dt(dt.now().year, month(s), day(s))
    return (to_dt(start), to_dt(end))


if __name__ == "__main__":
    main()
