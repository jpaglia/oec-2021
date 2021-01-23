import itertools

infected_set = [0.25, 0.25, 0.25, 0.25] # All student's probability of being sick

base_probability = sum(infected_set) # P(A) + P(B) + P(C) ....


add = False
for union_inclusion in range(2, len(infected_set)+1):
  for prob_set in itertools.combinations(infected_set, union_inclusion):
    multiplied_prob = 1
    for elem in prob_set:
      multiplied_prob = multiplied_prob * elem  
    if add:
      base_probability = base_probability + multiplied_prob
    else:
      base_probability = base_probability - multiplied_prob
  add = not add

print(base_probability)