"""Traffic simulation 4.0
Edited: 2019-03-24
Created: 2018-12-30
Author: Xibu Zhang
Purpose: Produce True if the conditions require a change of traffic light
Independent var: Number of cars behind red light, Current flow rate in green light direction
Dependent var: Boolean (true when it is time to switch lights)
Version notes: This is the final version of this stage, with n dependent acceleration function.
"""
import math

VEHICLE_NUMBER_MIN = 1      #used for boundaries of the rate input
VEHICLE_NUMBER_MAX = 100000

REACTION_TIME = 1.385714286 #seconds
VEHICLE_LENGTH = 4.7 #meters
FOLLOWING_DISTANCE = 2 #meters


def acceleration(n):
    accum = 1 #accumulator
    avg = 0 #avg acceleration
    while 1:
        if (accum > n):
            return avg/n #average acceleration in meters per second
        else:
            avg = avg + 4.89*accum**(-0.8) #accumulated acceleration
            accum = accum + 1
    return 0


def d_from_int(n):
    return (n-1)*VEHICLE_LENGTH + n*FOLLOWING_DISTANCE #total distance from nth car to intersection

def read_vehicle_number_input():
    return eval(input("Enter vehicle number: "))

def read_vehicles_per_second_input(rate_min, rate_max):
    string_input0 = "Green direction flow rate is recommended to be larger than "
    string_input1 = " and MUST be less than "
    string_out = string_input0 + str(rate_min) + string_input1 + str(rate_max)
    print(string_out) #combine string

    vehicles_per_second = eval(input("Enter green direction flow rate: "))

    if(vehicles_per_second < rate_min):
        if (read_vehicle_number_input()>0):
            print("Change the light!")
        else:
            print("Keep the light.")
        quit()
        return 0
    elif(vehicles_per_second > rate_max):
        print("ERROR: Input is too large")
        quit()
        return 0
    else:
        return vehicles_per_second

def calculate_time(vehicle_number):
    return math.sqrt(2*d_from_int(vehicle_number)/acceleration(vehicle_number)) + REACTION_TIME *vehicle_number + 1.5 # algorithm with time(n) isolated

def rate(vehicle_number, reach_time): #number of vehicles per second
    step = 0.00000001 #step size for approximation 
    acc0 = 0
    acc1 = 0
    acc0 = math.sqrt(2*d_from_int(vehicle_number+step)/acceleration(vehicle_number)) + REACTION_TIME *(vehicle_number+step) + 1.5 #approximated with limits
    acc1 = math.sqrt(2*d_from_int(vehicle_number-step)/acceleration(vehicle_number)) + REACTION_TIME *(vehicle_number-step) + 1.5
    return (2*step)/abs(acc0-acc1) #equivalent to the inverse of the derivative of time(n)

def compare(vehicles_per_second, reach_time): #compare to determine if it is time to change lights
    vehicle_number = 1 
    step = 1.0
    rate_u = rate(vehicle_number, reach_time) #rate updated
    while 1:
        if (rate_u > vehicles_per_second):
            return vehicle_number       #return number of cars it takes to reach vehicles per second input
        vehicle_number = vehicle_number + step
        rate_u = rate(vehicle_number, reach_time) #rate updated

def results():
    vehicle_number = 0 # car number
    reach_time = 0 # time
    vehicles_per_second = 0 # rate
    model_number = 0 # car number required predicted by model

### read rate of green light direction within specified range
    reach_time = calculate_time(VEHICLE_NUMBER_MIN)
    rate_min = rate(VEHICLE_NUMBER_MIN, reach_time) # minimum vehicles_per_second value should be the rate of one vehicle in front of red light
    reach_time = calculate_time(VEHICLE_NUMBER_MAX)
    rate_max = rate(VEHICLE_NUMBER_MAX, reach_time) # maximum vehicles_per_second value should be the rate of infinite vehicles in front of red light
    vehicles_per_second_read = read_vehicles_per_second_input(rate_min, rate_max)
    
### read number of vehicles waiting behind red light
    vehicle_number = read_vehicle_number_input()
    reach_time = calculate_time(vehicle_number)
    vehicles_per_second = rate(vehicle_number, reach_time)

    model_number = compare(vehicles_per_second_read, vehicles_per_second) #number of cars it takes for the potential rate to pass given rate

    if(vehicle_number >= model_number):
        print("Change the light!")
    else:
        print("Keep the light.")

results()
