if __name__ == "__main__":
    from svgrenderengine.pygame import PygameView
    from svgrenderengine.event import ExitEvent

    game = PygameView()

    running = True
    while running:
        for event in game.step():
            print(event)
            if isinstance(event, ExitEvent):
                running = False
    game.close()
