import argparse
from PIL import Image, ImageDraw, ImageFont
import random

# Активировать парсер
argParser = argparse.ArgumentParser(description="Creates colorful, nice Rainbow Card for memorizing all your passwords and more! ^_^")
argParser.add_argument('-s', '--seed', help="sets specific seed (default: randomized)", metavar="NUMBER", type=int)
argParser.add_argument('-l', '--length', help="amount of symbols on the RainbowCard (default: 24).", metavar="NUMBER", type=int, default=24)
groupText = argParser.add_argument_group('text arguments', 'Flags that let you specify custom text')
groupText.add_argument('-t', '--top-text', help="sets text on top of the card", metavar="STRING", type=str, nargs='*')
groupText.add_argument('-d', '--bottom-text', help="sets text on bottom of the card", metavar="STRING", type=str, nargs='*')
groupText.add_argument('-p', '--print-seed', action='store_true', help="print used seed on bottom of the card")
#groupColor = argParser.add_argument_group('color arguments', 'Flags that let you alternate colors')
#groupColor.add_argument('-g', '--grayscale', action='store_true', help="make grayscale version")
#groupColor.add_argument('-b', '--black-white', action='store_true', help="make black-white version")
groupPositions = argParser.add_argument_group('positional arguments', 'Flags that let you alternate positions')
groupPositions.add_argument('--x-padding', help="distance between letters (default: auto)", metavar="NUMBER", type=int)
groupPositions.add_argument('--x-offset', help="how wide is the offset in each line (default: 16)", metavar="NUMBER", type=int, default=16)
groupPositions.add_argument('--y-offset', help="how tight is the offset in each line (default: 6)", metavar="NUMBER", type=int, default=6)
args = argParser.parse_args()

# Инициировать рандом
random.seed()
randomSeed = args.seed if args.seed else random.randint(1, 2**64)
random.seed(randomSeed)

libraryOfAnchors = list('☺☻♥♦♣♠•◘○◙♂♀♪♫☼▲▼►◄¶↕↔§↑↓→←±®¡¢£¤¥€©$¿@∫∑∏')
libraryOfSymbols = 'ACDEFGHJKLMNPQRSTVXYZabcdefghijkmnpqrstvxyz2345679'
passwordLines = {
            'anchorLine': "",
            'redLine': "",
            'orangeLine': "",
            'yellowLine': "",
            'greenLine': "",
            'cyanLine': "",
            'blueLine': "",
            'purpleLine': "",
            'grayLine': "",
        }
for i in range(args.length):
    for l in passwordLines:
        passwordLines[l] += random.choice(libraryOfSymbols)
passwordLines['anchorLine'] = ""
for i in range(args.length):
    rc = random.choice(libraryOfAnchors)
    libraryOfAnchors.remove(rc)
    passwordLines['anchorLine'] += rc


# Позиции для полосок и иных вещей.
positions = {
                'title':        (16, 100),
                'anchorStrip':  (121, 212),
                'redStrip':     (213, 303),
                'orangeStrip':  (304, 394),
                'yellowStrip':  (395, 485),
                'greenStrip':   (486, 576),
                'cyanStrip':    (577, 667),
                'blueStrip':    (668, 758),
                'purpleStrip':  (759, 849),
                'grayStrip':    (850, 942),
                'bottom':       (962, 1034)
           }

# Создаем новый холст
canvas = Image.new('RGB', (1480, 1050), 0xFFFFFF)
# Начинаем на нем рисовать
canvasDraw = ImageDraw.Draw(canvas)

# Инициировать шрифт
canvasMainFont = ImageFont.truetype('cour.ttf', 200)

def isInTheBoundingBoxOfTheCard(fontsize, ypostuple, xoffset = 0):
    return fontsize[0]+xoffset <= 1480 and fontsize[1] + ypostuple[0] < ypostuple[1]

def printFromTopMiddle(canvas, position, text, color, font):
    canvas.text((position[0] - font.getsize(text)[0]/2, position[1]), text, color, font)
    
def createLine(canvas, lineposition, symbols, color, font):
    myFont = ImageFont.truetype(font.path, font.size)
    newLinePosition = (lineposition[0] + args.y_offset, lineposition[1] - args.y_offset)
    while not isInTheBoundingBoxOfTheCard(myFont.getsize('Q'), newLinePosition):
        myFont = ImageFont.truetype(myFont.path, myFont.size - 1)
    sizeOfSingleLetter = myFont.getsize('Q')
    amountOfSymbols = len(symbols)
    
    xpadding = args.x_padding if args.x_padding else int((1480-2*args.x_offset-sizeOfSingleLetter[0]*amountOfSymbols)/(amountOfSymbols-1))
    
    while sizeOfSingleLetter[0]*amountOfSymbols + xpadding*(amountOfSymbols-1) > 1480-args.x_offset*2:
        myFont = ImageFont.truetype(myFont.path, myFont.size - 1)
        sizeOfSingleLetter = myFont.getsize('Q')
    symNum = 0
    for symbol in symbols:
        canvas.text((args.x_offset + symNum*sizeOfSingleLetter[0] + symNum*xpadding, newLinePosition[0]), symbol, color, myFont)
        symNum += 1

# Титул.
if args.top_text:
    argsTitle = " ".join(args.top_text)
    canvasTitleFont = ImageFont.truetype(canvasMainFont.path, canvasMainFont.size)
    while not isInTheBoundingBoxOfTheCard(canvasTitleFont.getsize(argsTitle), positions['title']):
        canvasTitleFont = ImageFont.truetype(canvasTitleFont.path, canvasTitleFont.size - 1)
    printFromTopMiddle(canvasDraw, (740, positions['title'][0]), argsTitle, 0, canvasTitleFont)

# Якорь
# canvasDraw.rectangle( (0, positions['anchorStrip'][0], canvas.size[0], positions['anchorStrip'][1]), 0x123456 ) 
createLine(canvasDraw, positions['anchorStrip'], passwordLines['anchorLine'], 0, canvasMainFont)

# Линии
canvasDraw.rectangle( (0, positions['redStrip'][0], canvas.size[0], positions['redStrip'][1]), 0xCCCCFF )
createLine(canvasDraw, positions['redStrip'], passwordLines['redLine'], 0, canvasMainFont)
canvasDraw.rectangle( (0, positions['orangeStrip'][0], canvas.size[0], positions['orangeStrip'][1]), 0xCCDCFF )
createLine(canvasDraw, positions['orangeStrip'], passwordLines['orangeLine'], 0, canvasMainFont)
canvasDraw.rectangle( (0, positions['yellowStrip'][0], canvas.size[0], positions['yellowStrip'][1]), 0xCCFFFF )
createLine(canvasDraw, positions['yellowStrip'], passwordLines['yellowLine'], 0, canvasMainFont)
canvasDraw.rectangle( (0, positions['greenStrip'][0], canvas.size[0], positions['greenStrip'][1]), 0xCCFFCC )
createLine(canvasDraw, positions['greenStrip'], passwordLines['greenLine'], 0, canvasMainFont)
canvasDraw.rectangle( (0, positions['cyanStrip'][0], canvas.size[0], positions['cyanStrip'][1]), 0xFFFFCC )
createLine(canvasDraw, positions['cyanStrip'], passwordLines['cyanLine'], 0, canvasMainFont)
canvasDraw.rectangle( (0, positions['blueStrip'][0], canvas.size[0], positions['blueStrip'][1]), 0xFFCCCC )
createLine(canvasDraw, positions['blueStrip'], passwordLines['blueLine'], 0, canvasMainFont)
canvasDraw.rectangle( (0, positions['purpleStrip'][0], canvas.size[0], positions['purpleStrip'][1]), 0xFFCCDC )
createLine(canvasDraw, positions['purpleStrip'], passwordLines['purpleLine'], 0, canvasMainFont)
canvasDraw.rectangle( (0, positions['grayStrip'][0], canvas.size[0], positions['grayStrip'][1]), 0xCCCCCC )
createLine(canvasDraw, positions['grayStrip'], passwordLines['grayLine'], 0, canvasMainFont)
    
# Подпись.
if args.bottom_text:
    argsBottom = " ".join(args.bottom_text)
    canvasBottomFont = ImageFont.truetype(canvasMainFont.path, canvasMainFont.size)
    while not isInTheBoundingBoxOfTheCard(canvasBottomFont.getsize(argsBottom), positions['bottom']):
        canvasBottomFont = ImageFont.truetype(canvasBottomFont.path, canvasBottomFont.size - 1)
    printFromTopMiddle(canvasDraw, (740, positions['bottom'][0]), argsBottom, 0, canvasBottomFont)
    
if args.print_seed:
    canvasSeedFont = ImageFont.truetype(canvasMainFont.path, 18)
    canvasGetSizeOfSeedFont = canvasSeedFont.getsize("Seed: %d" % randomSeed)
    canvasDraw.text((1480-8-canvasGetSizeOfSeedFont[0], 1050-8-canvasGetSizeOfSeedFont[1]), "Seed: %d" % randomSeed, 0, canvasSeedFont)

del canvasDraw

canvas.save('RainbowCard.png')
