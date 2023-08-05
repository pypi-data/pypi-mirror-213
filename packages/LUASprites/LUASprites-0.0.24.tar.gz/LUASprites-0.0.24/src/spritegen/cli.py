import time
import requests
from colorama import Fore, Back, Style
import colorama
import os
import sys

from PIL import Image
IMAGE_SIZE = [1024, 1024];


colorama.init(autoreset=True)

BANNER = Fore.CYAN + "Welcome to reteach's SpriteSheet Generator..."""
LUA_HEADER = """
local Spritesheet = require(script:FindFirstAncestorWhichIsA("ModuleScript").Spritesheet)

local {name} = {{}}
{name}.__index = {name}
setmetatable({name}, Spritesheet)

{varibles}

function {name}.new()
	local new{name} = Spritesheet.new()
	setmetatable(new{name}, {name})

"""
class node:
    def __init__(self, position, size):
        self.image = None
        self.size = size; 
        self.position = position;
        self.down = None;
        self.right = None;


def sortImages(images):
    images.sort(key=lambda img: img.size[0] * img.size[1], reverse=True)#Sort all images by total area width * height 

def loadImages(path):
    sprites = [];
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            try:
                print(Fore.GREEN + "Loading: " + Fore.BLUE  + file)
                loadedImage = Image.open(file_path)
                sprites.append(loadedImage)
            except:
                print(Fore.RED + "Failed to open: " + Fore.BLUE  + file + Style.RESET_ALL + Fore.YELLOW + "(PNG files work best with this program)")
    return sprites;

def findTreeSpotHelper(node, img):
    if node.image is not None:
        return findTreeSpotHelper(node.right, img) or findTreeSpotHelper(node.down, img)
    elif (node.size[0] >= img.size[0] and node.size[1] >= img.size[1]):
        return node;
    else:
        return None;

def findTreeSpot(trees, img):
    found = None;
    for tree in trees: 
        found = findTreeSpotHelper(tree, img)
        if found:
            break;
    if found:
        return found;
    else:
        found = node([0,0],IMAGE_SIZE[:])
        trees.append(found)
        return found

def getImageSize(current):
    if current is None:
        return [0,0]
    if current.image is None:
        return [0,0]
    right = getImageSize(current.right)
    down = getImageSize(current.down)
    
    curExtent = [current.image.size[0] + current.position[0], current.image.size[1] + current.position[1]];
    return [max(curExtent[0],right[0],down[0]), max(curExtent[1],right[1],down[1])]


def packImagesRecursive(current, spriteSheet):
    if current is None:
        return
    if current.image is None:
        return
    spriteSheet.paste(current.image, box=(current.position[0],current.position[1]))
    packImagesRecursive(current.right, spriteSheet);
    packImagesRecursive(current.down, spriteSheet);

def getOutputFolder(path):
    name = "/output"
    ext = 0
    while os.path.exists(path + name + str(ext)):
        ext += 1

    os.mkdir(path + name + str(ext))
    return path + name + str(ext)

def packImages(trees,name,output):
    for idx,tree in enumerate(trees):
       size = getImageSize(tree)
       print("Spritesheet " + str(idx) + " will be " + str(size) + " pixels")
       spriteSheet = Image.new(mode="RGBA", size=(size[0],size[1]))
       packImagesRecursive(tree,spriteSheet)
       if len(trees) == 1:
           idx = ""
       filePath = output + "/"  + name + str(idx) + ".png"
       spriteSheet.save(filePath)
       usageTrack("imageCreated")
       print(Fore.GREEN + "Image wrote to: \033[0;34m" + Fore.BLUE +  filePath)

def buildTree(trees, sprites):
    print("Building tree...")
    for img in sprites:
        if img.size[0] > IMAGE_SIZE[0] or img.size[1] > IMAGE_SIZE[1]:
            raise Exception("All images must be <= 1024 pixels in both axes" + img.filename + " is too big")
        else:
            foundNode = findTreeSpot(trees, img)
            foundNode.image = img;
            foundNode.right = node(
                    [foundNode.position[0] + img.size[0], foundNode.position[1]], #Position
                    [foundNode.size[0] - img.size[0], img.size[1]] #Size
            ) 
            foundNode.down = node(
                    [foundNode.position[0], foundNode.position[1] + img.size[1]],#Position
                    [foundNode.size[0], foundNode.size[1] - img.size[1]] #Size
            )

def loadSprites(path):
    sprites = loadImages(path)
    sortImages(sprites)
    return sprites

def getName():
    name = input("Enter a name for the output spritesheet(s) " + Fore.YELLOW + "(Naming your spritesheet is important for referencing it later in lua): ")
    return name if name != "" else "untitled"

def getImageFolder():
    #spritesFolder = os.path.exists("./Sprites") if 
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        sys.exit(Fore.RED + "Must supply a source file\n" + Fore.YELLOW  + "Example: luasprite [sourcefilehere]")
       # while not os.path.exists("./Sprites"):
       #     print("\033[0;31mSprite folder not found\033[0m")   
       #     print("Please create a folder named \033[0;31m\"Sprites\"\033[0m in the parent directory \033[0;33m(This folder should contain the images you want on the spritesheet)\033[0m")
       #     print("\033[0;33m" + os.getcwd() + "\033[0;31m/Sprites\033[0m")
       #     input("Press \033[0;32mEnter\033[0m to continue...")
       # print("\033[0;32mSprite folder found\033[0m")
       # return "./Sprites"

def getOutputType():
    output = -1 
    while output == -1:
        print("How would you like the output formatted?")
        print(Fore.BLUE + Style.BRIGHT +"\t1" + Style.RESET_ALL + " Lua Sprite Sheet Module Compatible" + Fore.YELLOW +"(recommened)")
        print(Fore.BLUE + Style.BRIGHT +"\t2" + Style.RESET_ALL + " Lua table output")
        print(Fore.BLUE + Style.BRIGHT +"\t3" + Style.RESET_ALL + " No output")
        choice = input("Enter one of the options above: ")
        try:
            choice = int(choice)
            if choice > 0 and choice < 4: 
                output = choice
            else:
                print(Fore.RED + "Please enter a valid choice")
        except:
            print(Fore.RED + "Please enter a valid choice")
    return output

def getSpriteModuleHelper(current,name,idx):
    if current is None:
        return "" 
    if current.image is None:
        return ""
    fileName = os.path.basename(current.image.filename)
    periodPos = fileName.rfind(".")
    fileName = fileName[:periodPos]
    right = getSpriteModuleHelper(current.right, name, idx)
    down = getSpriteModuleHelper(current.down, name, idx)
    return "\tnew{name}:AddSprite(\"{fname}\", Vector2.new({p1}, {p2}), Vector2.new({s1}, {s2}), {name}Sheet{idx})\n".format(
            name = name, 
            fname = fileName,
            p1 = current.position[0],
            p2 = current.position[1],
            s1 = current.image.size[0],
            s2 = current.image.size[1],
            idx = idx
    ) + right + down

def genSpriteSheetModule(trees, output, name):
    elements = ""
    for idx,tree in enumerate(trees):
        if len(trees) == 1:
            idx = ""
        elements += getSpriteModuleHelper(tree, name, str(idx))
    output += elements + "\treturn new{name}\nend\n\nreturn {name}".format(name=name)
    return output

def imageVariblesGenerate(trees,name):
    output = ""
    for idx,tree in enumerate(trees):
        if len(trees) == 1:
            idx == ""
        output += "local {name}Sheet{idx} = \"rbxassetid://ID_OF_{upname}{idx}_HERE\"\n".format(name=name, idx=idx, upname=name.upper())
    return output
         
def generateLua(text,name, outputFolder):
    try:
        outputFile = open(outputFolder+ "/" + name + ".lua", "w")
        outputFile.write(text)
        outputFile.close()
    except E:
        print(Fore.RED + "Failed to write {name}.lua".format(name=name))
        raise E

    filePath = outputFolder+ "/" + name + ".lua"
    print(Fore.BLUE + "Lua module wrote to: " + Fore.GREEN + filePath)


def generateLuaOutput(outputType, name, trees, outputFolder):
    outputString = ""
    if outputType == 3:
        usageTrack("no-output")
        return;
    print("Generating output...")
    if outputType == 1:
        usageTrack("module-output")
        varibles = imageVariblesGenerate(trees, name)
        outputString = LUA_HEADER.format(name=name, varibles=varibles)
        outputString = genSpriteSheetModule(trees, outputString, name) 
    elif outputType == 2:
        usageTrack("table-output")
        outputString += imageVariblesGenerate(trees,name)
        outputString += "\nreturn {\n"
        outputString += generateLuaTableOutput(trees,name)
        outputString += "}"
    generateLua(outputString,name, outputFolder)


def genLuaTableHelper(current,name,idx):
    if current is None:
        return "" 
    if current.image is None:
        return ""
    fileName = os.path.basename(current.image.filename)
    periodPos = fileName.rfind(".")
    fileName = fileName[:periodPos]
    right = genLuaTableHelper(current.right, name, idx)
    down = genLuaTableHelper(current.down, name, idx)
    return "\t[\"{fname}\"] = {{Sheet = {name}Sheet{idx}, Position = Vector2.new({p1}, {p2}), Size = Vector2.new({s1}, {s2})}};\n".format(
            name = name, 
            fname = fileName,
            p1 = current.position[0],
            p2 = current.position[1],
            s1 = current.image.size[0],
            s2 = current.image.size[1],
            idx = idx
    ) + right + down


def generateLuaTableOutput(trees, name):
    output = ""
    for idx, tree in enumerate(trees):
        if len(trees) == 1:
            idx = ""
        output += genLuaTableHelper(tree, name, idx)
    return output
        
# This function goes to a counter api which lets me see how this application is being used and what features are being used most often. No personal data is being sent or anything linkable to yourself
# Having the usage data allows me to better prioritize what features to update/make better 
# Please don't spam the api, this is an open source tool and this data helps me tremendously 
#def usageTrack(usecase):
    #requests.get('https://api.countapi.xyz/hit/SpriteSheetGenerator_Deploy1/' + usecase)


def init():
    print(BANNER)
    usageTrack("start")


def main():
    path = getImageFolder()
    init()
    name = getName()
    sprites = loadSprites(path)
    trees = []
    buildTree(trees,sprites)
    outputFolder = getOutputFolder(path)
    packImages(trees,name, outputFolder)
    outputType = getOutputType()
    generateLuaOutput(outputType,name,trees, outputFolder)
    print("Finished...")
    usageTrack("finished")
    time.sleep(1)   

