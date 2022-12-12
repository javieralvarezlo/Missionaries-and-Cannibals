import sys
import pygame


def getclick():
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
    done = False
    for actor in who:
        actor["rect"] = actor["rect"].move((step, 0))
        if not arena.contains(actor["rect"]):
            actor["rect"] = actor["rect"].move((-step, 0))
            actor["surf"] = pygame.transform.flip(actor["surf"], True, False)
            done = True
    return done


def failure():
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("Failure", True, (255, 0, 0))
    msg_box = msg.get_rect()
    msg_box.center = arena.center
    window.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(10000)
    
    
def success():
    myfont = pygame.font.Font('freesansbold.ttf', 48)
    msg = myfont.render("Win", True, (0, 255, 0))
    msg_box = msg.get_rect()
    msg_box.center = arena.center
    window.blit(msg, msg_box)
    pygame.display.flip()
    pygame.time.wait(1000)
    
    
def draw_actors():
    for i, actor in enumerate(actors):
        actor["surf"] = pygame.image.load(actor["file"])
        actor["rect"] = actor["surf"].get_rect()
        actor["start"] = (0, (i+1)*arena.height/6.8)
        actor["rect"].midleft = actor["start"]
    
    boat["surf"] = pygame.image.load(boat["file"])
    boat["rect"] = boat["surf"].get_rect()
    boat["rect"].bottomleft = (arena.width/8, arena.height)


def mount(actor):  
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
    match len(mounted):
        case 0:
            return
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


def update_screen():
        window.blit(bg, (0, 0))
        for actor in actors:
            window.blit(actor["surf"], actor["rect"])
        pygame.display.flip()   

def move_passengers():
    if len(mounted) == 1:
         mounted[0]["rect"].midbottom = boat["rect"].midtop
    elif len(mounted) == 2:
        mounted[0]["rect"].bottomleft = boat["rect"].topleft
        mounted[1]["rect"].bottomright = boat["rect"].topright
        
def move_boat():
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
    global gamestate
    path = ""
    for m in mounted:
        path = path + m["type"]
    path = sorted(path)
    path = ''.join(path)
    print(path)
    gamestate = gamegraph[gamestate][path]


if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((1280, 650))
    arena = window.get_rect()
    bg = pygame.image.load("bg.png")


    boat = {"file": "boat.png", "status": "left"}
    cannibal1 = {"file": "cannibal.png", "status": "free", "type": "c"}
    cannibal2 = {"file": "cannibal.png", "status": "free", "type": "c"}
    cannibal3 = {"file": "cannibal.png", "status": "free", "type": "c"}    
    missionaire1 = {"file": "missionarie.png", "status": "free", "type": "m"}
    missionaire2 = {"file": "missionarie.png", "status": "free", "type": "m"}
    missionaire3 = {"file": "missionarie.png", "status": "free", "type": "m"}


    actors = [cannibal1, cannibal2, cannibal3, missionaire1, missionaire2, missionaire3, boat]
    draw_actors()

    gamegraph = {
                "cccmmmb-": {"m": "failure", "mm": "failure", "cm": "ccmm-cmb", "c": "ccmmm-cb", "cc": "cmmm-ccb" },
                "ccmm-cmb": {"m": "ccmmmb-c", "cm": "cccmmmb-", "c": "failure" },
                "ccmmm-cb": { "c": "cccmmmb-" },
                "cmmm-ccb": { "cc": "cccmmmb-", "c": "ccmmmb-c" },
                "ccmmmb-c": {"m": "ccmm-cmb", "mm": "failure", "cm": "failure", "c": "cmmm-ccb", "cc": "mmm-cccb"},
                "mmm-cccb": {"c": "cmmmb-cc"},
                "cmmmb-cc": {"m": "failure", "mm": "cm-ccmmb", "cm": "failure", "c": "mmm-cccb"},
                "cm-ccmmb": {"m": "failure", "mm": "cmmmb-cc", "cm": "ccmmb-cm", "c": "failure", "cc": "failure"},
                "ccmmb-cm": {"m": "failure", "mm": "cc-cmmmb", "cm": "cm-ccmmb", "c": "failure", "cc": "failure"},
                "cc-cmmmb": {"m": "failure", "mm": "ccmmb-cm", "cm": "failure", "c": "cccb-mmm", "cc": "failure"},
                "cccb-mmm": {"c": "cc-cmmmb", "cc": "c-ccmmmb"},
                "c-ccmmmb": {"m": "cmb-ccmm", "mm": "failure", "cm": "failure", "c": "ccb-cmmm", "cc": "cccb-mmm"},
                "cmb-ccmm": {"m": "c-ccmmmb", "cm": "success", "c": "failure"},
                "ccb-cmmm": {"c": "c-ccmmmb", "cc": "success"}
                }

    gamestate = "cccmmmb-"
    step = 1
    action = "listen"
    mounted = []

    fpsClock = pygame.time.Clock()
    
    while True:
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

        pygame.display.flip()
        fpsClock.tick(120)