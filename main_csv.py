import requests
import csv

# Create a session, login and receive token to work with.
s = requests.Session()
s.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})
clientid = "SOMETHING"
secretid = "SOMETHING"
authenticate = "grant_type=client_credentials&client_id={}&client_secret={}&scope=token".format(clientid, secretid)
print("Get token...")
x = s.post("https://id.sophos.com/api/v2/oauth2/token", authenticate)
authdata = x.json()
# Loose content type header
s.headers.pop('Content-Type')

# Update header data to use token from now on.
print("Update header for authentication")
s.headers.update({'Authorization': 'Bearer {}'.format(authdata.get("access_token"))})

# Get operation ID
print("Get organisation data...")
x = s.get("https://api.central.sophos.com/whoami/v1")
orgdata = x.json()

# Get all tenant data from all OpCo's
print("Get tenant data...")
s.headers.update({"X-Organization-ID": orgdata.get("id")})
x = s.get("https://api.central.sophos.com/organization/v1/tenants?pageTotal=true")
s.headers.pop('X-Organization-ID')
tenantdata = x.json()
print("Found {} tenants...".format(len(tenantdata.get("items"))))

# Loop over tenants to find all allowed sites from webcontrol system
# Collection of list below.
# List format: Tuple ("OpCoName", [ListSites]
itemlist = list()
for tenant in tenantdata.get("items"):
    print("Grabbing data from {}".format(tenant.get("name")))
    region = tenant.get("dataRegion")
    s.headers.update({"X-Tenant-ID": tenant.get("id")})

    # Paging vars.
    page = 1
    max = 2
    # Loop over pages, set max of 2 but overwrite data returned by the query.
    while page < max:
        print("Grabbing data from page {}".format(page))
        x = s.get("https://api-{}.central.sophos.com/endpoint/v1/settings/web-control/local-sites?page={}&pageSize=50&pageTotal=true".format(region, page))
        data = x.json()
        # Add data to tuple list
        itemlist.append((tenant.get("name"), data.get("items")))
        # Iterate pages
        page += 1
        # Ovewrite max page (if none, leave 2)
        max = data.get("pages").get("total", 2)

    s.headers.pop("X-Tenant-ID")

print("Providing results to user via CSV export")
with open('sophos_output.csv', mode='w') as csv_file:
    fieldnames = ['opco', 'url', 'tags', 'comment']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

    writer.writeheader()
    # Loop over tuple list
    for item in itemlist:
        for uri in item[1]:
            writer.writerow({
                'opco': item[0],
                'url': uri.get("url"),
                'tags': uri.get("tags"),
                'comment': uri.get("comment")
            })


print("Videns rocks, may the force be with us!")
print("""
    __.-._
    '-._"7'
     /'.-c
     |  /T
snd _)_/LI
""")
