import os
import sys
import time
import random
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5), 
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0), 
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectで画面の内外判定
    引数 : こうかとんRect or ばくだんRect
    戻り値 : 真理値タプル（横、縦）/画面内 : True, 画面外 : False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate



def game_over(screen: pg.Surface) -> None:
    screen_black = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(screen_black, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    screen_black.set_alpha(128)
    screen_rct = screen_black.get_rect()
    screen_rct.center = WIDTH/2, HEIGHT/2
    screen.blit(screen_black, screen_rct)

    fonto = pg.font.Font(None, 80)
    GO_txt = fonto.render("GameOver", True, (255, 255, 255))
    GO_txt_rct = GO_txt.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(GO_txt, GO_txt_rct)

    kk_img_sad = pg.image.load("fig/8.png")
    screen.blit(kk_img_sad, [300, 290])
    screen.blit(kk_img_sad, [750, 290])

    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾の画像リストと加速度リストの作成
    """
    bb_img_size = []
    accs = [a for a in range(1, 11)]
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_img_size.append(bb_img)
    return bb_img_size, accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20)) #爆弾用の空surface
    pg.draw.circle(bb_img, (0, 0, 255), (10, 10), 10)
    bb_img.set_colorkey((0, 0, 0)) #四隅透過
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH),random.randint(0, HEIGHT)
    vx = +5
    vy = +5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return
        screen.blit(bg_img, [0, 0]) 


        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key ,tpl in DELTA.items():
            if key_lst[key] == True:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        kk_rct.move_ip(sum_mv)
        #こうかとんが画面外なら、元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        #爆弾の加速、拡大
        bb_imgs, bb_accs = init_bb_imgs()
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_img.set_colorkey((0, 0, 0)) 
        bb_rct.move_ip(avx, avy)
        #爆弾が画面外なら、元の場所に戻す
        yoko, tate = check_bound(bb_rct)
        if not yoko: #横にはみ出てたら
            vx *= -1
        if not tate: #縦にはみ出てたら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
