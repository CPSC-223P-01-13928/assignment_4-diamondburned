from weather import Weather, read_data, write_data, report_daily, report_historical
from datetime import datetime

main_menu = """\
      *** TUFFY TITAN WEATHER LOGGER MAIN MENU")

1. Set data filename
2. Add weather data
3. Print daily report
4. Print historical report
9. Exit the program

"""

dbfile = "w.dat"
weather = read_data(filename=dbfile)


def assert_date(datestr: str) -> None:
    datetime.strptime(datestr, "%Y%m%d")


def assert_time(timestr: str) -> None:
    datetime.strptime(timestr, "%H%M%S")


while True:
    print(main_menu)
    mychoice = int(input("Enter menu choice: "))
    print()

    match mychoice:
        case 1:
            dbfile = input("Enter data filename: ")
            weather = read_data(filename=dbfile)

        case 2:
            date = input("Enter date (YYYYMMDD): ")
            assert_date(date)
            time = input("Enter time (hhmmss): ")
            assert_time(time)
            t = int(input("Enter temperature: "))
            h = int(input("Enter humidity: "))
            r = float(input("Enter rainfall: "))

            weather[date + time] = {"t": t, "h": h, "r": r}
            write_data(data=weather, filename=dbfile)

        case 3:
            date = input("Enter date (YYYYMMDD): ")
            print(report_daily(weather, date))

        case 4:
            print(report_historical(weather))

        case 9:
            break
