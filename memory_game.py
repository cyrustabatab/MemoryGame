import pygame 
import random
import time
import sys

pygame.init()

WIDTH = HEIGHT = 400
screen = pygame.display.set_mode((WIDTH,HEIGHT))
FPS = 60
clock = pygame.time.Clock()

pygame.display.set_caption("Memory Game")

font = pygame.font.SysFont("comicsansms",42)
BLUE = (0,0,255)
LIGHT_BLUE = (173,216,230)
LIGHT_RED = (255,204,203)
RED = (255,0,0)
GREEN = (0,255,0)
LIGHT_GREEN = (144,238,144)
LIGHT_YELLOW = (255,255,153)
YELLOW = (255,255,0)

class Square(pygame.sprite.Sprite):

    def __init__(self,number,x,y,size,colors):
        super().__init__()
        self.number = number
        self.light_surface = pygame.Surface([size,size])
        self.light_surface.fill(colors[0])
        self.blue_surface = pygame.Surface([size,size])
        self.blue_surface.fill(colors[1])
        self.image = self.light_surface
        self.rect = self.image.get_rect(topleft=(x,y))

    def switch_surface(self):
        if self.image is self.light_surface:
            self.image = self.blue_surface
        else:
            self.image = self.light_surface

def generate_sequence(n):
    numbers = [0,1,2,3]
    sequence = random.choices(numbers,k=n)
    '''    
    numbers = [0,1,2,3]
    sequence = []

    while len(sequence) != n:
        amount = min(n - len(sequence),len(numbers))

        sequence.extend(random.sample(numbers,amount))
    '''
    return sequence



    '''
    for number in sequence:
        screen.fill((0,0,0))
        square = number_to_square[number]
        square.switch_surface()
        squares.draw(screen)
        pygame.display.update()
        square.switch_surface()
        pygame.time.wait(1000)

    pygame.event.clear()
    '''






d500one = False

square_size = 100
boundary = 10

offset = (WIDTH - 202) // 2
squares = []
count = 0
colors = [(LIGHT_BLUE,BLUE),(LIGHT_RED,RED),(LIGHT_YELLOW,YELLOW),(LIGHT_GREEN,GREEN)]
squares = pygame.sprite.Group()
number_to_square = {}
for row in range(2):
    for col in range(2):
        number = row * 2 + col
        square = Square(number,((square_size + boundary) * row) + offset,((square_size + boundary) * col + offset),square_size,colors[number] )
        number_to_square[number] = square
        squares.add(square)




def main(scores):

    def sequence_animation(sequence,number_to_square):

        index = 0 
        previous_time = None
        done = False
        
        screen.fill((0,0,0))
        text = font.render("LOOK CLOSELY",True,(255,255,255))
        screen.blit(text,(WIDTH/2 - text.get_width()/2,20))
        squares.draw(screen)
        pygame.display.update()
        pygame.time.delay(1000)
        switched = False
        while not done:

            current_time = time.time()
            if previous_time:
                if current_time - previous_time >= 1:
                    index += 1
                    if index == len(sequence):
                        break
                    previous_time = None
                elif not switched and current_time - previous_time >= 0.5:
                    square.switch_surface()
                    switched = True






            if not previous_time:
                number = sequence[index]
                square = number_to_square[number]
                square.switch_surface()
                switched = False
                previous_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            screen.fill((0,0,0))
            screen.blit(text,(WIDTH/2 - text.get_width()/2,20))
            squares.draw(screen)
            screen.blit(sequence_length_text,(WIDTH//2 - sequence_length_text.get_width()/2,300))
            pygame.display.update()
            clock.tick(60)
    sequence_length = 1
    sequence_generated = False
    current_square = 0
    previous_square = None
    win = False
    text = None
    win_text = font.render("Correct",True,(255,255,255))
    lose_text = font.render("Incorrect",True,(255,255,255))
    start_time = None
    outro = False
    sequence_length_text = font.render("Length: " + str(sequence_length),True,(255,255,255))
    selected = False
    done = False




    while not done:

        current_time = time.time()

        if outro:
            if current_time - start_time >= 2:
                if text is lose_text:
                    check_to_insert_score(sequence_length,scores)
                    sequence_length = 1
                else:
                    sequence_length += 1
                
                sequence_length_text = font.render("Length: " + str(sequence_length),True,(255,255,255))

                text = None
                sequence_index = 0
                outro = False
                sequence_generated = False
            elif previous_square and current_time - start_time >= 1:
                previous_square.switch_surface()
                previous_square = None
        elif selected:
            if current_time - selected_time >= 0.5:
                if previous_square:
                    previous_square.switch_surface()
                    selected = False
                    previous_square = None
                selected = False


        if not sequence_generated:
            sequence = generate_sequence(sequence_length)

            sequence_animation(sequence,number_to_square)
            sequence_generated = True
            sequence_index = 0
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                check_to_insert_score(sequence_length,scores)
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    check_to_insert_score(sequence_length,scores)
                    return False
            elif event.type == pygame.MOUSEBUTTONDOWN and sequence_generated and not outro and not selected:

                x,y = pygame.mouse.get_pos()
                for square in squares:
                    if square.rect.collidepoint((x,y)):
                        square.switch_surface()
                        selected = True
                        selected_time = time.time()
                        #if previous_square:
                        #    previous_square.switch_surface()
                        previous_square = square
                        if sequence[sequence_index] != square.number:
                            text = lose_text
                            start_time = time.time()
                            selected= False
                            outro = True
                        elif sequence_index == len(sequence) - 1:
                            text = win_text
                            start_time = time.time()
                            selected = False
                            outro = True
                        else:
                            sequence_index += 1

                        break

        screen.fill((0,0,0)) 
        if text:
            screen.blit(text,(WIDTH//2 - text.get_width() /2,10))
        screen.blit(sequence_length_text,(WIDTH//2 - sequence_length_text.get_width()/2,300))
        squares.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

def high_scores_screen(scores):
    
    
    score_texts = []
    offset = 20
    for i,score in enumerate(scores):
        score_text= font.render(f"{i +1}. {score}",True,(255,255,255))
        score_rect= score_text.get_rect(center=(WIDTH/2 - score_text.get_width()/2,offset + 80 * i))
        score_texts.append((score_text,score_rect))




    done = False
     
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        screen.fill((0,0,0))
        
        for score_text in score_texts:
            screen.blit(*score_text)
        pygame.display.update()



def check_to_insert_score(score,scores):
    if score > scores[-1]:

        for i in range(len(scores)):
            s = scores[i]
            if score > s:
                scores.insert(i,score)
                scores.pop()
                break
        with open("memory_game_high_scores.txt",'w') as f:
            for score in scores:
                f.write(str(score) + '\n')



def main_menu():

    
    
    with open("memory_game_high_scores.txt",'r') as f:
        scores = f.readlines()
    scores = list(map(lambda x:int(x[:-1]),scores))

    title_text =font.render("Memory Puzzle",True,(255,0,0))
    enter_text = font.render("Press ENTER",True,(0,255,0))
    

    high_scores_text = font.render("High Scores",True,(255,255,255))
    button_rect = high_scores_text.get_rect(center=(WIDTH/2,200))
    done = False
    

    while not done:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    done = main(scores)
                    if done:
                        return
                    with open("memory_game_high_scores.txt",'r') as f:
                        scores = f.readlines()
                    scores = list(map(lambda x:int(x[:-1]),scores))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                point= pygame.mouse.get_pos()
                if button_rect.collidepoint(point):
                    high_scores_screen(scores)



            

            



    
        screen.fill((0,0,0))
        screen.blit(title_text,(WIDTH/2 - title_text.get_width()/2,10))
        screen.blit(enter_text,(WIDTH/2 - enter_text.get_width()/2,80))
        pygame.draw.rect(screen,(255,0,0),button_rect)
        screen.blit(high_scores_text,button_rect)
        pygame.display.update()




if __name__ == "__main__":
    
    main_menu()





