#agent_data:[(sequence number, place symbol,{service: True/False})]
#attack plan or attack ground

agent_type={
'redCommander':{'serve':[],'velocity': 30/60},
'redCommanderMiddle':{'serve':[],'velocity': 55/60},
'redAirArtillery':{'serve':[],'velocity': 0.001},
'redRocketGun':{'serve':[],'velocity': 0.001},
'redSAUGV':{'serve':['observe','attack','support','follow'],'velocity': 55/3.6},
'redRSUAVehicle':{'serve':[],'velocity': 55/60},
'redRSUAV':{'serve':['observe','support','follow','trick'],'velocity':212/60},
'redFSUAVehicle':{'serve':[],'velocity':55/60},
'redFSUAV':{'serve':['observe','support','follow','trick'],'velocity':212/60},
'redArCMUGV':{'serve':[],'velocity':55/60},
'redInCMUGV':{'serve':[],'velocity':55/60},
'redAJUGV':{'serve':['support'],'velocity':55/60},
'redArCMissle':{'serve':['attack'],'velocity':425/60},
'redInCMissle':{'serve':['attack'],'velocity':425/60},
    'break':{'serve':[],'velocity':0.01},
'redSuicideUAV':{'serve':['attack','trick'],'velocity':425/60},


'RC':{'serve':[],'velocity': 30/60},
'RUSV':{'serve':['attack'],'velocity':50/60},
'RSUAV':{'serve':['observe','support','follow','trick'],'velocity':212/60},
    'RAUAV':{'serve':['attack','support','trick'],'velocity':425/60},
'RM':{'serve':['attack'],'velocity':425/60},
'RAD':{'serve':[],'velocity':0.01/60}

            }


agent_resource={'redSAUGV':4,
'redArCMUGV':4,
'redInCMUGV':4,
'redArCMissle':1,
'redInCMissle':1,
'redSuicideUAV': 1,
                'RC': 7,
                'RUSV': 7,
                'RSUAV': 7,
                'RAUAV': 7,
                'RM': 6,
                'RAD': 6,
                'redCommander':0,
'redCommanderMiddle':0,
                'redAirArtillery':0,
'redRocketGun':0,
'redRSUAVehicle':1,
'redRSUAV':3,
'redFSUAVehicle':0,
'redFSUAV':0,
'redAJUGV':2,

                }