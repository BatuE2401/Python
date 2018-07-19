import ConnectFourRandomAI
import ConnectFourMinimaxAI

import ConnectFourEngine

if __name__ == '__main__':
    # Initialise the game engine
    # Modify these parameters to tweak the game
    app = ConnectFourEngine.ConnectFour(
            ai_delay = 2,
            red_player = ConnectFourRandomAI.AIcheck,
            blue_player = ConnectFourMinimaxAI.AIcheck,
            rewards = [ 0, 10, 50, 1000, 1000, 1000, 1000, 1000, 1000 ],
            winscore = 1000
            )
    # start the game engine
    app.game_loop()
