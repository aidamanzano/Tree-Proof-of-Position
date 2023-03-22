import random
import numpy as np

class Car():
    """class to create a car with a given position, range of sight and list of neighbours. Car is assumed to be honest"""
    def __init__(self, position: list, velocity: list, range_of_sight: float, ID, coerced, parent=None):
        self.position = position
        self.velocity = np.array(velocity)
        self.position_history = []
        self.position_history.append(np.array(position))
        self.range_of_sight = range_of_sight

        self.neighbours = set()
        self.ID = ID
        self.honest = True #is the car honest or a liar
        self.algorithm_honesty_output = None #does the algorithm dictate that this car is honest or a liar
        self.coerced = coerced
        self.neighbour_validations = 0

        self.parent = parent
        self.children = []
        self.verified = True
        self.counter = None


    @property
    def range_of_sight(self):
        return(self._range_of_sight)

    #The range of sight must be greater than 0
    @range_of_sight.setter
    def range_of_sight(self, value):
        if value <= 0:
            return ValueError("Your car must be able to see something")
        self._range_of_sight = value

    def is_in_range_of_sight(self, location):
        """This is a check to see if the position of a car that is being 'viewed' is within the range of sight of the viewing car.
        I assume the range of sight is a radius, and calculate if the position of the viewed car falls within the circle 
        of range of sight"""
        x = location[0]
        y = location[1]
        if (x - self.position[0])**2 + (y - self.position[1])**2 <= self.range_of_sight**2:
            return True
        else:
            return False

    def add_neighbours(self, city):
        """Find the grid quadrant of the car. Then, for every other neighbouring car in that quadrant, if it is in the range of sight 
        and not the car itself, add it to the set of neighbours"""

        x_index, y_index = self.get_position_indicies(city.grid_size)
        #loop through all adjacent grid squares

        for grid_square in [[x_index - 1, y_index], [x_index + 1, y_index], [x_index, y_index - 1], [x_index, y_index + 1], [x_index, y_index]]:
            #print(grid_square[0], environment_x_coordinates[0])
            if grid_square[0] < city.x_coordinates[0] or grid_square[0] >= city.width:
                pass
            elif grid_square[1] < city.y_coordinates[0] or grid_square[1] >= city.height:
                pass
            else:
                #print([grid_square[0], grid_square[1]])

                #coerced will chose to add a lying car it does NOT see in the fake position grid
                for car in city.grid[grid_square[0]][grid_square[1]]:

                    #first condition is redundant because coerced cars are a subset of honest, but leaving this in for clarity.
                    if self.honest == True and self.coerced is True:
                        #print('entered condition of honest and coerced')

                        #a coerced car will add the FAKE position of a lying car 
                        #if it is in its range of sight and same grid square


                        if car.honest is False and self.ID != car.ID:
                            x, y = car.get_fake_position_indicies(city.grid_size)
                            if x == grid_square[0] and y == grid_square[1] and self.is_in_range_of_sight(car.fake_position):
                                self.neighbours.add(car)
                                #print('coerced car sees fake car in its fake position')

                        #This covers both honest cars and coerced cars, since coerced are a subset of honest cars. 
                        elif car.honest is True and self.ID != car.ID and self.is_in_range_of_sight(car.position):
                            self.neighbours.add(car)
                            #print('coerced car sees honest car')

                    elif self.honest == True and self.coerced is False: 
                        #an honest car will add the REAL position of a lying car if it
                        #is in its range of sight and same grid square

                        if car.honest is False and self.ID != car.ID:
                            x, y = car.get_position_indicies(city.grid_size)
                            if x == grid_square[0] and y == grid_square[1] and self.is_in_range_of_sight(car.position):
                                self.neighbours.add(car)
                                #print('honest car sees fake car in their real position', car.honest)
                                

                        #This covers both honest cars and coerced cars, since coerced are a subset of honest cars. 
                        elif car.honest is True and self.ID != car.ID:
                            if self.is_in_range_of_sight(car.position):
                                self.neighbours.add(car)
                                #print('honest car sees honest car')


        return self.neighbours

    def is_car_a_neighbour(self, car):
        if car in self.neighbours:
            return True
        else:
            #print("The car is not a neighbour!")
            return False

    def claim_position(self):
        return self.position

    def name_witness(self, number = 2):
        """Function to return two witnesses (or attestors), provided the car has sufficient neighbours"""
        if len(self.neighbours) >= number:
            #select two witnesses at random from list of neighbours
            self.witnesses = random.sample(self.neighbours, number)
            return self.witnesses
        else:
            #print("The car does not have sufficient neighbours to witness its position!")
            return None
            #Even if a car has exactly one neighbour, I will ignore because it is not enough to proceed in the protocol.
        
    def move(self, dt, environment):
        """First removes the car from its current grid position, then checks that the next position is within bounds of the environment
        and then updates position if so. Finally, adds the car into the new position grid"""
        
        #Find the indicies of the car position
        x_index, y_index = self.get_position_indicies(environment.grid_size)
        #REMOVE the car from previous position
        environment.grid[x_index][y_index].remove(self) 
        
        preliminary_position = self.position + (dt * self.velocity) 
        #if the agent is getting close to the grid boundaries, invert the velocity
        #I am assuming no car would voluntarily drive towards a wall

        if preliminary_position[0] <= environment.x_coordinates[0] or preliminary_position[0] >= environment.x_coordinates[1]:
            
            self.velocity[0] = -1 * self.velocity[0]
            preliminary_position = self.position + (dt * self.velocity)
            
        if preliminary_position[1] <= environment.y_coordinates[0] or preliminary_position[1] >= environment.y_coordinates[1]:
            self.velocity[1] = -1 * self.velocity[1]
            preliminary_position = self.position + (dt * self.velocity)
        
        self.position = preliminary_position
        self.position_history.append(self.position)

        #Assign the car in its new position
        environment.assign(self) 

    def get_position_indicies(self, grid_size):
        """Calculating the grid indicies given a position"""
        x_index = int(np.floor(self.position[0]/grid_size))
        y_index = int(np.floor(self.position[1]/grid_size))
        return x_index, y_index

class lying_car(Car):
    """Class for dishonest cars. Position claim, move function, position indicies and neighbour adding functions are added to 
    consider the fake position."""

    def __init__(self, position: list, velocity: list, range_of_sight: float, ID, coerced, fake_position: list):
        super().__init__(position, velocity, range_of_sight, ID, coerced)
        self.fake_position = fake_position #(np.random.rand(2)*2).tolist()
        self.honest = False

    def claim_position(self):
        return self.fake_position

    def move_fake_position(self, dt, environment):
        """When the lying car moves, it moves it's fake position, the real position may or may not have changed"""

        #Find the indicies of the car's fake position
        x_index, y_index = self.get_fake_position_indicies(environment.grid_size)
        #REMOVE the car from previous position
        environment.grid[x_index][y_index].remove(self)

        preliminary_position = self.fake_position + (dt * self.velocity) 

        if preliminary_position[0] <= environment.x_coordinates[0] or preliminary_position[0] >= environment.x_coordinates[1]:
            
            self.velocity[0] = -1 * self.velocity[0]
            preliminary_position = self.fake_position + (dt * self.velocity)
            
        if preliminary_position[1] <= environment.y_coordinates[0] or preliminary_position[1] >= environment.y_coordinates[1]:
            self.velocity[1] = -1 * self.velocity[1]
            preliminary_position = self.fake_position + (dt * self.velocity)
        
        self.fake_position = preliminary_position
        self.position_history.append(self.fake_position)

        #add car to its new fake position in the grid
        environment.assign(self)

    def get_fake_position_indicies(self, grid_size):
        x_index = int(np.floor(self.fake_position[0]/grid_size))
        y_index = int(np.floor(self.fake_position[1]/grid_size))
        return x_index, y_index

    def is_in_range_of_sight(self, location):
        """This is a check to see if the position of a car that is being 'viewed' is within the range of sight of the viewing car.
        I assume the range of sight is a radius, and calculate if the position of the viewed car falls within the circle 
        of range of sight"""
        x = location[0]
        y = location[1]
        if (x - self.fake_position[0])**2 + (y - self.fake_position[1])**2 <= self.range_of_sight**2:
            return True
        else:
            return False
        
    def add_neighbours(self, city):

        #get the indicies of the fake location
        x_index, y_index = self.get_fake_position_indicies(city.grid_size)
        for grid_square in [[x_index - 1, y_index], [x_index + 1, y_index], [x_index, y_index - 1], [x_index, y_index + 1], [x_index, y_index]]:
            #print(grid_square[0], environment_x_coordinates[0])
            if grid_square[0] < city.x_coordinates[0] or grid_square[0] >= city.width:
                pass
            elif grid_square[1] < city.y_coordinates[0] or grid_square[1] >= city.height:
                pass
            else:

                for alleged_nearby_car in city.grid[grid_square[0]][grid_square[1]]:

                    if self.coerced == True:

                    #if a lying car finds another lying car claiming to be in the same FAKE position, it will add it as its neighbour. 
                    #it will NOT add the other lying car's real position, only its FAKE position

                        if alleged_nearby_car.honest == False:
                            
                            x, y = alleged_nearby_car.get_fake_position_indicies(city.grid_size)
                            if x == grid_square[0] and y == grid_square[1]:
                                
                                
                                if self.is_in_range_of_sight(alleged_nearby_car.fake_position) and alleged_nearby_car.ID != self.ID:
                                    self.neighbours.add(alleged_nearby_car)

                        elif alleged_nearby_car.honest == True:
                            x, y = alleged_nearby_car.get_position_indicies(city.grid_size)
                            if x == grid_square[0] and y == grid_square[1]:
                                
                                if self.is_in_range_of_sight(alleged_nearby_car.position) and alleged_nearby_car.ID != self.ID:
                                    self.neighbours.add(alleged_nearby_car)

                    elif self.coerced == False:
                        #A lying, not coerced car will see the true position of any car, with respect to its own fake position.
                        x, y = alleged_nearby_car.get_position_indicies(city.grid_size)
                        if x == grid_square[0] and y == grid_square[1]:
                            if self.is_in_range_of_sight(alleged_nearby_car.position) and alleged_nearby_car.ID != self.ID:
                                self.neighbours.add(alleged_nearby_car)
                    
                        

        return self.neighbours

