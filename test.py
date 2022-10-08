import tasks

# un ejemplo de trabajos sin horas libres
list = [ 
    tasks.Elem(tasks.DayActions.job, 0, 1),
    tasks.Elem(tasks.DayActions.job, 1, 2),
    tasks.Elem(tasks.DayActions.job, 5, 6),
]

# se rellenan los espacios entre las horas
fill_list = tasks.fill_emptys(list, 0, 10)
print("\nfill list:")
for i in fill_list:
    print(i)

# se separan los espacios libres en perceptiles
rest_list = tasks.emptys_gen(fill_list, 10)
print("\nrestore list:")
for i in rest_list:
    print(i)

# se vuelven a unir los espacios separados anteriormente
new_list = tasks.maping_emptys(rest_list)
print("\nnew list:")
for i in new_list:
    print(i)