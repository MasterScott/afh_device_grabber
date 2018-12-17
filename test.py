import requests
ua = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
}
print requests.get("https://androidfilehost.com/api/?action=devices&limit=1", headers=ua).content
