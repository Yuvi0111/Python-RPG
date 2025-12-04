import pickle
import csv
with open('characters.dat', 'wb') as file:
    chars = {
        'MainCharacter':{'Name':'', 'Sex':'', 'Class':'', 'Stats':{'Health':100, 'Defense':5,'Level':0 ,'XP':0}, 'Money':0, 'Moves':{'Attacks   ':{}, 'Defense':{}}, 'Inventory':['Small health potion', 'Medium health potion','Large health potion'],'Choices':{'Ally':''},'Progress':''},
        'BanditLeader':{'Name':'Bandit Leader', 'Sex':'Male', 'Class':'Bandit', 'Stats':{'Health':125}, 'Moves':{'Attacks':{'Throwing Axe':13,'Strike':18}, 'Defense':{}}, 'Inventory':[None]},
        'Bandit':{'Name':'Bandit', 'Sex':'Male', 'Class':'Bandit', 'Stats':{'Health':75}, 'Moves':{'Attacks':{'Strike':13,'Bleed':10}, 'Defense':{}}, 'Inventory':[None]},
        'Goblin':{'Name':'Goblin', 'Sex':'Undefined', 'Class':'Humanoid Monster', 'Stats':{'Health':60}, 'Moves':{'Attacks':{'Scratch':15,'Bleed':12}, 'Defense':{}}, 'Inventory':[None]},
        'Gorgon':{'Name':'Gorgon', 'Sex':'Undefined', 'Class':'Humanoid Monster', 'Stats':{'Health':70}, 'Moves':{'Attacks':{'Freeze':15,'Slap':20}, 'Defense':{}}, 'Inventory':[None]},
        'Hostile Nordwin Warrior':{'Name':'Hostile Nordwin Warrior', 'Sex':'Male', 'Class':'Nordwin', 'Stats':{'Health':80}, 'Moves':{'Attacks':{'Stab':16,'Kick':11}, 'Defense':{}}, 'Inventory':[None]}
        } 
    pickle.dump(chars, file)
    
    