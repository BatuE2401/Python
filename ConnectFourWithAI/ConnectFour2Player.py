import ConnectFourEngine

if __name__ == '__main__':
    # Initialise the game engine
    # Modify these parameters to tweak the game
    app = ConnectFourEngine.ConnectFour(
            red_player = None,
            blue_player = None,
            )
    # start the game engine
    app.game_loop()
