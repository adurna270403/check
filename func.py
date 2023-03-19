import pandas as pd
import numpy as np
import requests

from function import func
from acc.account import *
# Create a session to persistently store the headers
s = requests.Session()

#simulate alpha on acc
class Sim():
    def __init__(self,acc,
                instrumentType="EQUITY",
                region="USA",
                universe="TOP3000",
                delay=1,
                decay=5,
                neutralization= "SUBINDUSTRY",
                truncation= 0.1,
                pasteurization= "ON",
                unitHandling= "VERIFY",
                nanHandling= "OFF",
                language= "FASTEXPR",
                visualization= False,
    ): 
        self.acc = acc
        self.settings ={
                "instrumentType": instrumentType,
                "region": region,
                "universe": universe,
                "delay": delay,
                "decay": decay,
                "neutralization": neutralization,
                "truncation": truncation,
                "pasteurization": pasteurization,
                "unitHandling": unitHandling,
                "nanHandling": nanHandling,
                "language": language,
                "visualization": visualization,
            },
        # Save credentials into session
        s.auth = (username[self.acc], password[self.acc])

        # Send a POST request to the /authentication API
        self.response = s.post('https://api.worldquantbrain.com/authentication')


    def Simulation(self,alpha):
        simulate_data = {
            "type": "REGULAR",
            "settings": self.settings,
            "regular": alpha
        }
        simulate_response = s.post('https://api.worldquantbrain.com/simulations', json=simulate_data)

        simulation_progress_url = simulate_response.headers['Location']
        finished = False
        while True:
            simulation_progress = s.get(simulation_progress_url)
            if simulation_progress.headers.get("Retry-After", 0) == 0:
                break
            # print("Sleeping for " + simulation_progress.headers["Retry-After"] + " seconds")

            import time
            time.sleep(float(simulation_progress.headers["Retry-After"]))
        # print("Alpha done simulating, getting alpha details")
        alpha = simulation_progress.json()["alpha"]
        simulation_result = s.get("https://api.worldquantbrain.com/alphas/" + alpha)

        pnl = s.get("https://api.worldquantbrain.com/alphas/" + alpha)  
        return pnl.json()
    
def save(a,path):
    pd.DataFrame([a]).to_csv(f"{path}",mode="a",header=False)
