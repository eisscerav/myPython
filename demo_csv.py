import csv


def demo():
    csv_file = 'data/fifa_data.csv'
    with open(csv_file) as csv_fp:
        reader = csv.reader(csv_fp)
        for each in reader:
            # read each fow of csv as list
            print(each)
    print("done demo")


if __name__ == "__main__":
    demo()
