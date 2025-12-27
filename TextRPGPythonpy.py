from random import randint
from random import choice
import pickle
import pymysql as mysql
import copy
def main():
    chars = pickle.load(open('characters.dat', 'rb'))
    #Structure of characters.dat
    #chars = {
    #    'MainCharacter':{'Name':'', 'Sex':'', 'Class':'', 'Stats':{'Health':100, 'Defense':5,'Level':0 ,'XP':0}, 'Money':0, 'Moves':{'Attacks   ':{}, 'Defense':{}}, 'Inventory':['Small health potion', 'Medium health potion','Large health potion'],'Choices':{'Ally':''},'Progress':''},
    #    'BanditLeader':{'Name':'Bandit Leader', 'Sex':'Male', 'Class':'Bandit', 'Stats':{'Health':125}, 'Moves':{'Attacks':{'Throwing Axe':13,'Strike':18}, 'Defense':{}}, 'Inventory':[None]},
    #    'Bandit':{'Name':'Bandit', 'Sex':'Male', 'Class':'Bandit', 'Stats':{'Health':75}, 'Moves':{'Attacks':{'Strike':13,'Bleed':10}, 'Defense':{}}, 'Inventory':[None]},
    #    'Goblin':{'Name':'Goblin', 'Sex':'Undefined', 'Class':'Humanoid Monster', 'Stats':{'Health':60}, 'Moves':{'Attacks':{'Scratch':15,'Bleed':12}, 'Defense':{}}, 'Inventory':[None]},
    #    'Gorgon':{'Name':'Gorgon', 'Sex':'Undefined', 'Class':'Humanoid Monster', 'Stats':{'Health':70}, 'Moves':{'Attacks':{'Freeze':15,'Slap':20}, 'Defense':{}}, 'Inventory':[None]},
    #    'Hostile Nordwin Warrior':{'Name':'Hostile Nordwin Warrior', 'Sex':'Male', 'Class':'Nordwin', 'Stats':{'Health':80}, 'Moves':{'Attacks':{'Stab':16,'Kick':11}, 'Defense':{}}, 'Inventory':[None]}
    #    } 
    items = {
        'Health Consumables':{'Small health potion':20, 'Medium health potion':40, 'Large health potion':60, 'Defense boost':40}
        }
    menu(chars, items)

def menu(chars, items):
    while True:
        menu_input = input(
""" 
 ------------------------TextRPG----------------------------------
1. New Game
2. Load Character
3. Exit
              
Input: """
        )  
        if menu_input=='1':
            print('\n'*40)
            ally_choice_1 = new_game(chars, chars['MainCharacter'], items) 
            chars['MainCharacter']['Choices']['Ally'] = ally_choice_1
            chars['MainCharacter']['Progress'] = 'Act 1.0'
            save(chars)
            print('\n\n----ACT 1----')
            act1(chars, chars['MainCharacter'], items, chars['MainCharacter']['Choices']['Ally'])
            cathedral_and_beyond(chars, chars['MainCharacter'], items, chars['MainCharacter']['Choices']['Ally'])          
        elif menu_input=='2':
            while True:
                name = input('Enter character name: ').strip()
                try:
                    with open('savefile'+'_'+name+'.dat', 'rb') as file:
                        MainChar = pickle.load(file)
                        chars['MainCharacter'] = MainChar
                        print("Character loaded successfully.")
                        while True:
                            menu_input = input('''
    1. Continue
    2. View Character History
    Prompt: ''')
                            if menu_input=='1':
                                if chars['MainCharacter']['Progress'] == 'Act 1.0': #For demo purposes, setting progress to Act 1.0
                                    act1(chars, chars['MainCharacter'], items, chars['MainCharacter']['Choices']['Ally'])
                                else:
                                    print("Save Corrupted. Unable to load progress.")
                                    break
                            elif menu_input=='2':
                                print('\n\nCharacter History:')
                                connection = mysql.connect(
                                host='localhost',
                                user='root',
                                password='1234',
                                database='textrpg_'+chars['MainCharacter']['Name']
                                )
                                cursor = connection.cursor()
                                cursor.execute("SELECT * FROM enemies")
                                rows = cursor.fetchall()
                                for row in rows:
                                    print(row)
                                cursor.close()
                                connection.close()
                            else:
                                print('Invalid input, try again.')
                except FileNotFoundError:
                    print('Save file not found. Please try re-entering the name.')
                except Exception as error:
                    print('An error occurred while loading the character:', str(error))
        elif menu_input=='3':
            exit()
def lookforfight(chars, MainChar, items):
    print('''
You take a stroll outside in the wild looking for some adventure...


                  ''')
    if randint(0,100)>=60:
        print("You find yourself in an ambush!")
        while True:
            random_enemy = choice(tuple(chars.keys()))
            if random_enemy != 'MainCharacter':
                Victory = combat([chars[random_enemy]], MainChar, items, runaway=True)
                if Victory == True:
                    print("\n\nYou return back to the town after the victory, resting and replinishing yourself.")
                    break
                elif Victory == False:
                    print("\n\nYou return back to the town after the defeat, resting and replinishing yourself.")
                    break
        return
    elif randint(0,100)<60:
        print("Nothing exciting happens.")

def journal():
    while True:
                journal_choice = input('''
        Use the Journal to keep track of thoughts on your journey.
                                       
        Journal:
        1. Add Entry
        2. View Entries
        3. Erase Last Entry
        4. Back to Main Menu

        Prompt: ''')
                if journal_choice == '1':
                    entry = input("Write your journal entry: ").strip()
                    if entry!='':
                        MainChar['Journal'].append(entry)  
                        print("Entry added.")
                    else:
                        print("Entry cannot be empty.")
                elif journal_choice == '2':
                    if MainChar['Journal']!=[]:
                        print('Total Entries:', len(MainChar['Journal']))
                        print("Journal Entries (Last Page to First Page):") #Last in, First Out principle and stuff
                        len_journal = len(MainChar['Journal'])
                        for i in range(len_journal-1, -1, -1): # Just looping in reverse in a way that should be ideal for lists I think
                            print(MainChar['Journal'][i])
                            if i == 0:
                                print("----- End of Journal -----")
                                break
                            menu_input=input("\n\n\n1. Next Page\n2. Back to Journal Menu") 
                            if menu_input=='1':
                                print("------------------- Next Page ------------------")
                                continue
                            elif menu_input=='2':
                                break
                            else:
                                print("Invalid input, returning to journal menu.")
                                break
                    else:
                        print("Journal is empty.")
                elif journal_choice == '3':
                    if MainChar['Journal']!=[]:
                        print('Entry deleted:', MainChar['Journal'].pop())
                    else:
                        print("Journal is empty, nothing to erase.")
                elif journal_choice == '4':
                    break
                else:
                    print("Invalid input.")

def shop(MainChar):
    print(f'''
Narrator: You enter the shop, it almost seems empty, makes sense given the war. The shopkeeper passes you a ledger with the list of items available, not keen to talk, here is the list of items:
Money:{MainChar['Money']} coins
                  
1. Small health potion - 50 coins
2. Medium health potion - 100 coins
3. Large health potion - 150 coins
4. Defense boost - 125 coins
                  ''')
    while True:
        action = input('Prompt to buy: ')
        if action=='1':
            if MainChar['Money'] >= 50:
                MainChar['Money']-=50
                MainChar['Inventory'].append('Small health potion')
                print('Purchased successfully.')
                break
            else:
                print("Not enough money.")
        elif action=='2':
            if MainChar['Money'] >= 100:
                MainChar['Money']-=100
                MainChar['Inventory'].append('Medium health potion')
                print('Purchased successfully.')
                break
            else:
                print("Not enough money.")
        elif action=='3':
            if MainChar['Money'] >= 150:
                MainChar['Money']-=150
                MainChar['Inventory'].append('Large health potion')
                print('Purchased successfully.')
                break
            else:
                print("Not enough money.")
        elif action=='4':
            if MainChar['Money'] >= 125:
                MainChar['Money']-=125
                MainChar['Inventory'].append('Defense boost')
                print('Purchased successfully.')
                break
            else:
                print("Not enough money.")
        else:
            print("################### WRONG INPUT ########################")
            break

def levelup(PC):
    levelup_xp = 100
    while PC['Stats']['XP'] >= levelup_xp:
        PC['Stats']['Level'] += 1
        PC['Stats']['XP'] -= levelup_xp
        PC['Stats']['Health'] += 20
        PC['Stats']['Defense'] += 5
        print("\n\nCongratulations! You've leveled up to Level", PC['Stats']['Level'])
        print("Health increased to:", PC['Stats']['Health'])
        print("Defense increased to:", PC['Stats']['Defense'])
        levelup_xp += 100

def save(chars):
    with open('savefile'+'_'+chars['MainCharacter']['Name']+'.dat', 'wb') as file:
                pickle.dump(chars['MainCharacter'], file)
    print("Game Saved Successfully.")

def recorddata(enemies, PC, Victory):
    if Victory==True:
            Victory='Won'
    elif Victory==False:
            Victory='Lost'
    try:
        connection = mysql.connect(
            host='localhost',
            user='root',
            password='1234',
        )
    except Exception as e:
        print("Error connecting to MySQL database:", e)
        print("Data not being recorded, please check your MySQL settings.")
        return
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS textrpg_"+PC['Name']) #Create the database if it doesn't exist
    cursor.execute("USE textrpg_"+PC['Name'])  # Select the database
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS enemies (
            Enemies varchar(255),
            Victory varchar(5),
            Timestamp DATETIME DEFAULT NOW()
        )
    """)
    record_enemy = ''
    for enemy in range(len(enemies)):
        record_enemy += '_'+enemies[enemy]['Name']
    cursor.execute("INSERT INTO enemies (Enemies, Victory) VALUES (%s, %s)",
                    (record_enemy, Victory))
    connection.commit()
    cursor.close()
    connection.close()

def combat(og_enemy, PC, items, runaway=True, sql=True):
    print('You are now engaged in a battle with: ')
    enemies = copy.deepcopy(og_enemy)
    for enemy in range(len(enemies)):
        print(enemies[enemy]['Name'])
    print('\n\n\n')
    EnemyAlive=True
    while PC['Stats']['Health']>0 and EnemyAlive==True:
        move = input('''
1. Moves
2. Inventory
3. Run Away


Prompt: ''')
        
        if move=='1':
            print('1. Attacks: ')
            for PCattacks in PC['Moves']['Attacks']:
                print(PCattacks)
            print('\n2. Defenses: ')
            for defenses in PC['Moves']['Defense']:
                print(defenses)
            atk_or_def = input("\nPrompt: ")
            while True:
                if atk_or_def == '1' and len(tuple(PC['Moves']['Attacks'].keys()))>0:
                    PCattacks = PC['Moves']['Attacks']
                    PCatk_Index = tuple(PC['Moves']['Attacks'].keys())
                    for atks in range(len(PCatk_Index)):
                        print(str(atks+1)+'. '+PCatk_Index[atks])
                    while True:
                        PCattack = input("\nChoose an attack: ")                   
                        if PCattack == '1' and len(PCatk_Index)>0:
                            for enemy in range(len(enemies)):
                                enemy_attack_dict = enemies[enemy]['Moves']['Attacks']
                                enemy_attack_list = tuple(enemies[enemy]['Moves']['Attacks'].keys())
                                
                                if enemies[enemy]['Stats']['Health'] < 0:
                                    continue    
                                else:
                                    enemies[enemy]['Stats']['Health'] = enemies[enemy]['Stats']['Health']-PCattacks[PCatk_Index[int(PCattack)-1]]
                                if (randint(0,100)+PC['Stats']['Defense'])>90 or enemies[enemy]['Stats']['Health']<=0:
                                    print("\nAttack dodged.")
                                    print(enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                    
                                else:    
                                    enemy_attack = choice(enemy_attack_list)
                                    print('\n'+enemies[enemy]['Name']+' uses '+enemy_attack)
                                    PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[enemy_attack]
                                    print('\n'+enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health'])+'\n')
                            
                            
                                                           
                                
                        elif PCattack == '2' and len(PCatk_Index)>1:
                            for enemy in range(len(enemies)):
                                enemy_attack_dict = enemies[enemy]['Moves']['Attacks']
                                enemy_attack_list = tuple(enemies[enemy]['Moves']['Attacks'].keys())
                                
                                if enemies[enemy]['Stats']['Health'] < 0:
                                    continue    
                                else:
                                    enemies[enemy]['Stats']['Health'] = enemies[enemy]['Stats']['Health']-PCattacks[PCatk_Index[int(PCattack)-1]]
                                if (randint(0,100)+PC['Stats']['Defense'])>90:
                                    print("\nAttack dodged.")
                                    print(enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                    
                                else:    
                                    enemy_attack = choice(enemy_attack_list)
                                    print('\n'+enemies[enemy]['Name']+' uses '+enemy_attack)
                                    PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[enemy_attack]
                                    print('\n'+enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health'])+'\n')
                                
                        elif PCattack == '3' and len(PCatk_Index)>2:
                            for enemy in range(len(enemies)):
                                enemy_attack_dict = enemies[enemy]['Moves']['Attacks']
                                enemy_attack_list = tuple(enemies[enemy]['Moves']['Attacks'].keys())
                                
                                if enemies[enemy]['Stats']['Health'] < 0:
                                    continue    
                                else:
                                    enemies[enemy]['Stats']['Health'] = enemies[enemy]['Stats']['Health']-PCattacks[PCatk_Index[int(PCattack)-1]]
                                if (randint(0,100)+PC['Stats']['Defense'])>90:
                                    print("\nAttack dodged.")
                                    print(enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                    
                                else:    
                                    enemy_attack = choice(enemy_attack_list)
                                    print('\n'+enemies[enemy]['Name']+' uses '+enemy_attack)
                                    PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[enemy_attack]
                                    print('\n'+enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health'])+'\n')
                                
                                
                        elif PCattack == '4' and len(PCatk_Index) == 4:
                            for enemy in range(len(enemies)):
                                enemy_attack_dict = enemies[enemy]['Moves']['Attacks']
                                enemy_attack_list = tuple(enemies[enemy]['Moves']['Attacks'].keys())
                                
                                if enemies[enemy]['Stats']['Health'] < 0:
                                    continue    
                                else:
                                    enemies[enemy]['Stats']['Health'] = enemies[enemy]['Stats']['Health']-PCattacks[PCatk_Index[int(PCattack)-1]]
                                if (randint(0,100)+PC['Stats']['Defense'])>90:
                                    print("\nAttack dodged.")
                                    print(enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                    
                                else:    
                                    enemy_attack = choice(enemy_attack_list)
                                    print('\n'+enemies[enemy]['Name']+' uses '+enemy_attack)
                                    PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[enemy_attack]
                                    print('\n'+enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health'])+'\n')
                        else:
                            print('Wrong input')
                            continue 
                        break
                                
                        
                        
                elif atk_or_def == '2' and len(tuple(PC['Moves']['Defense'].keys()))>0:
                    PC_defs_dict = PC['Moves']['Defense']
                    PC_defs = tuple(PC['Moves']['Defense'].keys())
                    for defss in range(len(PC_defs)):
                        print(str(defss+1)+'. '+PC_defs[defss])
                    while True:
                        PCdefense = input("Choose a defense: ")                   
                        if PCdefense == '1' and len(PC_defs)>0:
                            for enemy in range(len(enemies)):
                                enemy_attack_dict = enemies[enemy]['Moves']['Attacks']
                                enemy_attack_list = tuple(enemies[enemy]['Moves']['Attacks'].keys())
                                PC['Stats']['Defense'] += PC_defs_dict[PC_defs[int(PCdefense)-1]]
                                if (randint(0,100)+PC['Stats']['Defense'])>90:
                                    print("\nAttack dodged.")
                                    print(enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))                                    
                                else:    
                                    enemy_attack = choice(enemy_attack_list)
                                    print('\n'+enemies[enemy]['Name']+' uses '+enemy_attack)
                                    PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[enemy_attack]
                                    print('\n'+enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health'])+'\n')
                                
                        elif PCdefense== '2' and len(PC_defs)>1:
                            for enemy in range(len(enemies)):
                                enemy_attack_dict = enemies[enemy]['Moves']['Attacks']
                                enemy_attack_list = tuple(enemies[enemy]['Moves']['Attacks'].keys())
                                PC['Stats']['Defense'] += PC_defs_dict[PC_defs[int(PCdefense)-1]]
                                if (randint(0,100)+PC['Stats']['Defense'])>90:
                                    print("\nAttack dodged.")
                                    print(enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))                                    
                                else:    
                                    enemy_attack = choice(enemy_attack_list)
                                    print('\n'+enemies[enemy]['Name']+' uses '+enemy_attack)
                                    PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[enemy_attack]
                                    print('\n'+enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health'])+'\n')
                                
                        elif PCdefense == '3' and len(PC_defs)>2:
                            for enemy in range(len(enemies)):
                                enemy_attack_dict = enemies[enemy]['Moves']['Attacks']
                                enemy_attack_list = tuple(enemies[enemy]['Moves']['Attacks'].keys())
                                PC['Stats']['Defense'] += PC_defs_dict[PC_defs[int(PCdefense)-1]]
                                if (randint(0,100)+PC['Stats']['Defense'])>90:
                                    print("\nAttack dodged.")
                                    print(enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))                                    
                                else:    
                                    enemy_attack = choice(enemy_attack_list)
                                    print('\n'+enemies[enemy]['Name']+' uses '+enemy_attack)
                                    PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[enemy_attack]
                                    print('\n'+enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health'])+'\n')
                                
                        elif PCdefense == '4' and len(PC_defs)>3:
                            for enemy in range(len(enemies)):
                                enemy_attack_dict = enemies[enemy]['Moves']['Attacks']
                                enemy_attack_list = tuple(enemies[enemy]['Moves']['Attacks'].keys())
                                PC['Stats']['Defense'] += PC_defs_dict[PC_defs[int(PCdefense)-1]]
                                if (randint(0,100)+PC['Stats']['Defense'])>90:
                                    print("\nAttack dodged.")
                                    print(enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))                                    
                                else:    
                                    enemy_attack = choice(enemy_attack_list)
                                    print('\n'+enemies[enemy]['Name']+' uses '+enemy_attack)
                                    PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[enemy_attack]
                                    print('\n'+enemies[enemy]['Name']+"'s health: " + str(enemies[enemy]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health'])+'\n')
                        else:
                            print('Wrong input')
                            continue
                        break        
                            
                else:
                    print("################### Wrong Input, try again. ###################")
                for health_of_enemies in range(len(enemies)):
                                if enemies[health_of_enemies]['Stats']['Health'] > 0:
                                    EnemyAlive = True 
                                    break
                                else:
                                    EnemyAlive = False  
                break    
            
        elif move=='2':
            if len(PC['Inventory'])>0:
                for item in PC['Inventory']:
                    print(item)
                item_input = input('Select Item: ').strip().lower().capitalize()
                if item_input in PC['Inventory']:
                    if item_input in items['Health Consumables']:
                        PC['Stats']['Health'] += items['Health Consumables'][item_input]
                        PC['Inventory'].remove(item_input)
                        print("Health regained.\nHealth is now: ", PC['Stats']['Health'])
                    else:
                        print('Unexpected bug, please refrain from using this item and report the issue to the developer ~ Yuvraj')
                    
                else:
                    print('Item not in inventory')
            elif len(PC['Inventory'])==0:
                print("Empty Inventory.")
        elif move=='3':
            if runaway==True:
                if randint(0,100)>70:
                    print("You ran away successfully.")
                    del(enemies)
                    return 
                elif randint(0,100)<=70:
                    print("Unable to run away from this fight. You are hit while trying to run away.")
                    PC['Stats']['Health']-=20
                    runaway=='Failed'
            elif runaway==False:
                print("Your character cannot avoid this fight.")
            elif runaway=='Failed':
                    print("Unable to run away from this fight. You are hit while trying to run away.")
                    PC['Stats']['Health']-=20
            else:
                print('Unknown Bug Encountered, terminating program...')
                runaway = 'BAD'
                return runaway
        else:
            print("################### Wrong Input, try again. ###################")
            continue
    if PC['Stats']['Health'] <= 0:
        Victory=False
        PC['Stats']['Health'] = 100
        money_lost = randint(0,30)
        if PC['Money']>money_lost:
            PC['Money'] -= money_lost
            print("Some of your money was lost upon defeat...")
        if sql==True:
            recorddata(enemies, PC, Victory)
        for health_of_enemies in range(len(enemies)):
            enemies[health_of_enemies]['Stats']['Health'] = enemies[health_of_enemies]['Stats']['Health']+50
        return Victory
    elif EnemyAlive==False:
        print("\n\nNarrator: You have won the battle.")
        money_earned = randint(0,80)
        xp_earned = randint(0,100)
        PC['Money'] += money_earned
        PC['Stats']['XP'] += xp_earned
        PC['Stats']['Health'] += 5
        if PC['Stats']['Health']>100:
            PC['Stats']['Health']=100
        print("You earned", money_earned, "coins")
        print("Total balance:", PC['Money'])
        print("XP Earned:", xp_earned)
        print("Total XP:", PC['Stats']['XP'])
        Victory=True
        levelup(PC)
        if sql==True:
            recorddata(enemies, PC, Victory)
        return Victory    
            
            
        

def new_game(chars, MainChar, items):
    #Character's Sex
    while True:
        MainChar['Sex'] = input("""1. Male 
2. Female
Select Gender of the character: """
                            )
        if MainChar['Sex'] == '1':
            MainChar['Sex'] = 'Male'
            break
        elif MainChar['Sex'] == '2':
            MainChar['Sex'] = 'Female'
            break
        else:
            print("################### Wrong Input, try again. ###################")
            
    #Character's Class
    
    
    print('\nNarrator: \n' +
'"You awaken in the ruins of a once-glorious kingdom. The air is thick with the scent of ash, and your mind is a blank slate, you have no memories of anything."'
+ "You know one thing: the answers to your lost past lie in the heart of Eldevar, you recall the mild details of this place, where you are now stranded suddenly" 
+' where as is well known, the legendary Staff of Zorith is said to hold the flow of all magic in the world itself."')
    
    while True:
        MainChar['Class'] = input('''
Prompt:
"Who are you?"

1. Warrior (Chief of War from Norwind)
(You were part of Norwind's conquest, a fierce captain with a straight sword. Now, you have no memory of your role in the war.)

2. Mage (Defender of Eldevar)
(You once fought to defend Eldevar with arcane might, but the war and the staff's magic took everything from you, including your memories.)

Narrator:"You are... "\n\n'''
                            ).strip().lower()
        if MainChar['Class'] == "1" or MainChar['Class'] == "warrior":
            MainChar['Class'] = 'Warrior'
            MainChar['Moves']['Attacks'] = {'Lunge':20}
            MainChar['Moves']['Defense'] = {'Brace':15}
            break
        elif MainChar['Class'] == "2" or MainChar['Class'] == "mage":
            MainChar['Class'] = 'Mage'
            MainChar['Moves']['Attacks'] = {'Zap':30}
            MainChar['Moves']['Defense'] = {'Mist':8}
            break
        else:
            print("Wrong Input, try again.")
    print('"A', MainChar['Class']+'"')
    
    MainChar['Name'] = input("\n\nPrompt: \n" +
'"What is your name?"\n Narrator: "Your name is...."\n\n') #Assign's Ma in character's name
    print('"'+MainChar['Name']+'"')
    
    
    print('''
          
"The ruins stretch out before you, the remains of the kingdom of Eldevar, its once-proud walls now crumbling under the weight of time and war. You have no memory of how you got here... but you feel the pull of something important, something you need to find. The Staff of Zorith... Yes, it holds the key to your past. If you can find it, you will regain your memories."''')
    print('''\n"As you begin walking through the ruins, you hear voices nearby, tense but not hostile. You instinctively hide behind a fallen pillar, peeking around to see two figures in the distance, engaged in a heated conversation."

(The camera pans out to show Kornak, a battle-hardened warrior, and Selena, a fierce-looking mage knight. They stand at odds, though they haven’t drawn their weapons... yet.)''')
    print('''
Kornak (gruffly):
"It doesn’t matter what you think, Selena. The Staff is the only way to restore what’s been lost. You know that as well as I do."''')
    print('''
Selena (angrily):
"Restore? Is that what you call it? The staff is cursed, Kornak! If we let it fall into the wrong hands again, it’ll destroy what little is left of Eldevar!"''') 
    print('''
Narrator:
"They argue, their voices growing louder. You realize now that these two are key players in the conflict that destroyed Eldevar—and you must choose whether to reveal yourself or listen a little longer."

(This gives you a moment to decide your approach.)''')
   
    hide_or_reveal = input("\n1. Approach them\n2. Eavesdrop\nPrompt: ").lower().strip()
    if hide_or_reveal == "2" or hide_or_reveal == "Eavesdrop":
        print('''
"You stay in the shadows, listening carefully."

Kornak:
"The warriors of Norwind, my brothers in battle, are closing in. We don’t have much time, Selena. Either we take the staff for ourselves or someone else will."

Selena:
"And you think your army can just waltz in and claim it? The staff’s guardian, Arin, is still out there, and she won’t let any of you lay a hand on it."

(After eavesdropping for a bit, you are forced to reveal yourselves after you can feel the gaze of Selena looking towards where you're hiding directly, you've been spotted.)

"You step out from behind the ruins, catching their attention. Both turn to face you, weapons ready, though neither attacks."
''')
    elif hide_or_reveal == "1" or hide_or_reveal == "approach them":
        print('''
Narrator:
"You step out from behind the ruins, catching their attention. Both turn to face you, weapons ready, though neither attacks."

''')
    else:
        print("################### Wrong Input, its too late to decide now, you've been spotted. ###################")
        
        
    if MainChar['Class'] == 'Warrior':
        print('Kornak: Kornak’s eyes widen slightly in recognition.', MainChar['Name'],
'''"is that really you? I thought you were dead!"
(He lowers his weapon.)
"You fought alongside me once, chief. I could use your help again, if you’re up for it. it’s been too long. We could use a fighter like you in this mess. There’s too much at stake for us to fight each other. What do you say? Help me get the staff, and we’ll set things right."

Selena: "Don't, you don't understand the consequences, if you help him obtain the staff, it would spell disaster for both kingdoms, it needs to be destroyed, that's the only way this conflict will end, trust me..."


''')
    elif MainChar['Class'] == 'Mage':
        print('''Selena narrows her eyes as she looks you up and down.
"A mage from Eldevar... I thought you all had fled, if you still have your power, I could use your help. If you’ve survived this long, it means you’re strong—and we need strength. But strength with a cause. The staff is too dangerous to fall into the hands of warriors who don’t understand its true power. Help me stop them. Unless, of course, you’re here to side with him..."''')
    while True:
        ally_choice_1 = input('''
            
    (You are now presented with the first major choice—whether to side with Kornak, Selena, or remain neutral for now.)

    Option 1: Ally with Kornak.
    Option 2: Ally with Selena.
    Option 3: "I...don't remember anything...what even is going on?!"

    Prompt: ''')
        if ally_choice_1 == '1':
            print('''
    Konrak: Nods approvingly, his grip on his axe tightening.
    "Good. We need to move quickly if we’re going to take the staff before anyone else does."
                
                ''')
            break
        elif ally_choice_1 == '2':
            print('''
    Selena: Gives a small, relieved smile.
    "I knew you’d make the right choice War Mage. Together, we might be able to prevent another disaster from taking place..."  
    
                ''')
            break
        elif ally_choice_1 == '3':
            print('''
    Selena: Looks over observingly, it seemed like she was going to say something, before she was interrupted...
                    
                    ''')
            break
        else:
            print("################### Wrong Input, try again. ###################")
    
    print('''
Narrator:
"Before you can make your decision final, a shout echoes through the ruins, and several figures emerge from the shadows—bandits, looking to loot whatever they can from the wreckage of Eldevar."

Bandit Leader:
"More survivors, huh? We're not gonna let you get away without a fight!"

          ''')
    while True:
        Victory = combat([chars['BanditLeader'], chars['Bandit']], MainChar, items, runaway=False)
        if Victory==False:
            print("\nNarrator: This was just the tutorial fight, you can keep trying it again and again until you win, resetting fight...")
            MainChar['Stats']['Health']=100
            MainChar['Inventory'] = ['Small health potion', 'Medium health potion','Large health potion']
        elif Victory==True:
            break
    input('''
Narrator: After defeating the bandits, the bandits had killed the tension for now, the three of them reaching a wrecked nearby village in a temporary alliance, a village with people surviving in there, barely, before deciding what they're gonna do, in the meantime you tell them of your lost memories...
          \n\n''')
    if MainChar['Class'] == 'Warrior':
        input('''
Narrator: Kornak tells you have you were a reputed war chief in the army of Norwind, and that you fought alongside each other once, although none of you know each other personally, and he doesn't know anything else about  you...a unique challenge comes in front as you reached the village.
              ''') 
    elif MainChar['Class'] == 'Mage':
        input('''
Narrator: Selena tells you about your past as one of the most skilled mages in the kingdom, where you were one of the most famous trainers, and were guarding an important point from Norwind's warrior's, she says she doesn't have a clue how you wounded up here, she says that you should stick with her, as she knows the most about the staff at the present time and she can help in restoring your memories, restore the kingdom and drive away invaders...meanwhile Konrak observes keenly, and obviously.
              ''')
    input('''
          Narrator: You reach the square of the village.
          
          Selena: "This is where we part ways, Konrak, and I hope we've reached an understanding that you won't hunt me down after you reunite with your band of warriors. We have the same goals, for now at least..."
          
          Konrak: "Fair enough, I don't have time to waste, I'll do my best to hunt down that staff, you'll find me along the journey, if you've got a lead, fill me in and we'll help each other reach that cursed staff...but what about..."
          
          Narrator: After forming a truce, they both turn to look at you...
          ''')
    if ally_choice_1 == '1':
        input('''Selena: "I remember you wisely decided to ally with me back there, I can help you reach the staff, we should work together, you're strong. Get yourself ready, and when you are, meet me in the tavern..."

Narrator: Konrak had suddenly disappeared while she was speaking before you could notice...either way...you agreed and now need to decide what you do next....
              ''')
        return ally_choice_1
    elif ally_choice_1 == '2':
        input('''Konrak: "I believe you'll still be sticking by me, I'll set up a camp outside the village and rest, meet me there, meanwhile warriors from Norwind will be coming here. Be on our side, and the power of the Norwind kingdom's army will successfully fight through the challenges to reach the staff."

Selena: "Well, I hope we don't have to cross paths again..."

Narrator: Selena had disappeared between the buildings rather quickly...either way...you agreed and now need to decide what you do next....
              ''')
        return ally_choice_1
    elif ally_choice_1 == '3':
        input('''
Selena: "Meet me at the tavern, if you want to get to the staff, currently I might be the only who knows the most about it. We can help each other"

Konrak: "Meh...you're strong, join me at my camp outside if you wanna fight alongside the Norwind kingdom to reach the staff, we actually have the manpower to make it happen and we will."

Narrator: You're left in the middle of the townsquare to decide, meanwhile they both left without saying anything else more. Now you need to make a choice...
     
              ''')
        while True:
            ally_choice_1 = input('''1. Go with Korlak
2. Go with Selena

Prompt:  ''')
            if ally_choice_1 == '1':
                return ally_choice_1             
            elif ally_choice_1 == '2':
                return ally_choice_1
            else:
                print("################### Wrong Input, try again. ###################")
    else:
        print("################### Wrong Input, try again. ###################")
    
def act1(chars, MainChar, items, ally):    
    while True:
        if ally=='1':
            print('''
    1. Go to the tavern (Continue Story - Not available in demo version)
    2. Visit the Alchemist and Exilir shop
    3. Go out in the wild
    4. Save Game and Exit


                ''')
            
        elif ally=='2':       
            print('''
    1. Go to the camp (Continue Story - Not available in demo version)
    2. Visit the Alchemist and Exilir shop
    3. Go out in the wild
    4. Journal
    5. Save Game and Exit

                ''')
            
        action = input('Prompt: ')
        if action=='1':
            if ally=='1':
                if MainChar['Class']=='Warrior':
                    if MainChar['Stats']['Level']>=3:
                        print('You look ready for the journey ahead, you head to the tavern to meet Selena and plan your next move towards the staff of Zorith...')
                        print('Narrator: You meet Selena at the tavern, and you both plan your next move towards the staff of Zorith...')
                        print('Selena: "Glad you made it, we need to move quickly if we want to reach the staff before Norwind\'s warriors do... as a warrior, your strength and connections will be invaluable on this journey."')
                        outcome = ashen(chars, MainChar, items, ally)
                        if outcome == True:
                            return 
                        elif outcome == False:
                            continue
                    elif MainChar['Stats']['Level']<3:
                        print('Narrator: You feel like you need to be stronger before facing the challenges ahead, but you go ahead and meet Selena Anyways...')
                        print("Selena: \"You look like you could use some more training before we head out, you're still weak from recent events...you should train and explore a little more before we set out.\"")
            elif ally=='2':
                if MainChar['Class']=='Mage':
                    if MainChar['Stats']['Level']>=3:
                        print('You look ready for the journey ahead, you head to the camp to meet Konrak and plan your next move towards the staff of Zorith...')
                        print('Narrator: You meet Konrak at the camp, and you both plan your next move towards the staff of Zorith...')
                        print('Konrak: "Glad you made it, we need to move quickly if we want to reach the staff before Eldevar\'s mages do... as a mage, your arcane prowess will be invaluable on this journey."')
                        ashen(chars, MainChar, items, ally)
                    elif MainChar['Stats']['Level']<3:
                        print('Narrator: You feel like you need to be stronger before facing the challenges ahead, but you go ahead and meet Konrak Anyways...')
                        print("Konrak: \"You look like you could use some more training before we head out, you're still weak from recent events...you should train and explore a little more before we set out.\"")
                elif MainChar['Class']=='Warrior':
                    if MainChar['Stats']['Level']>=3:
                        print('You look ready for the journey ahead, you head to the camp to meet Konrak and plan your next move towards the staff of Zorith...')
                        print('Narrator: You meet Konrak at the camp, and you both plan your next move towards the staff of Zorith...')
                        print('Konrak: "Glad you made it, we need to move quickly if we want to reach the staff before Eldevar\'s mages do... as a warrior, your strength and connections will be invaluable on this journey."')
                        outcome = ashen(chars, MainChar, items, ally)
                        if outcome == True:
                            return 
                        elif outcome == False:
                            continue
                    elif MainChar['Stats']['Level']<3:
                        print('Narrator: You feel like you need to be stronger before facing the challenges ahead, but you go ahead and meet Konrak Anyways...')
                        print("Konrak: \"You look like you could use some more training before we head out, you're still weak from recent events...you should train and explore a little more before we set out.\"")
        elif action=='2':
            shop(MainChar)
        elif action=='3':
            lookforfight(chars, MainChar, items)
        elif action=='5':
            save(chars)
            exit()
        elif action == '4': #This is the stacks section of the code
            journal()

def ashen(chars, MainChar, items, ally):
    """
    ACT 2 – THE FALL AND THE ASCENT (Final Act)
    This act resolves the story based on the player's early allegiance:
    ally == '1' -> Kornak (Norwind / Warrior path)
    ally == '2' -> Selena (Mage / Eldevar path)

    Themes:
    - Ruin of Eldevar
    - Truth of the Staff of Zorith
    - Final antagonist: Arin the Seraph of Zorith (the one who ended the war)
    - Final moral choice: Restore, Destroy, or Rule
    """

    print("\n\n---- ACT 2: THE ASHEN KINGDOM ----\n")

    input('''
Narrator:
"Weeks have passed since the uneasy truce. Eldevar rots in silence now. The sky above the kingdom is forever stained violet,
a scar left by the Staff of Zorith when it was unleashed during the final moments of the war."

"Whispers spread of a single figure seen at the heart of the capital—an angelic woman crowned in light and ruin.
The one who took the staff. The one who ended everything."

(You feel something stir inside you. The staff is calling.)

Press Enter to continue...
''')

    # --- LOCATION 1: THE SUNKEN CATHEDRAL ---
    print("\n--- LOCATION: THE SUNKEN CATHEDRAL OF ELDEVAR ---\n")

    d = input('''
Narrator:
"You arrive at the Sunken Cathedral, once the spiritual heart of Eldevar. Half of it lies buried beneath fractured earth,
and the rest floats unnaturally, suspended by lingering magic."

"Souls whisper here—mages and warriors alike, all victims of the staff."
''')

    if ally == '1':
        input('''
Kornak:
"This place makes my skin crawl. Norwind steel wasn’t meant for magic like this…"

Narrator:
(Kornak looks uneasy. For the first time, doubt creeps into his voice.)

              
Dialogue: 1. We'll get through this. (Rest your mind and encourage him)
          2. Stay alert. This place is dangerous. (Dismiss his concerns to stay alert)
          3. I smell something...we need to be careful. (Rolls perception check)''')
        if d == '1':
            input('''
Kornak: "Yeah… you’re right. We can’t let our guard down."

Narrator: (Something keeps watch from the shadows, undetectable, detecting your strength it hides itself to safety.)
          
            ''')
        elif d == '2':
            input('''
Kornak: (He tightens his grip on his axe.)
        "Always. This place gives me the creeps."

Narrator: (Something keeps watch from the shadows, undetectable, detecting your strength it hides itself to safety.)
          
            ''')
        elif d == '3':
            if randint(0,100)>=50:
                input('''Kornak: (He pauses, sniffing the air.)
                                "You’re right… there’s something off here."
                                (Suddenly, a spectral warrior materializes, eyes glowing with sorrow and rage.)
                                Spectral Warrior: "You trespass on sacred ground…"
                                ''')
                Victory = combat([{
                    'Name': 'Spectral Warrior',
                    'Stats': {'Health': 100},
                    'Moves': {'Attacks': {'Spectral Strike': 25, 'Glowing Gaze': 30}},
                    'Inventory': [None]
                }], MainChar, items, runaway=False)
            elif randint(0,100)<50:
                input('''Kornak: (He pauses, sniffing the air.)
                                "I don’t sense anything… maybe it was nothing."
                         Narrator: (He relaxes slightly, you too imagine it must be a false alarm.)
                                   (Although, something had already noticed you looking for it...)
                                   (And it strikes you, wounding you before you can react.)
                                   (You manage to fend it off, but not without injury.)
                                   (A spectral warrior materializes, eyes glowing with sorrow and rage.)
                         Spectral Warrior: "You trespass on sacred ground…"

                                ''')
                MainChar['Stats']['Health']-=20
                if MainChar['Stats']['Health']<0:
                    MainChar['Stats']['Health']=20
                Victory = combat([{
                    'Name': 'Spectral Warrior 1',
                    'Stats': {'Health': 120},
                    'Moves': {'Attacks': {'Spectral Strike': 25, 'Glowing Gaze': 30}},
                    'Inventory': [None]
                }, {
                    'Name': 'Spectral Warrior 2',
                    'Stats': {'Health': 120},
                    'Moves': {'Attacks': {'Spectral Strike': 25, 'Glowing Gaze': 30}},
                    'Inventory': [None]
                }], MainChar, items, runaway=False)
            if Victory == False:
                    print("\nNarrator: The spectral warrior overwhelms you. You collapse…\nReturning to the village to recover. Retry.\n")
                    return False
            elif Victory == True:
                    print("\nNarrator: You defeat the spectral warrior. As it crumbles, you notice a sword hilt radiating from it...\n")
                    if MainChar['Class']=='Warrior':
                        input('''
                              Kornak: "That sword... I can feel its power. It might come in handy. You should keep it"
                                Narrator: (You learn 'Spectral Blade', a new attack.)
                                ''')
                        MainChar['Moves']['Attacks']['Spectral Blade']=40
                        MainChar['Choices']['kornakHasSpectralBlade']=False
                    elif MainChar['Class']=='Mage':
                        input('''
                              Kornak: "That sword... I can feel its power. It might come in handy. I'll keep it, since you probably won't be able to use it effectively."
                              Narrator: (You watch as Kornak studies the sword, then tucks it away for later use. This should be handy....)
                                ''')
                        MainChar['Choices']['kornakHasSpectralBlade']=True
                    healthreset(MainChar)
                    MainChar['Stats']['XP']+=250
                    levelup(MainChar)
                    print('Narrator: "If these are only echoes… what does that make the one who commands them?"')
                    return True
    elif ally == '2':
        d = input('''
Selena:
"I trained here… before the war. Before she came."

Narrator:
(Her fists clench. Rage, grief, and guilt all tangled together.)

Dialogue: 1. We need to focus on the staff, and our surroundings. (Encourage her to stay focused while keeping a sharp eye)
          2. Take a moment. This place affects you. (Acknowledge her pain)
          3. Be careful. There’s something wrong here. (Rolls perception check)
''')
        if d == '1':
            input('''
Selena: "You're right. We can't let our guard down."

Narrator: (Something keeps watch from the shadows, undetectable, detecting your strength it hides itself to safety.)
          
            ''')
        elif d == '2':
            input('''
Selena: (She takes a deep breath, trying to steady herself.)
            "This place... it brings back memories. But we have to keep moving."

Narrator: (Something keeps watch from the shadows, undetectable, detecting your strength it hides itself to safety.)
            ''')
        elif d == '3':
            if randint(0,100)>=50:
                input('''Selena: (She pauses, sniffing the air.)
                                "You’re right… there’s something off here."
                                (Suddenly, a spectral mage materializes, eyes glowing with sorrow and rage.)
                                Spectral Mage: "You desecrate sacred ground…"
                                ''')
                Victory = combat([{
                    'Name': 'Spectral Mage 1',
                    'Stats': {'Health': 95},
                    'Moves': {'Attacks': {'Arcane Blast': 30, 'Ethereal Chains': 40}},
                    'Inventory': [None]
                }, {
                    'Name': 'Spectral Mage 2',
                    'Stats': {'Health': 95},
                    'Moves': {'Attacks': {'Arcane Blast': 30, 'Ethereal Chains': 40}},
                    'Inventory': [None]
                }], MainChar, items, runaway=False)
            elif randint(0,100)<50:
                input('''Selena: (She pauses, sniffing the air.)
                                "I don’t sense anything… maybe it was nothing."
                         Narrator: (She relaxes slightly, you too imagine it must be a false alarm.)
                                   (Although, something had already noticed you...)
                                   (And it strikes you, wounding you before you can react.)
                                   (You manage to fend it off, but not without injury.)
                                   (A spectral mage materializes, eyes glowing with sorrow and rage.)
                         Spectral Mage: "You desecrate sacred ground…"

                                ''')
                MainChar['Stats']['Health']-=20
                if MainChar['Stats']['Health']<0:
                    MainChar['Stats']['Health']=20
                Victory = combat([{
                    'Name': 'Spectral Mage',
                    'Stats': {'Health': 100},
                    'Moves': {'Attacks': {'Arcane Blast': 25, 'Ethereal Chains': 30}},
                    'Inventory': [None]
                }], MainChar, items, runaway=False)
            if Victory == False:
                    print("\nNarrator: The spectral mage overwhelms you. You collapse…\nReturning to the village to recover. Retry.\n")
                    return False
            elif Victory == True:
                    print("\nNarrator: You defeat the spectral mage. As it crumbles, you notice a spell scroll radiating from it...\n")
                    if MainChar['Class']=='Mage':
                        MainChar['Moves']['Attacks']['Arcane Blast']=35
                        input('''
                              Selena: "That spell... I can feel its power. It might come in handy. You should keep it"
                                Narrator: (You learn 'Spectral Bolt', a new attack.)
                                ''')
                        MainChar['Choices']['selenaHasSpectralBolt']=False
                    elif MainChar['Class']=='Warrior':
                        input('''
                              Selena: "That spell... I can feel its power. It might come in handy. I'll keep it, since you probably won't be able to use it effectively."
                              Narrator: (You watch as Selena studies the scroll, then tucks it away for later use. This should be handy....)
                                ''')
                        MainChar['Choices']['selenaHasSpectralBolt']=True
                    healthreset(MainChar)
                    MainChar['Stats']['XP']+=250
                    levelup(MainChar)
                    print('Narrator: "If these are only echoes… what does that make the one who commands them?"')
                    return True
        
def healthreset(PC):
    PC['Stats']['Health'] = 100+PC['Stats']['Level']*20
    

def cathedral_and_beyond(chars, MainChar, items):
    
    input('''
Narrator:
"Within the cathedral, a lone survivor appears—an Archivist bound to magic chains."

Archivist:
"The Seraph of Zorith… Arin… she believed herself our savior. The staff showed her a future without war."

"But the staff does not grant peace. It ENFORCES it."
''')

    input('''
Narrator:
"You spend a long moment with the Archivist, piecing together the present and find information."
          
"You learn the truth: Arin was once Eldevar’s guardian. When the war peaked, she took the staff,
ended both armies—and the kingdom—with divine force."

"She still rules from the Shattered Spire."
''')

    # --- LOCATION 2: THE ASHEN WILDS ---
    print("\n--- LOCATION: THE ASHEN WILDS ---\n")

    input('''
Narrator:
"Beyond the cathedral lies a land frozen in the moment of destruction.
Warriors turned to stone mid-charge. Mages crystallized in spellcasting poses.
The ground is littered with shattered weapons and broken dreams.
The staff’s magic lingers here, a haunting reminder of that final day.
You don't have too much time, you need to make a decision quickly....or keep moving forward...you don't have any time to waste or to hestitate...
Will you stop and pay your respects to the fallen, or will you march onward in silence?"
''')

    input('''
''')

    choice = input('''
Prompt:
1. Pray for the fallen
2. March onward in silence

Choice: ''')

    if choice == '1':
        input('''
Narrator:
"You kneel. The land trembles softly. The staff responds… approvingly."
(+Hidden Mercy Flag)
''')
    else:
        input('''
Narrator:
"You hesitated. You harden your heart. The past will not stop you."
(+Hidden Resolve Flag)
''')

    # --- FINAL LOCATION: THE SHATTERED SPIRE ---
    print("\n--- FINAL LOCATION: THE SHATTERED SPIRE ---\n")

    input('''
Narrator:
"The Shattered Spire pierces the sky, floating above the ruined capital.
Light pours from its peak like a false sun."

"She waits for you."
''')

    input('''
Arin, Seraph of Zorith:
"So… the lost one returns. The staff told me you would."

"I ended suffering. I ended chaos. Why do you still resist peace?"
''')

    input('''
Narrator:
(She descends—wings of pure magic unfurling, the Staff of Zorith burning with impossible power.)

FINAL BATTLE INITIATED
''')

    Victory = combat([{
        'Name':'Arin, Seraph of Zorith',
        'Stats':{'Health':200},
        'Moves':{'Attacks':{'Judgment':35,'Divine Ruin':45}},
        'Inventory':[None]
    }], MainChar, items, runaway=False)

    if Victory == False:
        input("\nNarrator: The staff rejects your weakness. The world fades… (Bad Ending)\n")
        return

    # --- POST BOSS ---
    print("\n--- THE STAFF OF ZORITH ---\n")

    input('''
Narrator:
"Arin falls, light fading from her wings. The staff floats before you."

"It recognizes you as its master."
''')

    # --- FINAL CHOICE ---
    ending = input('''
FINAL CHOICE:
1. Restore the Kingdom (Sacrifice the Staff)
2. Destroy the Staff Forever
3. Rule with the Staff as King/Queen

Choice: ''')

    if ending == '1':
        input('''
ENDING: THE RENEWAL

Narrator:
"You channel the staff one final time. The land heals. The dead rest. Magic fades from the world."

"Eldevar rises—not as it was, but as it should be."

(You vanish into legend.)

GOOD ENDING
''')

    elif ending == '2':
        input('''
ENDING: THE SILENCE

Narrator:
"You shatter the staff. Magic screams—then dies."

"No gods. No weapons of ruin. Only people."

(The world is safe… but forever changed.)

BITTERSWEET ENDING
''')

    elif ending == '3':
        input('''
ENDING: THE CROWN OF ORDER

Narrator:
"You take the throne. War ends. Crime ends. Freedom… ends."

"History will call you a savior."

"Time will call you a tyrant."

DARK ENDING
''')

    else:
        print("The staff consumes your indecision. (Secret Failure Ending)")

main()