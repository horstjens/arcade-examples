"""
Show how to have enemies shoot bullets aimed at the player.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_bullets_enemy_aims
"""

import arcade
import math
import os
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprites and Bullets Enemy Aims Example"
#BULLET_SPEED = 4


class Explosion(arcade.Sprite):
    """ This class creates an explosion animation """

    def __init__(self, texture_list):
        super().__init__()

        # Start at the first frame
        self.current_texture = 0
        self.textures = texture_list

    def update(self):

        # Update to the next frame of the animation. If we are at the end
        # of our frames, then delete this sprite.
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.set_texture(self.current_texture)
        else:
            self.remove_from_sprite_lists()



class Bullet(arcade.Sprite):
    
    def __init__(self, x, y, tx, ty):
        super().__init__(self)
        self.texture = arcade.load_texture(":resources:images/space_shooter/laserBlue01.png")
        self.center_x = x
        self.center_y = y
        x_diff = tx - x
        y_diff = ty - y
        angle = math.atan2(y_diff, x_diff)
        self.angle = math.degrees(angle)
        self.speed = random.random() * 7 + 0.1
        self.change_x = math.cos(angle) * self.speed #BULLET_SPEED
        self.change_y = math.sin(angle) * self.speed #BULLET_SPEED
        MyGame.bullet_list.append(self)
        
        
        
class MyGame(arcade.Window):
    """ Main application class """

    bullet_list = []#arcade.SpriteList()
    explosions_list = []

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        file_name = ":resources:images/spritesheets/explosion.png"
        self.explosion_texture_list = []
        columns = 16
        count = 60
        sprite_width = 256
        sprite_height = 256
        
        # Load the explosions from a sprite sheet
        self.explosion_texture_list = arcade.load_spritesheet(
               file_name, sprite_width, sprite_height, columns, count)
               
               

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        arcade.set_background_color(arcade.color.BLACK)

        self.frame_count = 0

        self.enemy_list = None
        #self.bullet_list = None
        self.player_list = None
        self.player = None

    def setup(self):
        self.hitpoints = 100
        self.enemy_list = arcade.SpriteList()
        MyGame.bullet_list = arcade.SpriteList()
        MyGame.explosions_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        

        # Add player ship
        self.player = arcade.Sprite(":resources:images/space_shooter/playerShip1_orange.png", 0.5)
        self.player_list.append(self.player)

        # Add top-left enemy ship
        enemy = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", 0.5)
        enemy.center_x = 120
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)
        
        # Add ground-left enemy ship
        enemy = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", 0.5)
        enemy.center_x = 120
        enemy.center_y = 0
        enemy.angle = 180
        self.enemy_list.append(enemy)
        
        # Add top-middle enemy ship
        enemy = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", 0.5)
        enemy.center_x = SCREEN_WIDTH //2
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)

        # Add top-right enemy ship
        enemy = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", 0.5)
        enemy.center_x = SCREEN_WIDTH - 120
        enemy.center_y = SCREEN_HEIGHT - enemy.height
        enemy.angle = 180
        self.enemy_list.append(enemy)
        
        # Add ground-right enemy ship
        enemy = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", 0.5)
        enemy.center_x = SCREEN_WIDTH - 120
        enemy.center_y = 0
        enemy.angle = 180
        self.enemy_list.append(enemy)


    def on_draw(self):
        """Render the screen. """

        arcade.start_render()

        self.enemy_list.draw()
        self.bullet_list.draw()
        self.player_list.draw()
        self.explosions_list.draw()

        arcade.draw_text("Hitpoints: {}".format(self.hitpoints),
                          10, 20, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        """All the logic to move, and the game logic goes here. """

        self.frame_count += 1

        hitlist = arcade.check_for_collision_with_list(
                  self.player, MyGame.bullet_list)  
        
        for bullet in hitlist:
            self.hitpoints -= 1
            explosion = Explosion(self.explosion_texture_list)
            explosion.center_x = bullet.center_x
            explosion.center_y = bullet.center_y
            explosion.update()
            self.explosions_list.append(explosion)
            bullet.kill()


        # Loop through each enemy that we have
        for enemy in self.enemy_list:

            # First, calculate the angle to the player. We could do this
            # only when the bullet fires, but in this case we will rotate
            # the enemy to face the player each frame, so we'll do this
            # each frame.

            # Position the start at the enemy's current location
            start_x = enemy.center_x
            start_y = enemy.center_y

            # Get the destination location for the bullet
            dest_x = self.player.center_x
            dest_y = self.player.center_y

            # Do math to calculate how to get the bullet to the destination.
            # Calculation the angle in radians between the start points
            # and end points. This is the angle the bullet will travel.
            x_diff = dest_x - start_x
            y_diff = dest_y - start_y
            angle = math.atan2(y_diff, x_diff)

            # Set the enemy to face the player.
            enemy.angle = math.degrees(angle)-90

            # Shoot every 60 frames change of shooting each frame
            if self.frame_count % 60 == 0:
                Bullet(start_x, start_y, dest_x, dest_y)
                #bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png")
                #bullet.center_x = start_x
                #bullet.center_y = start_y

                # Angle the bullet sprite
                #bullet.angle = math.degrees(angle)

                # Taking into account the angle, calculate our change_x
                # and change_y. Velocity is how fast the bullet travels.
                #bullet.change_x = math.cos(angle) * BULLET_SPEED
                #bullet.change_y = math.sin(angle) * BULLET_SPEED

                #self.bullet_list.append(bullet)

        # Get rid of the bullet when it flies off-screen
        for bullet in self.bullet_list:
            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

        self.bullet_list.update()
        self.explosions_list.update()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """Called whenever the mouse moves. """
        self.player.center_x = x
        self.player.center_y = y


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
