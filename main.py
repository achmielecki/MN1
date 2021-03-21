import pandas as pandas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt


def ema_denomonator(alpha, n):
    sum = 1
    for i in range(1, n + 1):
        sum += pow((1 - alpha), i)
    return sum


def ema_numerator(alpha, n, i, data):
    sum = data[i]
    for k in range(1, n + 1):
        sum += (pow((1 - alpha), k) * data[i - k])
    return sum


def ema(n, i, data):
    alpha = 2 / (n + 1)
    denominator = ema_denomonator(alpha, n)
    numerator = ema_numerator(alpha, n, i, data)
    return numerator / denominator


def macd(data):
    result = []
    start = 26
    for i, entry in enumerate(data[start:], start=start):
        result.append(ema(12, i, data) - ema(26, i, data))
    return result


def moving_average9(i, macd):
    sum = 0
    for k in range(0, 9):
        sum += macd[i - k]
    return sum / 9


def signal(macd):
    result = []
    start = 26
    for i, entry in enumerate(macd[start:], start=start):
        result.append(moving_average9(i, macd))
    return result


def buy_crosses(signal, macd, dates):
    cross = []
    macd_is_lower = macd[0] < signal[0]
    for i in range(0, len(macd)):
        if macd_is_lower:
            if macd[i] > signal[i]:
                cross.append(dates[i])
                macd_is_lower = False
        else:
            if macd[i] < signal[i]:
                macd_is_lower = True
    return cross


def sell_crosses(signal, macd, dates):
    cross = []
    macd_is_higher = macd[0] > signal[0]
    for i in range(0, len(macd)):
        if macd_is_higher:
            if macd[i] < signal[i]:
                cross.append(dates[i])
                macd_is_higher = False
        else:
            if macd[i] > signal[i]:
                macd_is_higher = True
    return cross


def play(start_capital, buy_cross, sell_cross, days, prices):
    capital = start_capital
    stocks = 0
    for i, day in enumerate(days):
        if day in buy_cross:
            stocks += capital/prices[i]
            capital = 0
            print("bought ", stocks, " stocks for", stocks*prices[i], " on day", day)
        if day in sell_cross:
            capital += prices[i]*stocks
            stocks = 0
            print("sold ", capital/prices[i], " stocks for", capital, " on day", day)
    capital += stocks * prices[-1]
    return capital


def calculate_macd_indicator(data):
    offset1 = 52
    offset2 = 26
    m = macd(data.Otwarcie)
    s = signal(m)
    days = [dt.datetime.strptime(d, '%Y-%m-%d').date() for d in data.Data]
    buy_cross = buy_crosses(s, m[offset2:], days[offset1:])
    sell_cross = sell_crosses(s, m[offset2:], days[offset1:])
    earnings = play(1000, buy_cross, sell_cross, days[offset1:], data.Otwarcie[offset1:].tolist())

    plot_for_macd(days[offset1:], m[offset2:], s, buy_cross, sell_cross)
    plot_for_macd_without_lines(days[offset1:], m[offset2:], s)
    plot_for_price(data, days)
    plot_for_price_with_lines(data, days, buy_cross, sell_cross)
    return earnings


def plot_for_price_with_lines(data, days, buy_cross, sell_cross):
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=360))
    plt.plot(days, data.Otwarcie, color='red', label='price', linewidth=1)
    for xc in buy_cross:
        plt.axvline(x=xc, color='green', linewidth='1')
    for xc in sell_cross:
        plt.axvline(x=xc, color='red', linewidth='1')
    plt.title('Wig20 price', fontsize=14)
    plt.xlabel('dni', fontsize=14)
    plt.ylabel('cena', fontsize=14)
    plt.grid(True)
    plt.legend(loc='lower left')
    plt.savefig('result/price_chart_with_lines.png', dpi=1440)
    plt.show()


def plot_for_price(data, days):
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=360))
    plt.plot(days, data.Otwarcie, color='red', label='price', linewidth=1)
    plt.title('Wig20 price', fontsize=14)
    plt.xlabel('dni', fontsize=14)
    plt.ylabel('cena', fontsize=14)
    plt.grid(True)
    plt.legend(loc='lower left')
    plt.savefig('result/price_chart.png', dpi=1440)
    plt.show()


def plot_for_macd(days, m, s, buy_cross, sell_cross):
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=360))
    plt.plot(days, m, color='red', label='macd', linewidth=1)
    plt.plot(days, s, color='blue', label='signal', linewidth=1)
    for xc in buy_cross:
        plt.axvline(x=xc, color='green', linewidth='1')
    for xc in sell_cross:
        plt.axvline(x=xc, color='red', linewidth='1')
    plt.title('Standard macd for Wig20', fontsize=14)
    plt.xlabel('dni', fontsize=14)
    plt.ylabel('macd', fontsize=14)
    plt.grid(True)
    plt.legend(loc='lower left');
    plt.savefig('result/macd_chart.png', dpi=1440)
    plt.show()


def plot_for_macd_without_lines(days, m, s):
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=360))
    plt.plot(days, m, color='red', label='macd', linewidth=1)
    plt.plot(days, s, color='blue', label='signal', linewidth=1)
    plt.title('Standard macd for Wig20', fontsize=14)
    plt.xlabel('dni', fontsize=14)
    plt.ylabel('macd', fontsize=14)
    plt.grid(True)
    plt.legend(loc='lower left');
    plt.savefig('result/macd_chart.png', dpi=1440)
    plt.show()


file = pandas.read_csv("data/wig20.csv")
res = calculate_macd_indicator(file)
print(res)
