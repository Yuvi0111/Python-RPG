from random import randint
from random import choice
def main():
    chars = {
        'MainCharacter':{'Name':'', 'Sex':'', 'Class':'', 'Stats':{'Health':100, 'Defense':5,'Level':0 ,'XP':0}, 'Moves':{'Attacks':{}, 'Defense':{}}, 'Inventory':['Small health potion', 'Medium health potion','Large health potion']},
        'BanditLeader':{'Name':'Bandit Leader', 'Sex':'Male', 'Class':'Bandit', 'Stats':{'Health':125}, 'Moves':{'Attacks':{'Throwing Axe':13,'Strike':18}, 'Defense':{}}, 'Inventory':[None]},
        'Bandit':{'Name':'Bandit', 'Sex':'Male', 'Class':'Bandit', 'Stats':{'Health':75}, 'Moves':{'Attacks':{'Strike':13,'Bleed':10}, 'Defense':{}}, 'Inventory':[None]}     
        } 
    items = {
        'Health Consumables':{'Small health potion':20, 'Medium health potion':40, 'Large health potion':60}
        }
    menu(chars, items)

def menu(chars, items):
    while True:
        menu_input = int(input(
""" 
 ------------------------TextRPG----------------------------------
1. New Game
2. Load Character (WIP)
3. Exit
              
Input: """
        ) ) 
        if menu_input==1:
            print('\n'*40)
            new_game(chars, chars['MainCharacter'], items)           
        elif menu_input==2:
            ...
        elif menu_input==3:
            exit()

def combat(enemies, PC, items, runaway=True):
    print('You are now engaged in a battle with: ')
    for enemy in range(len(enemies)-1):
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
                            for no_of_enemies in range(len(enemies)):
                                enemy_attack_dict = enemies[no_of_enemies]['Moves']['Attacks']
                                enemey_attack_list = tuple(enemies[no_of_enemies]['Moves']['Attacks'].keys())
                                
                                enemies[no_of_enemies]['Stats']['Health'] = enemies[no_of_enemies]['Stats']['Health']-PCattacks[PCatk_Index[int(PCattack)-1]]
                                if (randint(0,100)+PC['Stats']['Defense'])>90:
                                    print("\nAttack dodged.")
                                    print(enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                    
                                else:    
                                    PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[choice(enemey_attack_list)]
                                    print('\n'+enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health'])+'\n')
                            
                            for health_of_enemies in range(len(enemies)):
                                if enemies[health_of_enemies]['Stats']['Health'] > 0:
                                    EnemyAlive = True  # At least one enemy is alive, we don't need to do anything
                                    break
                                else:
                                    # This 'else' corresponds to the 'for' loop, meaning if no break occurs (i.e., all enemies are dead)
                                    EnemyAlive = False  # All enemies are dead if the loop completes without finding a 
                                                           
                                
                        elif PCattack == '2' and len(PCatk_Index)>1:
                            for no_of_enemies in range(len(enemies)):
                                enemy_attack_dict = enemies[no_of_enemies]['Moves']['Attacks']
                                enemey_attack_list = tuple(enemies[no_of_enemies]['Moves']['Attacks'].keys())
                                
                                enemies[no_of_enemies]['Stats']['Health'] = enemies[no_of_enemies]['Stats']['Health']-PCattacks[PCatk_Index[int(PCattack)-1]]
                                if (randint(0,100)+PC['Stats']['Defense'])>90:
                                    print("Attack dodged.")
                                    print(enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                    
                                else:    
                                    PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[choice(enemey_attack_list)]
                                    print(enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                    
                                
                                
                        elif PCattack == '3' and len(PCatk_Index)>2:
                            for no_of_enemies in range(len(enemies)):
                                enemy_attack_dict = enemies[no_of_enemies]['Moves']['Attacks']
                                enemey_attack_list = tuple(enemies[no_of_enemies]['Moves']['Attacks'].keys())
                                
                                enemies[no_of_enemies]['Stats']['Health'] = enemies[no_of_enemies]['Stats']['Health']-PCattacks[PCatk_Index[int(PCattack)-1]]
                                if (randint(0,100)+PC['Stats']['Defense'])>90:
                                    print("Attack dodged.")
                                    print(enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                    
                                else:    
                                    PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[choice(enemey_attack_list)]
                                    print(enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                        
                                
                                
                                
                        elif PCattack == '4' and len(PCatk_Index)>3:
                            enemy_attack_dict = enemies[no_of_enemies]['Moves']['Attacks']
                            enemey_attack_list = tuple(enemies[no_of_enemies]['Moves']['Attacks'].keys())
                            
                            for no_of_enemies in range(len(enemies)):
                                enemies[no_of_enemies]['Stats']['Health'] = enemies[no_of_enemies]['Stats']['Health']-PCattacks[PCatk_Index[int(PCattack)-1]]
                                if (randint(0,100)+PC['Stats']['Defense'])>90:
                                    print("Attack dodged.")
                                    print(enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                    
                                else:    
                                    PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[choice(enemey_attack_list)]
                                    print(enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                    input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                    
                        else:
                            print('Wrong input')
                            continue
                        break
                                
                        
                        
                elif atk_or_def == '2' and len(tuple(PC['Moves']['Defense'].keys()))>0:
                    PC_defs_dict = PC['Moves']['Defense']
                    PC_defs = tuple(PC['Moves']['Defense'].keys())
                    enemy_attack_dict = enemies['Moves']['Attacks']
                    enemey_attack_list = enemies['Moves']['Attacks'].keys()
                    for defss in range(len(PC_defs)):
                        print(str(defss+1)+'. '+PC_defs[defss])
                    while True:
                        PCdefense = input("Choose a defense: ")                   
                        if PCdefense == '1' and len(PC_defs)>0:
                            PC['Stats']['Defense'] += PC_defs_dict[PC_defs[int(PCdefense)-1]]
                            if (randint(0,100)+PC['Stats']['Defense'])>90:
                                print("Attack dodged.")
                                print(enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                break
                            else:    
                                PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[choice(enemey_attack_list)]
                                print(enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                break
                        elif PCdefense== '2' and len(PC_defs)>1:
                            PC['Stats']['Defense'] += PC_defs_dict[PC_defs[int(PCdefense)-1]]
                            if (randint(0,100)+PC['Stats']['Defense'])>90:
                                print("Attack dodged.")
                                print(enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                break
                            else:    
                                PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[choice(enemey_attack_list)]
                                print(enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                break
                        elif PCdefense == '3' and len(PC_defs)>2:
                            PC['Stats']['Defense'] += PC_defs_dict[PC_defs[int(PCdefense)-1]]
                            if (randint(0,100)+PC['Stats']['Defense'])>90:
                                print("Attack dodged.")
                                print(enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                break
                            else:    
                                PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[choice(enemey_attack_list)]
                                print(enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                break
                        elif PCdefense == '4' and len(PC_defs)>3:
                            PC['Stats']['Defense'] += PC_defs_dict[PC_defs[int(PCdefense)-1]]
                            if (randint(0,100)+PC['Stats']['Defense'])>90:
                                print("Attack dodged.")
                                print(enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                break
                            else:    
                                PC['Stats']['Health'] = PC['Stats']['Health']-enemy_attack_dict[choice(enemey_attack_list)]
                                print(enemies[no_of_enemies]['Name']+"'s health: " + str(enemies[no_of_enemies]['Stats']['Health']))
                                input(PC['Name']+"'s health: " + str(PC['Stats']['Health']))
                                break
                            
                else:
                    print("################### Wrong Input, try again. ###################")
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
                        print('Unexpected bug, please refrain from using this item and reporting the issue to the developer.')
                    
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
        
            
            
        

def new_game(chars, MainChar, items):
    #Character's Sex
    while True:
        MainChar['Sex'] = int(input("""1. Male 
2. Female
Select Gender of the character: """
                            ))
        if MainChar['Sex'] == 1:
            MainChar['Sex'] = 'Male'
            break
        elif MainChar['Sex'] == 2:
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
YuPrompt:
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
            MainChar['Moves']['Defense'] = {'Brace':25}
            break
        elif MainChar['Class'] == "2" or MainChar['Class'] == "mage":
            MainChar['Class'] = 'Mage'
            MainChar['Moves']['Attacks'] = {'Zap':30}
            MainChar['Moves']['Defense'] = {'Mist':15}
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
    elif ally_choice_1 == '2':
        print('''
Selena: Gives a small, relieved smile.
"I knew you’d make the right choice War Mage. Together, we might be able to prevent another disaster from taking place..."  
  
              ''')
    elif ally_choice_1 == '3':
        print('''
Selena: Looks over observingly, it seemed like she was going to say something, before she was interrupted...
                
                ''')
    else:
        print("################### Wrong Input, try again. ###################")
    
    print('''
Narrator:
"Before you can make your decision final, a shout echoes through the ruins, and several figures emerge from the shadows—bandits, looking to loot whatever they can from the wreckage of Eldevar."

Bandit Leader:
"More survivors, huh? Hand over your weapons, and we might let you live."

          ''')
    combat([chars['BanditLeader'], chars['Bandit']], MainChar, items, runaway=False)
        

    
    

    
            
    
    
    
        
        
main()