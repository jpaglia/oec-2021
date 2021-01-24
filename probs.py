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
  # Note that this is a heuristic to allow for speed
  # We take the 5 most infected students, with that logic, if 5 students are infected
  # They will infect an additiona 15 (ie the whole class)
  # So additional checks a superfluous

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

def update_with_factor(prev_probability, percent_increase, period):
  # Creates the Bayes interpretation logic
  new_percent_increase = percent_increase
  if period == 2 or period == 4:
    new_percent_increase += 0.25 # Our additional factor for dirty surfaces
  if period == 2.5:
    new_percent_increase += 1
  
  new_prob = prev_probability/(prev_probability + (1/new_percent_increase)*(1-prev_probability))
  return new_prob


def get_new_class_infection_probs(infected_set, unique_increase, dfwrapper, class_name, prev_period, current_period):
  # Steps of Algorithm
  # 1.) First get the base infection rate for an average student
  # 2.) Get the unique probability by increasing that amount by their specific conditions
  augmented_infected_set = copy.deepcopy(infected_set)
  teacher_info = []
  if not class_name == '':
    new_prev = prev_period
    if prev_period == 2.5:
      new_prev = 2
    teacher_info = dfwrapper.get_teachers_for_class(class_name, new_prev, current_period)
    augmented_infected_set.append(teacher_info[1])

  
  # Also have to consider teachers and TA's as well
  base_infection_amount = calculate_base_prob(augmented_infected_set)

  # Update teacher Data and TA data
  if not class_name == '':
    if teacher_info[1] == 1.0:
      dfwrapper.update_teacher_infection_value(teacher_info[0], current_period, 1.0)
    else:
      dfwrapper.update_teacher_infection_value(teacher_info[0], current_period, base_infection_amount)

  unique_infection_prob = []
  for index in range(0, len(infected_set)):
    
    if (infected_set[index] == 1.0):
      new_prob = 1.0
    else:
      new_prob = update_with_factor(base_infection_amount, unique_increase[index], current_period)
    unique_infection_prob.append(new_prob)
  return unique_infection_prob


def get_thresh_hold_infected(threshold, infection_list):
  data = 0
  for student in infection_list:
    if student[1] > threshold:
      data += 1
  return data
