import pygame


def paint_scoreboard(screen, score):
    font70 = pygame.font.Font('icons/rainyhearts.ttf', 70)
    font32 = pygame.font.Font('icons/rainyhearts.ttf', 40)
    game_over = font70.render("GAME OVER!", True, (255, 0, 0))
    score = font32.render("Score: " + str(score), True, (255, 255, 255))
    alert = font32.render("Press enter to continue", True, (0, 0, 255))
    screen.blit(game_over, (80, 300))
    screen.blit(score, (180, 400))
    screen.blit(alert, (60, 450))


def paint_main_menu(screen, connection, ready):
    font64 = pygame.font.Font('icons/rainyhearts.ttf', 64)
    font32 = pygame.font.Font('icons/rainyhearts.ttf', 40)
    menu_text = font64.render("MAIN MENU!", True, (255, 255, 255))
    connect = font32.render("Connect", True, (0, 0, 255))
    connecting = font32.render("Connecting", True, (255, 255, 0))
    connected = font32.render("Connected", True, (0, 255, 0))
    error = font32.render("Error", True, (255, 0, 0))
    logo = pygame.image.load("icons/menu_logo.png")
    play_button = pygame.image.load("icons/play-button.png")
    plug_button = pygame.image.load("icons/plug.png")
    green_plug_button = pygame.image.load("icons/greenplug.png")
    red_plug_button = pygame.image.load("icons/redplug.png")
    yellow_plug_button = pygame.image.load("icons/yellowplug.png")
    if ready:
        play = font32.render("Ready", True, (0, 255, 0))
        screen.blit(play, (322, 560))
    elif not ready:
        play = font32.render("Not ready", True, (255, 0, 0))
        screen.blit(play, (302, 560))
    screen.blit(logo, (140, 160))
    screen.blit(menu_text, (120, 400))
    screen.blit(play_button, (340, 500))
    if connection == 0:
        screen.blit(plug_button, (140, 500))
        screen.blit(connect, (100, 560))
    elif connection == 2:
        screen.blit(yellow_plug_button, (140, 500))
        screen.blit(connecting, (100, 560))
    elif connection == 1:
        screen.blit(green_plug_button, (140, 500))
        screen.blit(connected, (90, 560))
    else:
        screen.blit(red_plug_button, (140, 500))
        screen.blit(error, (100, 560))
