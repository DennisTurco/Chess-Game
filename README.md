![icon](https://user-images.githubusercontent.com/57963761/230503459-79155b02-d96e-4964-96c4-c4b9cef30872.png)

# Chess Game

This is a chess game made with python.

## Overview
### Demo

### Screenshots

![Capture1](https://user-images.githubusercontent.com/57963761/230503243-f7d41579-0b0d-40de-96f6-a5df39ea9648.PNG)

![Capture2](https://user-images.githubusercontent.com/57963761/230503247-59ca99c9-90ac-4245-aa7c-3facc848d99e.PNG)

---

## Tecnical info
* MainMenu created with: **[pygame-menu](https://pygame-menu.readthedocs.io/en/latest/_source/create_menu.html)**
* Game created with: **pygame**
* AI Engine: **[Stockfish](https://github.com/official-stockfish/Stockfish/)**
* AI ELO extended: **[Fairy-Stockfish](https://github.com/fairy-stockfish/Fairy-Stockfish)**

### Fairy-Stockfish ELO
| Skill Level | Estimated ELO  |
|-------------|----------------|
| -5          | ~400           |
| 0           | ~800           |
| 2           | ~1000          |
| 5           | ~1200          |
| 7           | ~1400          |
| 10          | ~1600          |
| 12          | ~1800          |
| 15          | ~2000          |
| 17          | ~2300          |
| 20          | ~2600+         |

### Notations used

#### 1. FEN (Forsyth–Edwards Notation)
```text
rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
```
Fields (from left to right):

1. Piece placement (8th rank to 1st rank)
2. Active color (w = White to move, b = Black)
3. Castling rights (KQkq = White can castle kingside/queenside, Black can too)
4. En passant target square (e.g., e3 or - if not available)
5. Halfmove clock (for 50-move rule)
6. Fullmove number (starts at 1, increments after each Black move)

Used for: saving board states, resuming games, setting up positions in engines or GUIs.

#### 2. UCI (Universal Chess Interface)
A communication protocol between chess engines and GUIs (graphical interfaces).
* Not a notation for people to read, but commands for software.
* Moves are in coordinate notation, such as:
```text
e2e4   (pawn moves from e2 to e4)
e7e8q  (pawn promotes to queen at e8)
```
* To set a position in the FEN notation

#### 3. SAN (Standard Algebraic Notation)
The standard move notation for humans.
Examples:
* e4 = pawn to e4
* Nf3 = knight to f3
* exd5 = pawn captures on d5
* O-O = kingside castling, O-O-O = queenside castling
* Qxe6+ = queen captures on e6 with check
* e8=Q = pawn promotes to queen on e8

---

## Licence

![https://img.shields.io/badge/License-MIT-green.svg](https://img.shields.io/badge/License-MIT-green.svg)

## Authors

- [@DennisTurco](https://www.github.com/DennisTurco)

## Support

For support, email: [dennisturco@gmail.com](mailto:dennisturco@gmail.com)
