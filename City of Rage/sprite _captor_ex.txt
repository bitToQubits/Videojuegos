Sprite Captor is the best tool to extract sprites from sprite sheets.
it is similar to the "2D Fighter Maker" one.

how to use it? :

to capture a sprite draw a rectangle around it 
by dragging the mouse cursor while clicking on the left button, 
then release the button when the sprite is inside the rectangle,
and you must not touch other sprites or other color 
than the image's blank area color with the rectangle while doing so.

and use the following keyboard keys :

i : scale up the image

j : scale down the image

o : reset the image's position to origin

r : reset the image's position and size to origin

c : center the captured sprite

e : add the captured sprite's position and size to the list

return : save changes to a file

s : enter the sprite editor

x : enter the animation editor

and use the arrows keys to move the image



while in the sprite editor screen use the following keyboard keys :

right arrow : go to the next sprite

left arrow : go to the previous sprite

up arrow : scale up the sprite

down arrow : scale down the sprite

o : set the sprite's position to origin

c : center the sprite

y : show or hide the hit boxes

t : toggle on/off the sprite's background color transparency 

d : delete the current sprite

return : save changes to a file

n : go to next animation

v : go to previous animation

space : add the current sprite to the selected animation

s : exit the sprite editor

and the keys ( u, h, j, k ) to move the sprite

drag the mouse cursor while clicking on the left button to daw an offense hitbox

drag the mouse cursor while clicking on the right button to daw an defense hitbox



while in the animation editor screen use the following keyboard keys :

right arrow : go to the next animation

left arrow : go to the previous animation

up arrow : go to the next frame in the current animation

down arrow : go to the previous frame in the current animation

i : scale up the image

j : scale down the image

c : center the sprite

p : pause or unpause the animation

y : show or hide the hit boxes

t : toggle on/off the sprite's background color transparency

d : delete the current frame

return : save changes to a file

x : exit the animation editor

click on the sprite with the left button of the mouse and drag it to adjust the sprite's position



sprite data are a list of rects in a form of list, exemple :
[ 10, 5, 20, 50 ] mean ==> x = 10, y = 5, width = 20, height = 50
this way you can interpret the sprite data as you want, 
you can create a subsurface of the main image or blit an area of it 
or create a sprite bounding box.....etc


TODO :

add the ability to choose the image that you want to edit from your files.

and why not?, turn this into a full "2D Fighter Maker".

