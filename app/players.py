from sqlalchemy import select, exc
from sqlalchemy.orm import Session
from connection import engine
from models import Players

class PlayerMenu():
    options = ["Create player", "Show all available players", "Show player statistics", "Back"]
    length = len(options)

    def create_player():
        player_name = input("Enter player's name: ")
        with Session(engine) as session:
            stmt = select(Players).where(Players.name == player_name)
            ps = session.scalars(stmt).first()
        if ps == None:
            session.add(Players(name = player_name))
            session.commit()
            print("user created")
        else:
            print(f"Player '{player_name}' already exists")

    def get_all_players():
        with Session(engine) as session:
            stmt = select(Players)
            ps = session.scalars(stmt).all()
            for player in ps:
                print(player.name)

    def get_player(player_name = None):
        # Print player if no argument was passed to the function but return player otherwise
        check_player = True
        if player_name == None:
            player_name = input("Enter player's name: ")
            check_player = False

        with Session(engine) as session:
            stmt = select(Players).where(Players.name == player_name)
            ps = session.scalars(stmt).first()

            if ps == None:
                print(f"Player '{player_name}' does not exists")
                return None
            elif check_player == False:
                print(ps)
            else:
                return ps
    
    ## Hidden functions "update_player" and "delete_player"
    def update_player():
        player_name = input("Enter player's name: ")
        new_games_won = input("Enter games won: ")
        new_games_lost = input("Enter games lost: ")
        result = PlayerMenu.get_player(player_name)
        if result != None:
            with Session(engine) as session:
                stmt = select(Players).where(Players.name == player_name)
                ps = session.scalars(stmt).first()
                setattr(ps, "games_won", new_games_won)
                setattr(ps, "games_lost", new_games_lost)
                try:
                    session.commit()
                except exc.DataError as e:
                    print(f"A data error occurred: " + str(e).split("\n")[0])
                    print(str(e).split("\n")[1])
                    print(str(e).split("\n")[2])

    ## Does not delete existing games related to user. Should 'not' be used
    def delete_player():
        player_name = input("Enter player's name: ")
        result = PlayerMenu.get_player(player_name)
        if result != None:
            with Session(engine) as session:
                session.delete(result)
                session.commit()

            print("Player deleted")

    functions = [create_player, get_all_players, get_player]