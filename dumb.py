lines = [
    "Show a collection of links to content such as documents, images, videos, and more in a variety of layouts with options for icons, images, and audience targeting.",
    "Quick links",
    "View & Download the Guiding Principles below.",
    "Guiding Principles",
    "指导原则",
    "Principes directeurs",
    "asdfasdf",
    "id-123123-uuid",
    "helloworldisthisreallyuseful",
    "hello thisasdf asdfa asdfa",
    "hello asljksdfasdfasdfa",
    "asfd fasd asdf"
]

THRESH = 3

def get_eng_dict():
    import urllib.request
    data = urllib.request.urlopen("https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words")
    lines = {}
    for line in data:
        l = line.decode('utf8').lower().strip()
        lines[l] = l
    return lines

def detect_with_naive_eng_only(line, eng_dict):
    words = line.split(" ")
    c = 0
    for word in words:
        if word.lower() in eng_dict:
            c = c + 1


    # tweak the THRESH to capture more/less translation candidates
    return c > (len(words) / THRESH)


def main():
    eng_dict = get_eng_dict()
    for line in lines:
        should_translate = detect_with_naive_eng_only(line, eng_dict)
        if should_translate:
            print(f"✅ {line}")
        else:
            print(f"❌ {line}")


main()
