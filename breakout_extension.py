"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao.

This program is the breakout game extension.
"""

from campy.gui.events.timer import pause
from breakoutgraphics_extension import BreakoutGraphics
from campy.gui.events.mouse import onmouseclicked

FRAME_RATE = 1000 / 120  # 120 frames per second
NUM_LIVES = 3  # Number of attempts

# global variables
click = 0
missed = 0
setup = BreakoutGraphics()
permission = True


def main():
    """
    This function waits for the user to click on the mouse and sets up heart status
    """
    global missed
    onmouseclicked(start_ball)
    setup.heart_update(missed)


def start_ball(e):
    """
    This function initiates the graphics of the game
    """
    global click, missed, setup, permission
    if permission and click < NUM_LIVES:
        click += 1
        permission = False
        while True:
            pause(FRAME_RATE)
            setup.ball.move(setup.get_dx(), setup.get_dy())
            setup.power_shrink.move(0, 2)
            setup.ball_touches_object()
            setup.paddle_touches_green_power()
            if setup.ball.x <= 0 or setup.ball.x + setup.ball.width >= setup.window.width or setup.ball.y <= 0:
                setup.change_dir()
            if setup.ball.y + setup.ball.height >= setup.window.height:  # missed
                missed += 1
                setup.heart_update(missed)
                setup.reset_ball_position()
                if click == 3:
                    setup.loser()
                break
            if setup.bricks_all_cleared():
                setup.winner()
                break
        permission = True

if __name__ == '__main__':
    main()
