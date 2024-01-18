import socket 
import threading
import pickle
import time
import random
import pygame

id = random.randint(1111111111,9999999999)

playerc = random.randint(1,2)

x,y = 0,0

player = {}

def send_data(client_socket):
    while True:
        data = pickle.dumps(f"{x}%!//{y}%!//{id}%!//{playerc}")
        client_socket.send(data)
        time.sleep(0.1)

def receive_data(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        addr, received_vars = pickle.loads(data)
        data = received_vars.split("%!//")
        player[data[2]] = [data[0],data[1],data[3]]
        
def main():
    host = '192.168.1.48'
    port = 12345
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    send_thread = threading.Thread(target=send_data, args=(client,))
    receive_thread = threading.Thread(target=receive_data, args=(client,))

    send_thread.start()
    receive_thread.start()

main()

pygame.init()

root = pygame.display.set_mode((800,800),pygame.RESIZABLE)

run = True
image = pygame.image.load("player.png").convert()
image2 = pygame.image.load("player2.png").convert()

if playerc == 2:
    imagep = image
else:
    imagep = image2

x,y = 100,100
speed = 10

clock = pygame.time.Clock()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
            
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_q]:
       x-=speed
    elif pressed[pygame.K_z]:
       y-=speed
    elif pressed[pygame.K_s]:
        y +=speed
    elif pressed[pygame.K_d]:
        x+=speed

    root.fill((0,0,0))    
    root.blit(imagep,(0,0))
    for player2 in player:
        x2,y2  = int(player[player2][0]),int(player[player2][1])
        if player[player2][2] == 1:
            imagea = image
        else:
            imagea = image2
        root.blit(imagea,(x2-x,y2-y))
        police = pygame.font.Font(None, 20)
        texte = police.render(player2, True, (255, 255, 255))
        root.blit(texte, ((x2-x,y2-y+10)))
    pygame.display.flip()
    clock.tick(10)

pygame.quit()