import car_class as c
import numpy as np
from concrete import fhe


position1 = [1, 2]
position2 = [3, 2]
velocity = ((np.random.rand(2)*2)-1)
range_of_sight = 10 #np.random.uniform(0, 0.25, size=(1)).astype(int)


car1 = c.Car(position1, velocity, range_of_sight, 'car1', coerced=False)
car2 = c.Car(position2, velocity, range_of_sight, 'car2', coerced=False)



def euclidean_distance(location1, location2):
    distance = (location2[0] - location1[0])**2 + (location2[1] - location1[1])**2

    return distance

distance = euclidean_distance(car1.position, car2.position)
print(distance)
#NOTE: https://docs.zama.ai/concrete/tutorials/floating_points floating points cant be inputs or outputs,
#only intermediate values. Not sure what to do about this?

#NOTE: no docs found on all the methods available for circuit, here is the github repo: 
# https://github.com/zama-ai/concrete/blob/main/frontends/concrete-python/concrete/fhe/compilation/circuit.py

compiler = fhe.Compiler(euclidean_distance, {"location1": "encrypted", "location2": "encrypted"})
#TODO: need to read about how to define the inputset exactly for the context of our simulations

inputset = [(car1.position, car2.position)]
circuit = compiler.compile(inputset)
encrypted = circuit.encrypt(car1.position, car2.position)
print(encrypted)
result = circuit.run(encrypted)
print(result)

decrypted_result = circuit.decrypt(result)

print(decrypted_result)

#Alternative method:
#running everything in one go.
compiler = fhe.Compiler(euclidean_distance, {"location1": "encrypted", "location2": "encrypted"})
#inputset defined in l33
homomorphic_evaluation = circuit.encrypt_run_decrypt(car1.position, car2.position)
print(homomorphic_evaluation)

str(circuit)
print(circuit)
