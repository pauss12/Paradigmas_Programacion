from requests import get

def main():

    print(get("http://www.utad.com").text)

main()