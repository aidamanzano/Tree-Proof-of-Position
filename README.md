# Tree-Proof-of-Position

We present Tree Proof of Position protocol (T-PoP). It is a decentralised, collaborative protocol that allows agents to prove their position. The protocol uses a tree architecture and does not rely on a central verifier to approve or reject each agent's claimed position.

The T-PoP algorithm script is tpop.py. The agent class is car_class.py and the environment is defined in the environment_class.py script.

The simulations showing the results of T-PoP's performance can be found in the notebook: `tpop_simulations.ipynb`. Feel free to change the threshold, depth and number of witnsesses parameters.


NOTE: the simulation script is set up to save all the results in text files in your cwd. If you don't want all this data saved, you will have to change this in the appropriate simulation generator function for each algorithm in the `tpop_simulation_functions.py` script.

The `initialiser_functions.py` script is to generate the different types of agents, and the simulation_functions.py script contains useful functions to generate the simulation results calling the different types of algorithms.

I will link the detailed explanation of T-PoP here as soon as the work is up on Arxiv, but you can check the comments of the `tpop.py` file to follow how the algorithm works.

The simulation generator notebooks will likely be updated, and details on the collaborative lying attack simulations will be up shortly too. 
