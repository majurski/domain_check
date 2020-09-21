# The original script is here, but I edited it and made it for my own purpose
# https://www.8bitavenue.com/godaddy-domain-name-api-in-python/
# This is needed to send POST and GET requests
import requests

# This is needed to limit the frequeny
# by which we are going to hit the API
# endpoints. Only certain number of
# requests can be made in a mintue
import time

# This is needed to convert API
# responses into JSON objects
import json

# Godaddy developer key and secret
api_key = ""
secret_key = ""

# API key and secret are sent in the header
headers = {"Authorization": "sso-key {}:{}".format(api_key, secret_key)}

# Domain availability and appraisal end points
url = "https://api.godaddy.com/v1/domains/available"
appraisal = "https://api.godaddy.com/v1/appraisal/{}"

# If a domain name is available
# decide whether to appraise or not
do_appraise = True

# Number of domains to check in each call.
# For example, we can not check more than 500
# domain names in one call so we need to split
# the list of domain names into chunks
chunk_size = 500

# Filter domain names by length
max_length = 30

# Filter domain names by price range
min_price = 0
max_price = 5000

# If appraisal is enabled, only include
# domain names with min appraisal price
min_appr_price = 0

# When a domain is appraised, Godaddy API
# returns similar domains sold. This is a
# nice feature to take a look at sold domains.
# To filter similar sold domains we can do that
# by setting the min sale price and the min
# year the domain was sold
min_sale_price = 0
min_sale_year = 2000

# Domain name structure:
# prefix + keyword + suffix + extension
# You can manually insert few values into
# these lists and start the search or read
# from files as demonstrated below
extensions = []

# This list holds all generated domains
# It is the list we are going to check
all_domains = []
# This list holds similar domains sold
# This is retrieved from Godaddy appraisal API
similar_domains = []
# This holds available domains found that match
# the search criteria
found_domains = []

# Open prefix, keyword, suffix and extension from files

keywords = []

# alph = "abcdefghijklmnopqrstuvxyz123456789"
alph = "abcdefghijklmnopqrstuvxyz"

for i in alph:
    for b in alph:
        for c in alph:
            for d in alph:
                    word = i + b + c + d
                    keywords.append(word)

print("Checking",len(keywords), "domain names...")
with open("extension.txt") as f:
    extensions = f.read().splitlines()

# Generate domains
for keyword in keywords:
    for extension in extensions:
        domain = "{}.{}".format(keyword, extension)
        # Filter by length
        if len(domain) <= max_length:
            all_domains.append(domain)

start_time = time.time()
# This function splits all domains into chunks
# of a given size
def chunks(array, size):
    for i in range(0, len(array), size):
        yield array[i:i + size]


# Split the original array into subarrays
domain_chunks = list(chunks(all_domains, chunk_size))

i = 0
counter = 0
class Chunkers:
    print("Oparation starts....")
    inx = 0
    # For each domain chunk (ex. 500 domains)
    while inx <= len(domain_chunks):
        if inx == len(domain_chunks):
            exit(1)
        counter += 1
        domains = domain_chunks[inx]
        # Get availability information by calling availability API
        availability_res = requests.post(url, json=domains, headers=headers)
        # print(json.loads(availability_res.text)["domains"])
        # Get only available domains with price range
        print(f"Chunk number: {inx}")
        print(f"Number of requests: {counter}")
        current_time = time.time()
        print("Approximatly Passed time ", (current_time - start_time) // 60, "minutes", (current_time - start_time) % 60, "sec")

        if availability_res.ok != True:
            if inx >= 1:
                inx = inx - 1
            time.sleep(5)
        # print(availability_res)
        # print(domains)
        if availability_res.ok:
            for domain in json.loads(availability_res.text)["domains"]:
                i += 1
                if domain["available"]:
                    found_domains.append(domain["domain"])
                    price = float(domain["price"]) / 1000000
                    if price >= min_price and price <= max_price:
                        print("{}, {:30}".format(i,domain["domain"]))

            print("-----------------------------------------------")
            # API call frequency should be ~ 30 calls per minute
            time.sleep(3)
        inx += 1
        print("Number of domains found ", len(found_domains))
        print("Domains found ", found_domains)


if __name__ == "__main__":
    while True:
        Chunkers()

