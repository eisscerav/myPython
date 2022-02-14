# -*- coding: UTF-8 -*-
import pandas as pd
import re
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


def test4():
    df = pd.read_csv(r"nba.csv")
    columns = df.columns
    # read each column
    # col_by_name = df['Team']
    #  try df.Team to read column Team
    col_by_name = df.Name
    col1 = df['Name'][1:5]
    # read multiple columns
    col2 = df[['Name', 'Team', 'Age']]
    # read each row
    rows = df.iloc[1]
    rows = df.iloc[1:4]
    # read a specific location (row, col)
    element1 = df.iloc[1, 2]
    element2 = df.iloc[1:4, 2:5]
    print("df.iterrows()")
    for index, row in element2.iterrows():
        print(index, row)
    # conditional dataframe or filtering data
    element3 = df.loc[df['Age'] == 25]
    # sort dataframe  sort1 = df.sort_values('Age', ascending=False)
    # ascending by age and descending by team
    sort1 = df.sort_values(['Age', 'Team'], ascending=[1, 0])
    desc = df.describe()

    # make changes to data
    df['number+age'] = df['Number'] + df['Age']
    df_1 = df.drop(columns=['number+age'])
    df_1 = df[['Name', 'Age', 'Team']]
    # save modified df to csv by df.to_csv('new_name.csv') or to excel df.to_excel
    # df.to_csv('new_name.csv', index=False)
    filter_df1 = df.loc[(df['Age'] == 25) & (df['Position'] == 'SF')]

    # filtering data
    # filter_df1.reset_index(drop=True) to remove old index
    # filter_df1 = filter_df1.reset_index()
    # filter_df2 = df.loc[(df['Age'] == 25) | (df['Salary'] > 100000)]
    #  df.loc[~df['Name'].str.contains("ph", na=False)] here ~ meaning not
    # filter_df3 = df.loc[~df['Name'].str.contains("ph", na=False)]
    filter_df4 = df.loc[df['Name'].str.contains("ph|ev", na=False, regex=True, flags=re.I)]

    # conditional changes
    # change inplace
    # df.loc[df['Team'] == 'Brooklyn Nets', 'Team'] = 'Atom nets'
    # df.loc[df['Team'] == 'Brooklyn Nets', 'College'] = 'Asernal'
    # df.loc[df['Weight'] > 210, ['College', 'Salary']] = ['AAAAA', '10020']
    print(df.head(2))


if __name__ == "__main__":
    test4()
