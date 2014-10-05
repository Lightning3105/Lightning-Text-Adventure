#####
#The main core function/script file for the Legend Of Aiopa Text Adventure
#Most of the functions included in the game are here
#####

#####
#All Module Imports

#Core Import All
from lightCore import * #@UnusedWildImport
import player
import world
import inventory
#General Modules
#import time #@UnusedImport
#import random #@UnusedImport
#import easygui #@UnresolvedImport @UnusedImport
#import sys #@UnusedImport @Reimport
#import atexit #@UnusedImport

#End Module Imports
#####

#####
#Setup print and pprint
#####
def print(string):  # @DontTrace @ReservedAssignment
    #easygui print
    easygui.msgbox(msg=string, title=world_time())

def pprint(pic, string):
    #easygui picture print
    easygui.msgbox(image=pic, msg=string, title=world_time())

#####
#Pictures
#####
Full_Bag = "Pics/Bag Full.png"
Fight_Symbol = "Pics/Fight.png"

#####
#PLAYER
#####

def player_damage(attacker, attackType, amount):
    #Deals damage to the player, displaying who did it
    print(attacker + " " + attackType + " " + player.Name + ". " + player.Name + " takes " + str(amount) + " damage")
    player.Health -= amount

    if player.Health < 1:
        player_die()

def player_die():
    #Displays the death message, and then returns you to your previous spot
    print("You collapse to the ground.")
    print("The world tumbles around you.")
    print("Your vision gets brighter and brighter, until...")
    #run(Last_Point)

def player_refresh():
    #Does a check of multiple player variables, checking if they make sense.
    if player.Health < 1:
        player_die()

def player_Xpa(xp):
    #Adds 'xp' XP to the players xp, checking if the player level can be increased
    player.Xp += xp
    while player.Xp > player.Xpn:
        if player.Xp > player.Xpn:
            player.Xpl += 1
            player.Xp -= player.Xpn
            player.Xpn *= 1.2
            player.Xpn = int(player.Xpn)

def player_defence():
    #Calculates the defence of a player
    TheOut = 1
    try:
        TheOut += int(getmet(player.Cloak, 1))
    except:
        TheOut += 0
    try:
        TheOut += int(getmet(player.Shirt, 1))
    except:
        TheOut += 0
    try:
        TheOut += int(getmet(player.Trouser, 1))
    except:
        TheOut += 0

    return int(TheOut)

def player_unEquip(item):
    #Unequips an item from the player
    debug("Un Equip")

    if item == "cloak":
        inventory_add(player.Cloak)
        player.Cloak = ""

    if item == "shirt":
        inventory_add(player.Shirt)
        player.Shirt = ""

    if item == "trouser":
        inventory_add(player.Trouser)
        player.Trouser = ""

def player_equip(item):
    #Equips an item to the player
    debug("equiping:")

    if getmet(item, 0) == "cloak":
        if player.Cloak == "":
            player.Cloak = item
            inventory_remove(item)

        else:
            inventory_remove(item)
            inventory_add(player.Cloak)
            player.Cloak = item




    if getmet(item, 0) == "shirt":
        if player.Shirt == "":
            player.Shirt = item
            inventory_remove(item)

        else:
            inventory_remove(item)
            inventory_add(player.Shirt)
            player.Shirt = item



    if getmet(item, 0) == "trouser":
        if player.Trouser == "":
            player.Trouser = item

            inventory_remove(item)

        else:
            inventory_remove(item)
            inventory_add(player.Trouser)
            player.Trouser = item

    else:
        print("Cannot equip a " + item)



def player_attack(tgt):
    #Player attacks 'tgt'
    debug("ATTACKING")
    tatt = getmet(tgt, 1)
    tdef = getmet(tgt, 2)
    tlife = getmet(tgt, 3)
    trnk = getmet(tgt, 4)
    taln = getmet(tgt, 5)
    target = getnam(tgt)

    weapons = []
    wdamage = []

    for i in range(0, len(inventory.Contents)):
        spl = getmet(inventory.Contents[i], 0)
        if spl == "weapon":
            weapons.append(getnam(inventory.Contents[i]))
            wdamage.append(getmet(inventory.Contents[i], 1))

    weapons.append("Your Fists")
    wdamage.append("2")

    #pprint(Fight_Symbol, player.Name + " (" + str(player.Health) + ", " + str(player_defence()) + ")" + " Attacks " + target + " (" + str(tlife) + ", " + str(tdef) + ")" + "!")
    pprint(Fight_Symbol, player.Name + " (Level " + str(player.Xpl) + ")" + " Attacks " + str(target) + " (Level " + str(trnk) + ")" + "!")
    att_weapon = easygui.choicebox(msg="Chose your weapon", choices=(weapons))

    patt = 0

    for i in range(0, len(weapons)):
        if weapons[i] == att_weapon:
            patt = int(wdamage[i])

    while True:
        ###Choose Attacker###
        rnd = random.randint(1,2)
        PtE = int( patt * (1 + random.random())- int(tdef))
        EtP = int( int (tatt) * (1 + random.random()) - player_defence())
        tlife = int(tlife)
        if PtE < 0:
            PtE = 0

        if EtP < 0:
            EtP = 0

        if rnd == 1:
            ###Player Attacks###
            print(player.Name + " Attacks!")
            print(player.Name + " Deals " + str(PtE) + " Damage To " + target)
            tlife -= PtE
            print(target + " Is Now On " + str(tlife) + " Health.")


            if tlife < 1:
                print("You defeat " + target + ".")
                pxp = int((int(trnk) + 1) * (random.randint(1, 3) + random.random()))
                print("you gain " + str(pxp) + " XP!")
                pka = int(int(trnk) * (random.randint(1, 2) + random.random()))
                player_Xpa(pka)
                if taln == "g":
                    print(target + " was good." + "You lose" + str(pka) + " karma")
                    player.Karma -= pka
                if taln == "e":
                    print(target + "was evil." + "You gain" + str(pka) + " karma")
                    player.Karma += pka
                return "win"

            print(target + " Deals " + str(EtP) + " Damage To " + player.Name)
            player.Health -= EtP
            print(player.Name + " Is Now On " + str(player.Health) + " Health.")


            if player.Health < 1:

                player_die()


        if rnd == 2:
            ###Opponent Attacks###
            print(target + " Attacks!")
            print(target + " Deals " + str(EtP) + " Damage To " + player.Name)
            player.Health -= EtP
            print(player.Name + " Is Now On " + str(player.Health) + " Health.")

            if player.Health < 1:
                player_die()

            print(player.Name + " Deals " + str(PtE) + " Damage To " + target)
            tlife -= PtE
            print(target + " Is Now On " + str(tlife) + " Health.")


            if tlife < 1:
                return "win"


#####
#END PLAYER
#####

#####
#INVENTORY
#####

def inventory_add(item):
    debug("ADD TO INVENTORY:")
    if 1 + len(inventory.Contents) > inventory.Size:
        spaceleft = inventory.Size - len(inventory.Contents)
        things = len(item)
        pprint(Full_Bag, "You Can't fit " + str(things) + " More item in a bag that can only hold " + str(spaceleft) + " more items!")

        INV_A_DC = easygui.choicebox(msg="What to discard: (cancel to not discard anything)", choices=(inventory.Contents))
        if not INV_A_DC == None:
            inventory_remove(INV_A_DC)
        if INV_A_DC == None:
            return

    else:
        if type(item) == tuple:
            inventory.Contents.append(item)

        if type(item) == list:
            for i in range(len(item)):

                inventory.Contents.append(item[i])




def inventory_get():
    debug("INVENTORY")
    debug("CONTENTS:\n" + str(inventory.Contents))
    ##Finding Money##
    for i in range(0, len(inventory.Contents)):
        spl = getmet(inventory.Contents[i], 0)
        if spl == "money":
            amt = getmet(inventory.Contents[i], 1)
            amti = int(amt)
            type(amti)
            inventory.Money += amti
            del inventory.Contents[i]
            break

    if inventory.Money % 10 == 0:
        inventory.Money = 0

    ##adding money string to inventory###

    mstring = "You Have: " + str(inventory.Money) + " Gold"
    mstringd = "Your small bag of money full of coins that are known as 'gold' by the comoners"
    mstringm = ""
    inventory.Contents.append((mstring, mstringd, mstringm))

    ##done money##

    ##adding equipped items to inventory##

    estring1 = "You Have Equipped: "
    try:
        if not player.Cloak == "":
            estring2 = player.Cloak[0]
            estring2d = player.Cloak[1]
            estring2m = "e|cloak"

        if player.Cloak == "":
            estring2 = "No Cloak"
            estring2d = "Your not wearing a cloak"
            estring2m = ""
    except:
        estring2 = "No Cloak"
        estring2d = "Your not wearing a cloak"
        estring2m = ""

    try:
        if not player.Shirt == "":
            estring3 = player.Shirt[0]
            estring3d = player.Shirt[1]
            estring3m = "e|shirt"

        if player.Shirt == "":
            estring3 = "No Extra Shirt"
            estring3d = "Your not wearing any extra shirt"
            estring3m = ""
    except:
        estring3 = "No Extra Shirt"
        estring3d = "Your not wearing an extra shirt"
        estring3m = ""

    try:
        if not player.Trouser == "":
            estring4 = player.Trouser[0]
            estring4d = player.Trouser[1]
            estring4m = "e|trouser"

        if player.Trouser == "":
            estring4 = "No Extra Trouser"
            estring4d = "Your not wearing any over trousers"
            estring4m = ""
    except:
        estring4 = "No Extra Trouser"
        estring4d = "Your not wearing any over trousers"
        estring4m = ""

    inventory.Contents.append((estring1 + estring2,estring2d, estring2m))
    inventory.Contents.append((estring1 + estring3,estring3d, estring3m))
    inventory.Contents.append((estring1 + estring4,estring4d, estring4m))

    ##adding player stats##
    pstring = "Your Statistics"
    pstringd = "Your Stats:\n" + "Health: " + str(player.Health) + "\nDefence: " + str(player_defence())
    pstringm = ""
    inventory.Contents.append((pstring, pstringd, pstringm))

    ##showing inventory##

    vop = easygui.choicebox(msg = "Your Inventory:", choices=(getnam(inventory.Contents)))

    vop = find_tup(vop, inventory.Contents)

    inventory.Contents.remove((mstring, mstringd, mstringm))
    inventory.Contents.remove((pstring, pstringd, pstringm))
    inventory.Contents.remove((estring1 + estring2,estring2d, estring2m))
    inventory.Contents.remove((estring1 + estring3,estring3d, estring3m))
    inventory.Contents.remove((estring1 + estring4,estring4d, estring4m))

    debug("\n VOP:")
    debug(vop)

    if vop == None:
        return "exit"

    if type(vop) == list:
        vop = vop[0]

    if getmet(vop, "all") == "i":
        #Is it an average item?
        pprint(Full_Bag, getdes(vop))

    if searchmet("e", vop) == "T":
        #Is it an equipped item?
        IgI = easygui.buttonbox(image=Full_Bag, msg=getdes(vop), choices=("Back", "Un Equip"))
        if IgI == "Un Equip":
            player_unEquip(getmet(vop, 1))

    if searchmet("c", vop) == "T":
        #Is it an eqipable item?
        IgI = easygui.buttonbox(image=Full_Bag, msg=getdes(vop), choices=("Back", "Equip"))
        if IgI == "Equip":
            player_equip(vop)

    else:
        verb = "Use"
        if searchmet("book", vop) == "T":
            verb = "Read"

        IgI = options(Full_Bag, getdes(vop), "Discard", verb, "Back")

        if IgI == "Discard":
            inventory_remove(vop)
        if IgI == verb:
            if getmet(vop, 0) == "book":
                read(vop)
            #other items


    inventory_get()
    return

def inventory_remove(item):
    inventory.Contents.remove(item)

#####
#END INVENTORY
#####

#####
#WORLD
#####

def world_time():
    if world.Day % 10 == 1:
        world.Dayp = "st"
    if world.Day % 10 == 2:
        world.Dayp = "nd"
    if world.Day % 10 == 3:
        world.Dayp = "rd"
    if world.Day % 10  == 0:
        world.Dayp = "th"
    if world.Day % 10 > 3:
        world.Dayp = "th"

    TheOut = str(world.Hour) + ":" + str(world.Minute) + "0" + " " + str(world.Day) + str(world.Dayp) + " of " + str(world.Month)

    #str(TheOut)
    return TheOut

#####
#END WORLD
#####

def getmet(item, metno):
    #Gets the metadata from a tuple (item)
    #finds the correct metadata by number (metno)
    TheOut = None

    if type(item) == tuple:
        TheOut = item[2].split('|')[metno]

        if metno == "all":
            TheOut = item[2]

    if type(item) == list:
        TheOut = item[0][2].split('|')[metno]
        if metno == "all":
            TheOut = item[0][2]

    return TheOut

def getdes(item):
    #Gets the description from a tuple (item)
    TheOut = item[1]
    return TheOut

def getnam(item):
    #Gets the name from a tuple (item)
    if type(item) == tuple:
        TheOut = item[0]
        return TheOut
    if type(item) == list:
        TheOut = t(item, 0)
        return TheOut

def searchmet(string, item):
    #string = what we want to find
    #item = tuple/string we want to search
    if type(item) == tuple:
        item = getmet(item, "all")

    for i in len(item.split('|')):
        if item.split('|')[i] == string:
            return "T"

    return "F"

def input(string):  # @ReservedAssignment
    #Creates an enter box with a string, and the time as the title
    TheInput = easygui.enterbox(msg=string, title=world_time())
    return TheInput

def options(pic, string, op1, op2, op3=None, op4=None):
    #creates an button box with 2, up to 4 choices
    if not op4 == None:
        TheOut = easygui.buttonbox(choices=(op1, op2, op3, op4, "Inventory"), msg=string, image=pic, title=world_time())
    if op4 == None:
        TheOut = easygui.buttonbox(choices=(op1, op2, op3, "Inventory"), msg=string, image=pic, title=world_time())
    if op4 and op3 == None:
        TheOut = easygui.buttonbox(choices=(op1, op2, "Inventory"), msg=string, image=pic, title=world_time())

    if TheOut == "Inventory":
        inventory_get()
        TheOut = options(pic, string, op1, op2, op3, op4)

    return TheOut

def move(choices):
    #Shows a choicebox with places that the player can move to
    #returns the selection

    choices = [i for i in choices if searchmet("building", i) == "T"]

    TheOut = easygui.choicebox(msg="Move To:", choices=(t(choices, 0)))

    TheOut = find_tup(TheOut, choices)

    return TheOut

def find_tup(item, lis):
    #gets a one or multiple string/s
    #item = the string/s
    #lis = the list it has to search through
    TheOut = []

    if type(item) == list:

        for i in range(0, len(item)):

            for t in range(0, len(lis)):

                if lis[t][0] == item[i]:

                    TheOut.append(lis[t])
                    break
        return TheOut

    if type(item) == str:


        for t in range(0, len(lis)):

            if lis[t][0] == item:

                TheOut = lis[t]

                return TheOut

def view(items, string=""):
    #Creates a choicebox from a list
    #Can use a string, by default shows 'you can see:'

    TheOut = ""
    str(TheOut)

    if string == "":
        TheOut = easygui.choicebox(msg="You Can See:", choices=(t(items, 0)), title=world_time())

    else:
        TheOut = easygui.choicebox(msg=string, choices=(t(items, 0)), title=world_time())


    TheOut = find_tup(TheOut, items)

    print(TheOut[1])


    return TheOut

def take(string, choices, mmax):
    #Takes an item and places it into the players inventory
    #Returns the item
    debug("TAKING")

    choices = [i for i in choices if searchmet("i", i) == "T"]

    TheOut = easygui.multchoicebox(msg=string, choices=(t(choices, 0)))

    if TheOut == None:
        return

    if len(TheOut) > mmax:
        return

    else:

        inventory_add(find_tup(TheOut, choices))
        return find_tup(TheOut, choices)

def read(item):
    book = getnam(item)
    book = book.split(':')[1]
    book = book.replace(" ", "")
    importVar(book)
    print("Knowledge Acquired! " + getmet(item, 1) + "!")
    player.Knowledge.append(getmet(item, 1))

def player_picture():
    pic1 = "Pics/Player_1.png"
    pic2 = "Pics/Player_2.png"
    pic3 = "Pics/Player_3.png"
    pic4 = "Pics/Player_4.png"

    picno = 1

    while True:
        if picno == 1:
            c = easygui.buttonbox(msg="What will you look like?", title="Character Creation", choices=("<---", "SELECT", "--->"), image=pic1)
            if c == "<---":
                picno = 4
            if c == "SELECT":
                player.Picture = pic1
                return
            if c == "--->":
                picno += 1
        if picno == 2:
            c = easygui.buttonbox(msg="What will you look like?", title="Character Creation", choices=("<---", "SELECT", "--->"), image=pic2)
            if c == "<---":
                picno -= 1
            if c == "SELECT":
                player.Picture = pic2
                return
            if c == "--->":
                picno += 1
                if picno > 4:
                    picno = 1
        if picno == 3:
            c = easygui.buttonbox(msg="What will you look like?", title="Character Creation", choices=("<---", "SELECT", "--->"), image=pic3)
            if c == "<---":
                picno -= 1
            if c == "SELECT":
                player.Picture = pic3
                return
            if c == "--->":
                picno += 1
                if picno > 4:
                    picno = 1
        if picno == 4:
            c = easygui.buttonbox(msg="What will you look like?", title="Character Creation", choices=("<---", "SELECT", "--->"), image=pic4)
            if c == "<---":
                picno -= 1
            if c == "SELECT":
                player.Picture = pic4
                return
            if c == "--->":
                picno += 1
                if picno > 4:
                    picno = 1

def player_name():
    player.Name = easygui.enterbox(msg="What will you be known as?", title="Character Creation", image=player.Picture)
    return

