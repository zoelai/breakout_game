"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

YOUR DESCRIPTION HERE
"""

from campy.gui.events.timer import pause
from breakoutgraphics import BreakoutGraphics
from campy.gui.events.mouse import onmouseclicked

FRAME_RATE = 1000 / 120  # 120 frames per second
NUM_LIVES = 3			 # Number of attempts

# global variables
click = 0
setup = BreakoutGraphics()
permission = True


def main():
    """
    This function waits for the user to click on mouse
    """
    onmouseclicked(start_ball)


def start_ball(e):
    """
    This function starts the ball and display graphics of the game
    """
    global click, permission
    if permission and click < NUM_LIVES:
        permission = False
        click += 1
        while True:
            setup.ball.move(setup.get_dx(), setup.get_dy())
            if setup.bricks_all_cleared():
                break
            if setup.ball_touches_object():
                pass
            if setup.ball.x <= 0 or setup.ball.x + setup.ball.width >= setup.window.width:
                setup.change_dir()
            if setup.ball.y <= 0:
                setup.change_dir()
                pass
            if setup.ball.y + setup.ball.height >= setup.window.height:  # miss
                setup.reset_ball_position()
                break
            pause(FRAME_RATE)
        permission = True
        


if __name__ == '__main__':
    main()
