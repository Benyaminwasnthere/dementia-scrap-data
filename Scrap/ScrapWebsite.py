import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_blog_data(year):
    base_url = f"https://creatingmemories.blogspot.com/{year}/"
    response = requests.get(base_url)
    if response.status_code != 200:
        print(f"Failed to access {base_url}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.find_all("div", class_="post")  # Adjust based on the blog's structure

    blog_data = []

    for post in posts:
        title_element = post.find("h3", class_="post-title")  # Adjust class name as needed
        content_element = post.find("div", class_="post-body")  # Adjust class name as needed

        if title_element and content_element:
            title = title_element.get_text(strip=True)
            content = content_element.get_text(strip=True)

            blog_data.append({"content": content, "title": title})  # Content first, then title

    return blog_data

def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Main Execution
if __name__ == "__main__":
    all_blog_data = []

    for year in range(2003, 2020):  # Loop through years 2003 to 2019
        print(f"Scraping data for the year {year}...")
        blog_data = scrape_blog_data(year)
        if blog_data:
            all_blog_data.extend(blog_data)  # Add current year's data to the main list
            print(f"Data for {year} added. Total posts so far: {len(all_blog_data)}")
        else:
            print(f"No data found for the year {year}.")

        time.sleep(2)  # Add a delay to avoid overloading the server

    # Save all data into one JSON file
    save_to_json(all_blog_data, "all_blog_posts_2003_2019.json")
    print(f"All data saved to all_blog_posts_2003_2019.json")
