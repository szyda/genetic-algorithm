import random
import math
import numpy as np
import matplotlib.pyplot as plt

# f(x) = 0.2*x(1/2) + 2*sin(2*pi*0.02x)+5
# x >= 0 x <= 255
# f_max(x) = 9.916

def generate_chromosomes(size_of_population):
    chromosomes = []

    chromosomes = [[random.randint(0, 1) for _ in range(8)] for _ in range(size_of_population)]
    return chromosomes

def calculate_function_value(x):
    return (0.2 * math.pow(float(x), 0.5) + 2 * math.sin(float(2 * math.pi * 0.02 * float(x))) + 5)

# def calculate_roulette(function_values):
#     sum_of_function_values = sum(function_values)
#     fittnes_of_chromosome = [round(y / sum_of_function_values * 100, 2) for y in function_values]
#     sum_of_fittnes = sum(fittnes_of_chromosome)

def choose_parents(population_size, population, sum_of_fittnes, fittnes_of_chromosome):
    parents = []

    for x in range(population_size):
        number_for_parent = random.uniform(0, sum_of_fittnes)
        fittnes_sum = 0

        for i, value in enumerate(fittnes_of_chromosome):
            fittnes_sum += value
            if fittnes_sum >= number_for_parent:
                parents.append(population[i])
                break

    return parents

def crossover(population_size, parents, pk):
    children = []
    size = population_size // 2

    for i in range(size):
        first_parent = random.choice(parents)
        parents.remove(first_parent)

        second_parent = random.choice(parents)
        parents.remove(second_parent)

        if random.uniform(0, 1) <= pk:
            crossover_point = random.randint(1, 7)
            children.append(first_parent[:crossover_point] + second_parent[crossover_point:])
            children.append(second_parent[:crossover_point] + first_parent[crossover_point:])
        else:
            children.append(first_parent)
            children.append(second_parent)

    return children

def mutation(population_size, children, pm):
    for i in range(population_size):
        if random.uniform(0, 1) <= pm:
            mutation_point = random.randint(0, 7)
            if children[i][mutation_point] == 1:
                children[i][mutation_point] = 0
            else:
                children[i][mutation_point] = 1


def update_function_values(function_values, best_fittness_value):
    avg_f_values = np.average(function_values)

    if avg_f_values > best_fittness_value:
        best_fittness_value = avg_f_values
        bestChromosome = population[np.argmax(function_values)]
    adaptation_values.append(avg_f_values * 10)

def genetic_algorithm(pk, pm, population_size, number_of_generations):
    population = generate_chromosomes(population_size)
    adaptation_values = []
    max_fittnes = -float('inf')
    current_generation = 0

    for current_generation in range(number_of_generations):
        function_values = []

        for i in range(population_size):
            x = sum([population[i][j] * pow(2, 7 - j) for j in range(8)])
            y = calculate_function_value(x)
            function_values.append(y)

        sum_of_function_values = sum(function_values)
        fittnes_of_chromosome = [round(y / sum_of_function_values * 100, 2) for y in function_values]
        sum_of_fittnes = sum(fittnes_of_chromosome)

        parents = choose_parents(population_size, population, sum_of_fittnes, fittnes_of_chromosome)
        children = crossover(population_size, parents, pk)
        mutation(population_size, children, pm)

        population = children

        update_avg_fittnes_value = np.average(function_values)
        if update_avg_fittnes_value > max_fittnes:
            max_fittnes = update_avg_fittnes_value
        adaptation_values.append(update_avg_fittnes_value)

    return adaptation_values, max_fittnes

# def show_result(ch, dec_values, wsk_przystosowania):
#     print("Chromosom | Wartosc funkcji | Wskaznik przystosowania")
#     for i in range(len(ch)):
#         print(ch[i], "  " ,dec_values[i], "           " , wsk_przystosowania[i])

# def show_pie_plot(chromosoms, wskazniki, procents):
#     colors = [plt.cm.viridis(random.random()) for _ in range(len(chromosoms))]
#     plt.figure(figsize=(14, 8))
#     plt.pie(procents, labels=chromosoms, colors=colors, autopct='%1.3f%%', startangle=140)
#     plt.legend(chromosoms, title="Chromosomy", loc="center left", bbox_to_anchor=(1, 0.5))
#     plt.axis('equal')
#     plt.title("Procentowy udział chromosomów\n\n")
#     plt.show()

def main():
    pk_values = [0.5, 0.6, 0.7, 0.8, 0.9, 1]
    pm_values = [0.0, 0.01, 0.06, 0.1, 0.2, 0.3, 0.5]
    population_size = 200
    number_of_generations = 200

    for pm in pm_values:
        plt.figure(figsize=(10, 6))

        for pk in pk_values:
            adaptation_values, max_fittnes = genetic_algorithm(pk, pm, population_size, number_of_generations)
            print(f'pk={pk}, pm={pm}:', max_fittnes)

            plt.plot(adaptation_values, label=f'pk={pk}')

        plt.title(f"Genetic algorithm for pm={pm}")
        plt.xlabel("Generations")
        plt.ylabel("Adaptation value")
        plt.legend()
        plt.show()

main()
