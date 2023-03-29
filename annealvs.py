import random, math
import matplotlib.pyplot as plt

def plot_all(best):
    #visualise
    x, y = [], []
    for i in best:
        x.append(cities_list[i][1])
        y.append(cities_list[i][0])
        plt.text(cities_list[i][1],cities_list[i][0],cities_list[i][2])
    x.append(x[0])
    y.append(y[0])
    plt.title("Simulated Annealing")
    plt.scatter(x,y)
    plt.plot(x,y)
    plt.axis([25,46,35,43])
    plt.show()
    plt.draw()

def f(try_current):
    #total value(length) of cities_list
    total = 0
    for index1, index2 in zip(try_current, try_current[1::]):
        total += math.sqrt((cities_list[index1][0] - cities_list[index2][0])**2 + (cities_list[index1][1] - cities_list[index2][1])**2)
    return total + math.sqrt((cities_list[try_current[0]][0] - cities_list[try_current[-1]][0])**2 + (cities_list[try_current[0]][1] - cities_list[try_current[-1]][1])**2)

#get data
cities_list = []
with open("data.txt", "r", encoding="UTF-8") as file:
    data = file.readlines()
    for elem in data:
        i = elem.split("\t")
        cities_list.append((float(i[3]), float(i[4]), i[2]))
#cities_list: [(36.98542, 35.32502, 'Adana'),(40.656314, 35.837068, 'Amasya')...]

def generate_nghbr(current):
    #changes random 2 value of the current
    new = current[:]
    index1 = random.randint(0, len(cities_list)-1)
    index2 = random.randint(0, len(cities_list)-1)
    while index1 == index2:
        index2 = random.randint(0, len(cities_list)-1)
    new[index1] = current[index2]
    new[index2] = current[index1]
    return new


def run(t_start = 1000, t_end = 0.01, alpha = 0.999, markov = 50):
    
    #starting values
    current = random.sample(range(len(cities_list)), len(cities_list))
    best = current[:]
    temp = t_start

    #algorithm
    while temp > t_end:
        for _ in range(markov):
            nghbr = generate_nghbr(current)[:]

            delta = f(nghbr) - f(current)
            if delta < 0 or math.e**(-delta/temp) > random.random():
                current = nghbr[:]

                if f(current) < f(best):
                    best = current[:]

        temp *= alpha
    #   print("temp: "+str(temp)[:5], "| best: "+str(f(best))[:7], "| current: "+str(f(current))[:7])
    
    print("Simulated Annealing: ", f(best))
    return (f(best), best)

print("annealing ready")