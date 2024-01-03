if __name__ == "__main__":
    from svgrenderengine.pygame import PygameSVGEngine

    def handle_key_events(events):
        # Handle key events here
        for event in events:
            print(f"Handling event: {event}")

    game = PygameSVGEngine(event_callback=handle_key_events)
    game.run()
