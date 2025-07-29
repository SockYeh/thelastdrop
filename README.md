# The Last Drop
![The Last Drop](https://github.com/SockYeh/thelastdrop/blob/main/thelastdrop/assets/title.png)
A stealth-based bottle collection game built with Pygame.

## Backstory

An alien from a poor family sets out on a journey to infiltrate a water factory to get water for his family.

## Features

- Animated character with sprite sheet
- Collect bottles scattered around the map
- Avoid rotating camera vision cones with shadows and outlines
- Dynamic menu screen with pulsating background and music
- Score tracking and respawn system

## How to Play

1. **Start the Game:**  
   When you launch, you'll see a menu screen with a pulsating background and a "Click Here to Start" button.  
   Click the button to begin playing.

2. **Controls:**

   - **Arrow keys / WASD:** Move character
   - **ESC:** Return to menu

3. **Objective:**
   - Collect all bottles on the map for points.
   - Avoid the colored camera cones—if you get caught, your score resets and bottles respawn.

## Installation

1. Install Python 3.x
2. Install Pygame:
   ```sh
   pip install pygame
   ```
3. Ensure all assets in `thelastdrop/assets/` are present.

## Running the Game

```sh
python thelastdrop/src/main.py
```

## License

MIT License. See [LICENSE](LICENSE) for details.
