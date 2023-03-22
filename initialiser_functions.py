import random
import numpy as np
import secrets
from car_class import Car, lying_car


def lying_car_init(position, fake_position, coerced):
    """creating a lying car with a given true and fake position. Velocity is given randomly, range of sight is given
    and the ID is unique."""

    velocity = ((np.random.rand(2)*2)-1)
    range_of_sight = 0.1 #round(random.uniform(0.1,0.2), 100)
    ID = str(secrets.token_hex(5))
    car = lying_car(position, velocity, range_of_sight, ID, coerced, fake_position)

    return car

def honest_car_init(position, coerced):
    """creating a lying car with a given true and fake position. Velocity is given randomly, range of sight is given
    and the ID is unique."""
    velocity = ((np.random.rand(2)*2)-1)
    range_of_sight = 0.1 #np.random.uniform(0, 0.25, size=(1)).astype(int)
    ID = str(secrets.token_hex(5))
    car = Car(position, velocity, range_of_sight, ID, coerced)

    return car

def coerced(q):
    coin_toss = np.random.rand()
        
    if coin_toss < q:
        return True
    else:
        return False

def honest(p):
    coin_toss = np.random.rand()
    if coin_toss < p:
        return True
    else:
        return False

def create_position(environment):
    x_position = np.random.uniform(low=environment.x_coordinates[0], high=environment.x_coordinates[1], size=1)
    y_position = np.random.uniform(low=environment.y_coordinates[0], high=environment.y_coordinates[1], size=1)
    
    position = np.concatenate((x_position, y_position), axis=0)
    
    return position

def car_gen(p, q, environment):
    h = honest(p)
    c = coerced(q)

    position = create_position(environment)
    fake_position = create_position(environment)

    if h is True:
        car = honest_car_init(position, c)
    else:
        car = lying_car_init(position, fake_position, c)
    
    return car


