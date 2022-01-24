# -*- coding: UTF-8 -*-
import pandas as pd
import os


def test1():
    lst1 = [
    "作死高手",
    "左手项羽右手刘邦",
    "左边的风声",
    "遵命！姑奶奶",
    "最新版西游记",
    "粽子来袭",
    "总统千金欧游记",]

    for each in lst1:
        if "高手" in each:
            print(each)


def test2():
    df = pd.read_csv(r'd:\test.csv', encoding='GBK')
    df = df.iloc[:, 0].dropna()
    df = df[df.duplicated(keep=False)]
    if not df.empty:
        print(df)
        no_dup = df.drop_duplicates()
        if os.path.exists(r"d:\dup.csv"):
            os.remove(r"d:\dup.csv")
        with open(r"d:\dup.csv", "w") as f:
            print(no_dup)
            no_dup.to_csv(f, encoding="GBK", index=False, line_terminator='\n')


def test3(file1=r"d:\a.csv", file2=r"d:\b.csv"):
    df1 = pd.read_csv(file1, encoding='GBK')
    df2 = pd.read_csv(file2, encoding='GBK')
    df1 = df1.drop_duplicates().dropna()
    df2 = df2.drop_duplicates().dropna()
    df = df1.append(df2)
    # pick out all dup items
    df = df[df.duplicated(keep=False)]
    if not df.empty:
        no_dup = df.drop_duplicates()
        with open(r"d:\dup.csv", "w") as f:
            print(no_dup)
            no_dup.to_csv(f, encoding="GBK", index=False)


if __name__ == "__main__":
    test2()
