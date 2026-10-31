from parse import load_measurements
import matplotlib.pyplot as plt

CACHE_SIZES = [0,1024,2048,4096,8192,16384,32768,65536,131072,262144,524288,1048576,2097152,4194304]

TASKS = ["pca", "disparity"]

VALGRIND_RESULTS = load_measurements()

print("------------------------------------------------------------------")
print("Exploration")
print("------------------------------------------------------------------")

# en théorie on run valgrind, en pratique on récupère les resultats dans les logs
def get_valgrind_result(task, cache_size):
    return VALGRIND_RESULTS[task][cache_size]



# la formule de la question 4 du td
def get_execution_time(valgrind_result):
    L1_hits = valgrind_result.I_refs - valgrind_result.I1_misses + valgrind_result.D_refs - valgrind_result.D1_misses
    L1_miss_L2_hits = valgrind_result.I1_misses - valgrind_result.LLi_misses + valgrind_result.D1_misses - valgrind_result.LLd_misses
    L2_miss = valgrind_result.LLi_misses + valgrind_result.LLd_misses
    return 0.5 * valgrind_result.I_refs + L1_hits + 13 * L1_miss_L2_hits + 124 * L2_miss



pca_period = 1.75 * get_execution_time(get_valgrind_result("pca",0))
disparity_period = 1.75 * get_execution_time(get_valgrind_result("disparity",0))

print("tasks periodes : ", pca_period, disparity_period)



def is_feasible(l_execution_time, l_period):
    n = len(l_execution_time)
    if n == 0:
        return True
    U = sum(C / T for C, T in zip(l_execution_time, l_period))
    U_max = n * (2 ** (1 / n) - 1)
    return U <= U_max, U



def pareto_front(l_cache_size_cpu):
    x, y = zip(*l_cache_size_cpu)
    plt.scatter(x, y)
    plt.xlabel("Cache total (kB)")
    plt.ylabel("Utilisation CPU")
    plt.title("Front de Pareto")
    plt.grid()
    plt.show()



def branch_and_bound(l_cache):
    valgrind_results = {}
    nb_valgrind = 0
    solutions = []

    # pca en premier
    for pca_cache_size in l_cache: 

        key = f"pca_{pca_cache_size}"

        if key in valgrind_results:
            pca_execution_time = get_execution_time(valgrind_results[key])
        else:
            val_result = get_valgrind_result("pca", pca_cache_size)
            valgrind_results[key] = val_result
            pca_execution_time = get_execution_time(valgrind_results[key])
            nb_valgrind +=1

        # si pas faisable on élimine la branche
        if not is_feasible([pca_execution_time],[pca_period])[0]:
            print(f"{pca_cache_size} not feasible")
            continue

        # sinon on passe sur le disparity
        else:
            for disparity_cache_size in l_cache:
                key = f"disparity_{disparity_cache_size}"
                
                if key in valgrind_results:
                    disparity_execution_time = get_execution_time(valgrind_results[key])
                else:
                    val_result = get_valgrind_result("disparity", disparity_cache_size)
                    valgrind_results[key] = val_result
                    disparity_execution_time = get_execution_time(valgrind_results[key])
                    nb_valgrind +=1
        
                # si pas faisable on élimine la branche
                if not is_feasible([pca_execution_time, disparity_execution_time],[pca_period, disparity_period])[0]:
                    print(f"{pca_cache_size} and {disparity_cache_size} not feasible")
                    continue

                solutions.append((pca_cache_size+disparity_cache_size, is_feasible([pca_execution_time, disparity_execution_time],[pca_period, disparity_period])[1]))
                print(f"new solution found {[pca_cache_size, disparity_cache_size]}")
                break

                

    return solutions, nb_valgrind


res = branch_and_bound(CACHE_SIZES)

pareto_front(res[0])
