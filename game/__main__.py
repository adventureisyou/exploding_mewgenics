from .game import Game

def main():
  for _ in range(10000):
    game = Game([1,2])
    game.play()

if __name__ == "__main__":
    main()
