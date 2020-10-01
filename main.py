from src.sporting_tournament import RankingTable, print_table, matches_of, matches_of_date, all_teams


def main():
    seasons = ["2012/2013", "2013/2014", "2014/2015", "2015/2016", "2016/2017", "2017/2018", "2018/2019", "2019/2020"]
    print("Russian Premier League")

    while True:
        print("""\nChoose Season:
1 - 2012/2013, 2 - 2013/2014,
3 - 2014/2015, 4 - 2015/2016,
5 - 2016/2017, 6 - 2017/2018,
7 - 2018/2019, 8 - 2019/2020""")

        ind = input("Enter a number to make a choice, or press 'Return' to exit: ")
        if ind == "":
            break
        else:
            season = seasons[int(ind) - 1]

        while True:
            print("""Choose option:
1 - Show all matches of given team;
2 - Show matches played on a given date;
3 - Show the ranking table;""")

            action = input("Enter a number to make a choice, or press 'Return' to exit: ")

            if not action:
                break

            elif int(action) == 1:
                print("Choose a team:")
                all_teams(season)
                team = input("Enter a team: ")
                print_table(matches_of(team, season))

            elif int(action) == 2:
                date = input("\nEnter a date in day/month/year format: ")
                print_table(matches_of_date(date))

            elif int(action) == 3:
                table = RankingTable(season)
                print_table(table.rank())


if __name__ == '__main__':
    main()
