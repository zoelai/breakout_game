"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao

YOUR DESCRIPTION HERE
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmousemoved
import random


BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 16      # Height of a brick (in pixels).
BRICK_ROWS = 10       # Number of rows of bricks.
BRICK_COLS = 10    # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10      # Radius of the ball (in pixels).
PADDLE_WIDTH = 120      # Width of the paddle (in pixels).75
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).

INITIAL_Y_SPEED = 7  # Initial vertical speed for the ball.
MAX_X_SPEED = 7      # Maximum initial horizontal speed for the ball.

count = 0  # the number that the powered ball bounces a paddle
bricks_removed = 0
power = False
once_green = True


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
        self.window.filled = True

        # brick_rows and brick_cols
        self.brick_rows = brick_rows
        self.brick_cols = brick_cols

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height, x=(window_width - paddle_width)/2, y=window_height - paddle_offset)
        self.paddle.color = 'black'
        self.paddle.filled = True
        self.paddle.fill_color = 'black'
        self.window.add(self.paddle)

        # Create a shrunk paddle
        self.shrunk_paddle = GRect(self.window.width * 0.5, paddle_height, x=(window_width - paddle_width) / 2,
                            y=window_height - paddle_offset)
        self.shrunk_paddle.color = 'green'
        self.shrunk_paddle.filled = True
        self.shrunk_paddle.fill_color = 'green'

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

        # power_rectangle
        self.power_rect = GRect(15, 15)
        self.power_rect.color = 'salmon'
        self.power_rect.filled = True
        self.power_rect.fill_color = 'salmon'

        # power_shrink
        self.power_shrink = GRect(15, 15)
        self.power_shrink.color = 'green'
        self.power_shrink.filled = True
        self.power_shrink.fill_color = 'green'

        # Draw bricks
        a = 0
        b = 0
        for i in range(brick_rows):
            for j in range(brick_cols):
                self.brick = GRect(brick_width, brick_height, x=a, y=brick_offset+b)
                a += brick_width + brick_spacing
                self.window.add(self.brick)
                if i % 10 == 0 or i % 10 == 1:
                    self.brick.filled = True
                    self.brick.color = 'midnightblue'
                    self.brick.fill_color = 'midnightblue'
                elif i % 10 == 2 or i % 10 == 3:
                    self.brick.filled = True
                    self.brick.color = 'steelblue'
                    self.brick.fill_color = 'steelblue'
                elif i % 10 == 4 or i % 10 == 5:
                    self.brick.filled = True
                    self.brick.color = 'cornflowerblue'
                    self.brick.fill_color = 'cornflowerblue'
                elif i % 10 == 6 or i % 10 == 7:
                    self.brick.filled = True
                    self.brick.color = 'skyblue'
                    self.brick.fill_color = 'skyblue'
                else:
                    self.brick.filled = True
                    self.brick.color = 'powderblue'
                    self.brick.fill_color = 'powderblue'
            a = 0
            b += brick_height + brick_spacing

            # hearts
            self.heart1 = GLabel('\u2764\uFE0F')
            self.heart2 = GLabel('\u2764\uFE0F')
            self.heart3 = GLabel('\u2764\uFE0F')

            # score_board
            self.score_board = GLabel('Score: ', x=0, y=self.window.height-10)
            self.score_board.font = '-20'
            self.score_board.font = 'Courier-18'
            self.score_board.color = 'darkblue'
            self.window.add(self.score_board)

            # power_label
            self.power_label = GLabel('POWER UP!', x=self.window.width/2 - 100, y=370)
            self.power_label.color = 'salmon'
            self.power_label.font = '-40'

    def reset_ball_position(self):
        """
        This method resets ball velocity and position and negates power when the player loses.
        """
        # negates power
        global power
        power = False
        self.window.remove(self.shrunk_paddle)
        self.window.add(self.paddle)
        self.ball.color = 'black'
        self.ball.fill_color = 'black'

        # reset position and velocity
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

    # moves paddle horizontally
    def paddle_hor(self, e):
        """
        This method links the position of the paddle to that of the mouse
        """
        if e.x - self.paddle.width/2 < 0:
            self.paddle.x = self.paddle.x/2
        elif e.x + self.paddle.width/2 > self.window.width:
            self.paddle.x = self.window.width - self.paddle.width
        else:
            self.paddle.x = e.x - self.paddle.width/2

        if e.x - self.shrunk_paddle.width/2 < 0:
            self.shrunk_paddle.x = self.shrunk_paddle.x/2
        elif e.x + self.shrunk_paddle.width/2 > self.window.width:
            self.shrunk_paddle.x = self.window.width - self.shrunk_paddle.width
        else:
            self.shrunk_paddle.x = e.x - self.shrunk_paddle.width/2

    # bounce off on window sides
    def change_dir(self):
        """
        This method changes the direction of the ball when ball bounces against window sides
        """
        if self.ball.x + self.__dx <= 0:
            self.__dx = -self.__dx
        elif self.ball.x + self.ball.width + self.__dx >= self.window.width:
            self.__dx = -self.__dx
        elif self.ball.y + self.__dy <= 0:
            self.__dy = -self.__dy

    def ball_touches_object(self):
        """
        This method checks if the ball touches any object
        """
        global bricks_removed, power
        maybe_obj_1 = self.window.get_object_at(self.ball.x, self.ball.y)
        maybe_obj_2 = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y)
        maybe_obj_3 = self.window.get_object_at(self.ball.x + self.ball.width, self.ball.y + self.ball.height)
        maybe_obj_4 = self.window.get_object_at(self.ball.x, self.ball.y + self.ball.height)
        if maybe_obj_1 is not None:   # has an object
            if maybe_obj_1 is not self.paddle:
                if maybe_obj_1 is not self.shrunk_paddle:
                    if maybe_obj_1 is not self.heart1:
                        if maybe_obj_1 is not self.heart2:
                            if maybe_obj_1 is not self.heart3:
                                if maybe_obj_1 is not self.power_rect:
                                    if maybe_obj_1 is not self.power_label:
                                        if maybe_obj_1 is not self.power_shrink:
                                            if maybe_obj_1 is not self.score_board:
                                                self.window.remove(maybe_obj_1)
                                                bricks_removed += 1
                                                if not power:
                                                    self.bounce_off_brick()
                                                self.update_score()
                                else:
                                    self.window.remove(self.power_rect)
                                    self.window.add(self.power_label)
                                    self.ball.color = 'red'
                                    self.ball.fill_color = 'red'
                                    power = True
                else:
                    self.bounce_off_shrunk_paddle()
            else:
                self.bounce_off_paddle()

        elif maybe_obj_2 is not None:
            if maybe_obj_2 is not self.paddle:
                if maybe_obj_2 is not self.shrunk_paddle:
                    if maybe_obj_2 is not self.heart1:
                        if maybe_obj_2 is not self.heart2:
                            if maybe_obj_2 is not self.heart3:
                                if maybe_obj_2 is not self.power_rect:
                                    if maybe_obj_2 is not self.power_label:
                                        if maybe_obj_2 is not self.power_shrink:
                                            if maybe_obj_2 is not self.score_board:
                                                self.window.remove(maybe_obj_2)
                                                bricks_removed += 1
                                                if not power:
                                                    self.bounce_off_brick()
                                                self.update_score()
                                else:
                                    self.window.remove(self.power_rect)
                                    self.window.add(self.power_label)
                                    self.ball.color = 'red'
                                    self.ball.fill_color = 'red'
                                    power = True
                else:
                    self.bounce_off_shrunk_paddle()
            else:
                self.bounce_off_paddle()

        elif maybe_obj_3 is not None:
            if maybe_obj_3 is not self.paddle:
                if maybe_obj_3 is not self.shrunk_paddle:
                    if maybe_obj_3 is not self.heart1:
                        if maybe_obj_3 is not self.heart2:
                            if maybe_obj_3 is not self.heart3:
                                if maybe_obj_3 is not self.power_rect:
                                    if maybe_obj_3 is not self.power_label:
                                        if maybe_obj_3 is not self.power_shrink:
                                            if maybe_obj_3 is not self.score_board:
                                                # bricks
                                                self.window.remove(maybe_obj_3)
                                                bricks_removed += 1
                                                if not power:
                                                    self.bounce_off_brick()
                                                self.update_score()
                                else:
                                    self.window.remove(self.power_rect)
                                    self.window.add(self.power_label)
                                    self.ball.color = 'red'
                                    self.ball.fill_color = 'red'
                                    power = True
                else:
                    self.bounce_off_shrunk_paddle()
            else:
                self.bounce_off_paddle()
        elif maybe_obj_4 is not None:
            if maybe_obj_4 is not self.paddle:
                if maybe_obj_4 is not self.shrunk_paddle:
                    if maybe_obj_4 is not self.heart1:
                        if maybe_obj_4 is not self.heart2:
                            if maybe_obj_4 is not self.heart3:
                                if maybe_obj_4 is not self.power_rect:
                                    if maybe_obj_4 is not self.power_label:
                                        if maybe_obj_4 is not self.power_shrink:
                                            if maybe_obj_4 is not self.score_board:
                                                self.window.remove(maybe_obj_4)
                                                bricks_removed += 1
                                                if not power:
                                                    self.bounce_off_brick()
                                                self.update_score()
                                else:
                                    self.window.remove(self.power_rect)
                                    self.window.add(self.power_label)
                                    self.ball.color = 'red'
                                    self.ball.fill_color = 'red'
                                    power = True
                else:
                    self.bounce_off_shrunk_paddle()
            else:
                self.bounce_off_paddle()
        else:
            pass

    def paddle_touches_green_power(self):
        """
        This method changes the original paddle to the green paddle when green power is in effect
        """
        global once_green
        if once_green:
            if self.window.height - PADDLE_OFFSET >= self.power_shrink.y + self.power_shrink.height >= self.window.height - PADDLE_OFFSET - self.paddle.height\
             and self.shrunk_paddle.x <= self.power_shrink.x <= self.shrunk_paddle.x + self.shrunk_paddle.width:
                self.window.remove(self.power_shrink)
                self.window.remove(self.paddle)
                self.window.add(self.shrunk_paddle)
                once_green = False

    def heart_update(self, missed):
        """
        This method updates the number of hearts left on the top left
        """
        if missed == 0:  # never missed:
            self.window.add(self.heart1, x=0, y=20)
            self.window.add(self.heart2, x=20, y=20)
            self.window.add(self.heart3, x=40, y=20)
        elif missed == 1:  # missed once:
            self.window.remove(self.heart3)
        elif missed == 2:
            self.window.remove(self.heart2)
        else:
            self.window.remove(self.heart1)

    def bricks_all_cleared(self):
        """
        This method checks if all the bricks are cleared
        """
        global bricks_removed
        if bricks_removed == self.brick_cols * self.brick_rows:
            return True

    def winner(self):
        """
        This method displays the winner banner when the player wins
        """
        winner = GLabel('You Won!', x=self.window.width / 2 - 30, y=self.window.height / 2)
        winner.font = '-80'
        winner.font = 'Courier-18'
        self.window.remove(self.ball)
        self.window.remove(self.paddle)
        self.window.add(winner)

    def bounce_off_paddle(self):
        """
        This method controls the velocity of the ball when bounced against the paddle
        """
        global count, power

        # controls interval of red power
        if power:
            count += 1
        if count >= 4:
            self.ball.fill_color = 'black'
            self.ball.color = 'black'
            power = False

        # if paddle is bounced, power_label disappears
        self.window.remove(self.power_label)

        # bounce off paddle
        if self.ball.y + self.ball.height + self.__dy >= self.window.height - PADDLE_OFFSET - self.paddle.height or \
           self.ball.x + self.ball.width + self.__dx >= self.paddle.x or self.ball.x + self.__dx <= self.paddle.x + self.paddle.width:  # adjust vibration on paddle
            position = self.ball.x
            self.window.remove(self.ball)
            self.window.add(self.ball, x=position, y=self.window.height - PADDLE_OFFSET - self.paddle.height - 2 * self.ball_r)
        self.__dx = random.randint(-MAX_X_SPEED, MAX_X_SPEED)
        self.__dy = -self.__dy

    def bounce_off_shrunk_paddle(self):
        """
        This method controls the velocity of the ball when bounced against the shrunk paddle
        """
        global count, power

        # controls interval of red power
        if power:
            count += 1
        if count >= 5:
            self.ball.fill_color = 'black'
            self.ball.color = 'black'
            power = False

        # if paddle is bounced, power_label disappears
        self.window.remove(self.power_label)

        # bounce off shrunk paddle
        if self.ball.y + self.ball.height + self.__dy >= self.window.height - PADDLE_OFFSET - self.shrunk_paddle.height or \
                self.ball.x + self.ball.width + self.__dx >= self.shrunk_paddle.x or self.ball.x + self.__dx <= self.shrunk_paddle.x + self.shrunk_paddle.width:  # adjust vibration on paddle
            position = self.ball.x
            self.window.remove(self.ball)
            self.window.add(self.ball, x=position,
                            y=self.window.height - PADDLE_OFFSET - self.shrunk_paddle.height - 2 * self.ball_r)
        self.__dx = random.randint(-MAX_X_SPEED, MAX_X_SPEED)
        self.__dy = -self.__dy

    def bounce_off_brick(self):
        """
        This method bounces off ball from bricks and reveals red/green powers
        """
        global bricks_removed
        self.__dx = random.randint(-MAX_X_SPEED, MAX_X_SPEED)
        self.__dy = -self.__dy

        # green power reveals
        if bricks_removed == 7:
            self.power_shrink.x = self.ball.x
            self.power_shrink.y = self.ball.y - 15
            self.window.add(self.power_shrink)

        # red power reveals
        if bricks_removed == 15:
            self.power_rect.x = self.ball.x
            self.power_rect.y = self.ball.y - 15
            self.window.add(self.power_rect)

    def loser(self):
        """
        This method displays loser banner when the player loses
        """
        loser = GLabel('You Lost!', x=self.window.width / 2 - 55, y=self.window.height / 2)
        loser.font = '-50'
        loser.font = 'Courier-18'
        self.window.remove(self.ball)
        self.window.remove(self.paddle)
        self.window.add(loser)

    def update_score(self):
        global bricks_removed
        if bricks_removed <= self.brick_rows * self.brick_cols:
            self.score_board.text = 'Score: ' + str(bricks_removed)


if __name__ == 'breakoutgraphics_extension':
    print('Thanks for using breakoutgraphics_extension')