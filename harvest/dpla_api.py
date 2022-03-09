from dpla.api import DPLA
import json

# -- DLG API key
dpla = DPLA('9a476ab6c2c161ebcfe7d2de1b520863')

# -- Search string
result = dpla.search(q='goldfish bowl')

# -- Number of results/pages
print("Records: " + result.count)
totalPages = round(result.count / 10)
pageParam = 1

# -- Export results to json
fullData = []
pageCount = 1

for page in range(1, totalPages+1):
    paginatedResult = dpla.search(q='goldfish bowl', page=pageParam)
    x = 0
    if pageCount == totalPages:
        itemRange = result.count % 10
    else:
        itemRange = 10
    for item in range(0, itemRange):
        print(paginatedResult.items[x]["sourceResource"]["title"])
        fullData.append(paginatedResult.items[x])
        x += 1
    pageParam += 1
    pageCount += 1

with open("C:\\Users\\Nicole Lawrence\\Desktop\\dpla_response\\dplaData.json", "w") as f:
    json.dump(fullData, f)