import pygame
import sys
import random
from pygame.locals import *  # udostępnienie wszystkich nazw metod z locals

# inicjacja modułu pygame
pygame.init()

# przygotowanie powierzchni do rysowania, czyli inicjacja okna gry
# inicjalizujemy okno gry o rozmiarach 150x150 pikseli i 32 bitowej głębi kolorów.
OKNOGRY = pygame.display.set_mode((150, 150), 0, 32)

# tytuł okna gry
pygame.display.set_caption('Kółko i krzyżyk')

# lista opisująca stan pola gry, 0 - pole puste, 1 - gracz, 2 - komputer
POLE_GRY = [0, 0, 0,
            0, 0, 0,
            0, 0, 0]

# Zmienne określają, do kogo należy następny ruch, kto wygrał i czy nastąpił koniec gry.
RUCH = 1  # do kogo należy ruch: 1 – gracz, 2 – komputer
WYGRANY = 0  # wynik gry: 0 - nikt, 1 - gracz, 2 - komputer, 3 - remis
WYGRANA = False

# rysowanie planszy gry, czyli linii oddzielających pola
# funkcja wykorzystuje zagnieżdżone pętle, rysuje 9 kwadratów o białym obramowaniu # i szerokości 50 pikseli (są to obiekty Rect zwracane przez metodę draw.rect())

def rysuj_plansze():
    for i in range(0, 3):  # x
        for j in range(0, 3):  # y
            # argumenty: powierzchnia, kolor, x,y, w,h, grubość linii
            pygame.draw.rect(OKNOGRY, (255, 255, 255),
                             Rect((j * 50, i * 50), (50, 50)), 1)


#  funkcja rysuje w zależności od stanu planszy gry zapisanego w liście
# POLE_GRY kółka niebieskie lub czerwone za pomocą metody pygame.draw.circle().

def rysuj_pole_gry():
    for i in range(0, 3):
        for j in range(0, 3):
            pole = i * 3 + j  # zmienna pole przyjmuje wartości od 0-8
            # x i y określają środki kolejnych pól,
            # a więc: 25,25, 25,75 25,125 75,25 itd.
            x = j * 50 + 25
            y = i * 50 + 25

            if POLE_GRY[pole] == 1:
                # rysuj kółko gracza
                pygame.draw.circle(OKNOGRY, (0, 0, 255), (x, y), 10)
            elif POLE_GRY[pole] == 2:
                # rysuj kółko komputera
                pygame.draw.circle(OKNOGRY, (255, 0, 0), (x, y), 10)


# postaw kółko lub… kółko
# zadaniem jest zapisanie w POLU_GRY pod otrzymanym indeksem wartości symbolizującej znak komputera (czyli 2) oraz nadanie i zwrócenie zmiennej RUCH wskazującej na gracza (wartość 1).

def postaw_znak(pole, RUCH):
    if POLE_GRY[pole] == 0:
        if RUCH == 1:  # ruch gracza
            POLE_GRY[pole] = 1
            return 2
        elif RUCH == 2:  # ruch komputera
            POLE_GRY[pole] = 2
            return 1

    return RUCH


# funkcja pomocnicza sprawdzająca, czy komputer może wygrać, czy powinien
# blokować gracza, czy może wygrał komputer lub gracz


def sprawdz_pola(uklad, wygrany=None):
    wartosc = None
    # lista wielowymiarowa, której elementami są inne listy zagnieżdżone
    # są to układy dla których następuje wygrana
    POLA_INDEKSY = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # indeksy pól w poziomie
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # indeksy pól w pionie
        [0, 4, 8], [2, 4, 6]  # indeksy pól na skos
    ]

    # Pętla pobiera kolejne listy, tworzy w liście pomocniczej trójkę wartości odczytanych z POLA_GRY i próbuje ją dopasować do przekazanego jako argument układu wygrywającego lub blokującego. Jeżeli znajdzie dopasowanie zwraca liczbę oznaczającą gracza lub komputer, o ile opcjonalny argument WYGRANY ma wartość inną niż None, w przeciwnym razie zwracany jest indeks POLA_GRY, na którym komputer powinien postawić swój znak.

    for lista in POLA_INDEKSY:
        kol = []  # lista pomocnicza
        for ind in lista:
            kol.append(POLE_GRY[ind])  # zapisz wartość odczytaną z POLE_GRY
        if (kol in uklad):  # jeżeli znalazłeś układ wygrywający lub blokujący
            # zwróć wygranego (1,2) lub indeks pola do zaznaczenia
            wartosc = wygrany if wygrany else lista[kol.index(0)]

    return wartosc


# funkcja która odpowiada za ruchy komputera

def ai_ruch(RUCH):
    pole = None  # które pole powinien zaznaczyć komputer

    # listy wielowymiarowe, których elementami są inne listy zagnieżdżone
    # zawierają układy wartości, dla których komputer wygrywa oraz które powinien
    # zablokować, aby nie wygrał gracz
    uklady_wygrywam = [[2, 2, 0], [2, 0, 2], [0, 2, 2]]
    uklady_blokuje = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]

    # sprawdź, czy komputer może wygrać
    pole = sprawdz_pola(uklady_wygrywam)

    # Jeżeli indeks zwrócony przez funkcję sprawdz_pola() jest inny niż None,
    # przekazywany jest do funkcji postaw_znak()
    if pole is not None:
        return postaw_znak(pole, RUCH)

    # jeżeli komputer nie może wygrać, blokuj gracza
    pole = sprawdz_pola(uklady_blokuje)
    if pole is not None:
        return postaw_znak(pole, RUCH)

    # jeżeli nie można wygrać i gracza nie trzeba blokować, wylosuj pole
    # O ile na planszy nie ma układu wygrywającego lub nie ma konieczności blokowania gracza, komputer w pętli losuje przypadkowe pole (random.randrange(0,9)), dopóki nie znajdzie pustego, i przekazuje jego indeks do funkcji postaw_znak().

    while pole is None:
        pos = random.randrange(0, 9)  # wylosuj wartość od 0 do 8
        if POLE_GRY[pos] == 0:
            pole = pos

    return postaw_znak(pole, RUCH)

# sprawdzamy kto wygrał,

def kto_wygral():
    # układy wygrywające dla gracza i komputera
    uklad_gracz = [[1, 1, 1]]
    uklad_komp = [[2, 2, 2]]

    WYGRANY = sprawdz_pola(uklad_gracz, 1)  # czy wygrał gracz?
    if not WYGRANY:  # jeżeli gracz nie wygrywa
        WYGRANY = sprawdz_pola(uklad_komp, 2)  # czy wygrał komputer?

    # sprawdź remis
    if 0 not in POLE_GRY and WYGRANY not in [1, 2]:
        WYGRANY = 3

    # zwracamy wartość wygranego (1,2,3) lub None, o ile możliwe są kolejne ruchy
    return WYGRANY


# funkcja wyświetlająca komunikat końcowy

def drukuj_wynik(WYGRANY):
    # tworzy obiekt czcionki z podanego pliku
    fontObj = pygame.font.Font('freesansbold.ttf', 16)
    if WYGRANY == 1:
        tekst = u'Wygrał gracz!'
    elif WYGRANY == 2:
        tekst = u'Wygrał komputer!'
    elif WYGRANY == 3:
        tekst = 'Remis!'

    # renderuje nowy obrazek z odpowiednim tekstem
    tekst_obr = fontObj.render(tekst, True, (20, 255, 20))
    # pobiera powierzchnię prostokątną obiektu
    tekst_prost = tekst_obr.get_rect()
    # pozycjonowanie obiektu
    tekst_prost.center = (75, 75)
    # rysuje w oknie gry
    OKNOGRY.blit(tekst_obr, tekst_prost)


# pętla główna programu

while True:

    # W obrębie głównej pętli programu pętla for odczytuje kolejne zdarzenia zwracane przez metodę pygame.event.get(). Innymi słowami jest to obsługa zdarzeń generowanych przez gracza

    for event in pygame.event.get():
        # przechwytujemy zamknięcie okna czyli zamkniecie aplikacji
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # sprawdzamy czy nikt nie wygrał (zmienna WYGRANA ma wartość False)
        if WYGRANA is False:
            # jeżeli kolej na ruch gracza (zmienna RUCH ma wartość 1)
            if RUCH == 1:
                # przechwytujemy wydarzenie MOUSEBUTTONDOWN, tj. kliknięcie myszą.
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:  # jeżeli naciśnięto 1. przycisk
                        mouseX, mouseY = event.pos  # pobieramy współrzędne kursora
                        # wylicz indeks klikniętego pola
                        pole = (int(mouseY / 50) * 3) + int(mouseX / 50)
                        # wywołujemy omówioną wcześniej funkcję postaw_znak().
                        RUCH = postaw_znak(pole, RUCH)
            # Jeżeli kolej na komputer to uruchamiamy (ai_ruch())
            elif RUCH == 2:
                RUCH = ai_ruch(RUCH)
            # Po wykonaniu ruchu sprawdzamy, czy ktoś nie wygrał
            WYGRANY = kto_wygral()
            if WYGRANY is not None:
                WYGRANA = True

    OKNOGRY.fill((0, 0, 0))  # definicja koloru powierzchni w RGB
    rysuj_plansze()
    rysuj_pole_gry()
    if WYGRANA:
        drukuj_wynik(WYGRANY)
    pygame.display.update()  # funkcja aktualizuje obraz na ekranie



