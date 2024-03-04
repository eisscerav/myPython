from strsimpy.levenshtein import Levenshtein
from strsimpy.normalized_levenshtein import NormalizedLevenshtein
from strsimpy.jaro_winkler import JaroWinkler

str1 = "I may be a good boy"
str2 = "I'm not a good boy"
str3 = "I may be a good boy"


def print_sepline():
    print("#"*30)


def jaro():
    print("Using JaroWinkler")
    jarowinkler = JaroWinkler()
    print(jarowinkler.similarity(str1, str2))
    print(jarowinkler.similarity(str1, str3))
    print_sepline()
    return


def norm_leven():
    print("Using NormalizedLevenshtein")
    normalized_levenshtein = NormalizedLevenshtein()
    print(normalized_levenshtein.distance(str1, str2))
    print(normalized_levenshtein.distance(str1, str3))
    print_sepline()
    return


def main():
    norm_leven()
    jaro()
    return


if __name__ == "__main__":
    main()
