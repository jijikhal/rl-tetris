from random import choice, randint, seed
import cv2
import numpy as np

EMPTY = 0
PIECE = 1
MOVING = 2

DO_NOTHING = 0
MOVE_RIGHT = 1
MOVE_LEFT = 2
ROTATE_CW = 3
ROTATE_CCW = 4

Piece = list[tuple[int, int]]
PIECES: list[Piece] = [
    [(0,0), (0, 1), (0, 2), (0, -1)], # I
    [(0,0), (0, 1), (1, 0), (1, 1)], # square
    [(0,0), (0, 1), (0, 2), (1, 0)], #L
    [(0,0), (0, 1), (0, 2), (-1, 0)], #J
    [(0,0), (0, 1), (1, 0), (1, -1)], #S
    [(0,0), (0, 1), (-1, 0), (-1, -1)], #Z
    [(0,0), (0, 1), (1, 0), (-1, 0)] #T
]

def rotate_cw(piece: Piece) -> Piece:
    new_p: Piece = []
    for x, y in piece:
        new_p.append((y, -x))
    return new_p

def rotate_ccw(piece: Piece) -> Piece:
    new_p: Piece = []
    for x, y in piece:
        new_p.append((-y, x))
    return new_p

class Tetris:
    def __init__(self):
        self.board = [[EMPTY for _ in range(10)] for _ in range(20)]
        self.score = 0
        self.piece: Piece = choice(PIECES)
        self.pos: tuple[int, int] = (4, 0)

    def reset(self):
        self.board = [[EMPTY for _ in range(10)] for _ in range(20)]
        self.score = 0
        self.piece = choice(PIECES)
        self.pos = (4, 0)

    def move(self, dir: tuple[int, int], piece: Piece) -> bool:
        dx, dy = dir
        x_pos, y_pos = self.pos
        for x, y in piece:
            ry = y+y_pos+dy
            rx = x+x_pos+dx
            if (ry >= 20 or rx < 0 or rx >= 10 or (ry >= 0 and self.board[ry][rx] != EMPTY)):
                return False
        
        self.piece = piece
        self.pos = (x_pos+dx, y_pos+dy)
        return True
    
    def move_down(self) -> bool:
        if self.move((0, 1), self.piece):
            return True
        
        x_pos, y_pos = self.pos
        for x, y in self.piece:

            ry = y+y_pos
            rx = x+x_pos
            if (ry < 0):
                return False
            else:
                self.board[ry][rx] = PIECE

        self.pos = (4, 0)
        self.piece = choice(PIECES)

        return True
    

    def clear_lines(self):
        to_clear: list[int] = []
        for i in range(19, -1, -1):
            if all([True if x == PIECE else False for x in self.board[i]]):
                to_clear.append(i)

        for i in to_clear:
            self.board.pop(i)

        for i in to_clear:
            self.board.insert(0, [EMPTY for _ in range(10)])

        if len(to_clear) > 0:
            return 2*len(to_clear)-1
        return 0

    def step(self, action: int) -> bool:
        if action == DO_NOTHING:
            pass
        elif action == MOVE_RIGHT:
            self.move((1, 0), self.piece)
        elif action == MOVE_LEFT:
            self.move((-1, 0), self.piece)
        elif action == ROTATE_CW:
            self.move((0, 0), rotate_cw(self.piece))
        elif action == ROTATE_CCW:
            self.move((0, 0), rotate_ccw(self.piece))

        if not self.move_down():
            return False
        self.score += self.clear_lines()
        return True

    def draw(self):
        field = np.zeros((400, 200), dtype=np.uint8)
        field = field + 255
        for row in range(len(self.board)):
            for c in range(len(self.board[row])):
                value = self.board[row][c]
                if value == EMPTY:
                    cv2.rectangle(field, (c*20, row*20), ((c+1)*20, (row+1)*20), (0,), 1)
                else:
                    cv2.rectangle(field, (c*20, row*20), ((c+1)*20, (row+1)*20), (0,), -1)

        x_pos, y_pos = self.pos
        for x, y in self.piece:

            row = y+y_pos
            c = x+x_pos
            if (row < 0):
                continue
            else:
                cv2.rectangle(field, (c*20, row*20), ((c+1)*20, (row+1)*20), (128,), -1)
    
        cv2.imshow("lol", field)
        if (cv2.waitKey(10) == ord("q")):
            exit(0)


if __name__ == "__main__":
    seed(2)
    t = Tetris()
    result = True
    while(result):
        action = int(input())
        print(action)
        result = t.step(action)
        t.draw()