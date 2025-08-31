import requests
from bs4 import BeautifulSoup
from datetime import date
import re

def get_tasks_for_date(calendar_url: str, target_date: date):
    """
    Scrapes a specific calendar URL to find homework tasks for a given date.

    Args:
        calendar_url: The full URL of the calendar page to scrape.
        target_date: A datetime.date object for the desired day.

    Returns:
        A formatted string with the tasks for the given date, or None if no tasks are found.
    """
    print(f"Scraping {calendar_url} for date {target_date.strftime('%Y-%m-%d')}...")
    try:
        response = requests.get(calendar_url, timeout=20)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching URL {calendar_url}: {e}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')

    # Regex to find the date in format "Month Day, Year" (e.g., "August 29, 2025")
    target_date_pattern = re.compile(
        fr'{target_date.strftime("%B")}\s+{target_date.day},\s+{target_date.year}',
        re.IGNORECASE
    )

    date_elements = soup.find_all(string=target_date_pattern)
    if not date_elements:
        print("No date elements found on the page.")
        return None

    all_tasks = []
    for element in date_elements:
        container = element.find_parent('li')
        if container:
            text_content = container.get_text(separator='\\n', strip=True)
            lines = text_content.split('\\n')

            title = lines[0] if lines else "Tarea"

            task_lines = []
            date_found_in_container = False
            for line in lines:
                if date_found_in_container:
                    cleaned_line = re.sub(r'^[+\d\.]+\s*', '', line).strip()
                    # Filter out the generic "information was sent" line and empty lines
                    if cleaned_line and "esta información se envió" not in cleaned_line.lower():
                        task_lines.append(f"* {cleaned_line}")

                if target_date_pattern.search(line):
                    date_found_in_container = True

            if task_lines:
                formatted_task = f"**{title}**\\n" + "\\n".join(task_lines)
                if formatted_task not in all_tasks:
                    all_tasks.append(formatted_task)

    if not all_tasks:
        print("Date elements were found, but no tasks could be parsed.")
        return None

    print(f"Found {len(all_tasks)} tasks.")
    return "\\n\\n".join(all_tasks)
