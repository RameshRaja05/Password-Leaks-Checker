import requests
import hashlib
import sys


def response_api(pass_char):
    url = "https://api.pwnedpasswords.com/range/"+pass_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f"fetching has errors:please check your status code={res.status_code} and api")
    else:
        return res


def get_count_leaks(hashes, hashes_to_chk):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hashes_to_chk:
            return count
    return 0


def check_the_password(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first_five, remaining = sha1password[:5], sha1password[5:]
    response = response_api(first_five)
    return get_count_leaks(response, remaining)


def main(*args):
    for password in args:
        count = check_the_password(password)
        if count:
            print(f'{password} is not safe it founds in {count} times> you should change the password')
        else:
            print(f"{password} is safe keep carry on!")


if __name__ == "__main__":
    main(sys.argv[1:])
