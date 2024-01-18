words = [
    "Show a collection of links to content such as documents, images, videos, and more in a variety of layouts with options for icons, images, and audience targeting.",
    "Quick links",
    "View & Download the Guiding Principles below.",
    "Guiding Principles",
    "指导原则",
    "Principes directeurs",
    "asdfasdf",
    "id-123123-uuid",
    "helloworldisthisreallyuseful"
]

from langdetect import detect
from iso639 import Lang
from iso639.exceptions import InvalidLanguageValue
import json

def detect_language_with_langid(line):
    from py3langid.langid import LanguageIdentifier, MODEL_FILE
    identifier = LanguageIdentifier.from_pickled_model(MODEL_FILE, norm_probs=True)
    lang, prob = identifier.classify(line)
    return lang, prob


# langid will return a language and confidence value between 0 and 1
# 0 => not confident
# 1 => very confident
# tweak this to be more or less selective with text considered for translation
MIN_TRANSLATION_THRESHOLD = 0.5


def get_eng_dict():
    import urllib.request
    data = urllib.request.urlopen("https://gist.githubusercontent.com/wchargin/8927565/raw/d9783627c731268fb2935a731a618aa8e95cf465/words")
    lines = {}
    for line in data:
        l = line.decode('utf8').lower().strip()
        lines[l] = l
    return lines

eng_dict = get_eng_dict()

# def walk(data, detecter):
#     for k in data:
#         if type(data[k]) is str:
#             [lang, confidence] = detecter(data[k]) 
#             if confidence > MIN_TRANSLATION_THRESHOLD:
#                 print(f"✅ Identified: {data[k]} in {lang} with {confidence} confidence")
#             else:
#                 print(f"❌ Skipping {data[k]} in {lang} due to low confidence {confidence}")
#         elif type(data[k]) is dict:
#             walk(data[k], detecter)
#         elif type(data[k]) is list:
#             print(f"{k} is list")
#             for item in data[k]:
#                 walk(item, detecter)
#     return out

# def detect_with_langid():
#     f = open("data.json")
#     corpus = json.load(f)
#     walk(corpus, detect_language_with_langid)

def detect_with_naive_eng_only(line):
    words = line.split(" ")
    c = 0
    for word in words:
        if word.lower() in eng_dict:
            c = c + 1

    if c > len(words) / 3:
        return ["en", 1]
    else:
        return ["en", 0]


# def short_list():
#     print("detect_language_with_langid")
#     for word in words:
#         [lang, conf] = detect_language_with_langid(word)
#         e = "✅" if conf > MIN_TRANSLATION_THRESHOLD else "❌"
#         print(f"{e} {word}. Lang: {lang}. Conf: {conf}\n") 
# 
#     print("naive")
#     for word in words:
#         [lang, conf] = detect_with_naive(word)
#         e = "✅" if conf > MIN_TRANSLATION_THRESHOLD else "❌"
#         print(f"{e} {word}. Lang: {lang}. Conf: {conf}\n") 

def do_bench(detector, label, expected):
    print(f"\nBenchmarking {label}()")
    score = 0
    expectedtotal = 0
    missed = []
    for k in expected:
        res = detector(k)
        if expected[k] is True:
            expectedtotal = expectedtotal + 1
            if res[1] > MIN_TRANSLATION_THRESHOLD:
                score = score + 1
            else:
                # unlucky, error
                missed.append(k)

    print(f"Score: {score} / {expectedtotal}")
    print("Missed:", ",".join(missed))


def bench():
    dataset = open("expect.json")
    corpus = json.load(dataset)
    do_bench(detect_language_with_langid, "detect_language_with_langid", corpus)
    do_bench(detect_with_naive_eng_only, "detect_with_naive", corpus)

def main():
    # short_list()
    bench()

main()

def other():
    for word in words:
        try:
            lang = Lang(detect(word))
            print(f"Detecting for {word} -> {lang.name}")
        except InvalidLanguageValue as e:
            # just skip it for now
            pass

