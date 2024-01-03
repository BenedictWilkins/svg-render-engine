if __name__ == "__main__":
    from svgrenderengine.pygame import PygameView

    def handle_events(events):
        for event in events:
            print(f"Handling event: {event}")

    game = PygameView(event_callback=handle_events)
    game.run()
