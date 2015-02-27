from random import randrange
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from time import time

Base = declarative_base()


class Player(Base):
    __tablename__ = 'player'
    name = Column(String, primary_key=True)
    highscore = Column(Integer)

engine = create_engine("sqlite:///mathgame.db")
Base.metadata.create_all(engine)

session = Session(bind=engine)


def get_command():
    command = input(">>>")
    return command


def welcome_menu():
    print('Welcome to the \' do you even math \' game!')
    print("Here are your options:\n- start\n- highscore")
    return input('>>>')


def check_if_player_exists(name):
    global session
    player = session.query(Player).filter(Player.name == name).all()
    return player != []


def add_player(player_name):
    global session
    player = Player(name=player_name, highscore=0)
    session.add(player)
    session.commit()

# returns true or false depending on
# whether problem is correctly solved

def generate_problem():
    start_time = int(time())
    if randrange(2) == 0:
        operator = '+'
        a = randrange(11)
        b = randrange(11)
        expected_answer = a + b
    else:
        a = randrange(11)
        b = randrange(11)
        operator = '*'
        expected_answer = a * b
    answer = input('{} {} {} = ?\n'.format(a, operator, b))
    if int(time()) - start_time > 100:
        print("You ran out of time :(")
        return False
    return int(answer) == expected_answer

# returns score

def give_problem():
    question_number = 1
    while question_number > 0:
        print('Question #{}:'.format(question_number))
        if generate_problem():
            question_number += 1
            print("Correct!")
        else:
            print('Incorrect. your score is: {}'.format(
                (question_number - 1) ** 2))
            return (question_number - 1) ** 2

def print_highscores():
    global session
    highscores = session.query(Player).all()
    counter = 1
    info = []
    for item in highscores:
        info.append([(item.name), (item.highscore)])
        counter += 1
        if counter == 10:
            return 0
    info = sorted(info, key = lambda x: x[1], reverse = True)
    counter = 1
    for row in info:
        print('{}: {} - {} points'.format(counter, row[0], row[1]))
        counter += 1

def start():
    global session
    command = welcome_menu()
    if command == 'start':
        player_name = input('Enter your playername:\n')
        print('Welcome {}'.format(player_name))
        if not check_if_player_exists(player_name):
            add_player(player_name)  # create new player if name is not in db
        player = session.query(Player).filter(Player.name == player_name).one()
        highscore = give_problem()
        if highscore > player.highscore:
            player.highscore = highscore
            session.commit()
    elif command == 'highscore':
        print_highscores()


def main():
    start()

if __name__ == '__main__':
    main()
