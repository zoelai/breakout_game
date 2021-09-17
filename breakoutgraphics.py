"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao

This program is the breakout game.
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect
from campy.gui.events.mouse import onmousemoved
import random


BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10       # Number of rows of bricks.
BRICK_COLS = 7    # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 16      # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).75
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 5  # Initial vertical speed for the ball.
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball.

count = 2
bricks_removed = 0


class BreakoutGraphics:
    def __init__(self, ball_radius=BALL_RADIUS, paddle_width = PADDLE_WIDTH,
                 paddle_height = PADDLE_HEIGHT, paddle_offset = PADDLE_OFFSET,
                 brick_rows = BRICK_ROWS, brick_cols = BRICK_COLS,
                 brick_width = BRICK_WIDTH, brick_height = BRICK_HEIGHT,
                 brick_offset = BRICK_OFFSET, brick_spacing = BRICK_SPACING,
                 title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height, x=(window_width - paddle_width)/2, y=window_height - paddle_offset)
        self.paddle.color = 'black'
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.window.add(self.paddle)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius*2, ball_radius*2, x=(window_width-ball_radius)/2, y=(window_height-ball_radius)/2)
        self.ball.filled = True
        self.ball.fill_color = 'black'
        self.window.add(self.ball)
        self.ball_r = ball_radius

        # Default initial velocity for the ball
        self.__dx = random.randint(-MAX_X_SPEED, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED
        if (random.random()) > 0.5:
            self.__dx = -1 * self.__dx

        # Initialize mouse
        onmousemoved(self.paddle_hor)

        #
        self.brick_rows = brick_rows
        self.brick_cols = brick_cols

        # Draw bricks
        a = 0
        b = 0
        for i in range(brick_rows):
            for j in range(brick_cols):
                self.brick = GRect(brick_width, brick_height, x=a, y=brick_offset+b)
                self.brick.color = 'black'
                a += brick_width + brick_spacing
                self.window.add(self.brick)
                if i % 10 == 0 or i % 10 == 1:
                    self.brick.filled = True
                    self.brick.color = 'red'
                    self.brick.fill_color = 'red'
                elif i % 10 == 2 or i % 10 == 3:
                    self.brick.filled = True
                    self.brick.color = 'orange'
                    self.brick.fill_color = 'orange'
                elif i % 10 == 4 or i % 10 == 5:
                    self.brick.filled = True
                    self.brick.color = 'yellow'
                    self.brick.fill_color = 'yellow'
                elif i % 10 == 6 or i % 10 == 7:
                    self.brick.filled = True
                    self.brick.color = 'green'
                    self.brick.fill_color = 'green'
                else:
                    self.brick.filled = True
                    self.brick.color = 'blue'
                    self.brick.fill_color = 'blue'
            a = 0
            b += brick_height + brick_spacing

    def reset_ball_position(self):
        """
        This method resets the position and the velocity of the ball when player lost.
        """
        self.ball.x = (self.window.width - self.ball.width)/2
        self.ball.y = (self.window.height - self.ball.height)/2
        self.__dx = random.randint(-MAX_X_SPEED, MAX_X_SPEED)
        self.__dy = INITIAL_Y_SPEED

    # getter for dx
    def get_dx(self):
        return self.__dx

    # getter for dy
    def get_dy(self):
        return self.__dy

    def paddle_hor(self, e):
        """
        This method links the paddle position with mouse location
        """
        if e.x - self.paddle.width/2 < 0:
            self.paddle.x = self.paddle.x/2
        elif e.x + self.paddle.width/2 > self.window.width:
            self.paddle.x = self.window.width - self.paddle.width
        else:
            self.paddle.x = e.x - self.paddle.width/2

    def change_dir(self):  # bounce off on window sides
        if self.ball.x + self.__dx <= 0 or self.ball.x + self.ball.width + self.__dx >= self.window.width:
            self.__dx = -self.__dx
        if self.ball.y + self.__dy <= 0:
            self.__dy = -self.__dy

    def ball_touches_object(self):
        """
        This method checks for collision between the ball and the paddle or brick
        """
        global bricks_removed
        maybe_obj_1 = self.window.get_object_at(self.ball.x, self.ball.y)
        maybe_obj_2 = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y)
        maybe_obj_3 = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y + self.ball.height)
        maybe_obj_4 = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height)
        if maybe_obj_1 is not None:   # has an object
            if maybe_obj_1 is not self.paddle:
                self.window.remove(maybe_obj_1)
                self.bounce_off_brick()
                bricks_removed += 1
            else:
                self.bounce_off_paddle()
        elif maybe_obj_2 is not None:
            if maybe_obj_2 is not self.paddle:
                self.window.remove(maybe_obj_2)
                self.bounce_off_brick()
                bricks_removed += 1
            else:
                self.bounce_off_paddle()
        elif maybe_obj_3 is not None:
            if maybe_obj_3 is not self.paddle:
                self.window.remove(maybe_obj_3)
                self.bounce_off_brick()
                bricks_removed += 1
            else:
                self.bounce_off_paddle()
        elif maybe_obj_4 is not None:
            if maybe_obj_4 is not self.paddle:
                self.window.remove(maybe_obj_4)
                self.bounce_off_brick()
                bricks_removed += 1
            else:
                self.bounce_off_paddle()
        else:
            pass

    def bricks_all_cleared(self):
        """
        This method returns whether the player had the bricks all cleared
        """
        if bricks_removed == self.brick_rows * self.brick_cols:  # bricks were all hit
            return True

    def bounce_off_paddle(self):  # bounce off paddles
        """
        This method determines the velocity of the ball when it bounces against the paddle
        """
        if self.ball.y + self.ball.height + self.__dy >= self.window.height - PADDLE_OFFSET - self.brick.height or self.ball.x + self.ball.width + self.__dx >= self.brick.x or self.ball.x + self.__dx <= self.brick.x + self.brick.width:  # adjust vibration on paddle
            self.window.remove(self.ball)
            self.window.add(self.ball, x=self.ball.x, y=self.window.height - PADDLE_OFFSET - self.brick.height - self.ball.height)
        self.__dx = random.randint(-MAX_X_SPEED, MAX_X_SPEED)
        self.__dy = -self.__dy

    def bounce_off_brick(self):
        """
        This method determines the velocity of the ball when it bounces against a brick
        """
        self.__dx = random.randint(-MAX_X_SPEED, MAX_X_SPEED)
        self.__dy = -self.__dy


if __name__ == 'breakout':
    print('Thanks for using breakoutgraphics')