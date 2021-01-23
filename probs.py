import itertools
# Function to determine the probability of infection
# Based on who is infected in the class
def calculate_base_prob(infected_set):
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

  return base_probability

def update_with_factor(prev_probability, percent_increase):
  # Creates the Bayes interp
  new_prob = prev_probability/(prev_probability + (1/percent_increase)*(1-prev_probability))
  return new_prob


def get_new_class_infection_probs(infected_set):
  # Steps of Algorithm
  # 1.) First get the base infection rate for an average student
  # 2.) Get the unique probability by increasing that amount by their specific conditions
  base_infection_amount = calculate_base_prob(infected_set)
  unique_infection_prob = []
  for index in range(0, len(infected_set)):
    new_prob = update_with_factor(base_infection_amount, unique_increase[index])
    unique_infection_prob.append(new_prob)
  return unique_infection_prob
 
infected_set = [0.25, 0.25, 0.25, 0.25, 0] # All student's probability of being sick + TA + Teacher
unique_increase = [1.25, 1.25, 1.25, 1.95, 1.25]
test = get_new_class_infection_probs(infected_set)
print(test)