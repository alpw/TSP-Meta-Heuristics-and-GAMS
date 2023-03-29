import geneticvs, annealvs
from time import time, sleep
sleep(1)

def sim_anneal():
    anneal_start = time()
    anneal_best = annealvs.run(alpha=0.95)
    annel_end = time()
    anneal_total_time = annel_end - anneal_start
    return (anneal_best[0], anneal_best[1], anneal_total_time) #(f(best), best, time)

def genetic_algh(time):
    genetic_best = geneticvs.run(time)
    return (genetic_best[0], genetic_best[1]) #(f(best), best)

anneal_data = []
genetic_data = []
for i in range(5):
    anneal_data.append(sim_anneal())
    genetic_data.append(genetic_algh(anneal_data[i][2]))


print("Toplam zaman | Tavlama Benzetimi | Genetik Algoritma")
for i, elem in enumerate(anneal_data):
    print(f"{str(elem[2])[:5]}        | {str(elem[0])[0:5]}             | {str(genetic_data[i][0])[0:5]}")

anneal_data.sort(reverse=True)
genetic_data.sort(reverse=True)

print("\nOrtalama zaman", sum(x[2] for x in anneal_data)/len(anneal_data))

print("Tavlama benzetimi ortalama değeri: ", sum(x[0] for x in anneal_data)/len(anneal_data))
print("Genetik algoritma ortalama değeri: ", sum(x[0] for x in genetic_data)/len(genetic_data))

#plotting
annealvs.plot_all(anneal_data[0][1])
geneticvs.plot_all(genetic_data[0][1])