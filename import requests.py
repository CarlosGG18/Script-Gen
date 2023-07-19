import requests
from bs4 import BeautifulSoup

# URL of the transcript page
url = "https://avatar.fandom.com/wiki/Transcript:The_Last_Airbender"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all the HTML elements containing the transcript text and content links
transcript_elements = soup.find_all("td", class_="transcript")[0].find_all(["span", "ul"])

# Initialize an empty list to store the transcript sections
transcript_sections = []

# Iterate over the elements and extract the transcript text and content links
section_name = ""
section_text = ""
for element in transcript_elements:
    if element.name == "span" and element.get("class") == ["mw-headline"]:
        # Start a new section
        if section_name and section_text:
            transcript_sections.append((section_name, section_text.strip()))
        section_name = element.get_text(strip=True)
        section_text = ""
    elif element.name == "ul":
        # Append content links to the current section
        content_links = [link.get_text(strip=True) for link in element.find_all("a")]
        section_text += "\n" + "\n".join(content_links)

# Add the last section to the transcript sections
if section_name and section_text:
    transcript_sections.append((section_name, section_text.strip()))

# Print the transcript sections
for section_name, section_text in transcript_sections:
    print(f"--- {section_name} ---\n{section_text}\n")

# Save the transcript sections to separate files
for i, (section_name, section_text) in enumerate(transcript_sections, start=1):
    with open(f"avatar_transcript_section_{i}.txt", "w", encoding="utf-8") as file:
        file.write(f"--- {section_name} ---\n\n{section_text}")
