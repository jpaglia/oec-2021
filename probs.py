import itertools
import heapq
import df_ops
import copy

# Function to determine the probability of infection
# Based on who is infected in the class
def calculate_base_prob(infected_set):
  infected_set_small = heapq.nlargest(5, infected_set)
  for i in range(len(infected_set_small)):
    infected_set_small[i] = infected_set_small[i] * 3/len(infected_set)
  
  base_probability = sum(infected_set_small) # P(A) + P(B) + P(C) ....
  add = False
  for union_inclusion in range(2, len(infected_set)+1):
    x = 0
    for prob_set in itertools.combinations(infected_set_small, union_inclusion):   
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


def get_new_class_infection_probs(infected_set, unique_increase, dfwrapper, class_name, period):
  # Steps of Algorithm
  # 1.) First get the base infection rate for an average student
  # 2.) Get the unique probability by increasing that amount by their specific conditions
  # teacher_infection = dfwrapper.get_teachers_for_class(class_name, period)
  # Also have to consider teachers and TA's as well
  base_infection_amount = calculate_base_prob(infected_set)
  unique_infection_prob = []
  for index in range(0, len(infected_set)):
    
    if (infected_set[index] == 1.0):
      new_prob = 1.0
    else:
      new_prob = update_with_factor(base_infection_amount, unique_increase[index])
    unique_infection_prob.append(new_prob)
  return unique_infection_prob


def get_thresh_hold_infected(threshold, infection_list):
  data = 0
  for student in infection_list:
    if student[1] > threshold:
      data += 1
  return data
