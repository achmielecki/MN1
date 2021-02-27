import pandas as pandas
import matplotlib.pyplot as plt


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


def calculate_macd_indicator(data):
    m = macd(data)
    s = signal(m)
    x1 = list(range(1, len(m)+1))

    plt.plot(x1, m, color='red')
    plt.title('Standard macd for Wig20', fontsize=14)
    plt.xlabel('dni', fontsize=14)
    plt.ylabel('macd', fontsize=14)
    plt.grid(True)
    plt.savefig('result/chart.png', dpi=300)
    plt.show()
    return []


file = pandas.read_csv("data/wig20.csv")
res = calculate_macd_indicator(file.Otwarcie)
print(res)
#TODO testy jednostkowe na funkcje macd() i signal
#TODO wlasny wskaznik