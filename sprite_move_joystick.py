import arcade
import enum
import math
import os


class JoystickType(enum.Enum):
    move = 0
    teleport = 1
    circle = 2


DEBUG = 0
DEBUG_EX = 1

SPEED_TO_CENTER = 2.5

JOYSTICK_TYPE = JoystickType.circle

SPRITE_SCALING = 1
BASE_TRANSLATE = 37054

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "JoyStick IRZ"

HASH_LIST_JOYSTICK_LEN = 2
HASH_LIST_JOYSTICK_VALUE_X = [0.0]
HASH_LIST_JOYSTICK_VALUE_Y = [0.0]
HASH_LIST_JOYSTICK_FLAG = False

HASH_LIST_COORD_LEN = 20
HASH_LIST_COORD_VALUE_X = [0.0]
HASH_LIST_COORD_VALUE_Y = [0.0]
HASH_LIST_COORD_FLAG = False

START_MOVEMENT_SPEED = 50
MOVEMENT_SPEED = 50
DEAD_ZONE = 0.10

SCREEN_MIDDLE_X = SCREEN_WIDTH / 2
SCREEN_MIDDLE_Y = SCREEN_HEIGHT / 2


class Circle:
    def __init__(self):
        # d = math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2)
        # loge(d)
        # c = d/2
        # loge(c)
        self.r = SCREEN_WIDTH/4
        self.color = arcade.color.BUD_GREEN

    def update(self):
        pass

    def draw(self):
        arcade.draw_circle_filled(SCREEN_MIDDLE_X,
                                  SCREEN_MIDDLE_Y,
                                  self.r,
                                  self.color)


def log(info):
    global DEBUG
    if DEBUG == 1:
        print(info)


def loge(info):
    global DEBUG_EX
    if DEBUG_EX == 1:
        print(info)


class Button(enum.Enum):
    one = 0
    two = 1
    three = 2


NOW_COORD_X = 0
NOW_COORD_Y = 0


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class Player(arcade.Sprite):
    """ Player sprite """

    def __init__(self, filename, scale):
        super().__init__(filename, scale)

        # Get list of game controllers that are available
        joysticks = arcade.get_joysticks()

        # If we have any...
        if joysticks:
            # Grab the first one in  the list
            self.joystick = joysticks[0]

            # Open it for input
            self.joystick.open()

            # self.scale = IMG_SCALING

            # Push this object as a handler for joystick events.
            # Required for the on_joy* events to be called.
            self.joystick.push_handlers(self)
        else:
            # Handle if there are no joysticks.
            print("There are no joysticks, plug in a joystick and run again.")
            self.joystick = None

    def get_dist(self, x1, x2, y1, y2):
        return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

    def update(self):
        """ Move the player """

        global HASH_LIST_JOYSTICK_FLAG
        global HASH_LIST_JOYSTICK_VALUE_X
        global HASH_LIST_JOYSTICK_VALUE_Y
        global HASH_LIST_JOYSTICK_LEN

        global HASH_LIST_COORD_LEN
        global HASH_LIST_COORD_VALUE_X
        global HASH_LIST_COORD_VALUE_Y
        global HASH_LIST_COORD_FLAG

        global NOW_COORD_Y
        global NOW_COORD_X

        if (len(HASH_LIST_JOYSTICK_VALUE_X) > HASH_LIST_JOYSTICK_LEN
                and len(HASH_LIST_JOYSTICK_VALUE_Y) > HASH_LIST_JOYSTICK_LEN):
            HASH_LIST_JOYSTICK_VALUE_X.clear()
            HASH_LIST_JOYSTICK_VALUE_Y.clear()
            HASH_LIST_JOYSTICK_FLAG = False

        if (len(HASH_LIST_COORD_VALUE_X) > HASH_LIST_COORD_LEN
                and len(HASH_LIST_COORD_VALUE_Y) > HASH_LIST_COORD_LEN):
            HASH_LIST_COORD_VALUE_X.clear()
            HASH_LIST_COORD_VALUE_Y.clear()
            HASH_LIST_COORD_FLAG = False

        # If there is a joystick, grab the speed.
        if self.joystick:

            # x-axis
            log(f"joystick = x:{self.joystick.x} - y:{self.joystick.y}")
            HASH_LIST_JOYSTICK_VALUE_X.append(self.joystick.x)
            HASH_LIST_JOYSTICK_VALUE_Y.append(self.joystick.y)
            self.change_x = self.joystick.x
            # Set a "dead zone" to prevent drive from a centered joystick
            if abs(self.change_x) < DEAD_ZONE:
                self.change_x = 0

            # y-axis
            self.change_y = -self.joystick.y
            # Set a "dead zone" to prevent drive from a centered joystick
            if abs(self.change_y) < DEAD_ZONE:
                self.change_y = 0

            log(f"coords = x:{self.center_x} - y:{self.center_y}")
            HASH_LIST_COORD_VALUE_X.append(self.center_x)
            HASH_LIST_COORD_VALUE_Y.append(self.center_y)

        center_round_x = round(self.change_x, 2)
        center_round_y = round(self.change_y, 2)
        # Move the player
        if len(set(HASH_LIST_JOYSTICK_VALUE_X)) == 1 and len(set(HASH_LIST_JOYSTICK_VALUE_Y)) == 1 \
                and len(HASH_LIST_JOYSTICK_VALUE_X) == HASH_LIST_JOYSTICK_LEN and \
                len(HASH_LIST_JOYSTICK_VALUE_Y) == HASH_LIST_JOYSTICK_LEN:
            HASH_LIST_JOYSTICK_FLAG = True

        if len(set(HASH_LIST_COORD_VALUE_X)) == 1 and len(set(HASH_LIST_COORD_VALUE_Y)) == 1 \
                and len(HASH_LIST_COORD_VALUE_X) == HASH_LIST_COORD_LEN and \
                len(HASH_LIST_COORD_VALUE_Y) == HASH_LIST_COORD_LEN:
            HASH_LIST_COORD_FLAG = True

        if JOYSTICK_TYPE == JoystickType.teleport:

            if HASH_LIST_COORD_FLAG is True:
                self.center_x = SCREEN_MIDDLE_X
                self.center_y = SCREEN_MIDDLE_Y
            else:
                self.center_x += center_round_x * MOVEMENT_SPEED
                self.center_y -= center_round_y * MOVEMENT_SPEED
        elif JOYSTICK_TYPE == JoystickType.move:

            if HASH_LIST_JOYSTICK_FLAG:
                global SPEED_TO_CENTER
                if self.center_y + self.center_x != SCREEN_MIDDLE_Y + SCREEN_MIDDLE_X:
                    if self.center_y < SCREEN_MIDDLE_Y:
                        self.center_y += SPEED_TO_CENTER
                    else:
                        self.center_y -= SPEED_TO_CENTER

                    if self.center_y > SCREEN_MIDDLE_Y:
                        self.center_y -= SPEED_TO_CENTER
                    else:
                        self.center_y += SPEED_TO_CENTER

                    if self.center_x < SCREEN_MIDDLE_X:
                        self.center_x += SPEED_TO_CENTER
                    else:
                        self.center_x -= SPEED_TO_CENTER

                    if self.center_x > SCREEN_MIDDLE_X:
                        self.center_x -= SPEED_TO_CENTER
                    else:
                        self.center_x += SPEED_TO_CENTER
            else:
                self.center_x += center_round_x * MOVEMENT_SPEED
                self.center_y -= center_round_y * MOVEMENT_SPEED
        elif JOYSTICK_TYPE == JoystickType.circle:

            cofd = 1
            R = math.fabs(SCREEN_WIDTH/4)

            joyd_x = self.joystick.x * (BASE_TRANSLATE / 200) + SCREEN_MIDDLE_X
            joyd_y = self.joystick.y * (BASE_TRANSLATE / 200) + SCREEN_MIDDLE_Y
            scd_x = self.center_x - SCREEN_MIDDLE_X
            scd_y = self.center_y - SCREEN_MIDDLE_Y

            loge(f"joyd_x = {joyd_x}, joyd_y = {joyd_y}")
            self.center_x = joyd_x
            self.center_y = joyd_y

#            if self.left < SCREEN_WIDTH/4 - cofd:
#                self.left = SCREEN_WIDTH/4 - cofd
#
#            if self.right > SCREEN_WIDTH/2 + SCREEN_WIDTH/4 - cofd:
#                self.right = SCREEN_WIDTH/2 + SCREEN_WIDTH/4 - cofd
#
#            if self.bottom < SCREEN_HEIGHT/4 - cofd:
#                self.bottom = SCREEN_HEIGHT/4 - cofd
#
#            if self.top > SCREEN_HEIGHT/2 + SCREEN_HEIGHT/4 - cofd:
#                self.top = SCREEN_HEIGHT/2 + SCREEN_HEIGHT/4 - cofd

        NOW_COORD_Y = self.center_y
        NOW_COORD_X = self.center_x

        # Keep from moving off-screen
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

    # noinspection PyMethodMayBeStatic
    def on_joybutton_press(self, _joystick, button):
        """ Handle button-down event for the joystick """
        print("Button {} down".format(button))

    # noinspection PyMethodMayBeStatic
    def on_joybutton_release(self, _joystick, button):
        """ Handle button-up event for the joystick """
        print("Button {} up".format(button))

    # noinspection PyMethodMayBeStatic
    def on_joyhat_motion(self, _joystick, hat_x, hat_y):
        """ Handle hat events """
        print("Hat ({}, {})".format(hat_x, hat_y))


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Initializer
        """

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        self.center_figure = Circle()

        # Call the parent class initializer
        super().__init__(width, height, title)

        joysticks = arcade.get_joysticks()

        # If we have any...
        if joysticks:
            # Grab the first one in  the list
            self.joystick = joysticks[0]

            # Open it for input
            self.joystick.open()

            # self.scale = IMG_SCALING

            # Push this object as a handler for joystick events.
            # Required for the on_joy* events to be called.
            self.joystick.push_handlers(self)
        else:
            # Handle if there are no joysticks.
            log("There are no joysticks, plug in a joystick and run again.")
            self.joystick = None

        # Variables that will hold sprite lists
        self.player_list = None
        self.button1 = "OFF"
        self.button2 = "OFF"
        self.button3 = "OFF"

        # Set up the player info
        self.player_sprite = None

        #        self.set_mouse_cursor(False)
        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.player_lsi

        # Set up the player
        self.player_sprite = Player("img/pool_cue_ball.png",
                                    SPRITE_SCALING)
        self.player_sprite.set_position(SCREEN_MIDDLE_X, SCREEN_MIDDLE_Y)
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        self.clear()
        self.center_figure.draw()
        arcade.draw_line(SCREEN_MIDDLE_X/2,
                         SCREEN_MIDDLE_Y,
                         SCREEN_MIDDLE_X + SCREEN_MIDDLE_X/2,
                         SCREEN_HEIGHT/2,
                         arcade.color.AO,
                         2)
        arcade.draw_line(SCREEN_MIDDLE_X,
                         SCREEN_MIDDLE_Y/2,
                         SCREEN_MIDDLE_X,
                         SCREEN_MIDDLE_Y + SCREEN_MIDDLE_Y/2,
                         arcade.color.AO,
                         2)

        # Draw all the sprites.
        self.player_list.draw()
#        global MOVEMENT_SPEED
#        output_movement_speed = f"Speed: {MOVEMENT_SPEED}"
#        arcade.draw_text(text=output_movement_speed, start_x=10, start_y=20,
#                         color=arcade.color.WHITE, font_size=14)

        # output_shift = f"Shift[x:{round(self.player_sprite.change_x, 2)} y:{round(self.player_sprite.change_y, 2)}]"
        # arcade.draw_text(text=output_shift, start_x=600, start_y=20,
        #                  color=arcade.color.WHITE, font_size=14)
        global BASE_TRANSLATE
        output_x = f"X:{ math.ceil(self.joystick.x * BASE_TRANSLATE)}"
        output_y = f"Y:{ math.ceil(self.joystick.y * BASE_TRANSLATE)}"
        dy = SCREEN_HEIGHT - 30
        arcade.draw_text(text=output_x, start_x=10, start_y=dy,
                         color=arcade.color.WHITE, font_size=14)
        arcade.draw_text(text=output_y, start_x=10, start_y=dy - 30,
                         color=arcade.color.WHITE, font_size=14)

#        output_coords = f"Coord[x:{NOW_COORD_X} y:{NOW_COORD_Y}]"
#        arcade.draw_text(text=output_coords, start_x=570, start_y=20,
#                         color=arcade.color.WHITE, font_size=14)

        bx = 10
        by = dy - 60
        bdy = 30
        button1 = "Button 1:"
        button1_v = f"{self.button1}"
        self.draw_button_info(button1, button1_v, bx, by)

        button2 = "Button 2:"
        button2_v = f"{self.button2}"
        self.draw_button_info(button2, button2_v, bx, by - bdy)

        button3 = "Button 3:"
        button3_v = f"{self.button3}"
        self.draw_button_info(button3, button3_v, bx, by - bdy*2)

    def draw_button_info(self, button_text, button_value, x, y):
        arcade.draw_text(text=button_text, start_x=x, start_y=y,
                         color=arcade.color.WHITE, font_size=14)
        if button_value == "OFF":
            arcade.draw_text(text=button_value, start_x=x + 100, start_y=y,
                             color=arcade.color.RED, font_size=14)
        else:
            arcade.draw_text(text=button_value, start_x=x + 100, start_y=y,
                             color=arcade.color.GREEN, font_size=14)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.player_sprite.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_joybutton_press(self, _joystick, button):
        """ Handle button-down event for the joystick """
        log("He press on joybutton in menu")
        if button == Button.one.value:
            log("He press button1 in menu")
            self.button1 = "ON"
        elif button == Button.two.value:
            log("He press button2 in menu")
            self.button2 = "ON"
        elif button == Button.three.value:
            log("He press button3 in menu")
            self.button3 = "ON"

    def on_joybutton_release(self, _joystick, button):
        """ Handle button-up event for the joystick """
        log("He release on joybutton in menu")
        if button == Button.one.value:
            log("He release button1 in menu")
            self.button1 = "OFF"
        elif button == Button.two.value:
            log("He release button2 in menu")
            self.button2 = "OFF"
        elif button == Button.three.value:
            log("He release button3 in menu")
            self.button3 = "OFF"


def main():
    """ Main function """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
