import pygame
import random
import style

pygame.init()
pygame.font.init()
SCREEN_SIZE = (700, 500)
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("STONK")
CLOCK = pygame.time.Clock()
BUYIMG = pygame.image.load("buy_btn.png").convert_alpha()
SELLIMG = pygame.image.load("sell_btn.png").convert_alpha()
FONT = pygame.font.SysFont("Arial", 48)
GRAPH_FONT = pygame.font.SysFont("Arial", 18)

class Button:
    def __init__(self, x, y, image, scale):
        self.x = x
        self.y = y
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,
                                            (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        return action


def main():

    # MAIN EVENT LOOP VARS
    RUNNING = True
    FPS = 60

    # OBJECTS
    BUY_BTN = Button(20, 20, BUYIMG, 0.1)
    SELL_BTN = Button(140, 20, SELLIMG, 0.1)
    PRICE = 100.0
    MONEY = 1000.0
    STOCK = 0
    TICKRATE = 0
    PREV_TICK = 0
    LAST_CANDLES = [100]

    while RUNNING:
        time_passed = CLOCK.tick()
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

        #LOGIC
        TICKRATE += time_passed
        if PREV_TICK != TICKRATE // 10:
            PREV_TICK = TICKRATE // 10
            PRICE = PRICE * ((100 + random.gauss(0, 2))/100)
            if len(LAST_CANDLES) < 58:
                LAST_CANDLES.append(PRICE)
            else:
                LAST_CANDLES.pop(0)
                LAST_CANDLES.append(PRICE)



        #DRAW
        SCREEN.fill(style.GREY)
        if BUY_BTN.draw():
            if MONEY >= PRICE:
                INVESTED = True
                STOCK += 1
                MONEY -= PRICE
        if SELL_BTN.draw():
            if STOCK > 0:
                INVESTED = False
                MONEY = MONEY + PRICE
                STOCK -= 1
        #GUI
        money_text = FONT.render("MONEY: ", False, style.WHITE)
        money_amount = FONT.render("%.2f€" % MONEY, False, style.WHITE)
        stock_text = FONT.render("STOCKS: ", False, style.WHITE)
        stock_amount = FONT.render(str(STOCK), False, style.WHITE)
        price_text = FONT.render("PRICE: ", False, style.WHITE)
        price_amount = FONT.render("%.2f€" % PRICE, False, style.WHITE)
        SCREEN.blit(money_text, (350, 20))
        SCREEN.blit(money_amount, (510, 20))
        SCREEN.blit(stock_text, (350, 70))
        SCREEN.blit(stock_amount, (530, 70))
        SCREEN.blit(price_text, (20, 70))
        SCREEN.blit(price_amount, (160, 70))

        #GRAPH
        chart_start_x = 30
        chart_start_y = 150
        chart_max = max(LAST_CANDLES) + 0.1
        chart_min = min(LAST_CANDLES) - 0.1
        last_price = (0, 0)
        pygame.draw.rect(SCREEN, style.DARK_GREY, (20, 140, 660, 340))
        pygame.draw.line(SCREEN, style.WHITE, (620, 150), (620, 470), 2)
        pygame.draw.line(SCREEN, style.GREY, (30, 160), (610, 160))
        pygame.draw.line(SCREEN, style.GREY, (30, 235), (610, 235))
        pygame.draw.line(SCREEN, style.GREY, (30, 310), (610, 310))
        pygame.draw.line(SCREEN, style.GREY, (30, 385), (610, 385))
        pygame.draw.line(SCREEN, style.GREY, (30, 460), (610, 460))
        upper_price = GRAPH_FONT.render("%.2f" % chart_max, False, style.GREEN)
        middle_price = GRAPH_FONT.render("%.2f" % ((chart_max+chart_min)/2), False, style.WHITE)
        lower_price = GRAPH_FONT.render("%.2f" % chart_min, False, style.RED)
        SCREEN.blit(upper_price, (630, 145))
        SCREEN.blit(middle_price, (630, 300))
        SCREEN.blit(lower_price, (630, 455))
        for point in range(0, len(LAST_CANDLES)-1):
            if point == 0:
                x = chart_start_x
                y = (150 + (310 * (chart_max - LAST_CANDLES[point])/(chart_max - chart_min)))
                last_price = (x, y)
            else:
                x = chart_start_x
                y = (150 + (310 * (chart_max - LAST_CANDLES[point]) / (chart_max - chart_min)))
                if last_price[1] < y:
                    pygame.draw.line(SCREEN, style.RED, last_price, (x, y), 4)
                else:
                    pygame.draw.line(SCREEN, style.GREEN, last_price, (x, y), 4)
                last_price = (x, y)
            chart_start_x += 10


        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()


