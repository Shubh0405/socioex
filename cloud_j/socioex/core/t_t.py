import random

def get_tone(text_to_analyze):
    emotions = ["HAPPY", "SAD", "EXCITED", "NERVOUS", "DEPRESSED", "ANGER", "FEAR", "JOY"]
    em_len = len(emotions)

    rating = random.randint(9000,10000) / 10000
    
    data = {
        "tone": emotions[random.randint(0,em_len-1)],
        "percent": rating
    }

    return data
