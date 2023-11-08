import pygame 
import sys
from molecule import molecule, moleculeArr


    
#Colors 
white = (255, 255, 255)
blue = (0, 0, 255)
light_blue = (100, 100, 255)
yellow = (255, 255, 153)
red = (219, 112, 147)
black = (0, 0, 0)

#function to return a text object to draw
def getText(font, text1, loco):
    surface = font.render(text1, True, white)
    rect = surface.get_rect()
    rect.center = loco
    return [surface, rect]

#initialize Trashcan Image 
img = pygame.transform.scale(pygame.image.load("4021663.png"), (50, 60))
image_rect = img.get_rect()
sprite = pygame.sprite.Sprite()
sprite.image = img
sprite.rect = image_rect
sprite.rect.x = 300
sprite.rect.y = 690

sprite_group = pygame.sprite.Group()
sprite_group.add(sprite)

#Initialize Screen and Window
pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Will's Game")

quit = False

#Initialize molecule button
button = pygame.Rect(20, 700, 200, 50)
button_color = blue
hover_color = light_blue
button_clicked = False

#Initialize Link button
LinkButton = pygame.Rect(440, 700, 130, 50,)
link_button_clicked = False
connect1 = -1
connect2 = -1
#Initialize Text button
textButton = pygame.Rect(640, 700, 130, 50,)
text_button_clicked = False


#Add Molecule Button Text
font = pygame.font.Font(None, 36)
text = "Add Molecule"
molButtonInfo = getText(font, text, button.center)
#Add Link Button Text
link_text = "Link"
link_button_info = getText(font, link_text, LinkButton.center)
#Add Text Button Text
add_text = "Add Text"
add_text_info = getText(font, add_text, textButton.center)

#Array of Molecules
molecule_array = moleculeArr((400//2, 500//2), 25)
mol = -1

while not quit:
    if text_button_clicked:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if textButton.collidepoint(event.pos):
                        text_button_clicked = False
                    if mol == -1:
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        mol = molecule_array.checkCollisions(mouse_x, mouse_y)
            elif event.type == pygame.KEYDOWN:
                if mol != -1 and event.key >= pygame.K_a and event.key <= pygame.K_z:
                    # Check if the pressed key is a letter key (a to z)
                    letter = chr(event.key)
                    text_button_clicked = False
                    molecule_array.array[mol].text = letter.capitalize()
                    mol = -1
                    
        for i in range(len(molecule_array.array)):
            if not molecule_array.array[i].show:
                continue 
            mouse_x, mouse_y = pygame.mouse.get_pos()
            molCol = blue if i != mol else yellow
            pygame.draw.circle(screen, molCol, molecule_array.array[i].location, molecule_array.array[i].radius)
            if molecule_array.array[i].text:
                SandR = getText(font, molecule_array.array[i].text, molecule_array.array[i].location)
                screen.blit(SandR[0], SandR[1])
    
    elif not link_button_clicked:
        #Check for mouse and keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Check if the left mouse button is clicked
                    if button.collidepoint(event.pos):
                        button_clicked = True
                    elif LinkButton.collidepoint(event.pos):
                        link_button_clicked = True
                    elif textButton.collidepoint(event.pos):
                        mol = -1
                        text_button_clicked = True
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mol = molecule_array.checkCollisions(mouse_x, mouse_y)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    button_clicked = False
                    if image_rect.collidepoint(pygame.mouse.get_pos()):
                        molecule_array.deleteMol(mol)
                    mol = -1
            
        screen.fill((255,255,255))
        
        #Draw Molecule Buttton
        button_color = blue if button.collidepoint(pygame.mouse.get_pos()) else hover_color  
        pygame.draw.rect(screen, button_color, button)
        screen.blit(molButtonInfo[0], molButtonInfo[1])
        #Draw Link Buttton
        button_color = blue if LinkButton.collidepoint(pygame.mouse.get_pos()) else hover_color  
        pygame.draw.rect(screen, button_color, LinkButton)
        screen.blit(link_button_info[0], link_button_info[1])
        #Draw Text Buttton
        button_color = blue if textButton.collidepoint(pygame.mouse.get_pos()) else hover_color  
        pygame.draw.rect(screen, button_color, textButton)
        screen.blit(add_text_info[0], add_text_info[1])
        
        #Draw Trash
        sprite_group.update()
        sprite_group.draw(screen)

        #Draw Links
        drawn = set()
        for node in molecule_array.links:
            for n in molecule_array.links[node]:
                if (node, n) in drawn or (n, node) in drawn:
                    continue
                pygame.draw.line(screen, black, molecule_array.array[n].location, molecule_array.array[node].location)
        #Draw Molecules
        for i in range(len(molecule_array.array)):
            if not molecule_array.array[i].show:
                continue 
            mouse_x, mouse_y = pygame.mouse.get_pos()
            molCol = blue
            if mol == i and image_rect.collidepoint(pygame.mouse.get_pos()):
                molCol = red
            elif mol == i and molecule_array.checkCollision(mol, mouse_x, mouse_y):
                molCol = yellow
            pygame.draw.circle(screen, molCol, molecule_array.array[i].location, molecule_array.array[i].radius)
            if molecule_array.array[i].text:
                SandR = getText(font, molecule_array.array[i].text, molecule_array.array[i].location)
                screen.blit(SandR[0], SandR[1])
                            
            
        
        if mol != -1:
            molecule_array.setMolLocation(mol, pygame.mouse.get_pos())

        #Add molecule
        if button_clicked:
            molecule_array.addMolecule()
            button_clicked = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if LinkButton.collidepoint(event.pos):
                        link_button_clicked = False
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mol = molecule_array.checkCollisions(mouse_x, mouse_y)
                    if mol != -1 and connect1 == -1:
                        connect1 = mol
                    elif mol != -1 and mol != connect1:
                        connect2 = mol
                        
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mol = -1
        for i in range(len(molecule_array.array)):
            if not molecule_array.array[i].show:
                continue 
            mouse_x, mouse_y = pygame.mouse.get_pos()
            molCol = blue if i != connect1 and i != connect2 else yellow
            pygame.draw.circle(screen, molCol, molecule_array.array[i].location, molecule_array.array[i].radius)
            if molecule_array.array[i].text:
                SandR = getText(font, molecule_array.array[i].text, molecule_array.array[i].location)
                screen.blit(SandR[0], SandR[1])
        if connect1 != -1 and connect2 != -1:
            molecule_array.createLink(connect1, connect2)
            connect1 = connect2 = -1
            link_button_clicked = False            
       
    pygame.display.flip()
        
pygame.quit()
sys.exit()



    