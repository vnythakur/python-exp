import json
import gazpacho

URL = "https://en.wikipedia.org/wiki/List_of_world_records_in_swimming"

RECORDS = (0, 1, 3, 4)
COURSES = ("LC Men", "LC Women", "SC Men", "SC Women")
JSON_RECORD = "records.json"
# WHERE = "/home/vinay4pyanywhere/webapp"
WHERE = ""

html = gazpacho.get(URL)
soup = gazpacho.Soup(html)


tables = soup.find("table", mode="list")

result = {}
for table, course in zip(RECORDS, COURSES):
    result[course] = {}
    for i, row in enumerate(tables[table].find("tr", mode="list")[1:]):
        columns = row.find("td", mode="list")
        event = columns[0].text
        time = columns[1].text
        if "relay" not in event:
            result[course][event] = time

with open(WHERE + JSON_RECORD, "w") as file:
    json.dump(result, file)
