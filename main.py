import sys
import random

class Individual:
    def __init__(self):
        self.gnome = ""
        self.fitness = 0

    def __lt__(self, other): # allows < comparison
        return self.fitness < other.fitness

    def __gt__(self, other): # allows > comparison
        return self.fitness > other.fitness


Genes = "01234"
numberOfCities = 5
INT_MAX = sys.maxsize # maximum signed integer value 2^64 - 1
population_size = 10
temperature = 10000

def repeated(str, ch):
    for i in range(len(str)):
        if str[i] == ch:
            return True
    return False

def mutate(gnome):
    gnome = list(gnome)
    while True:
        r = random.randint(1, numberOfCities - 1)
        r1 = random.randint(1, numberOfCities - 1)
        if r != r1:
            temp = gnome[r]
            gnome[r] = gnome[r1]
            gnome[r1] = temp
            break

    return ''.join(gnome)

def create_gnome():
    gnome = "0"
    while True:
        if len(gnome) == numberOfCities:
            gnome += gnome[0]
            break

        temp = random.randint(1, numberOfCities - 1)
        if not repeated(gnome, chr(temp + 48)):
            gnome += chr(temp + 48)

    return gnome

def cal_fitness(gnome, mp):
    f = 0
    for i in range(len(gnome) - 1):
        if mp[ord(gnome[i]) - 48][ord(gnome[i + 1]) - 48] == INT_MAX:
            return INT_MAX
        f += mp[ord(gnome[i]) - 48][ord(gnome[i + 1]) - 48]

    return f

def cooldown(temp):
    return (90*temp)/100

def TSPUtil(mp):
    gen = 1
    gen_thres = 5

    population = []
    temp = Individual()

    for i in range(population_size):
        temp.gnome = create_gnome()
        temp.fitness = cal_fitness(temp.gnome, mp)
        population.append(temp)

    print("\nInitial population: \nGNOME     FITNESS VALUE\n")
    for i in range(population_size):
        print(population[i].gnome, population[i].fitness)
    print()

    temperature = 10000

    while temperature > 1000 and gen <= gen_thres:
        population.sort()
        print("\nCurrent temp: ", temperature)
        new_population = []

        for i in range(population_size):
            p1 = population[i]

            while True:
                new_g = mutate(p1.gnome)
                new_gnome = Individual()
                new_gnome.gnome = new_g
                new_gnome.fitness = cal_fitness(new_gnome.gnome, mp)

                if new_gnome.fitness <= population[i].fitness:
                    new_population.append(new_gnome)
                    break

                else: # disallows use of children that have too little of a deviation to parent in a negative way in e^(-dFitness)
                    prob = pow(2.7,-1* ((float)(new_gnome.fitness - population[i].fitness)/temperature),)
                    if prob > 0.5:
                        new_population.append(new_gnome)
                        break

        temperature = cooldown(temperature)
        population = new_population
        print("Generation", gen)
        print("GNOME     FITNESS VALUE")

        for i in range(population_size):
            print(population[i].gnome, population[i].fitness)
        gen += 1


if __name__ == "__main__":

    mp = [
        [0, 3, INT_MAX, 12, 5],
        [5, 0, 4, 8, INT_MAX],
        [INT_MAX, 4, 0, 1, 3],
        [10, 8, 3, 0, 9],
        [5, INT_MAX, 3, 10, 0],
    ]
    TSPUtil(mp)