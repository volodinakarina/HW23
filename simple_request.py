import requests

url = "http://127.0.0.1:5000/perform_query"

queries = {
    'queries': [
        {
            'cmd': 'filter',
            'value': 'POST'
        },
        {
            'cmd': 'map',
            'value': 'st'
        },
        {
            'cmd': 'unique',
            'value': ''
        }
    ],
    'file_name': 'apache_logs.txt',
}

response = requests.request("POST", url, json=queries)
print(response.text)