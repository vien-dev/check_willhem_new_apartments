#you should install pip module requests first
import requests
import re

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"}

r = requests.get("https://www.hemnet.se/bostader?location_ids%5B%5D=17920&item_types%5B%5D=bostadsratt&living_area_min=35&price_max=1750000&fee_max=4500", headers=headers)

#print(r.text)

#with open("hemnet.html", mode="w") as f:
#  print(r.text, file=f)

mo = re.search(".*itemListElement.*", r.text) #regex for the string
print(mo)