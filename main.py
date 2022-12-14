"""
Missionaries and Cannibals game developed for
Scripting Languages using pygame
"""
import sys
import pygame


def getclick():
    """
    Returns the actor clicked
    on the screen
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            for actor in actors:
                if actor["rect"].collidepoint(mouse):
                    return actor


def ferry(who):
    """
    Moves the boat and
    the actors mounted on it
    """
    done = False
    for actor in who:
        actor["rect"] = actor["rect"].move((step, 0))
        if not arena.contains(actor["rect"]):
            actor["rect"] = actor["rect"].move((-step, 0))
            actor["surf"] = pygame.transform.flip(actor["surf"], True, False)
            done = True
    return done


def failure():
    """
    Handles game failure
    """
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("Failure", True, (255, 0, 0))
    msg_box = msg.get_rect()
    msg_box.center = arena.center
    window.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(1000)


def success():
    """
    Handles game success
    """
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("Win", True, (0, 255, 0))
    msg_box = msg.get_rect()
    msg_box.center = arena.center
    window.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(1000)


def draw_actors():
    """
    Draws the actors in
    the screen
    """
    for i, actor in enumerate(actors):
        actor["surf"] = pygame.image.load(actor["file"])
        actor["rect"] = actor["surf"].get_rect()
        actor["start"] = (0, (i+1)*arena.height/6.8)
        actor["rect"].midleft = actor["start"]

    boat["surf"] = pygame.image.load(boat["file"])
    boat["rect"] = boat["surf"].get_rect()
    boat["rect"].bottomleft = (arena.width/8, arena.height)


def mount(actor):
    """
    Mounts the actors
    in the boat
    """
    if boat["status"] == "right" and actor["rect"].left < WIDTH/2:
        return
    if boat["status"] == "left" and actor["rect"].right > WIDTH/2:
        return

    match len(mounted):
        case 0:
            mounted.append(actor)
            actor["rect"].midbottom = boat["rect"].midtop
            actor["status"] = "mounted"
        case 1:
            mounted.append(actor)
            actor["rect"].bottomright = boat["rect"].topright
            actor["status"] = "mounted"
            mounted[0]["rect"].bottomleft = boat["rect"].topleft
        case _:
            return


def unmount(actor):
    """
    Unmounts the actors
    form the boat
    """
    match len(mounted):
        case 1:
            mounted.remove(actor)
            actor["status"] = "free"
            if boat["status"] == "left":
                actor["rect"].midleft = (0, actor["start"][1])
            if boat["status"] == "right":
                actor["rect"].midright = (arena.width, actor["start"][1])
        case 2:
            mounted.remove(actor)
            actor["status"] = "free"
            if boat["status"] == "left":
                actor["rect"].midleft = (0, actor["start"][1])
            if boat["status"] == "right":
                actor["rect"].midright = (arena.width, actor["start"][1])
            mounted[0]["rect"].midbottom = boat["rect"].midtop
        case _:
            return


def update_screen():
    """
    Updates the screen
    """
    window.blit(bg, (0, 0))
    for actor in actors:
        window.blit(actor["surf"], actor["rect"])
    show_moves()
    pygame.display.flip()


def move_passengers():
    """
    Moves the passengers
    """
    if len(mounted) == 1:
        mounted[0]["rect"].midbottom = boat["rect"].midtop
    elif len(mounted) == 2:
        mounted[0]["rect"].bottomleft = boat["rect"].topleft
        mounted[1]["rect"].bottomright = boat["rect"].topright


def move_boat():
    """
    Moves the boat
    """
    global boat

    if len(mounted) == 0:
        return False

    if boat["status"] == "left":
        while boat["rect"].right < 6*arena.width/8:
            boat["rect"] = boat["rect"].move(step, 0)
            move_passengers()
            update_screen()
        boat["status"] = "right"

    elif boat["status"] == "right":
        while boat["rect"].left > arena.width/8:
            boat["rect"] = boat["rect"].move(-step, 0)
            move_passengers()
            update_screen()
        boat["status"] = "left"
    return True


def update_graph():
    """
    Updates the graph and
    the gamestate
    """
    global gamestate
    path = ""
    for m in mounted:
        path = path + m["type"]
    path = sorted(path)
    path = ''.join(path)
    print(path)
    gamestate = gamegraph[gamestate][path]


def show_menu():
    """
    Shows the menu options and handles
    the click event
    """
    global menu

    # title
    maintext = largefont.render("Missionaries and Cannibals", True, white)
    maintext_rect = maintext.get_rect()
    maintext_rect.center = (HEIGHT/2, WIDTH/2 - 200)
    window.blit(maintext, maintext_rect)

    # instructions
    instr1 = smallfont.render("Click on the missionaries and "
                              "cannibals to mount "
                              "them on the boat", True, white)
    instr1_rect = instr1.get_rect()
    instr1_rect.center = (HEIGHT/2, WIDTH/2 - 50)
    window.blit(instr1, instr1_rect)

    # instructions 2
    instr2 = smallfont.render("Click the boat to transport them", True, white)
    instr2_rect = instr2.get_rect()
    instr2_rect.center = (HEIGHT/2, WIDTH/2 - 15)
    window.blit(instr2, instr2_rect)

    # instructions 3
    instr3 = smallfont.render("Ensure to have always the "
                              "same misionaries than cannibals!", True, white)
    instr3_rect = instr3.get_rect()
    instr3_rect.center = (HEIGHT/2, WIDTH/2 + 15)
    window.blit(instr3, instr3_rect)

    # play text
    playtext = largefont.render("PRESS ENTER TO PLAY", True, white)
    playtext_rect = playtext.get_rect()
    playtext_rect.center = (HEIGHT/2, WIDTH/2 + 270)
    window.blit(playtext, playtext_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                menu = False

    pygame.display.flip()


def show_moves():
    """
    Shows on screen
    the game moves
    """
    text = smallfont.render(str(moves) + " move(s)", True, black)
    text_rect = text.get_rect()
    text_rect.center = (HEIGHT/4, 50)
    window.blit(text, text_rect)


if __name__ == "__main__":
    HEIGHT = 1280
    WIDTH = 650
    pygame.init()
    window = pygame.display.set_mode((HEIGHT, WIDTH))
    arena = window.get_rect()
    bg = pygame.image.load("bg.png")

    menu = True

    gamestate = "cccmmmb-"
    step = 1
    action = "listen"
    mounted = []
    moves = 0

    largefont = pygame.font.Font('freesansbold.ttf', 50)
    smallfont = pygame.font.Font('freesansbold.ttf', 30)
    white = pygame.Color("white")
    black = pygame.Color("black")

    boat = {"file": "boat.png", "status": "left"}
    cannibal1 = {"file": "cannibal.png", "status": "free", "type": "c"}
    cannibal2 = {"file": "cannibal.png", "status": "free", "type": "c"}
    cannibal3 = {"file": "cannibal.png", "status": "free", "type": "c"}
    missionaire1 = {"file": "missionarie.png", "status": "free", "type": "m"}
    missionaire2 = {"file": "missionarie.png", "status": "free", "type": "m"}
    missionaire3 = {"file": "missionarie.png", "status": "free", "type": "m"}

    actors = [cannibal1, cannibal2, cannibal3,
              missionaire1, missionaire2, missionaire3, boat]
    draw_actors()

    gamegraph = {
                "cccmmmb-": {"m": "failure",
                             "mm": "failure",
                             "cm": "ccmm-cmb",
                             "c": "ccmmm-cb",
                             "cc": "cmmm-ccb"},
                "ccmm-cmb": {"m": "ccmmmb-c",
                             "cm": "cccmmmb-",
                             "c": "failure"},
                "ccmmm-cb": {"c": "cccmmmb-"},
                "cmmm-ccb": {"cc": "cccmmmb-",
                             "c": "ccmmmb-c"},
                "ccmmmb-c": {"m": "ccmm-cmb",
                             "mm": "failure",
                             "cm": "failure",
                             "c": "cmmm-ccb",
                             "cc": "mmm-cccb"},
                "mmm-cccb": {"c": "cmmmb-cc"},
                "cmmmb-cc": {"m": "failure",
                             "mm": "cm-ccmmb",
                             "cm": "failure",
                             "c": "mmm-cccb"},
                "cm-ccmmb": {"m": "failure",
                             "mm": "cmmmb-cc",
                             "cm": "ccmmb-cm",
                             "c": "failure",
                             "cc": "failure"},
                "ccmmb-cm": {"m": "failure",
                             "mm": "cc-cmmmb",
                             "cm": "cm-ccmmb",
                             "c": "failure",
                             "cc": "failure"},
                "cc-cmmmb": {"m": "failure",
                             "mm": "ccmmb-cm",
                             "cm": "failure",
                             "c": "cccb-mmm",
                             "cc": "failure"},
                "cccb-mmm": {"c": "cc-cmmmb",
                             "cc": "c-ccmmmb"},
                "c-ccmmmb": {"m": "cmb-ccmm",
                             "mm": "failure",
                             "cm": "failure",
                             "c": "ccb-cmmm",
                             "cc": "cccb-mmm"},
                "cmb-ccmm": {"m": "c-ccmmmb",
                             "cm": "success",
                             "c": "failure"},
                "ccb-cmmm": {"c": "c-ccmmmb",
                             "cc": "success"}
                }

    fpsClock = pygame.time.Clock()

    while True:

        if menu:
            show_menu()
        else:

            if action == "listen":
                click = getclick()
                if click in actors:
                    if click is boat:
                        action = "ferry"
                    else:
                        if click["status"] == "mounted":
                            unmount(click)
                        else:
                            mount(click)

            if action == "ferry":
                if move_boat():
                    update_graph()
                    moves = moves + 1
                print(gamestate)
                if gamestate == "failure":
                    action = "failure"
                elif gamestate == "success":
                    action = "success"
                else:
                    action = "listen"

            if action == "failure":
                failure()
                sys.exit()

            if action == "success":
                success()
                sys.exit()

            update_screen()

            fpsClock.tick(120)
