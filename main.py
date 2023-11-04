import random
import math
import matplotlib.pyplot as plt

# f(x) = 0.2*x(1/2) + 2*sin(2*pi*0.02x)+5
# x >= 0 x <= 255

# Funkcja generuje chromosomy i oblicza dla nich wartość funkcji,
# Zwraca dwie tablice:
# pierwsza to tablica chromosomów,
# druga to tablica wyników wartości funkcji poszczególnego chromosomu
def generate_chromosoms():
    chromosoms = []
    wartosc_funkcji = []
    check_number = []

    for i in range(10):
        x = random.randint(0, 256)
        while x in check_number:
            x = random.randint(0, 256)
        check_number.append(x)

        w_funkcji = 0.2 * pow(x, 0.5) + 2 * math.sin(2 * math.pi * 0.02 * x) + 5
        wartosc_funkcji.append(round(w_funkcji, 3))

        curr_chromosom = format(x, '#010b').removeprefix('0b')
        chromosoms.append(curr_chromosom)

    return chromosoms, wartosc_funkcji

# Funkcja wyświetla poszczególny chromosom, wartość funkcji oraz jego wskaźnik przystosowania
def show_result(ch, dec_values, wsk_przystosowania):
    print("Chromosom | Wartosc funkcji | Wskaznik przystosowania")
    for i in range(len(ch)):
        print(ch[i], "  " ,dec_values[i], "           " , wsk_przystosowania[i])

# Funkcja oblicza wskaznik przystosowania pojedynczego chromosomu w procentach
def wskaznik_przystosowania(wartosc_funkcji):
    result = []
    suma = sum(wartosc_funkcji)
    for number in wartosc_funkcji:
        result.append(round((number/suma)*100, 3))

    return result

# def show_decimal():
#     chromosoms = generate_chromosoms()
#     sum_of_chromosoms = 0
#
#     for chromosom in chromosoms:

def show_plot(chromosoms, wskazniki, procents):
    colors = [plt.cm.viridis(random.random()) for _ in range(len(chromosoms))]
    plt.figure(figsize=(14, 8))
    plt.pie(procents, labels=chromosoms, colors=colors, autopct='%1.3f%%', startangle=140)
    plt.legend(chromosoms, title="Chromosomy", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.axis('equal')
    plt.title("Procentowy udział chromosomów\n\n")
    plt.show()

def select_parents(chromosoms, wskazniki):
    temp = []
    rodzice = {}

    suma_prob = sum(wskazniki)
    zaokraglona_suma_prob = round(suma_prob, 2)

    while len(temp) < 2:
        losowy_punkt = random.uniform(0, zaokraglona_suma_prob)
        suma_prob = 0
        for i in range(len(chromosoms)):
            suma_prob += wskazniki[i]
            if suma_prob >= losowy_punkt:
                chromosom = chromosoms[i]
                temp.append(chromosom)
                rodzice[chromosom] = rodzice.get(chromosom, 0) + 1

    wybrane_chromosomy = list(rodzice.keys())
    return wybrane_chromosomy, rodzice


def krzyzowanie(chromosoms, pula_rodzicielska):
    pk = 0.75
    wsk_krzyzowania = [random.uniform(0, 1) for _ in range(len(pula_rodzicielska))]

    for i in range(0, len(pula_rodzicielska), 2):
        rodzic1 = pula_rodzicielska[i]
        rodzic2 = pula_rodzicielska[i + 1]

        if wsk_krzyzowania[i] < pk:
            punkt_krzyzowania = random.randint(1, len(rodzic1) - 1)
            dziecko1 = rodzic1[:punkt_krzyzowania] + rodzic2[punkt_krzyzowania:]
            dziecko2 = rodzic2[:punkt_krzyzowania] + rodzic1[punkt_krzyzowania:]

        else:
            dziecko1 = rodzic1
            dziecko2 = rodzic2

        chromosoms[chromosoms.index(rodzic1)] = dziecko1
        chromosoms[chromosoms.index(rodzic2)] = dziecko2

    print(chromosoms)


def mutacja(pula_rodzicielska):
    pass


def main():
    # Generowanie chromosomow i obliczenie wartosci funkcji
    chromosomy, wskazniki = generate_chromosoms()

    # Obliczenie wskaznika przystosowania
    procents = wskaznik_przystosowania(wskazniki)

    show_result(chromosomy, wskazniki, procents)

    # Wykres kolowy
    # show_plot(chromosomy, wskazniki, procents)

    print("------------------------------------------------------")

    # Wybor chromosomow na zasadzie koła ruletki
    print("Wybrane chromosomy na zasadzie koła ruletki: ")

    pula_rodzicielska, chroms_z_licznikiem = select_parents(chromosomy, wskazniki)
    print(chroms_z_licznikiem)
    print(pula_rodzicielska)
    krzyzowanie(chromosomy, pula_rodzicielska)


main()
