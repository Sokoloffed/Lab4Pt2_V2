import random

from Professor import Professor
from Room import Room
from Slot import Slot
from Group import Group
from Course import Course

POPULATION = 15
# here we specify the amount of population members which are supposed to be best
N_BEST = int(POPULATION * 0.3)
MUTATION_LEVEL = 10

Group.groups = [
    Group("TTP-41", 25),
    Group("TTP-42", 20),
    Group("MI-4", 23),
    Group("TK-4", 12),
    Group("TTP-32", 24),
    Group("K-26", 24)
]

Professor.professors = [
    Professor("Taranukha"),
    Professor("Bugayov"),
    Professor("Fedorus"),
    Professor("Hlybovets"),
    Professor("Radyvonenko"),
    Professor("Ryabokon"),
    Professor("Kulyabko"),
    Professor("Zavadsky"),
    Professor("Tereschchenko"),
    Professor("Tymashoff"),
    Professor("Vergunova"),
    Professor("Panchenko"),
    Professor("Pashko"),
    Professor("Fedorova"),
]

Room.rooms = [
    Room("1", 30, is_lab=False),
    Room("2", 30, is_lab=False),
    Room("3", 15, is_lab=True),
    Room("4", 15, is_lab=True),
    Room("204", 18, is_lab=True),
    Room("205", 18, is_lab=True),
    Room("232", 25, is_lab=True),
    Room("234", 18, is_lab=True),
    Room("302", 30, is_lab=False),
    Room("303", 30, is_lab=False),
    Room("304", 30, is_lab=False),
    Room("305", 30, is_lab=False),
    Room("306", 30, is_lab=False),
    Room("307", 30, is_lab=False),
    Room("308", 30, is_lab=False),
    Room("39", 120, is_lab=False),
    Room("43", 120, is_lab=False),
    Room("42", 60, is_lab=False),
    Room("40", 60, is_lab=False),
]

Course.courses = [
    Course("Intelligence Systems", ["MI-4", "TK-4", "TTP-41", "TTP-42"], "Hlybovets", ["Bugayov", "Fedorus"]),
    Course("QA", ["TTP-41", "TTP-42"], "Panchenko", ["Pahcnenko", "Fedorova"]),
    Course("Business-analytics systems", ["TTP-41", "TTP-42"], "Panchenko", ["Panchenko"]),
    Course("Management", ["MI-4", "TK-4", "TTP-41", "TTP-42"], "Tymashoff", ["Vergunova"]),
    Course("Machine Learning", ["MI-4"], "Radyvonenko"),
    Course("Image Recognition", ["MI-4"], "Ryabokon"),
    Course("Refactoring Problems", ["MI-4"], "Kulyabko"),
    Course("Algorithms", ["K-26"], "Zavadsky", ["Taranukha", "Zavadsky"]),
    Course("DBMS", ["K-26"], "Kulyabko", ["Kulyabko", "Taranukha", "Zavadsky"]),
    Course("Computational Geometry", ["TTP-32"], "Tereschenko", ["Tereschenko"]),
    Course("Quantum Computation", ["TTP-32"], "Zavadsky"),
    Course("Operating Systems", ["TTP-32"], "Panchenko", ["Panchenko", "Fedorova"]),
    Course("Artificial Intelligence", ["TK-4"], "Pashko", ["Pashko"]),
    Course("Programming Paradigms", ["TK-4"], "Pashko", ["Pashko"])
]

Slot.slots = [
    Slot("08:40", "10:15", "Mon"),
    Slot("10:35", "12:10", "Mon"),
    Slot("12:20", "13:55", "Mon"),
    Slot("08:40", "10:15", "Tue"),
    Slot("10:35", "12:10", "Tue"),
    Slot("12:20", "13:55", "Tue"),
    Slot("08:40", "10:15", "Wed"),
    Slot("10:35", "12:10", "Wed"),
    Slot("12:20", "13:55", "Wed"),
    Slot("08:40", "10:15", "Thu"),
    Slot("10:35", "12:10", "Thu"),
    Slot("12:20", "13:55", "Thu"),
    Slot("08:40", "10:15", "Fri"),
    Slot("10:35", "12:10", "Fri"),
    Slot("12:20", "13:55", "Fri"),
]


def generate_random_schedule():
    # Here we generate a dictionary for all timeslots and all group, looks like:
    # (8:40 - 10:15(Mon), 'TTP-4') = None, where at left part is timeslot + groupname, at right part = class name
    schedule = {(slot, group.name): None for slot in Slot.slots for group in Group.groups}

    for course in Course.courses:
        # here we get random timeslot-groupname pair from schedule
        random_key = get_random_key(schedule)
        # generating schedule record for lecture class (is_lab flag == 0)
        for group in course.groups:
            schedule[(random_key[0], group)] = {
                'course': course,
                'professor': course.lecturer,
                # randomly get room
                'room': random.choice(Room.rooms),
                'is_lab': 0
            }

        # if there are trainers - teachers, who lead seminars - are present for this course, we also
        # add one more record in schedule,but with is_lab flag == 1
        if course.trainers is not None:
            for group in course.groups:
                random_key = get_random_key(schedule)
                schedule[(random_key[0], group)] = {
                    'course': course,
                    'professor': random.choice(course.trainers),
                    'room': random.choice(Room.rooms),
                    'is_lab': 1
                }

    return schedule


def get_random_key(schedule):
    random_key = random.choice(list(schedule.keys()))
    while schedule[random_key] is not None:
        random_key = random.choice(list(schedule.keys()))
    return random_key


def generate_random_schedule_2():
    schedule = {}
    temp_list = Slot.slots
    random.shuffle(temp_list)

    for group in Group.groups:

        appended_courses = []

        for slot in temp_list:

            rand_course = random.choice([c for c in Course.courses if group.name in c.groups])
            is_lab = random.choice([1, 0]) if rand_course.trainers else 0

            if (rand_course, is_lab) in appended_courses:
                schedule[(group, slot)] = None
                continue
            appended_courses.append((rand_course, is_lab))

            if (group, slot) not in schedule:
                schedule[(group, slot)] = {
                    'course': rand_course,
                    'professor': random.choice(
                        [rand_course.lecturer] + rand_course.trainers) if is_lab else rand_course.lecturer,
                    'room': random.choice(Room.rooms),
                    'is_lab': is_lab
                }

            if not is_lab and len(rand_course.groups) > 1:
                for split_group in rand_course.groups:
                    if split_group != group and (split_group, slot) not in schedule:
                        schedule[(split_group, slot)] = {
                            'course': rand_course,
                            'professor': random.choice(
                                [rand_course.lecturer] + rand_course.trainers) if is_lab else rand_course.lecturer,
                            'room': random.choice(Room.rooms),
                            'is_lab': is_lab
                        }

    return schedule


def generate_schedules(n: int):
    return [generate_random_schedule() for i in range(n)]


def count_rooms_overlaps(schedule: dict):
    counts = 0
    for room in Room.rooms:
        for slot in Slot.slots:
            temp = sum(
                1 if schedule[(slot, group.name)] is not None and schedule[(slot, group.name)]['room'] == room else 0 for group in
                Group.groups)
            counts += 0 if temp == 1 else temp
    return counts


def count_professors_overlaps(schedule):
    counts = 0
    for professor in Professor.professors:
        for slot in Slot.slots:
            temp = sum(
                1 if schedule[(slot, group.name)] is not None and schedule[(slot, group.name)]['professor'] == professor else 0 for group in
                Group.groups)
            counts += 0 if temp == 1 else temp
    return counts

# this method calculates course overlapses
def count_courses_overlaps(schedule):
    counts = 0
    for course in Course.courses:
        for slot in Slot.slots:
            temp = sum(
                1 if schedule[(slot, group.name)] is not None and schedule[(slot, group.name)]['course'] == course else 0 for group in
                Group.groups)
            counts += 0 if temp == 1 else temp
    return counts


def check_lectures(schedule):
    counts = 0
    for key, value in schedule.items():
        slot, group = key
        if len(value['groups']) > 1:
            for split_group in value['groups']:
                if split_group != group and schedule[(slot, split_group.name)]['room'] != schedule[key]['room']:
                    counts += 1
    return counts


def count_none(schedule):
    counts = 0
    for key, value in schedule.items():
        counts += 10 if schedule[key] is None else 0
    return counts


def check_room_fitness(schedule):
    counts = 0
    for key, value in schedule.items():
        _, group = key
        counts += 1 if value is not None and Group.groups[Group.get_id(group)].size > value['room'].size else 0
        counts += 1 if value is not None and value['is_lab'] == value['room'].is_lab else 0
    return counts

# here the fitness value for schedule is being calculated
# if all coefficients equals 0, the fitness is 1/1 = 1 == the fittest solution has been founded
def single_fitness(schedule):

    return 1 / (1 + count_courses_overlaps(schedule)
                + count_professors_overlaps(schedule)
                + count_rooms_overlaps(schedule)
                + check_room_fitness(schedule)
                + count_none(schedule))


def fitness(schedules):
    res = {}
    for i in range(len(schedules)):
        res[i] = single_fitness(schedules[i])
    return res


def check_goal(schedules):
    fitn = fitness(schedules)
    best_pair = min(zip(fitn.values(), fitn.keys()))
    if best_pair[0] == 1:
        return best_pair[1]
    else:
        return None


def selection(schedules):
    return random.sample(schedules, POPULATION)


def crossover_single(schedule_one, schedule_two):
    schedule_1, schedule_2 = schedule_one.copy(), schedule_two.copy()
    for key, _ in schedule_1.items():

        # here we swap rooms for timeslot-group pairs in dictionary from 1 and 2 schedules
        if random.choice([True, False]) and (schedule_1[key] is not None) and (schedule_2[key] is not None):
            schedule_1[key]['room'], schedule_2[key]['room'] = schedule_2[key]['room'], schedule_1[key]['room']

        if random.choice([True, False]) and (schedule_1[key] is not None) and (schedule_2[key] is not None):
            if (schedule_1[key]['is_lab'] == 0 and len(schedule_1[key]['course'].groups) > 1) \
                    or (schedule_2[key]['is_lab'] == 0 and len(schedule_2[key]['course'].groups) > 1):
                continue

            else:
                schedule_1[key]['course'], schedule_2[key]['course'] = schedule_2[key]['course'], schedule_1[key][
                    'course']
                schedule_1[key]['professor'], schedule_2[key]['professor'] = schedule_2[key]['professor'], \
                                                                             schedule_1[key][
                                                                                 'professor']
                schedule_1[key]['is_lab'], schedule_2[key]['is_lab'] = schedule_2[key]['is_lab'], schedule_1[key][
                    'is_lab']



        else:
            schedule_1[key], schedule_2[key] = schedule_2[key], schedule_1[key]

    return [schedule_1, schedule_2]


def mutate_single(schedule):
    rand_schedule = generate_random_schedule()
    return crossover_single(schedule, rand_schedule)


def pretty_print(schedule):
    by_group = {group.name: [] for group in Group.groups}
    for key, value in schedule.items():
        slot, group = key
        if value:
            by_group[group].append({'course': value['course'],
                                    'professor': value['professor'],
                                    'room': value['room'],
                                    'is_lab': value['is_lab'],
                                    'slot': slot})
        else:
            by_group[group].append({'course': ' ',
                                    'professor': ' ',
                                    'room': ' ',
                                    'is_lab': ' ',
                                    'slot': slot})

    for key, values in by_group.items():
        print('----------> {}'.format(key))
        per_day = {day: [] for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']}
        for value in values:
            per_day[value['slot'].day].append(value)
        for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']:
            print('|---> DAY: {}'.format(day.upper()))
            for el in per_day[day]:

                if el['course'] != ' ':
                    print("|-> {} - {}: {}, {} ({}) ({})".format(el['slot'].start, el['slot'].end, el['course'],
                                                                 el['professor'], el['room'],
                                                                 'P' if el['is_lab'] else 'L'))
                else:
                    print("|-> {} - {}: free".format(el['slot'].start, el['slot'].end))
        print("---------->\n\n")


def genetic_algorithm(iteration_count):
    # here we generated 15 (POPULATION value) random schedules
    population = generate_schedules(POPULATION)
    # here we sort generated schedules (population) on their fitness value in descending order
    population = list(sorted(population, key=lambda x: single_fitness(x), reverse=True))
    # we take the first value of list of sorted population as best individual, because it has the biggest fitness value
    best_individual = {
        'individual': population[0],
        'fitness': single_fitness(population[0])
    }

    i = 0
    while i < iteration_count:
        print("{}-th iteration...".format(i))
        i += 1
        # Fitness block
        for individ in population:
            if single_fitness(individ) == 1:
                # in this case, the individ is the fittest solution
                return individ
            if single_fitness(individ) > best_individual['fitness']:
                # if fitness of individ is bigger than fitness of the best individual, we reassign
                # the values of best individuals and continue
                best_individual['individual'] = individ
                best_individual['fitness'] = single_fitness(individ)

        # Selection block
        best_individuals = population[:N_BEST].copy()
        ordinary_individuals = population[N_BEST:POPULATION].copy()

        # Crossover block
        population = best_individuals.copy()
        for bi in best_individuals:
            for oi in ordinary_individuals:
                population.extend(crossover_single(bi, oi))

        # Mutation block
        for ind in random.sample(best_individuals + ordinary_individuals, MUTATION_LEVEL):
            population.extend(mutate_single(ind))

    return best_individual


if __name__ == '__main__':
    while True:
        iteration_count = input("Enter a number of iterations:\n")
        res = genetic_algorithm(int(iteration_count))
        pretty_print(res['individual'])
