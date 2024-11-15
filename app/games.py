from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from connection import engine
from models import Players, Games, Rounds
from players import PlayerMenu
from utils import run_until_num_entered, is_number
from collections import defaultdict

class GameMenu():
    options = ["Add new game", "Show all games", "Check game statistics", "Remove game", "Back"]
    length = len(options)

    def add_game():
        # Check if winner exists
        input_winner = input("Enter winner's name: ")
        result = PlayerMenu.get_player(input_winner)
        if result == None:
            print("Game not added")
        else:
            # Make sure players of the current game exist
            while True:
                incorrect_player = False
                players = input("Enter players separated by a comma: \n")
                parsed_players = players.replace(" ", "").split(",")
                for player in parsed_players:
                    result = PlayerMenu.get_player(player)
                    if result == None:
                        print("Please enter players that exist on the database")
                        print("")
                        incorrect_player = True
                        break
                if incorrect_player:
                    continue
                elif input_winner not in parsed_players:
                    print("'Winner' not listed in the entered players")
                else:
                    break

            # Create game
            new_game = Games(winner = input_winner)
            with Session(engine) as session:
                session.add(new_game)
                session.commit()
                session.refresh(new_game)
                
            print(f"Game added with id {new_game.id}\n")

            # Add rounds to game
            for current_player in parsed_players:

                # Prompt for number of rounds and points from each round
                n_of_rounds = 0
                while n_of_rounds <= 0:
                    n_of_rounds = run_until_num_entered(f"How many rounds did '{current_player}' play?: ")
                    if n_of_rounds <= 0:
                        print("Amount of rounds must be bigger than 0")

                for round in range(int(n_of_rounds)):
                    points_per_round = run_until_num_entered(f"Enter points made on the round {round + 1}: ")
                    new_round = Rounds(
                        round_number = round + 1,
                        game_id = new_game.id,
                        player = current_player,
                        points = int(points_per_round)
                    )
            
                    with Session(engine) as session:
                        session.add(new_round)
                        session.commit()
                
                # Add wins and loses to each player
                with Session(engine) as session:
                    stmt = select(Players).where(Players.name == current_player)
                    ps = session.scalars(stmt).first()
                    if current_player == input_winner:
                        setattr(ps, "games_won", ps.games_won + 1)
                    else:    
                        setattr(ps, "games_lost", ps.games_lost + 1)
                    session.commit()

    def show_all_games():
        with Session(engine) as session:
            stmt = select(Games)
            ps = session.scalars(stmt).all()
            for game in ps:
                print(game)
            print("")

    def get_game():
        # Check if game exists and print the game
        game_id = input("Enter game's id: ")
        with Session(engine) as session:
            stmt = select(Games).where(Games.id == game_id)
            ps = session.scalars(stmt).first()

            if ps == None:
                print(f"Game '{game_id}' does not exists")
                return None
            else:
                print(ps)

            # Print rounds
            stmt_rounds = select(Rounds).where(Rounds.game_id == ps.id)
            ps_rounds = session.scalars(stmt_rounds).all()
            list_of_rounds = []
            for round in ps_rounds:
                list_of_rounds.append(round.return_dict())
            
            grouped = defaultdict(list)
            for round in list_of_rounds:
                for key, value in round.items():
                    grouped[key].append({key: value})

            for key, player_and_points in grouped.items():
                print(f"Round {key}:")
                for values in player_and_points:
                    print(values[key])

    def remove_game():
        # Check input data and that the game exists
        game_id = input("Enter game's id: ")
        test = is_number(game_id)
        if test == False:
            print("Game id entered is not an integer")
        else:
            with Session(engine) as session:
                stmt = select(Games).where(Games.id == game_id)
                ps = session.scalars(stmt).first()

                if ps == None:
                    print(f"Game '{game_id}' does not exists")
                    return None
                else:
                    # Retrieve players
                    stmt_retrieve_players = select(Rounds.player).where(Rounds.game_id == game_id)
                    ps_retrieve_players = session.scalars(stmt_retrieve_players).all()
                    unique_players_list = list(set(ps_retrieve_players))
                    
                    # Modify games_won and games_lost accordingly to each player
                    for current_player in unique_players_list:
                        stmt_update_player = select(Players).where(Players.name == current_player)
                        ps_update_player = session.scalars(stmt_update_player).first()
                        if current_player == ps.winner:
                            setattr(ps_update_player, "games_won", ps_update_player.games_won - 1)
                        else:    
                            setattr(ps_update_player, "games_lost", ps_update_player.games_lost - 1)
                    
                    # Delete first the rounds related to game, then the game itself
                    stmt_rounds_delete = delete(Rounds).where(Rounds.game_id == game_id)
                    session.execute(stmt_rounds_delete)
                    session.delete(ps)
                    session.commit()
                    print("Game removed")

    functions = [add_game, show_all_games, get_game, remove_game]