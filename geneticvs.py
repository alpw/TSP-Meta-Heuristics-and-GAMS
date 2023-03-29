import random, math
import matplotlib.pyplot as plt
from time import time


def plot_all(best):
    #visualise
    x, y = [], []
    for i in best:
        x.append(cities_list[i][1])
        y.append(cities_list[i][0])
        plt.text(cities_list[i][1],cities_list[i][0],cities_list[i][2])
    x.append(x[0])
    y.append(y[0])
    plt.title("Genetic Algorithm")
    plt.scatter(x,y)
    plt.plot(x,y)
    plt.axis([25, 46, 35, 43])
    plt.show()
    plt.draw()


def f(try_current):
    #total value(length) of cities_list
    total = 0
    for index1, index2 in zip(try_current, try_current[1::]):
        total += math.sqrt((cities_list[index1][0] - cities_list[index2][0])**2 + (cities_list[index1][1] - cities_list[index2][1])**2)
    return total + math.sqrt((cities_list[try_current[0]][0] - cities_list[try_current[-1]][0])**2 + (cities_list[try_current[0]][1] - cities_list[try_current[-1]][1])**2)


def create_gnome():
    while True:
        gnome = random.sample(range(len_cities), len_cities)
        if gnome not in population:
            return gnome


def fill_population(size):
    for _ in range(size - len(population)):
        population.append(create_gnome())


def cross_over(gnome1, gnome2):
    index = random.randint(1, len(gnome1)-1)
    new_gnome1 = gnome1[:index]
    for gene in gnome2:
        if not gene in new_gnome1:
            new_gnome1.append(gene)

    new_gnome2 = gnome2[:index]
    for gene in gnome1:
        if not gene in new_gnome2:
            new_gnome2.append(gene)

    return [new_gnome1, new_gnome2]


def mutated(gnome):
    new_gnome = gnome[:]
    while True:
        index1 = random.randint(0, len(gnome)-1)
        index2 = random.randint(0, len(gnome)-1)
        if index1 != index2:
            new_gnome[index1] = gnome[index2]
            new_gnome[index2] = gnome[index1]
            return new_gnome


def tournament(size, func):
    global population
    sample = random.sample(population, size)
    sample_fitness = list(zip([func(x) for x in sample], sample))
    return max(list(sample_fitness))[1]


#get data
cities_list = []
with open("data.txt", "r", encoding="UTF-8") as file:
    data = file.readlines()
    for elem in data:
        i = elem.split("\t")
        cities_list.append((float(i[3]), float(i[4]), i[2]))
#cities_list: [(36.98542, 35.32502, 'Adana'),(40.656314, 35.837068, 'Amasya')...]
len_cities = len(cities_list)


population = [] #[[2,0,1,4,3...], [0,4,3,1,2...]...]


def run(time_limit=20, Cx = 0.9, Mx = 0.1, pop_size = 20, T_size = 3, E_size = 1):
    #Cx = crossover, Mx = mutation, pop_size = population size, T_size = tournament size, E_size = elitism size
    
    global population
    fitness = lambda x: 1/f(x)

    fill_population(pop_size)

    now = time()
    timeint = int(now)
    #algorithm
    while (time() - now) < time_limit:

        new_population = []

        #elitism
        fitness_list = [fitness(x) for x in population]
        fit_gnome = list(zip(fitness_list, population))
        fit_gnome.sort(reverse=True)
        new_population += [x[1] for x in fit_gnome][:E_size]

        while len(new_population) <= pop_size:

            #choosing parents
            parent1 = tournament(T_size, fitness)
            parent2 = tournament(T_size, fitness)

            #one point crossover
            if Cx > random.random():
                child1, child2 = cross_over(parent1, parent2)
            else:
                child1, child2 = parent1, parent2

            #mutation
            if Mx > random.random():
                child1 = mutated(child1)
            if Mx > random.random():
                child2 = mutated(child2)

            new_population += [child1, child2]

        population = new_population[:pop_size]

        #print best every second
    #    if timeint != int(time()):
    #        print(f"time: {int(timeint - now +1)} | best: {f(population[0])}")
    #    timeint = int(time())


    fitness_list = [fitness(x) for x in population]
    fit_gnome = list(zip(fitness_list, population))
    fit_gnome.sort(reverse=True)
    print("Genetic Algorithm: ",f(fit_gnome[0][1]))
    return (f(fit_gnome[0][1]), fit_gnome[0][1])

print("genetic ready")