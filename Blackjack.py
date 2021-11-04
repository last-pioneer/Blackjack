# IMPORT STATEMENTS AND VARIABLE DECLARATIONS:
"""
Моя вторая программа (несамостоятельная, с подсказками)

"""
import random

suits = ('Червы', 'Бубны', 'Пики', 'Трефы')
ranks = (
    'Двойка', 'Тройка', 'Четвёрка', 'Пятерка', 'Шестёрка', 'Семёрка', 'Восьмёрка', 'Девятка', 'Десятка', 'Валет',
    'Дама', 'Король', 'Туз')
values = {'Двойка': 2, 'Тройка': 3, 'Четвёрка': 4, 'Пятерка': 5, 'Шестёрка': 6, 'Семёрка': 7, 'Восьмёрка': 8,
          'Девятка': 9, 'Десятка': 10, 'Валет': 10, 'Дама': 10, 'Король': 10, 'Туз': 11}

playing = True


# CLASS DEFINITIONS:

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + ' - ' + self.suit


class Deck:

    def __init__(self):
        self.deck = []  # start with an empty list (начинаем с пустого списка)
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))  # создаём объекты Card и добавляем их в список

    def __str__(self):
        deck_comp = ''  # start with an empty string (начинаем с пустой строки)
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()  # add each Card object's print string
            # (добавляем строку print для каждого объекта Card)
        return 'В колоде есть:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:

    def __init__(self):
        self.cards = []  # начинаем с пустого списка, так же как и в классе Deck
        self.value = 0  # начинаем со значения 0
        self.aces = 0  # добавляем атрибут, чтобы учитывать тузы

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Туз':
            self.aces += 1  # увеличиваем значение self.aces

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    def __init__(self):
        self.total = 1000  # можно установить значение по умолчанию, или запрашивать значение у пользователя
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet


# FUNCTION DEFINITIONS:

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input('Сколько фишек Вы хотите поставить? '))
        except ValueError:
            print('Извините, ставка должна  быть числом!')
        else:
            if chips.bet > chips.total:
                print("Извините, Ваша ставка не должна превышать ", chips.total)
            else:
                break


def hit(deck, hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()


def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input(
            "Вы хотите взять дополнительную карту (h - Hit) или остаться при текущих "
            "картах (s - Stand)? Введите 'h' или 's' ")

        if x[0].lower() == 'h':
            hit(deck, hand)  # определённая выше функция hit()

        elif x[0].lower() == 's':
            print("Игрок остается при текущих картах. Ход дилера.")
            playing = False

        else:
            print("Извините, пожалуйста попробуйте снова.")
            continue
        break


def show_some(player, dealer):
    print("\nКарты Дилера:")
    print(" <карта скрыта>")
    print('', dealer.cards[1])
    print("\nКарты Игрока:", *player.cards, sep='\n ')


def show_all(player, dealer):
    print("\nКарты Дилера:", *dealer.cards, sep='\n ')
    print("Карты Дилера =", dealer.value)
    print("\nКарты Игрока:", *player.cards, sep='\n ')
    print("Карты Игрока =", player.value)


def player_busts(player, dealer, chips):
    print("Игрок превысил 21!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("Игрок выиграл!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("Дилер превысил 21!")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("Дилер выиграл!")
    chips.lose_bet()


def push(player, dealer):
    print("Ничья!.")


# GAMEPLAY!

while True:
    print('Добро пожаловать в игру Блекджэк! Постарайтесь приблизиться к сумме 21 как можно ближе, не превышая её!\n\
    Дилер берёт дополнительные карты до тех пор, пока не получит сумму больше 17. Туз считается как 1 или 11.')

    # Create & shuffle the deck, deal two cards to each player
    # Создаём и перемешиваем колоду карт, выдаём каждому Игроку по две карты
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Set up the Player's chips (Установите количество фишек Игрока)
    player_chips = Chips()  # remember the default value is 100 (помните, значение по умолчанию равно 100)

    # Prompt the Player for their bet: (Спросите у Игрока его ставку)
    take_bet(player_chips)

    # Show the cards: (Покажите карты (но оставьте одну и карт Дилера скрытой))
    show_some(player_hand, dealer_hand)

    while playing:  # recall this variable from our hit_or_stand function
        # (помните, это переменная из нашей функции hit_or_stand)

        # Prompt for Player to Hit or Stand
        # (Спросите Игрока, хочет ли он взять дополнительную карту или остаться при текущих картах)
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)  # Покажите карты (но оставьте одну и карт Дилера скрытой)

        if player_hand.value > 21:  # Если карты Игрока превысили 21, запустите player_busts() и выйдите из цикла (break)
            player_busts(player_hand, dealer_hand, player_chips)
            break

    # If Player hasn't busted, play Dealer's hand
    # Если карты Игрока не превысили 21, перейдите к картам Дилера и берите доп. карты до суммы карт >=17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards (Показываем все карты)
        show_all(player_hand, dealer_hand)

        # Test different winning scenarios (Выполняем различные варианты завершения игры)
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)

        else:
            push(player_hand, dealer_hand)

    # Inform Player of their chips total (Сообщить Игроку сумму его фишек)
    print("\nСумма фишек Игрока - ", player_chips.total)

    # Ask to play again (Спросить его, хочет ли он сыграть снова)
    new_game = input("Хотите ли сыграть снова? Введите 'y' или 'n' ")
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Спасибо за игру!")
        break
