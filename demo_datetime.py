from datetime import datetime


def demo():
    now = datetime.now()
    microsecond = now.microsecond
    stamp = now.timestamp()
    print('done demo')


if __name__ == '__main__':
    today = datetime.now().date()
    if today.month == 1:
        last_month = 12
    else:
        last_month = today.month-1
    last_month_date = str(last_month)+"/"+str(today.day)+"/"+str(today.year)
    demo()
