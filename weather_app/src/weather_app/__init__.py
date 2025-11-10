from requests import request


def get(url: str) -> str:
    return request("GET", url).text


print(get("https://wttr.in/?format=3"))
