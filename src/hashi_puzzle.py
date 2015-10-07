'''
Created on Mar 9, 2015

@author: Tommy
'''
import copy
import math

#from bst_linked import *

SAME_DIRECTION_BRIDGES = 2
MAX_COORDINATE = 10
'''
islands = []
marked_coordinates = []
'''
def is_there_enough_num_of_edges_left_in_the_neighbors_for_the_center(i, neighbor_coordinates, islands):
    result = False
    num_of_edges_for_the_neighbors = 0
    for n in neighbor_coordinates:
        num_of_edges_for_the_neighbors += how_many_left(n, islands)
    if islands[i]["num_of_bridges_left"] <= num_of_edges_for_the_neighbors:
        result = True
    print("is_there_enough_num_of_edges_left_in_the_neighbors_for_the_center() returns {0}".format(result))
    return result

#1 == len(temp_hv_answers[0]) has to be 1 becuz it's adding A BRIDGE!!!!!!!!!!!!!!!!!!!
#temp_hv_answers = [ [(1, 1, 1, 4)], [(1, 1, 3, 1)] ]
def isolating_a_segment_by_adding_a_bridge(i, temp_hv_answers, islands):
    coordy = extract_the_neighbor_coordy_from_t(temp_hv_answers[0][0], i)
    smallest = how_many_left( coordy, islands )
    smallest_tha = copy.deepcopy( temp_hv_answers[0][0] )
    hml = 0
    for tha in temp_hv_answers:
        hml = how_many_left( extract_the_neighbor_coordy_from_t(tha[0], i), islands )
        if smallest > hml and hml >= islands[i]["num_of_bridges_left"]:
            smallest = copy.deepcopy(hml)
            smallest_tha = copy.deepcopy(tha[0])
    print("isolating_a_segment_by_adding_a_bridge(): {0} is removed from {1}".format([smallest_tha], temp_hv_answers))
    temp_hv_answers.remove( [smallest_tha] )
    print("isolating_a_segment_by_adding_a_bridge() returns {0} and {1}".format(smallest_tha, temp_hv_answers))   
    return smallest_tha, temp_hv_answers

def list_difference(list1, list2):
    """uses list1 as the reference, returns list of items not in list2"""
    diff_list = []
    for item in list1:
        if not item in list2:
            diff_list.append(item)
        else:
            if list2.count(item) != list1.count(item) and not item in diff_list:
                diff_list.append(item)       
    return diff_list

def is_it_already_in_temp_hv_answers(num_bridges_to_deduct, i, temp, temp_hv_answer, temp_hv_answers):#, temp_num_of_bridges_left):
    if (num_bridges_to_deduct != 0) and (islands[i]['num_of_bridges_left'] == len(temp+temp_hv_answer)) and (temp+temp_hv_answer in temp_hv_answers):
        #print("num_bridges_to_deduct: {0} will be added to temp_num_of_bridges_left: {1}".format(num_bridges_to_deduct, temp_num_of_bridges_left))
        #temp_num_of_bridges_left += num_bridges_to_deduct
        print("because temp: {0} + temp_hv_answer: {1} is already in temp_hv_answers: {2}".format(temp, temp_hv_answer, temp_hv_answers))
        result = True
    elif (num_bridges_to_deduct == 0):
        result = False
        print("is_it_already_in_temp_hv_answers(): num_bridges_to_deduct == 0")
    else:
        result = False
    print("is_it_already_in_temp_hv_answers() returns result: {0}".format(result)) #and temp_num_of_bridges_left: {1}".format(result, temp_num_of_bridges_left))
    return result#, temp_num_of_bridges_left

def find_j(i, neighbor_coordinates):
    j=0
    n=0
    found=False
    while not(found) and n < len(islands[i]["neighbors"]):
        if (((islands[i]["num_of_bridges"] == 1) and (islands[i]["neighbors"][n][1] != 1)) or ((islands[i]["num_of_bridges"] == 2) and (islands[i]["neighbors"][n][1] != 2))) and (islands[i]["neighbors"][n][0] in neighbor_coordinates):
            j=copy.deepcopy(n)
            found=True
        else:
            n += 1
    print("find_j() returns {0} for islands[i]['neighbors'][j]={1}".format(j, islands[i]["neighbors"][j]))
    return j

def is_this_iso_tech_1(neighbors_length, i, neighbor_bridges, h_answer, v_answer):
    if (neighbors_length == 2) and\
    (  ((islands[i]["num_of_bridges"] == 1) and (islands[i]["num_of_bridges_left"] == 1) and (((1 in neighbor_bridges) and (1 == len(neighbor_bridges) - neighbor_bridges.count(1)))) )\
    or ((islands[i]["num_of_bridges"] == 2) and (islands[i]["num_of_bridges_left"] == 2) and (((2 in neighbor_bridges) and (1 == len(neighbor_bridges) - neighbor_bridges.count(2)))) )   )\
    and not(iso_1_neighbor_connected(islands[i]["coordinates"], islands[i]["neighbors"], h_answer, v_answer)):#and (islands[i]["num_of_bridges_left"] == 2) was taken off because of (8, 2) of ultra easy    #or ((2 == how_many_left(neighbor_coordinates[0]) or 2 == how_many_left(neighbor_coordinates[1])) and 4 != how_many_left(neighbor_coordinates[0]) + how_many_left(neighbor_coordinates[1])) ))   ):#and (islands[i]["neighbors"][j][1] != 2) # iso 1 #or (neighbors_length == 3) was added because of step 11
        #connected_neighbor(islands[i]["coordinates"], find_neighbor_coordinate_without_the_input_vertex(neighbor_coordinates, [2]), h_answer, v_answer) was changed to
        print("iso tech 1 after: ")# this was updated because of (6,2) of ultra easy
        result=True
    else:
        result=False
    print("is_this_iso_tech_1() returns {0}".format(result))
    return result

def connect_after_find_duplicates(connections, i, h_answer, v_answer, islands):
    for line in connections:
        print("the line is {0}".format(line))
        k = 0
        line_found = False
        while k < len(islands[i]["neighbors"]) and not(line_found):#neighbors_length
            if (islands[i]["neighbors"][k][0] == (line[0], line[1])):
                #is_there_isolation_for_else() was commented out because of (7, 5) of ultra easy 
                if (0 <= how_many_left((line[0], line[1]), islands) - 1):# and not(is_there_isolation_for_else(i, k, neighbor_blocked, h_answer, v_answer)):# and not(is_this_neighbor_isolation(i, k, neighbor_blocked, h_answer, v_answer)):
                    connect_to_neighbor_and_mark(i, k, True, h_answer, v_answer, True, islands)
                    line_found = True
                else:
                    print("if: 0 !<= island[k]['num_of_bridges_left']-1")#islands[i]['num_of_bridges_left']")
                    k = len(islands)
            elif (islands[i]["neighbors"][k][0] == (line[2], line[3])):
                #is_there_isolation_for_else() was commented out because of (7, 5) of ultra easy 
                if (0 <= how_many_left((line[2], line[3]), islands) - 1):# and not(is_there_isolation_for_else(i, k, neighbor_blocked, h_answer, v_answer)):# and not(is_this_neighbor_isolation(i, k, neighbor_blocked, h_answer, v_answer)):
                    connect_to_neighbor_and_mark(i, k, True, h_answer, v_answer, True, islands)
                    line_found = True
                else:
                    print("elif: 0 !<= island[k]['num_of_bridges_left']-1")#-islands[i]['num_of_bridges_left']")
                    k = len(islands)
            else:
                k += 1
    print("connect_after_find_duplicates() returns connections: {0}, h_answer: {1}, v_answer: {2}".format(connections, h_answer, v_answer))
    return connections, h_answer, v_answer

def all_neighbors_connected(center_coordinate, neighbor_coordinates, h_answer, v_answer):
    result = True
    
    for n in neighbor_coordinates:
        result = result and connected_neighbor(center_coordinate, n[0], h_answer, v_answer)
    print("all_neighbors_connected() returns {0}".format(result))
    return result

def basic_5_neighbors_connected(center_coordinate, neighbor_coordinates, h_answer, v_answer):
    result = True
    
    for n in neighbor_coordinates:
        if n[1] != 1:
            result = result and connected_neighbor(center_coordinate, n[0], h_answer, v_answer) and (what_is_vertex(center_coordinate) == 6 and n[1] != 1)
        else:#n[1] ==1
            print("basic_5_neighbors_connected(): we don't care if {0} is connected to {1}".format(center_coordinate, n[1])) 
    print("basic_5_neighbors_connected() returns {0}".format(result))
    return result

def iso_1_neighbor_connected(center_coordinate, neighbor_coordinates, h_answer, v_answer):
    result = False
    i=0
    #for n in neighbor_coordinates:
    while not(result) and i <len(neighbor_coordinates):
        result = connected_neighbor(center_coordinate, neighbor_coordinates[i][0], h_answer, v_answer) and ((what_is_vertex(center_coordinate) == 2 and neighbor_coordinates[i][1] != 2) or (what_is_vertex(center_coordinate) == 1 and neighbor_coordinates[i][1] != 1))
        i += 1 
    print("iso_1_neighbor_connected() returns {0}".format(result))
    return result

def is_this_valid_basic_3(i, j, neighbor_coordinates, neighbors_length, basic_tech_3):
    #checking if there are enough number of neighbors with enough edges left corresponding to the islands, 3, 5, or 7
    #ex) for the island 3, there should be the neighbor with n["num_of_bridges_left"]>=2 and the neighbor with n["num_of_bridges_left"]==1
    #    for the island 5, there should be the two neighbors with n["num_of_bridges_left"]>=2 and the neighbor with n["num_of_bridges_left"]==1
    #(islands[i]["num_of_bridges_left"]<=how_many_left(neighbor_coordinates[0])+how_many_left(neighbor_coordinates[1]))
    print("is_this_valid_basic_3(): The inputs were {0}, {1}, and {2}".format(islands[i]["num_of_bridges_left"], neighbor_coordinates, neighbors_length))
    bool = False
    count_one = 0
    count_twos = 0
    neighbor_total = 0
    
    for n in neighbor_coordinates:
        how_many = how_many_left(n, islands)
        neighbor_total += how_many
        if how_many is 1:
            count_one += 1
        elif how_many >= 2:
            count_twos += 1
    if j == 0 and basic_tech_3:
        if count_one == 1 and count_twos + count_one == neighbors_length and islands[i]["num_of_bridges_left"] <= neighbor_total:
            bool = True
        else:
            print("more than 1s/too less or many 2s/the num of neighbor bridges left!=the num of island bridges left")
    elif basic_tech_3:#if this is not a first neighbor
        if islands[i]["num_of_bridges_left"] <= neighbor_total:
            bool = True
        else:
            print("what the ?????")
    else:
        print("basic_tech_3==False")
    print("is_this_valid_basic_3() returns {0}".format(bool))
    #basic_tech_3=bool
    return bool

def what_are_neighbor_coordinates_marked_blocked(islands, i, v_answer, h_answer):
    neighbor_bridges = []
    neighbor_coordinates = []
    neighbor_marked_and_not_blocked = []
    neighbor_blocked = []
    
    print("what_are_neighbor_coordinates_marked_blocked(): The first argument is islands[i]['neighbors']: {0}".format(islands[i]["neighbors"]))
    for n in islands[i]["neighbors"]:
        if n[0][0] == islands[i]["coordinates"][0]:#horizontal neighbor
            #for v_a in v_answer:
            l = 0
            v_block_found = False
            while l < len(v_answer) and not(v_block_found):
                #print("the line, {0} is between {1} and {2}!!!".format(v_answer[l], n[0], islands[i]["coordinates"]))
                if (islands[i]["coordinates"][0] in range(v_answer[l][0] + 1, v_answer[l][2])) and v_answer[l][1] in range(min(n[0][1], islands[i]["coordinates"][1]) + 1, max(n[0][1], islands[i]["coordinates"][1])):#if there is a vertical line between the vertex and the neighbor
                    print("what_are_neighbor_coordinates_marked_blocked(): {0} is between {1} and {2}, and ".format(islands[i]["coordinates"][0], v_answer[l][0] + 1, v_answer[l][2]), end="")
                    print("what_are_neighbor_coordinates_marked_blocked(): {0} is between {1} and {2}".format(v_answer[l][1], min(n[0][1], islands[i]["coordinates"][1]) + 1, max(n[0][1], islands[i]["coordinates"][1])))
                    print("what_are_neighbor_coordinates_marked_blocked(): the line, {0} is between {1} and {2}".format(v_answer[l], n[0], islands[i]["coordinates"]))
                    v_block_found = True
                l += 1
                
            if not(v_block_found) and not(marked(n[0], islands)):
                neighbor_coordinates.append(n[0])
                neighbor_bridges.append(n[1])
            if not(v_block_found) and (marked(n[0], islands)):
                neighbor_marked_and_not_blocked.append(n[0])

        elif n[0][1] == islands[i]["coordinates"][1]:
            l = 0
            h_block_found = False
            while l < len(h_answer) and not(h_block_found):
                if (h_answer[l][0] in range(min(n[0][0], islands[i]["coordinates"][0]) + 1, max(n[0][0], islands[i]["coordinates"][0]) + 1)) and (islands[i]["coordinates"][1] in range(min(h_answer[l][1], h_answer[l][3]) + 1, max(h_answer[l][1], h_answer[l][3]))):#if there is a horizontal line between the vertex and the neighbor
                    print("what_are_neighbor_coordinates_marked_blocked(): {0} is between {1} and {2}, and ".format(h_answer[l][0], min(n[0][0], islands[i]["coordinates"][0]), max(n[0][0], islands[i]["coordinates"][0]) + 1), end="")
                    print("what_are_neighbor_coordinates_marked_blocked(): {0} is between {1} and {2}".format(islands[i]["coordinates"][1], min(h_answer[l][1], h_answer[l][3]), max(h_answer[l][1], h_answer[l][3]) + 1))
                    print("what_are_neighbor_coordinates_marked_blocked(): the line, {0} is between {1} and {2}".format(h_answer[l], n[0], islands[i]["coordinates"]))
                    h_block_found = True
                l += 1
    
            if not(h_block_found) and not(marked(n[0], islands)):
                neighbor_coordinates.append(n[0])
                neighbor_bridges.append(n[1])
            if not(h_block_found) and (marked(n[0], islands)):
                neighbor_marked_and_not_blocked.append(n[0])
    j = 0
    while (j < len(islands[i]["neighbors"])):
        if (islands[i]["neighbors"][j][0] not in neighbor_coordinates) and (islands[i]["neighbors"][j][0] not in neighbor_marked_and_not_blocked):# and (islands[i]["neighbors"][j][0] not in neighbor_marked_and_not_blocked):
            #print("{0} was popped because there was a line.".format(islands[i]["neighbors"].pop(j)))
            neighbor_blocked.append(islands[i]["neighbors"][j][0])
            print("what_are_neighbor_coordinates_marked_blocked(): {0} was appended to neighbor_blocked: {1} because there was a line/it wasn't marked.".format(islands[i]["neighbors"][j][0], neighbor_blocked))
        #else:
        j += 1
    return neighbor_bridges, neighbor_coordinates, neighbor_marked_and_not_blocked, neighbor_blocked
#[[(3, 1, 5, 1), (5, 1, 5, 3)], [(3, 1, 5, 1), (5, 1, 8, 1)], [(5, 1, 5, 3), (5, 1, 8, 1)], [(5, 1, 5, 3), (5, 1, 5, 3)], [(5, 1, 8, 1), (5, 1, 8, 1)]]
def extract_the_neighbor_coordies_from_temp_hv_answers(temp_hv_answers, index):
    #[[(2, 3, 2, 5), (2, 5, 2, 7)],   [(2, 3, 2, 5), (2, 5, 5, 5)],   [(2, 5, 2, 7), (2, 5, 5, 5)],   [(2, 5, 2, 7), (2, 5, 2, 7)],   [(2, 5, 5, 5), (2, 5, 5, 5)]]
    coordies = []
    #[(3, 1, 5, 1), (5, 1, 5, 3)]
    for n_coordinates in temp_hv_answers:
        coordy = []
        #(3, 1, 5, 1)
        for n_coordinate in n_coordinates:
            if islands[index]['coordinates'] == (n_coordinate[0], n_coordinate[1]):
                coordy.append((n_coordinate[2], n_coordinate[3]))
            else:#islands[index]['coordinates'] != (n_coordinate[0], n_coordinate[1])
                coordy.append((n_coordinate[0], n_coordinate[1]))
        coordies.append(coordy)
    print("extract_the_neighbor_coordies_from_temp_hv_answers() returned {0}".format(coordies))
    return coordies

def extract_the_neighbor_coordies_from_temp_hv_answer(temp_hv_answer, index):
    #temp_hv_answer=[(2, 8, 5, 8), (2, 8, 5, 8)]
    print("extract_the_neighbor_coordies_from_temp_hv_answer(): {0} and {1} were the inputs".format(temp_hv_answer, index))
    coordies = []
    for line in temp_hv_answer:
        #line=(2, 8, 5, 8)
        if islands[index]['coordinates'] == (line[0], line[1]):
            coordy = (line[2], line[3])
        else:#islands[index]['coordinates'] != (line[0], line[1])
            coordy = (line[0], line[1])
        coordies.append(coordy)
    print("extract_the_neighbor_coordies_from_temp_hv_answer() returned {0}".format(coordies))
    return coordies
#t = (1, 1, 1, 4)
def extract_the_neighbor_coordy_from_t(t, index):
    #[(2, 8, 5, 8), (2, 8, 5, 8)]
    print("extract_the_neighbor_coordy_from_t(): {0} and {1} were the inputs".format(t, index))
    #coordy = ()
    #for n_coordinate in temp_hv_answer:
        #(2, 8, 5, 8)
    #print("{0}".format(islands[index]['coordinates']))
    if islands[index]['coordinates'] == (t[0], t[1]):
        coordy = (t[2], t[3])
    else:#islands[index]['coordinates'] != (n_coordinate[0], n_coordinate[1])
        coordy = (t[0], t[1])
    #coordies.append(coordy)
    print("extract_the_neighbor_coordy_from_t() returned {0}".format(coordy))
    return coordy

def extract_the_num_of_lines_from_line_with_count_in_list(line_with_count_in_list, index, neighbor_index):
    num_of_lines = 0
    found = False
    etnolflwcil = 0
    #[(2, 3, 2, 5), 1]
    #for line_with_count in line_with_count_in_list:#[[(2, 3, 2, 5), 1], [(2, 5, 2, 7), 1]]
    #line_w_count_in_list = line_with_count_in_list_in_iti(temp_hv_answers[t_n_i])
    while not(found) and etnolflwcil < len(line_with_count_in_list):#[[(2, 3, 2, 5), 1], [(2, 5, 2, 7), 1]]
        if islands[index]['coordinates'] == (line_with_count_in_list[etnolflwcil][0][0], line_with_count_in_list[etnolflwcil][0][1]) or islands[index]['coordinates'] == (line_with_count_in_list[etnolflwcil][0][2], line_with_count_in_list[etnolflwcil][0][3]):
            print("islands[index]['neighbors'][neighbor_index][0] == (line_with_count[0][0], line_with_count[0][1]): {0} ?= {1}".format(islands[index]["neighbors"][neighbor_index][0], (line_with_count_in_list[etnolflwcil][0][0], line_with_count_in_list[etnolflwcil][0][1])))
            print("{0}".format((line_with_count_in_list[etnolflwcil][0][2], line_with_count_in_list[etnolflwcil][0][3])))
            if islands[index]["neighbors"][neighbor_index][0] == (line_with_count_in_list[etnolflwcil][0][0], line_with_count_in_list[etnolflwcil][0][1]):
                num_of_lines = line_with_count_in_list[etnolflwcil][1]
                found = True
                print("extract_the_num_of_lines_from_line_with_count_in_list(): if")
            elif islands[index]["neighbors"][neighbor_index][0] == (line_with_count_in_list[etnolflwcil][0][2], line_with_count_in_list[etnolflwcil][0][3]):
                num_of_lines = line_with_count_in_list[etnolflwcil][1]
                found = True
                print("extract_the_num_of_lines_from_line_with_count_in_list(): elif")
            else:
                print("extract_the_num_of_lines_from_line_with_count_in_list(): line_with_count is {0}".format(line_with_count_in_list[etnolflwcil]))
        else:#islands[index]['coordinates'] != (n_coordinate[0], n_coordinate[1])
            print("extract_the_num_of_lines_from_line_with_count_in_list(): islands[index]['coordinates'] != (line_with_count[0][0], line_with_count[0][1]) and islands[index]['coordinates'] != (line_with_count[0][2], line_with_count[0][3])")
            num_of_lines = -1
            
        etnolflwcil += 1
        
    print("extract_the_num_of_lines_from_line_with_count_in_list() returned {0}".format(num_of_lines))
    return num_of_lines

def extract_the_num_of_lines_from_line(line, index, neighbor_index):
    num_of_lines = 0
    found = False
    #(2, 3, 2, 5)
    #for line_with_count in line_with_count_in_list:#[[(2, 3, 2, 5), 1], [(2, 5, 2, 7), 1]]
    if islands[index]['coordinates'] == (line[0], line[1]) or islands[index]['coordinates'] == (line[2], line[3]):
        print("islands[index]['neighbors'][neighbor_index][0] == (line[0], line[1]) or (line[2], line[3]): {0} ?= {1} or {2}".format(islands[index]["neighbors"][neighbor_index][0], (line[0], line[1]), (line[2], line[3])))
        if islands[index]["neighbors"][neighbor_index][0] == (line[0], line[1]):
            num_of_lines += 1
            found = True
        elif islands[index]["neighbors"][neighbor_index][0] == (line[2], line[3]):
            num_of_lines = line[1]
            found = True
        else:
            print("extract_the_num_of_lines_from_line(): line is {0}".format(line))
    else:#islands[index]['coordinates'] != (n_coordinate[0], n_coordinate[1])
        print("extract_the_num_of_lines_from_line(): islands[index]['coordinates'] != (line[0], line[1]) or islands[index]['coordinates'] != (line[2], line[3])")
        num_of_lines = -1
        
    print("extract_the_num_of_lines_from_line() returned {0}".format(num_of_lines))
    return num_of_lines

def find_neighbor_coordinates(index, neighbor_index_inside_neighbors, neighbor_blocked):#, islands, marked_coordinates):
    l = 0
    found = False
    neighbor_coordinates = []
    while (l < len(islands)) and (not(found)):
        #print(l)
        #print(islands[index]["neighbors"][neighbor_index_inside_neighbors][0])
        #print(islands[l]["coordinates"])
        if islands[index]["neighbors"][neighbor_index_inside_neighbors][0] == islands[l]["coordinates"]:
            found = True
            
            if 0 != len(islands[l]["neighbors"]):
                #make sure that there is no neighbors blocked
                for n in islands[l]["neighbors"]:
                    if (n[0] not in neighbor_blocked) and (n[0] != islands[index]['coordinates']):#################################################################################################################################################
                        neighbor_coordinates.append(n[0])
                print("find_neighbor_coordinates(): without the vertex and the neighbors blocked, neighbor_coordinates are {0}".format(neighbor_coordinates))
            else:#there is no neighbor or the num_of_bridges is 1 or 2
                print("find_neighbor_coordinates(): shit")
                
        else:
            l += 1
    print("find_neighbor_coordinates() is returning {0}".format(neighbor_coordinates))
    return neighbor_coordinates

def find_neighbor_coordinate_without_the_input_vertex(neighbor_coordinates, input_vertexs):
    l = 0
    found = False
    coordinate = []
    while (l < len(islands)) and (not(found)):
        #print(l)
        #print(islands[index]["neighbors"][neighbor_index_inside_neighbors][0])
        #print(islands[l]["coordinates"])
        for n in neighbor_coordinates:
            if (n == islands[l]["coordinates"]) and (islands[l]["num_of_bridges"] not in input_vertexs):
                found = True
                coordinate = copy.deepcopy(islands[l]["coordinates"])
        l += 1
    print("find_neighbor_coordinate_without_the_input_vertex(): the result is {0}".format(coordinate))
    return coordinate

def find_connected_neighbor_coordinates_of_target_neighbor(index, neighbor_index_inside_neighbors, neighbor_blocked, h_answer, v_answer):
    l = 0
    found = False
    neighbor_coordinates = []
    while (l < len(islands)) and (not(found)):
        #print(l)
        #print(islands[index]["neighbors"][neighbor_index_inside_neighbors][0])
        #print(islands[l]["coordinates"])
        if islands[index]["neighbors"][neighbor_index_inside_neighbors][0] == islands[l]["coordinates"]:
            found = True
            
            if 0 != len(islands[l]["neighbors"]):
                #make sure that there is no neighbors blocked
                for n in islands[l]["neighbors"]:
                    if (n[0] not in neighbor_blocked) and (n[0] != islands[index]['coordinates']) and connected_neighbor(islands[l]['coordinates'], n[0], h_answer, v_answer):#################################################################################################################################################
                        neighbor_coordinates.append(n[0])
                print("find_connected_neighbor_coordinates_of_target_neighbor(): without the vertex and the neighbors blocked, neighbor_coordinates are {0}".format(neighbor_coordinates))
            else:#there is no neighbor or the num_of_bridges is 1 or 2
                print("find_connected_neighbor_coordinates_of_target_neighbor(): shit")
                
        else:
            l += 1
    return neighbor_coordinates

def connected_neighbor(center_coordinate, neighbor_coordinate, h_answer, v_answer):
    i = 0
    result = False
    #for h_line in h_answer:
    while not(result) and i < len(h_answer):
        if ((h_answer[i][0], h_answer[i][1]) == center_coordinate and (h_answer[i][2], h_answer[i][3]) == neighbor_coordinate) or\
           ((h_answer[i][2], h_answer[i][3]) == center_coordinate and (h_answer[i][0], h_answer[i][1]) == neighbor_coordinate):
            result = True
        else:
            i += 1
    #for v_line in v_answer:
    i = 0
    while not(result) and i < len(v_answer):
        if ((v_answer[i][0], v_answer[i][1]) == center_coordinate and (v_answer[i][2], v_answer[i][3]) == neighbor_coordinate) or\
           ((v_answer[i][2], v_answer[i][3]) == center_coordinate and (v_answer[i][0], v_answer[i][1]) == neighbor_coordinate):
            result = True
        else:
            i += 1
    print("connected_neighbor(): were center:{0} and neighbor:{1} connected?: {2}".format(center_coordinate, neighbor_coordinate, result))
    return result

def marked(coordinates, islands):
    bool = False
    i = 0
    done = False
    while i < len(islands) and not(done):
        if coordinates == islands[i]['coordinates']:
            print("marked(): {0}".format(islands[i]))
            bool = islands[i]['mark']
            done = True
        i += 1
    print("marked(): {0} is marked? {1}".format(coordinates, bool))
    return bool

def find_the_index_for_neighbor_index(index, neighbor_index_inside_neighbors):
    l = 0
    found = False
    result_index = -1
    while (l < len(islands)) and (not(found)):
        #print(l)
        #print(islands[index]["neighbors"][neighbor_index_inside_neighbors][0])
        #print(islands[l]["coordinates"])
        if islands[index]["neighbors"][neighbor_index_inside_neighbors][0] == islands[l]["coordinates"]:
            found = True
            result_index = l
        else:
            l += 1
    print("find_the_index_for_neighbor_index(): result_index is {0} which is {1}".format(result_index, islands[l]["coordinates"]))
    return result_index

def find_the_index_for_the_input_coordinate(index, coordinate):
    l = 0
    found = False
    result_index = -1
    while (l < len(islands)) and (not(found)):
        #print(l)
        #print(islands[index]["neighbors"][neighbor_index_inside_neighbors][0])
        #print(islands[l]["coordinates"])
        if coordinate == islands[l]["coordinates"]:
            found = True
            result_index = l
        else:
            l += 1
    print("find_the_index_for_the_input_coordinate(): result_index is {0} which is {1}".format(result_index, islands[l]["coordinates"]))
    return result_index

def find_neighbor_coordinates_for_the_input_coordinate(coordinate, index, neighbor_blocked, h_answer, v_answer):#, islands, marked_coordinates):
    l = 0
    found = False
    neighbor_coordinates = []
    while (l < len(islands)) and (not(found)):
        #print(l)
        #print(islands[index]["neighbors"][neighbor_index_inside_neighbors][0])
        #print(islands[l]["coordinates"])
        if coordinate == islands[l]["coordinates"]:
            found = True
            
            if 0 != len(islands[l]["neighbors"]):
                #make sure that there is no neighbors blocked
                for n in islands[l]["neighbors"]:
                    if (n[0] not in neighbor_blocked) and (n[0] != islands[index]['coordinates']) and connected_neighbor(coordinate, n[0], h_answer, v_answer):#################################################################################################################################################
                        neighbor_coordinates.append(n[0])
                print("find_neighbor_coordinates_for_the_input_coordinate(): without the vertex and the neighbors blocked, neighbor_coordinates are {0}".format(neighbor_coordinates))
            else:#there is no neighbor or the num_of_bridges is 1 or 2
                print("find_neighbor_coordinates_for_the_input_coordinate(): shit")
                
        else:
            l += 1
    return neighbor_coordinates

def line_with_count_in_list_in_iti(temp_hv_answers):
    print("line_with_count_in_list_in_iti(): {0} is passed to this func".format(temp_hv_answers))
    line_count_in_list = []
    for line in temp_hv_answers:#[(2, 3, 2, 5), (2, 5, 2, 7)]
        line_with_count = [line, temp_hv_answers.count(line)]
        if line_with_count not in line_count_in_list:
            line_count_in_list.append(line_with_count)
    print("line_with_count_in_list_in_iti() returns line_count_in_list={0}".format(line_count_in_list))
    return line_count_in_list

def target_coordy_with_count_in_list_in_iti(temp_hv_answers, center_coordinate):
    print("target_coordy_with_count_in_list_in_iti(): {0} is passed to this func".format(temp_hv_answers))
    target_count_in_list = []
    for line in temp_hv_answers:#[(2, 3, 2, 5), (2, 5, 2, 7)]
        if center_coordinate == (line[0], line[1]):
            target_with_count = [(line[2], line[3]), temp_hv_answers.count(line)]
        else:
            target_with_count = [(line[0], line[1]), temp_hv_answers.count(line)]
        if target_with_count not in target_count_in_list:
            target_count_in_list.append(target_with_count)
    print("target_coordy_with_count_in_list_in_iti() returns line_count_in_list={0}".format(target_count_in_list))
    return target_count_in_list
#line_count_in_list=[[(6, 8), 1], [(9, 6), 1]]
def is_there_isolation_aux(neighbors, index, neighbor_index, checked_coordinates, neighbor_blocked, h_answer, v_answer, line_count_in_list, islands):
    print("is_there_isolation_aux(): start")
    if neighbor_index < len(neighbors) and connected_neighbor(islands[index]["coordinates"], neighbors[neighbor_index], h_answer, v_answer):
        print("is_there_isolation_aux(): checking {0} which is {1}'s neighbor".format(neighbors[neighbor_index], islands[index]["coordinates"]))
        
        #line_count_in_list=[[(6, 8), 1], [(9, 6), 1]]
        just_found=False
        just_index=0
        print("neighbors is {0}".format(neighbors))
        print("neighbors[neighbor_index] is {0}".format(neighbors[neighbor_index]))
        print("line_count_in_list is {0}".format(line_count_in_list))
        while not(just_found) and just_index < len(line_count_in_list):
            if neighbors[neighbor_index] == line_count_in_list[just_index][0] and line_count_in_list[just_index][1] == how_many_left(neighbors[neighbor_index], islands):
                just_found = True
                print("is_there_isolation_aux(): neighbors[neighbor_index]: {0} is virtually marked".format(neighbors[neighbor_index]))
            just_index += 1
                
        if (marked(neighbors[neighbor_index], islands) or just_found or neighbors[neighbor_index] in checked_coordinates) and neighbors[neighbor_index] not in checked_coordinates:
            checked_coordinates.append(neighbors[neighbor_index])
            print("is_there_isolation_aux(): {0} is appended to {1}".format(neighbors[neighbor_index], checked_coordinates))
            
            if (neighbor_index == len(neighbors) - 1) and (what_is_vertex(neighbors[neighbor_index]) == 1 or (what_is_vertex(neighbors[neighbor_index]) == 2 and len(neighbors) == 1)) and (marked(neighbors[neighbor_index], islands)):#Last one 
                print("is_there_isolation_aux(): if")
                
                if marked(neighbors[neighbor_index], islands):
                    new_index = find_the_index_for_the_input_coordinate(index, neighbors[neighbor_index])
                    new_neighbors = find_neighbor_coordinates_for_the_input_coordinate(neighbors[neighbor_index], index, neighbor_blocked, h_answer, v_answer)
                    
                    if marked(islands[new_index]['coordinates'], islands) and new_neighbors != []:
                        print("if marked(islands[new_index]['coordinates'], islands) and new_neighbors != []:")
                        result = is_there_isolation_aux(new_neighbors, new_index, 0, checked_coordinates, neighbor_blocked, h_answer, v_answer, line_count_in_list, islands)
                    else:
                        print("if new_neighbors == []:")
                        result = marked(islands[new_index]['coordinates'], islands)
                else:
                    print("else: is {0} marked? {1}".format(neighbors[neighbor_index], marked(neighbors[neighbor_index], islands)))
                    result = False            
            elif (what_is_vertex(neighbors[neighbor_index]) == 1 or (what_is_vertex(neighbors[neighbor_index]) == 2 and len(neighbors) == 1)) and (marked(neighbors[neighbor_index], islands)):
                print("is_there_isolation_aux(): elif")
                if (neighbor_index < len(neighbors) - 1):
                    result = marked(neighbors[neighbor_index], islands) and is_there_isolation_aux(neighbors, index, neighbor_index + 1, checked_coordinates, neighbor_blocked, h_answer, v_answer, line_count_in_list, islands)
                else:
                    print("neighbor_index !< len(neighbors)-1")
                    result = marked(neighbors[neighbor_index], islands)
            else:#when it's not the last one and not the above 
                print("is_there_isolation_aux(): else")#(neighbors, index, neighbor_index, checked_coordinates, neighbor_blocked, h_answer, v_answer)
                there_is_pre_result = False
                if (neighbor_index < len(neighbors) - 1):
                    result = is_there_isolation_aux(neighbors, index, neighbor_index + 1, checked_coordinates, neighbor_blocked, h_answer, v_answer, line_count_in_list, islands)
                    there_is_pre_result = True
                    
                new_index = find_the_index_for_the_input_coordinate(index, neighbors[neighbor_index])
                new_neighbors = find_neighbor_coordinates_for_the_input_coordinate(neighbors[neighbor_index], index, neighbor_blocked, h_answer, v_answer)
                
                #result = marked(neighbors[neighbor_index], islands) and is_there_isolation_aux(new_neighbors, new_index, 0, checked_coordinates, neighbor_blocked, h_answer, v_answer)
                if (marked(islands[new_index]['coordinates'], islands) or neighbors[neighbor_index] in checked_coordinates) and new_neighbors != []:
                    print("else: if marked(islands[new_index]['coordinates'], islands) and new_neighbors != []:")
                    if there_is_pre_result == True:
                        result = result and is_there_isolation_aux(new_neighbors, new_index, 0, checked_coordinates, neighbor_blocked, h_answer, v_answer, line_count_in_list, islands)
                    else:
                        result = is_there_isolation_aux(new_neighbors, new_index, 0, checked_coordinates, neighbor_blocked, h_answer, v_answer, line_count_in_list, islands)
                else:
                    print("else: if new_neighbors == []:")
                    if there_is_pre_result == True:
                        result = result and marked(islands[new_index]['coordinates'], islands)
                    else:
                        result = marked(islands[new_index]['coordinates'], islands)
        
        else:
            print("is_there_isolation_aux(): {0} is in checked_coordinates or not marked.".format(neighbors[neighbor_index]))#or in line_count_in_list
            
            result = marked(neighbors[neighbor_index], islands)# or just_found
            
    else:#neighbor_index >= len(neighbors) and/or NOT(connected_neighbor(islands[index]["coordinates"], neighbors[neighbor_index], h_answer, v_answer)):
        if neighbor_index < len(neighbors) and not(connected_neighbor(islands[index]["coordinates"], neighbors[neighbor_index], h_answer, v_answer)):
            print("is_there_isolation_aux(): {0} < {1} or {2} is not connected to {3}".format(neighbor_index, len(neighbors), islands[index]["coordinates"], neighbors[neighbor_index]))
            result = marked(neighbors[neighbor_index], islands)
        elif neighbor_index >= len(neighbors) and (connected_neighbor(islands[index]["coordinates"], neighbors[neighbor_index], h_answer, v_answer)):
            print("is_there_isolation_aux(): {0} >= {1} or {2} is connected to {3}".format(neighbor_index, len(neighbors), islands[index]["coordinates"], neighbors[neighbor_index]))
            print("neighbor_index >= len(neighbors) shouldn't happen")
        else:#neighbor_index >= len(neighbors) and not(connected_neighbor(islands[index]["coordinates"], neighbors[neighbor_index], h_answer, v_answer)):
            print("is_there_isolation_aux(): {0} >= {1} or {2} is not connected to {3}".format(neighbor_index, len(neighbors), islands[index]["coordinates"], neighbors[neighbor_index]))
            print("neighbor_index >= len(neighbors) shouldn't happen") 
    print("is_there_isolation_aux(): the result is {0}".format(result))
    return result
'''
def is_this_coordinate_s_connected_and_marked_neighbor_isolated(index, target_neighbor_indexes):
    isolation = False
    #for neighbor in islands[index]["neighbors"]:
    for connected_and_marked_neighbor in islands[index]["marked_neighbor_coordinates"]:#connected_neighbor(islands[index]["coordinates"], neighbor[0], h_answer, v_answer) and
        result_index = find_the_index_for_the_input_coordinate(index, connected_and_marked_neighbor)
        if result_index != -1:
            
        else:
            print("there is no index for the neighbor: {0}".format(connected_and_marked_neighbor))
    return isolation
'''

def is_there_the_only_way_without_isolation(index, target_neighbor_indexes, neighbor_blocked, h_answer, v_answer, neighbor_marked_and_not_blocked, temp_hv_answers, islands):#temp_num_of_bridges_left, num_bridges_to_deduct, 
    #before deciding the connection between the target neighbor and the vertex, we have to check whether this vertex is connected to a isolated segment or not
    #this works only when how_many_num_of_bridges_left == 0 and how_many_left(islands[index]["neighbors"][target_neighbor_index][0]) == 0
    #temp_num_of_bridges_left -= num_bridges_to_deduct
    result = False
    result_list = []#False
    #if (temp_num_of_bridges_left == 0):# and (how_many_left(islands[index]["neighbors"][target_neighbor_index][0])-num_bridges_to_deduct == 0):
        #see if the neighbors of the index coordinate are marked or not
    #count = 0
    
    #n_i = 0
    t_n_i = 0
    suspicious_neighbor = -1
    isolation = []
    for target_neighbor_index in target_neighbor_indexes:
        isolation.append(False)
    #for neighbor in islands[index]["neighbors"]:
    #while quit and n_i < len(islands[index]["neighbors"]):
    while t_n_i < len(target_neighbor_indexes):#keep_going and 
        #if (n_i not in target_neighbor_indexes) and (islands[index]["neighbors"][n_i][0] not in neighbor_blocked) and not(marked(islands[index]["neighbors"][n_i][0], islands)):#and (islands[index]["neighbors"][n_i][0] not in neighbor_marked_and_not_blocked):
        #num_of_lines = extract_the_num_of_lines_from_line_with_count_in_list(line_w_count_in_list, index, n_i)
        
        #how_many, the_n_is_for_non_marked_neighbors = how_many_marked_target_neighbors()
        
        #if (n_i in [[0, 1], [0, 2], [1, 2], [1, 1], [2, 2]])
        line_w_count_in_list = line_with_count_in_list_in_iti(temp_hv_answers[t_n_i])
        target_w_count_in_list = target_coordy_with_count_in_list_in_iti(temp_hv_answers[t_n_i], islands[index]['coordinates'])
        target_in_list = []
        
        for target_w_count in target_w_count_in_list:
            target_in_list.append(target_w_count[0])
        print("target_in_list is {0}.".format(target_in_list))
            
        
        print("target_neighbor_indexes[t_n_i] is {0}".format(target_neighbor_indexes[t_n_i]))
        
        last_index_of_target_neighbor_indexes = len(target_neighbor_indexes[t_n_i]) - 1
        n_i = 0
        keep_going = True
        
        is_there_isolation_aux_result = []
        for each_line in target_neighbor_indexes[t_n_i]:
            is_there_isolation_aux_result.append(False)
        #for n_i in target_neighbor_indexes[t_n_i]:
        while keep_going and n_i < len(target_neighbor_indexes[t_n_i]):
            print("target_neighbor_indexes[t_n_i][n_i] is {0}".format(target_neighbor_indexes[t_n_i][n_i]))
            num_of_lines = extract_the_num_of_lines_from_line_with_count_in_list(line_w_count_in_list, index, target_neighbor_indexes[t_n_i][n_i])
            #if (n_i in target_neighbor_indexes[t_n_i]) and ((how_many_left(islands[index]["neighbors"][n_i][0]) == 1 and num_of_lines == 1) or (how_many_left(islands[index]["neighbors"][n_i][0]) == 2 and num_of_lines == 2)):
            if (how_many_left(islands[index]["neighbors"][target_neighbor_indexes[t_n_i][n_i]][0], islands) == 1 and num_of_lines == 1) or (how_many_left(islands[index]["neighbors"][target_neighbor_indexes[t_n_i][n_i]][0], islands) == 2 and num_of_lines == 2):
                '''
                if marked(islands[index]["neighbors"][n_i][0], islands):
                    print("is_there_isolation(): False is appended to result_list")
                    result_list.append(False)
                else:
                '''
                #print("is_there_isolation(): {0} is one of the current target neighbors, one of the neighbors not blocked and is not marked so is_there_isolation() quit.".format(islands[index]["neighbors"][n_i][0]))
                print("is_there_the_only_way_without_isolation(): ({0} in {1}) and {2} will be marked.".format(target_neighbor_indexes[t_n_i][n_i], target_neighbor_indexes[t_n_i], islands[index]['neighbors'][target_neighbor_indexes[t_n_i][n_i]][0]))
                print("we need further investigations here")
                print()
                print()
                #connected neighbor coordies without the vertex
                neighbor_coordinates = find_connected_neighbor_coordinates_of_target_neighbor(index, target_neighbor_indexes[t_n_i][n_i], neighbor_blocked, h_answer, v_answer)
                print("is_there_the_only_way_without_isolation(): neighbor_coordinates are {0}".format(neighbor_coordinates))
                #if connected_neighbor(islands[index]["coordinates"], islands[index]["neighbors"][target_neighbor_indexes[t_n_i][n_i]][0], h_answer, v_answer):  islands[index]["neighbors"][][0]
                new_index = find_the_index_for_neighbor_index(index, target_neighbor_indexes[t_n_i][n_i])
                                                                    #neighbor_coordinates[0]
                neighbor_bridges_iti, neighbor_coordinates_iti, neighbor_marked_and_not_blocked_iti, neighbor_blocked_iti = what_are_neighbor_coordinates_marked_blocked(islands, new_index, v_answer, h_answer)
                print("neighbor_marked_and_not_blocked_iti is {0}".format(neighbor_marked_and_not_blocked_iti))
                print("neighbor_blocked_iti is {0}".format(neighbor_blocked_iti)) 
                checked_coordinates = [islands[index]['coordinates'], islands[new_index]['coordinates']]
                
                additional_neighbor_coordinates = find_neighbor_coordinates_for_the_input_coordinate(islands[index]['coordinates'], index, neighbor_blocked, h_answer, v_answer)
                print("additional_neighbor_coordinates is {0}".format(additional_neighbor_coordinates))
                if islands[new_index]['coordinates'] in additional_neighbor_coordinates:
                    additional_neighbor_coordinates.remove(islands[new_index]['coordinates'])
                neighbor_coordinates += additional_neighbor_coordinates
                print("after adding additional_neighbor_coordinates, neighbor_coordinates is {0}".format(neighbor_coordinates))
                    
                if neighbor_coordinates != []:
                    '''
                    additional_neighbor_coordinates = find_neighbor_coordinates_for_the_input_coordinate(islands[index]['coordinates'], index, neighbor_blocked, h_answer, v_answer)
                    print("additional_neighbor_coordinates is {0}".format(additional_neighbor_coordinates))
                    if islands[new_index]['coordinates'] in additional_neighbor_coordinates:
                        additional_neighbor_coordinates.remove(islands[new_index]['coordinates'])
                    neighbor_coordinates += additional_neighbor_coordinates
                    print("after adding additional_neighbor_coordinates, neighbor_coordinates is {0}".format(neighbor_coordinates))
                    '''
                    #The last change I made
                    isolated_neighbor = True
                    index_for_neighbor = 0
                    while isolated_neighbor and index_for_neighbor < len(neighbor_coordinates):
                        print()
                        print("Checking {0}'s side!".format(neighbor_coordinates[index_for_neighbor]))
                        
                        if connected_neighbor(islands[new_index]["coordinates"], neighbor_coordinates[index_for_neighbor], h_answer, v_answer):
                            isolated_neighbor = is_there_isolation_aux([neighbor_coordinates[index_for_neighbor]], new_index, 0, checked_coordinates, neighbor_blocked_iti, h_answer, v_answer, target_w_count_in_list, islands)
                        elif connected_neighbor(islands[index]["coordinates"], neighbor_coordinates[index_for_neighbor], h_answer, v_answer):
                            isolated_neighbor = is_there_isolation_aux([neighbor_coordinates[index_for_neighbor]], index, 0, checked_coordinates, neighbor_blocked_iti, h_answer, v_answer, target_w_count_in_list, islands)
                        else:
                            print("??????????????????????????")
                        print("Is all the nodes connected to {0} isolated?: {1}".format(neighbor_coordinates[index_for_neighbor], isolated_neighbor))
                        index_for_neighbor += 1
                    is_there_isolation_aux_result[n_i] = isolated_neighbor
                    print("is_there_isolation_aux_result[{0}] is set to {1}".format(n_i, isolated_neighbor))
                    #print("is_there_isolation_aux_result[n_i] is set to True")
                    ##################################################################################################################################################################
                    #is_there_isolation_aux_result[n_i] = is_there_isolation_aux(neighbor_coordinates, new_index, 0, checked_coordinates, neighbor_blocked_iti, h_answer, v_answer)
                else:#neighbor_coordinates == []:
                    print("else: there is no neighbors for {0}".format(islands[index]["neighbors"][target_neighbor_indexes[t_n_i][n_i]][0]))
                    
                    any_non_marked_target_neighbor_except_the_current_one = False
                    k = 0
                    #for t_n_ii in target_neighbor_indexes:#target_neighbor_indexes: [ [2], [3] ]     or [[1, 2, 3], [1, 2], [3], [2, 3], [1], [1, 3], [2]]
                    while not(any_non_marked_target_neighbor_except_the_current_one) and k < len(target_neighbor_indexes[t_n_i]):
                        print()
                        print("while not(any_non_marked_target_neighbor_except_the_current_one) and k < len(target_neighbor_indexes):")
                        print("any_non_marked_target_neighbor_except_the_current_one: {0}".format(any_non_marked_target_neighbor_except_the_current_one))
                        
                        if k != n_i:
                            print("k: {0} < len({1}): {2}".format(k, target_neighbor_indexes[t_n_i], len(target_neighbor_indexes[t_n_i])))
                            #t_n_ii = target_neighbor_indexes[k]
                                #target_neighbor_indexes[t_n_i][k]
                            '''
                            print("t_n_ii is {0}".format(t_n_ii))
                            #for t_n_i_t in t_n_ii:#[2], [3]...
                            l = 0
                            while l < len(t_n_ii):#not(any_non_marked_target_neighbor_except_the_current_one) and 
                                t_n_i_t = t_n_ii[l]
                                print()
                                print("for t_n_i_t in t_n_ii: for {0} in {1}".format(t_n_i_t, t_n_ii))
                            '''
                            print("islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0] in marked_coordinate: {0} in {1}?".format(islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0], marked_coordinates))
                            print(target_neighbor_indexes[t_n_i][n_i])
                            print("{0} !=? {1}".format(islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0], islands[index]['neighbors'][target_neighbor_indexes[t_n_i][n_i]][0]))
                            '''
                            if (islands[index]['neighbors'][t_n_i_t][0] in marked_coordinates) and (islands[index]['neighbors'][t_n_i_t][0] != islands[index]['neighbors'][target_neighbor_indexes[t_n_i][n_i]][0]):
                                #is_there_isolation_aux_result[n_i] = True
                                print("not looking for this...")
                            '''
                            how_many = 0
                            for t in target_w_count_in_list:
                                if islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0] == t[0]:
                                    how_many = t[1]
                            print("{0} is found in target_w_count_in_list: {1}".format(how_many, target_w_count_in_list))
                                    
                            if (islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0] not in marked_coordinates) and \
                               (how_many_left(islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0], islands) != how_many) and \
                               (islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0] != islands[index]['neighbors'][target_neighbor_indexes[t_n_i][n_i]][0]):
                                #is_there_isolation_aux_result[n_i] = False
                                """
                                matter of (1, 6, 4, 6) and (6, 6, 6, 8)
                                """
                                print("{0} is in {1}?".format(islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0], target_in_list))
                                if (islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0] in target_in_list):# and (islands[index]['neighbors'][t_n_i_t][0] != islands[index]['neighbors'][target_neighbor_indexes[t_n_i][n_i]][0]):
                                    print("there is a non-marked and one of the target neighbors!")
                                    any_non_marked_target_neighbor_except_the_current_one = True
                                #elif islands[index]['neighbors'][t_n_i_t][0] not in target_in_list and
                                elif not(connected_neighbor(islands[index]['coordinates'], islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0], h_answer, v_answer)):
                                    print("the centre, {0} and {1} are not connected".format(islands[index]['coordinates'], islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0]))     
                                else:
                                    print("this is not marked and not a target neighbor!")
                                    any_non_marked_target_neighbor_except_the_current_one = True
                            else:#(islands[index]['neighbors'][t_n_i_t][0] == islands[index]['neighbors'][target_neighbor_indexes[t_n_i][n_i]][0])
                                print("this is the current neighbor working on;(")
                                #if the other neighbors are all marked, then
                                print("{0} not in {1}?".format(target_neighbor_indexes[t_n_i][k], target_neighbor_indexes[t_n_i]))
                                print("{0} ?= {1}".format(how_many_left(islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0], islands), how_many))
                                
                                if (islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0] != islands[index]['neighbors'][target_neighbor_indexes[t_n_i][n_i]][0]) and (target_neighbor_indexes[t_n_i][k] not in target_neighbor_indexes[t_n_i]) and (marked(islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0], islands)): #connected and not marked    #neighbor_indexes: [[1], [2]]    #is_this_neighbor_isolation(index, neighbor_index, neighbor_blocked, h_answer, v_answer, line)
                                    print("{0}!={1}".format(islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0], islands[index]['neighbors'][target_neighbor_indexes[t_n_i][n_i]][0]), end=" ")
                                    print("and {0} not in {1}".format(target_neighbor_indexes[t_n_i][k], target_neighbor_indexes[t_n_i]), end=" ")
                                    print("and is {0} marked in the prev line?".format(islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0]))
                                    print("if another neighbor is marked, then") 
                                elif (islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0] != islands[index]['neighbors'][target_neighbor_indexes[t_n_i][n_i]][0]) and (target_neighbor_indexes[t_n_i][k] in target_neighbor_indexes[t_n_i]) and (how_many_left(islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0], islands) == how_many):#if another neighbor is not marked, then
                                    print("{0}!={1}".format(islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0], islands[index]['neighbors'][target_neighbor_indexes[t_n_i][n_i]][0]), end=" ")
                                    print("and {0} in {1}".format(target_neighbor_indexes[t_n_i][k], target_neighbor_indexes[t_n_i]), end=" ")
                                    print("and how many is left for {0} == {1} in the prev line?".format(islands[index]['neighbors'][target_neighbor_indexes[t_n_i][k]][0], how_many))
                                    print("if another neighbor will be marked, then")
                                #elif not in marked_coordinates and not in target_neighbor_indexes:#[ [2], [3] ]
                                    #print("coordinates: (6, 8)")
                                else:#if another neighbor is NOT marked and if another neighbor will NOT be marked, then
                                    index_found = False
                                    possible_isolation = False
                                    looking_for_index = 0
                                    #for neighbor in islands[index]['neighbors']:
                                    while not(index_found) and looking_for_index < len(islands[index]['neighbors']):
                                        if (connected_neighbor(islands[index]['coordinates'], islands[index]['neighbors'][looking_for_index][0], h_answer, v_answer)):
                                            
                                            if (islands[index]['neighbors'][looking_for_index][0] in neighbor_marked_and_not_blocked) and (looking_for_index not in target_neighbor_indexes[t_n_i]):#marked(islands[index]['neighbors'][looking_for_index][0], islands) and :
                                                print("{0} is in {1} and connected to {2}".format(islands[index]['neighbors'][looking_for_index][0], neighbor_marked_and_not_blocked, islands[index]['coordinates']))
                                                print("{0} is not in {1}".format(looking_for_index, target_neighbor_indexes[t_n_i]))
                                                i = find_the_index_for_neighbor_index(index, looking_for_index)
                                                w_neighbor_bridges, w_neighbor_coordinates, w_neighbor_marked_and_not_blocked, w_neighbor_blocked = what_are_neighbor_coordinates_marked_blocked(i, v_answer, h_answer)
                                                w_neighbor_coordinates = find_connected_neighbor_coordinates_of_target_neighbor(index, looking_for_index, w_neighbor_blocked, h_answer, v_answer)
                                                print("is_there_the_only_way_without_isolation(): w_neighbor_coordinates are {0}".format(w_neighbor_coordinates))
                                                #if connected_neighbor(islands[index]["coordinates"], islands[index]["neighbors"][target_neighbor_indexes[t_n_i][n_i]][0], h_answer, v_answer):  islands[index]["neighbors"][][0]
                                                
                                                                                                    #neighbor_coordinates[0]
                                                w_neighbor_bridges_iti, w_neighbor_coordinates_iti, w_neighbor_marked_and_not_blocked_iti, w_neighbor_blocked_iti = what_are_neighbor_coordinates_marked_blocked(i, v_answer, h_answer)
                                                print("w_neighbor_marked_and_not_blocked_iti is {0}".format(w_neighbor_marked_and_not_blocked_iti))
                                                print("w_neighbor_blocked_iti is {0}".format(w_neighbor_blocked_iti)) 
                                                w_checked_coordinates = [islands[index]['coordinates'], islands[i]['coordinates']]
                                                
                                                if w_neighbor_coordinates != []:#line_count_in_list=[[(6, 8), 1], [(9, 6), 1]]
                                                    any_non_marked_target_neighbor_except_the_current_one = is_there_isolation_aux(w_neighbor_coordinates, i, 0, w_checked_coordinates, w_neighbor_blocked_iti, h_answer, v_answer, line_count_in_list, islands)
                                                    print("is_there_isolation_aux() is determined to be {0}".format(any_non_marked_target_neighbor_except_the_current_one))
                                                    if any_non_marked_target_neighbor_except_the_current_one == True:
                                                         possible_isolation = True
                                                         print("if isolation, target neighbors have to be non-isolated")
                                                else:#w_neighbor_coordinates == []:
                                                    print("there is no neighbors for {0}".format(islands[index]["neighbors"][target_neighbor_indexes[t_n_i][n_i]][0]))
############################################################################################################                                                
                                                    possible_isolation = True
                                                
                                            elif (islands[index]['neighbors'][looking_for_index][0] not in neighbor_marked_and_not_blocked) and (looking_for_index not in target_neighbor_indexes[t_n_i]):
                                                print("{0} is not in {1}".format(islands[index]['neighbors'][looking_for_index][0], neighbor_marked_and_not_blocked))
                                                print("{0} is not in {1}".format(looking_for_index, target_neighbor_indexes[t_n_i]))
                                                index_found = True
                                                if possible_isolation == False:
                                                    any_non_marked_target_neighbor_except_the_current_one = True
                                                    print("because of possible_isolation==False, any_non_marked_target_neighbor_except_the_current_one can be True")
                                            elif (islands[index]['neighbors'][looking_for_index][0] not in neighbor_marked_and_not_blocked) and (looking_for_index in target_neighbor_indexes[t_n_i]):
                                                print("{0} is not in {1}?".format(islands[index]['neighbors'][looking_for_index][0], neighbor_marked_and_not_blocked))
                                                print("{0} is in {1}?".format(looking_for_index, target_neighbor_indexes[t_n_i]))
                                                index_found = True
                                                if possible_isolation == False:
                                                    any_non_marked_target_neighbor_except_the_current_one = True
                                                    print("because of possible_isolation==False, any_non_marked_target_neighbor_except_the_current_one can be True")
                                            else:#(islands[index]['neighbors'][looking_for_index][0] in neighbor_marked_and_not_blocked)     and (looking_for_index in target_neighbor_indexes[t_n_i]):
                                                 
                                                print("{0} is in {1}?? and ".format(islands[index]['neighbors'][looking_for_index][0], neighbor_marked_and_not_blocked), end="")
                                                print("{0} is in {1}??".format(looking_for_index, target_neighbor_indexes[t_n_i]))
                                                if possible_isolation == False:
                                                    any_non_marked_target_neighbor_except_the_current_one = True
                                                    print("because of possible_isolation==False, any_non_marked_target_neighbor_except_the_current_one can be True")
                                        else:
                                            print("{0} is not connected to the centre {1}".format(islands[index]['neighbors'][looking_for_index][0], islands[index]['coordinates']))
                                        print()    
                                        looking_for_index += 1
                                        #possible_isolation = False
                            #l += 1
                        else:#k == n_i:
                            print("k == n_i: {0} == {1}: this neighbor doesn't have its' neighbors, so we don't need to check if this side is isolated or not".format(k, n_i))
                            
                        k += 1
                        print("k is increased to {0}".format(k)) 
                                   
                    if any_non_marked_target_neighbor_except_the_current_one == True:
                        print("1")
                        is_there_isolation_aux_result[n_i] = False
                    elif any_non_marked_target_neighbor_except_the_current_one == False and k == len(target_neighbor_indexes) and index_found:
                        print("2")
                        is_there_isolation_aux_result[n_i] = True# changed to False again for (1, 3) of get_started    #this was changed to True from False because of (6, 6) of easy?
                    elif any_non_marked_target_neighbor_except_the_current_one == False and k == len(target_neighbor_indexes) and not(index_found):
                        print("3")
                        is_there_isolation_aux_result[n_i] = False
                    else:#any_non_marked_target_neighbor_except_the_current_one == False:
                        is_there_isolation_aux_result[n_i] = True
                        print("is_there_isolation_aux_result[n_i] is set to True")
                
                if n_i == len(target_neighbor_indexes[t_n_i]) - 1 or is_there_isolation_aux_result[n_i] == False:
                    isolation[t_n_i] = is_there_isolation_aux_result[n_i]
                    print("isolation[{0}] is {1} now".format(t_n_i, isolation[t_n_i]))
                    keep_going = False
                    print("n_i == len(target_neighbor_indexes[t_n_i])-1: {0} ?= {1} or is_there_isolation_aux_result[n_i] == {2} so keep_going = False".format(n_i, len(target_neighbor_indexes[t_n_i]) - 1, is_there_isolation_aux_result[n_i]))
                else:
                    print("n_i != len(target_neighbor_indexes[t_n_i])-1: {0} != {1} or is_there_isolation_aux_result[n_i] != False: is_there_isolation_aux_result[n_i] != {2}".format(n_i, len(target_neighbor_indexes[t_n_i]) - 1, is_there_isolation_aux_result[n_i]))
                
            else:#(how_many_left(islands[index]["neighbors"][n_i][0]) != 1 and num_of_lines == 1) or (how_many_left(islands[index]["neighbors"][n_i][0]) != 2 and num_of_lines == 2)
                #print("is_there_isolation(): this is one of the current target neighbors/neighbor blocked/marked: {0}".format(islands[index]["neighbors"][n_i]))
                print("is_there_the_only_way_without_isolation(): {0} will not be marked.".format(islands[index]['neighbors'][target_neighbor_indexes[t_n_i][n_i]][0]))
                keep_going = False
                
            #if n_i == len(target_neighbor_indexes[t_n_i])-1 and keep_going == True:
                
            n_i += 1
                
            #if target_neighbor_indexes[t_n_i][last_index_of_target_neighbor_indexes] == n_i:
        '''
        if keep_going == False:
            isolation[t_n_i] = False
        else:
            isolation[t_n_i] = True
            suspicious_neighbor = t_n_i
        ''' 
            #n_i += 1
        t_n_i += 1
    n_i = 0
    #we only need to investigate the neighbor with isolation[?]==True
    count_false = 0
    
    for iso in isolation:
        #if keep_going == True:#== False:
        if iso == False:
            count_false += 1
            print("is_there_the_only_way_without_isolation(): is_there_isolation(): iso == False")
    
    #and then see if all the neighbors of the neighbors are marked or not
    #islands[index]["coordinates"] islands[index]["neighbors"][target_neighbor_index][0]
    index_w_no_isolation = -1
    isolation_indexes=[]
    
    if count_false == 1:
        result = True
        index = 0
        false_found = False
        while not(false_found) and index < len(isolation):
            if isolation[index] == False:
                false_found = True
                index_w_no_isolation = index
            else:
                index += 1
                 
    else:
        result = False
        index = 0
        while index < len(isolation):
            if isolation[index] == True:
                isolation_indexes.append(index)
            index += 1
        
    '''   
    print("result_list: {0}".format(result_list))
    for r in result_list:
        result = result and r
    '''
    #else:
        #print("is_there_isolation(): temp_num_of_bridges_left != 0")
    print("isolation is {0}".format(isolation))
    print("is_there_the_only_way_without_isolation(): returns result: {0}, index_w_no_isolation: {1}, and isolation_indexes: {2}".format(result, index_w_no_isolation, isolation_indexes))
    return result, index_w_no_isolation, isolation_indexes

def line_with_count_in_list(temp_hv_answers):
    print("line_with_count_in_list(): {0} is passed to this func".format(temp_hv_answers))
    line_count_in_list = []
    for lines in temp_hv_answers:#[(2, 3, 2, 5), (2, 5, 2, 7)]
        lines_with_count = []
        for line in lines:#(2, 3, 2, 5)
            line_with_count = [line, lines.count(line)]
            if line_with_count not in lines_with_count:
                #print("{0} is appended to lines_with_count".format(line_with_count))
                lines_with_count.append(line_with_count)
                #print("line_with_count: {0}".format(lines_with_count))
            else:
                print("{0} is already in lines_with_count".format(line_with_count))
        #print(line_with_count)
        #print("{0} not in {1}".format(lines_with_count, line_count_in_list))
        if lines_with_count not in line_count_in_list:
            line_count_in_list.append(lines_with_count)
        else:
            print("{0} is already in line_count_in_list".format(lines_with_count))
    print("line_with_count_in_list() returns line_count_in_list={0}".format(line_count_in_list))
    return line_count_in_list

def is_this_neighbor_isolation(index, neighbor_index, neighbor_blocked, h_answer, v_answer, line):#, line_with_count_in_list):#temp_num_of_bridges_left, num_bridges_to_deduct,
    #line has to be in the format of ...
    result = False
    #result_list = []#False
    num_of_lines = 0
    quit = False
    print("is_this_neighbor_isolation():")
    #[[(2, 3, 2, 5), (2, 5, 2, 7)],     [(2, 3, 2, 5), (2, 5, 5, 5)],     [(2, 5, 2, 7), (2, 5, 5, 5)],     [(2, 5, 2, 7), (2, 5, 2, 7)],     [(2, 5, 5, 5), (2, 5, 5, 5)]]
    #line_w_count_in_list = line_with_count_in_list_in_iti(temp_hv_answers[])
    num_of_lines = extract_the_num_of_lines_from_line(line, index, neighbor_index)
        
    #not checking if it's marked or not since this is going to be used in else case...
    if (islands[index]["neighbors"][neighbor_index][1] == 1 and marked(islands[index]["neighbors"][neighbor_index][0], islands)) or (how_many_left(islands[index]["neighbors"][neighbor_index][0], islands) == 0):# and ((marked(islands[index]["neighbors"][neighbor_index][0], islands)) or (islands[index]["neighbors"][neighbor_index][0])):
        result = True
        quit = True
        print("is_this_neighbor_isolation(): {0} is marked 1 or num_of_lines_left is 0, therefore is_this_neighbor_isolation() quit.".format(islands[index]["neighbors"][neighbor_index][0]))
    else:
        print("is_this_neighbor_isolation(): {0} is not marked 1 and num_of_lines_left is not 0, therefore is_this_neighbor_isolation() goes to if quit == False:.".format(islands[index]["neighbors"][neighbor_index][0]))


    if quit == False and (islands[index]["num_of_bridges_left"] == num_of_lines):
        checked_coordinates = []
        #for n_i in range(len(islands[index]["neighbors"])):#== n_i not in target_neighbor_indexes:
        if not(connected_neighbor(islands[index]["coordinates"], islands[index]["neighbors"][neighbor_index][0], h_answer, v_answer)):
            n_coordies = find_neighbor_coordinates(index, neighbor_index, neighbor_blocked)
                
            if n_coordies != []:# and all_marked:            #line_count_in_list=[[(6, 8), 1], [(9, 6), 1]]
                result = is_there_isolation_aux(n_coordies, index, 0, checked_coordinates, neighbor_blocked, h_answer, v_answer, line_count_in_list, islands)
            else:
                print("is_this_neighbor_isolation(): if quit == False: for loop: n_coordies == [] for {0}".format(islands[index]["neighbors"][neighbor_index]))
                result = False
        else:
            print("is_this_neighbor_isolation(): if quit == False: for loop: the neighbor: {1} is connected to the vertex: {0}".format(islands[index]["coordinates"], islands[index]["neighbors"][neighbor_index][0]))
            result
    else:
        print("is_this_neighbor_isolation(): quit!= False")
    return result

def what_is_neighbor_index(coordinates, i):
    index = 0
    winii = 0
    what_is_index_found = False
    while not(what_is_index_found) and winii < len(islands[i]['neighbors']):
        print("coordinates:{0} == islands[i]['neighbors'][winii]:{1}".format(coordinates, islands[i]['neighbors'][winii][0]))
        if coordinates == islands[i]['neighbors'][winii][0]:
            index = winii
            print("what_is_neighbor_index(): index is set to winii: {0}".format(winii))
            what_is_index_found = True
            #print("{0} has {1} left".format(coordinates, how_many))
        else:
            winii += 1
            print("what_is_neighbor_index(): winii is increased to {0}".format(winii))
    print("what_is_neighbor_index() found {0}".format(index))
    return index

def what_is_vertex(coordinates):
    vertex = 0
    i = 0
    what_is_vertex_found = False
    while not(what_is_vertex_found) and i < len(islands):
        if coordinates == islands[i]['coordinates']:
            vertex = islands[i]['num_of_bridges']
            what_is_vertex_found = True
            #print("{0} has {1} left".format(coordinates, how_many))
        i += 1
    return vertex

def is_there_isolation_for_else(index, target_neighbor_index, neighbor_blocked, h_answer, v_answer):#temp_num_of_bridges_left, num_bridges_to_deduct, 
    #before deciding the connection between the target neighbor and the vertex, we have to check whether this vertex is connected to a isolated segment or not
    #this works only when how_many_num_of_bridges_left == 0 and how_many_left(islands[index]["neighbors"][target_neighbor_index][0]) == 0
    #temp_num_of_bridges_left -= num_bridges_to_deduct
    print("is_there_isolation_for_else() Start")
    result = True
    checked_coordinates = []
    #n_coordies = find_neighbor_coordinates(index, target_neighbor_index, neighbor_blocked)
    
    neighbor_coordinates = find_connected_neighbor_coordinates_of_target_neighbor(index, target_neighbor_index, neighbor_blocked, h_answer, v_answer)
    print("is_there_isolation_for_else(): neighbor_coordinates are {0}".format(neighbor_coordinates))
    #if connected_neighbor(islands[index]["coordinates"], islands[index]["neighbors"][target_neighbor_indexes[t_n_i][n_i]][0], h_answer, v_answer):  islands[index]["neighbors"][][0]
    new_index = find_the_index_for_neighbor_index(index, target_neighbor_index)
    neighbor_bridges_iti, neighbor_coordinates_iti, neighbor_marked_and_not_blocked_iti, neighbor_blocked_iti = what_are_neighbor_coordinates_marked_blocked(new_index, v_answer, h_answer)
    '''
    print("neighbor_marked_and_not_blocked_iti is {0}".format(neighbor_marked_and_not_blocked_iti))
    print("neighbor_blocked_iti is {0}".format(neighbor_blocked_iti)) 
    checked_coordinates = [islands[index]['coordinates'], islands[new_index]['coordinates']]
    
    if neighbor_coordinates != []:
        additional_neighbor_coordinates = find_neighbor_coordinates_for_the_input_coordinate(islands[index]['coordinates'], index, neighbor_blocked, h_answer, v_answer)
        print("additional_neighbor_coordinates is {0}".format(additional_neighbor_coordinates))
        if islands[new_index]['coordinates'] in additional_neighbor_coordinates:
            additional_neighbor_coordinates.remove(islands[new_index]['coordinates'])
        neighbor_coordinates += additional_neighbor_coordinates
        print("after adding additional_neighbor_coordinates, neighbor_coordinates is {0}".format(neighbor_coordinates))
        is_there_isolation_aux_result[n_i] = is_there_isolation_aux(neighbor_coordinates, new_index, 0, checked_coordinates, neighbor_blocked_iti, h_answer, v_answer)
    '''
    itife_index = 0
    itife_result = True
    #for n_coordy in n_coordies:
    while itife_result and itife_index < len(neighbor_coordinates):
        itife_result = itife_result and connected_neighbor(islands[index]["neighbors"][target_neighbor_index][0], neighbor_coordinates[itife_index], h_answer, v_answer)
        itife_index += 1
        
    if neighbor_coordinates != [] and itife_result:# and all_marked:        #line_count_in_list=[[(6, 8), 1], [(9, 6), 1]]
        result = is_there_isolation_aux(neighbor_coordinates, new_index, 0, checked_coordinates, neighbor_blocked, h_answer, v_answer, line_count_in_list, islands)
    else:
        print("is_there_isolation_for_else(): n_coordies == []/itife_result=False/both for {0}".format(islands[index]["neighbors"][target_neighbor_index]))
        result = False
    print("is_there_isolation_for_else() returned {0}".format(result))
    return result

'''
def is_there_isolation_aux_two(neighbor, checked_coordinates):
    if len(neighbor) != 0:
        for n in neighbor:
            result = marked(n, islands)
    else:
        result =   
    return result
'''
def is_it_marked_or_blocked_coordinate(neighbor_coordinates, i, j, else_done_index):
    print("is_it_marked_or_blocked_coordinate(): {0}, {1}, {2}, and {3} are passed to".format(neighbor_coordinates, i, j, else_done_index))
    neighbor_coordinates_index = 0
    #else_done_index = 0
    else_done_index_found = False
    l = 0
    while not(else_done_index_found) and (neighbor_coordinates_index < len(neighbor_coordinates)):
        print("{0} ?= {1}".format(islands[i]["neighbors"][j][0], neighbor_coordinates[neighbor_coordinates_index]))
        if islands[i]["neighbors"][j][0] == neighbor_coordinates[neighbor_coordinates_index]:     
            l = j
            print("is_it_marked_or_blocked_coordinate(): l:{0} is found".format(l))
            else_done_index_found = True
            #else_done_index += 1
        else:
            neighbor_coordinates_index += 1
        '''    
        if (len(neighbor_coordinates) == neighbor_coordinates_index) and not(else_done_index_found):
            j += 1
            neighbor_coordinates_index = 0
        '''     
    if not(else_done_index_found):
        print("is_it_marked_or_blocked_coordinate(): else_done_index_found wasn't found")
        
    return l, neighbor_coordinates_index, else_done_index, else_done_index_found
                        
def get_line_ordered(coordinates, neighbor):
    if coordinates[0] > neighbor[0]:
        tuple = neighbor + coordinates
    elif coordinates[1] > neighbor[1]:
        tuple = neighbor + coordinates
    else:
        tuple = coordinates + neighbor
    print("get_line_ordered(): the result is {0}".format(tuple))
    return tuple
def is_only_else_done(done):
    result = True
    for d in done:
        result = result and d
    return result
            
def is_it_done(done, temp_num_of_bridges_left, num_of_edges_left, len_of_possible_combnation):#neighbors_length
    boolean = copy.deepcopy(done[0])
    k = 1
    result = False
    while boolean and (k < temp_num_of_bridges_left):#neighbors_length):
        boolean = boolean and done[k]
        k += 1
    if boolean or (num_of_edges_left == len_of_possible_combnation):
        result = True
    print("is_it_done(): else_done: {0}".format(done))
    print("is_it_done(): boolean={0} and result={1}".format(boolean, result))
    return result

def compare_coordinates(c1, c2):
    if c1[0] == c2[0]:
        if c1[1] > c2[1]:
            result = 'left'
        elif c1[1] < c2[1]:
            result = 'right'
        else:
            result = 'same'  
    elif c1[1] == c2[1]:
        if c1[0] > c2[0]:
            result = 'down'
        elif c1[0] < c2[0]:
            result = 'up'
        else:
            result = 'same'
    else:
        if c1[0] > c2[0]:
            result = 'down'
        elif c1[0] < c2[0]:
            result = 'up'
        else:
            result = 'same'
    return result
'''
def print_( morse ):
    print( "( '{0}', '{1}' )".format( morse[0], morse[1] ) )
    return

bst = bst_init( print_, compare_coordinates )
'''

def how_many_lines(coordinates, h_answer, v_answer):
    how_many = 0
    #i = 0
    for h_line in h_answer:
        if (h_line[0], h_line[1]) == coordinates:
            how_many += 1
        elif (h_line[2], h_line[3]) == coordinates:
            how_many += 1
    for v_line in v_answer:
        if (v_line[0], v_line[1]) == coordinates:
            how_many += 1
        elif (v_line[2], v_line[3]) == coordinates:
            how_many += 1
    print("how_many_lines()?{0}".format(how_many))
    return how_many

def how_many_left(coordinates, islands):
    how_many = 0
    i = 0
    how_many_left_found = False
    while not(how_many_left_found) and i < len(islands):
        if coordinates == islands[i]['coordinates']:
            how_many = islands[i]['num_of_bridges_left']
            how_many_left_found = True
            #print("{0} has {1} left".format(coordinates, how_many))
        i += 1
    return how_many

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

def are_there_too_many_edges(t_h, temp_h_answer, h_answer, num_bridges_to_deduct):
    for h in t_h:
            how_many_temp = temp_h_answer.count(h)
            print("are_there_too_many_edges(): there is/are {0} {1}(s)".format(how_many_temp, h))
            how_many = h_answer.count(h)
            print("are_there_too_many_edges(): there is/are {0} {1}(s)".format(how_many, h))
            if 2 < how_many_temp + how_many:
                num_bridges_to_deduct = 0
                temp_h_answer = []
    print("are_there_too_many_edges() return {0} and {1}".format(num_bridges_to_deduct, temp_h_answer))
    return num_bridges_to_deduct, temp_h_answer

def connect_to_neighbor_temporarily(index, neighbor_index_inside_neighbors, no_two_bridges, temp_h_answer, temp_v_answer, how_many_num_of_bridges_left, h_answer, v_answer, islands):
    #if islands[index]["mark"] != True:
    num_bridges_to_deduct = 0
    print("how_many_num_of_bridges_left: {0} would be decreased to ".format(how_many_num_of_bridges_left), end="")
    if (how_many_left(islands[index]["neighbors"][neighbor_index_inside_neighbors][0], islands) < 2) and not(no_two_bridges):
        num_bridges_to_deduct = 0
        print("***num_bridges_to_deduct = 0***")
    elif (how_many_num_of_bridges_left != 1) and (how_many_left(islands[index]["neighbors"][neighbor_index_inside_neighbors][0], islands) > 1) and not(no_two_bridges):
        #islands[index]['num_of_bridges_left'] = islands[index]['num_of_bridges_left'] - 2
        print("connect_to_neighbor_temporarily(): elif")
        num_bridges_to_deduct = hv_answers(index, neighbor_index_inside_neighbors, 2, temp_h_answer, temp_v_answer, False, islands)
        #islands[index]['num_of_bridges_left'] = islands[index]['num_of_bridges_left'] - num_bridges_to_deduct
    else:
        print("connect_to_neighbor_temporarily(): else")
        #islands[index]['num_of_bridges_left'] = islands[index]['num_of_bridges_left'] - 1
        num_bridges_to_deduct = hv_answers(index, neighbor_index_inside_neighbors, 1, temp_h_answer, temp_v_answer, False, islands)
        #islands[index]['num_of_bridges_left'] = islands[index]['num_of_bridges_left'] - num_bridges_to_deduct
    print("how many left?: {0} for {1}{2}".format(how_many_left(islands[index]["neighbors"][neighbor_index_inside_neighbors][0], islands)-num_bridges_to_deduct, islands[index]["neighbors"][neighbor_index_inside_neighbors][1], islands[index]["neighbors"][neighbor_index_inside_neighbors][0]))
    print("{0} for {1}{2}".format((how_many_num_of_bridges_left - num_bridges_to_deduct), islands[index]['num_of_bridges'], islands[index]['coordinates']))
    print("temp_h_answer is {0}".format(temp_h_answer))
    print("temp_v_answer is {0}".format(temp_v_answer))
    
    if 0 != num_bridges_to_deduct:
        t_h = f7(temp_h_answer)
        print("f7() returned {0}".format(t_h))
        t_v = f7(temp_v_answer)
        print("f7() returned {0}".format(t_v))
        num_bridges_to_deduct, temp_h_answer = are_there_too_many_edges(t_h, temp_h_answer, h_answer, num_bridges_to_deduct)
        num_bridges_to_deduct, temp_v_answer = are_there_too_many_edges(t_v, temp_v_answer, v_answer, num_bridges_to_deduct)
    else:#0==num_bridges_to_deduct
        temp_h_answer = []
        temp_v_answer = []
    print("connect_to_neighbor_temporarily() returns {0} and {1}".format(temp_h_answer + temp_v_answer, num_bridges_to_deduct))
    return temp_h_answer + temp_v_answer, num_bridges_to_deduct

def find_duplicates(temp_hv_answers):
    connections = []
    print("{0} is passed to find_duplicates()".format(temp_hv_answers))
    for list in temp_hv_answers[0]:#[[5,7,5,9],[5,7,5,9]]
        print("for loop: {0}".format(list))
        j = 1
        k = 0
        smallest = temp_hv_answers[0].count(list)
        stop = False
        
        if list not in connections:
            while j < len(temp_hv_answers) and not(stop):
                #print("j: {0} < len(temp_hv_answers): {1}".format(j, len(temp_hv_answers)))
                found = False
                while k < len(temp_hv_answers[j]) and not(found):# and not(stop):#[[5,7,5,9], [5,9,8,9]]
                    
                    #print("k: {0} < len(temp_hv_answers[j]): {1}".format(k, len(temp_hv_answers[j])))
                    #smallest_to_compare = 0
                    #print("comparing {0} and {1}".format(list, temp_hv_answers[j][k]))
                    
                    if list == temp_hv_answers[j][k]:#[[5,7,5,9],...
                        found = True
                        smallest_to_compare = temp_hv_answers[j].count(list)
                        if smallest > smallest_to_compare:
                            smallest = smallest_to_compare
                    else:
                        k += 1
        
                if found:    
                    j += 1
                else:
                    stop = True
            
            if not(stop):
                for s in range(smallest):
                    connections.append(list)
                    print("{0} is appended to connections".format(list))
            print()
        else:
            print("{0} is already in connections".format(list))
    #find_duplicates(): the result is [(2, 5, 2, 7), (2, 7, 5, 7)]
    print("find_duplicates(): the result is {0}".format(connections))
    return connections

def connect_to_neighbor_and_mark(index, neighbor_index_inside_neighbors, no_two_bridges, h_answer, v_answer, double_line, islands):
    #if islands[index]["mark"] != True:
    num_bridges_to_deduct = 0
    print("islands[index]['num_of_bridges_left']: {0} is decreased to ".format(islands[index]['num_of_bridges_left']), end="")
    # how_many_left(islands[index]["neighbors"][neighbor_index_inside_neighbors][0]) <- (islands[index]["neighbors"][neighbor_index_inside_neighbors][1] != 1)
    if (islands[index]['num_of_bridges'] != 1) and (islands[index]['num_of_bridges_left'] != 1) and (how_many_left(islands[index]["neighbors"][neighbor_index_inside_neighbors][0], islands) != 1) and not(no_two_bridges):
        #islands[index]['num_of_bridges_left'] = islands[index]['num_of_bridges_left'] - 2
        num_bridges_to_deduct = hv_answers(index, neighbor_index_inside_neighbors, 2, h_answer, v_answer, double_line, islands)
        islands[index]['num_of_bridges_left'] = islands[index]['num_of_bridges_left'] - num_bridges_to_deduct
    else:
        #islands[index]['num_of_bridges_left'] = islands[index]['num_of_bridges_left'] - 1
        print("###else")
        num_bridges_to_deduct = hv_answers(index, neighbor_index_inside_neighbors, 1, h_answer, v_answer, double_line, islands)
        islands[index]['num_of_bridges_left'] = islands[index]['num_of_bridges_left'] - num_bridges_to_deduct
    print("{0} for {1}{2}".format(islands[index]['num_of_bridges_left'], islands[index]['num_of_bridges'], islands[index]['coordinates']))
    print("h_answer is {0}".format(h_answer))
    print("v_answer is {0}".format(v_answer))
    '''                
        if islands[index]['num_of_bridges_left'] == 0:
            islands[index]["mark"] = True                       
        else:
            print("islands[index]['num_of_bridges_left'] != 0")
        if (islands[index]["mark"] == True) and (islands[index]["coordinates"] not in marked_coordinates):
            marked_coordinates.append(islands[index]["coordinates"])
        else:
            print("{0} is not marked or already in marked_coordinates".format(islands[index]["coordinates"]))
    '''
    mark(index, neighbor_index_inside_neighbors, islands)
    
    if (0 != num_bridges_to_deduct):
        find_neighbor_deduct_num_of_bridges_and_mark(index, neighbor_index_inside_neighbors, num_bridges_to_deduct, islands)
    else:
        print("there is nothing to deduct for the neighbors")
    #else:
        #print("connect_to_neighbor_and_mark: islands[index][\"mark\"] == True")
    return

def hv_answers(index, neighbor_index, how_many_times, h_answer, v_answer, double_line, islands):#double_line means adding a line on top of one existing line
    if ((islands[index]["coordinates"][0] == islands[index]["neighbors"][neighbor_index][0][0]) and (islands[index]["neighbors"][neighbor_index][0][0], islands[index]["neighbors"][neighbor_index][0][1], islands[index]["coordinates"][0], islands[index]["coordinates"][1]) not in h_answer)   or\
       ((islands[index]["coordinates"][1] == islands[index]["neighbors"][neighbor_index][0][1]) and (islands[index]["neighbors"][neighbor_index][0][0], islands[index]["neighbors"][neighbor_index][0][1], islands[index]["coordinates"][0], islands[index]["coordinates"][1]) not in v_answer)   or\
       ((islands[index]["coordinates"][0] == islands[index]["neighbors"][neighbor_index][0][0]) and double_line)  or\
       ((islands[index]["coordinates"][1] == islands[index]["neighbors"][neighbor_index][0][1]) and double_line):
        for i in range(how_many_times):
            if (islands[index]["coordinates"][0] == islands[index]["neighbors"][neighbor_index][0][0]):
                if   islands[index]["coordinates"][1] < islands[index]["neighbors"][neighbor_index][0][1]    and (h_answer.count( (islands[index]["coordinates"][0], islands[index]["coordinates"][1], islands[index]["neighbors"][neighbor_index][0][0], islands[index]["neighbors"][neighbor_index][0][1]) )<2) :
                    h_answer.append( (islands[index]["coordinates"][0], islands[index]["coordinates"][1], islands[index]["neighbors"][neighbor_index][0][0], islands[index]["neighbors"][neighbor_index][0][1]) )
                elif islands[index]["coordinates"][1] >= islands[index]["neighbors"][neighbor_index][0][1] and (h_answer.count( (islands[index]["coordinates"][0], islands[index]["neighbors"][neighbor_index][0][1], islands[index]["neighbors"][neighbor_index][0][0], islands[index]["coordinates"][1]) )<2):
                    h_answer.append( (islands[index]["coordinates"][0], islands[index]["neighbors"][neighbor_index][0][1], islands[index]["neighbors"][neighbor_index][0][0], islands[index]["coordinates"][1]) )
                else:
                    print("hv_answers(): nothing is happened to h_answer, so how_many_times -= 1")
                    how_many_times -= 1
            else:
                if   islands[index]["coordinates"][0] < islands[index]["neighbors"][neighbor_index][0][0]    and (v_answer.count( (islands[index]["coordinates"][0], islands[index]["coordinates"][1], islands[index]["neighbors"][neighbor_index][0][0], islands[index]["neighbors"][neighbor_index][0][1]) )<2):
                    v_answer.append( (islands[index]["coordinates"][0], islands[index]["coordinates"][1], islands[index]["neighbors"][neighbor_index][0][0], islands[index]["neighbors"][neighbor_index][0][1]) )
                    print("hv_answers(): {0} is appended to {1}".format( (islands[index]["coordinates"][0], islands[index]["coordinates"][1], islands[index]["neighbors"][neighbor_index][0][0], islands[index]["neighbors"][neighbor_index][0][1]), v_answer))
                elif islands[index]["coordinates"][0] >= islands[index]["neighbors"][neighbor_index][0][0] and (v_answer.count( (islands[index]["neighbors"][neighbor_index][0][0], islands[index]["coordinates"][1], islands[index]["coordinates"][0], islands[index]["neighbors"][neighbor_index][0][1]) )<2):
                    v_answer.append( (islands[index]["neighbors"][neighbor_index][0][0], islands[index]["coordinates"][1], islands[index]["coordinates"][0], islands[index]["neighbors"][neighbor_index][0][1]) )
                    print("hv_answers(): {0} is appended to {1}".format( (islands[index]["coordinates"][0], islands[index]["coordinates"][1], islands[index]["neighbors"][neighbor_index][0][0], islands[index]["neighbors"][neighbor_index][0][1]), v_answer))
                else:
                    print("hv_answers(): nothing is happened to v_answer, so how_many_times -= 1")
                    how_many_times -= 1
    else:
        print("(No change in h_answer, v_answer) ", end="")
        how_many_times = 0
    return how_many_times#h_answer, v_answer

def mark(index, neighbor_index_inside_neighbors, islands):
    if islands[index]['num_of_bridges_left'] == 0:
        islands[index]["mark"] = True  
        print("mark(): the island, {0} is marked".format(islands[index]["coordinates"]))                     
    else:
        print("mark(): islands[index]['num_of_bridges_left'] != 0")
    
    if (islands[index]["mark"] == True) and (islands[index]["coordinates"] not in marked_coordinates):
        marked_coordinates.append(islands[index]["coordinates"])
        #bst_insert( bst, islands[index]["coordinates"] )
        #islands[neighbor_index]["marked_neighbor_coordinates"].append(islands[index]["coordinates"])
        find_neighbor_and_add_the_current_coordy_to_its_marked_neighbor_coordinates(index, neighbor_index_inside_neighbors, islands)    
    else:
        print("mark(): {0} is not marked or already in marked_coordinates".format(islands[index]["coordinates"]))
        #find_neighbor_and_add_the_current_coordy_to_its_marked_neighbor_coordinates(index, neighbor_index_inside_neighbors)
    return

def find_neighbor_and_add_the_current_coordy_to_its_marked_neighbor_coordinates(index, neighbor_index_inside_neighbors, islands):#, islands, marked_coordinates):
    l = 0
    found = False
    while (l < len(islands)) and (not(found)):
        print(l)
        print(islands[index]["neighbors"][neighbor_index_inside_neighbors][0])
        print(islands[l]["coordinates"])
        if islands[index]["neighbors"][neighbor_index_inside_neighbors][0] == islands[l]["coordinates"]:
            found = True
            print("get in?")
            if islands[index]["coordinates"] not in islands[l]["marked_neighbor_coordinates"]:#islands[l]["mark"] != True and (islands[l]['num_of_bridges_left'] >= 1):
                islands[l]["marked_neighbor_coordinates"].append(islands[index]["coordinates"])
                print("{0}{1} is added to {2}{3} as one of marked_neighbor_coordinates".format(islands[index]["num_of_bridges"], islands[index]["coordinates"], islands[index]["neighbors"][neighbor_index_inside_neighbors][1], islands[index]["neighbors"][neighbor_index_inside_neighbors][0]))
            #else:
                
            '''
            else:
                print("find_neighbor_deduct_num_of_bridges_and_mark: the neighbor of the island:{0}, {1} is already marked or islands[k]['num_of_bridges_left'] !>= 1".format(islands[index]["coordinates"], islands[index]["neighbors"][neighbor_index][0]))
            '''
        '''        
        else:
            print("islands[index][\"neighbors\"][neighbor_index][0] != islands[k][\"coordinates\"]: {0} != {1}".format(islands[index]["neighbors"][neighbor_index][0], islands[k]["coordinates"]))
        '''
        l += 1
    return #islands, marked_coordinates

def find_neighbor_deduct_num_of_bridges_and_mark(index, neighbor_index_inside_neighbors, num_bridges_to_deduct, islands):#, islands, marked_coordinates):
    k = 0
    found = False
    while (k < len(islands)) and (not(found)):
        if islands[index]["neighbors"][neighbor_index_inside_neighbors][0] == islands[k]["coordinates"]:
            found = True
            if islands[k]["mark"] != True and (islands[k]['num_of_bridges_left'] >= 1):
                
                print("islands[k]['num_of_bridges_left']: {0} is decreased to ".format(islands[k]['num_of_bridges_left']), end="")
                '''
                if (islands[index]["num_of_bridges"] != 1) and (islands[index]["neighbors"][neighbor_index][1] != 1):
                    islands[k]['num_of_bridges_left'] = islands[k]['num_of_bridges_left'] - 2
                else:
                    print("(islands[index][\"num_of_bridges\"] == 1) or (islands[index][\"neighbors\"][neighbor_index][1] == 1)")
                    islands[k]['num_of_bridges_left'] = islands[k]['num_of_bridges_left'] - 1
                '''
                islands[k]['num_of_bridges_left'] = islands[k]['num_of_bridges_left'] - num_bridges_to_deduct    
                #print("{0}".format(islands[k]['num_of_bridges_left']))
                print("{0} for {1}{2}".format(islands[k]['num_of_bridges_left'], islands[k]['num_of_bridges'], islands[k]['coordinates']))
                
                l = 0
                index_found = False
                while (l < len(islands[k]["neighbors"])) and (not(index_found)):
                    print("{0}".format(islands[k]["neighbors"][l][0]), end="=")
                    print("{0}".format(islands[index]["coordinates"]))
                    if islands[k]["neighbors"][l][0] == islands[index]["coordinates"]:
                        index_found = True
                        #if islands[index]["mark"] != True and (islands[index]['num_of_bridges_left'] >= 1):
                        mark(k, l, islands)
                    l += 1
                #islands[k]["marked_neighbor_coordinates"], islands[index]["neighbors"][j][1] != 3
            '''
            else:
                print("find_neighbor_deduct_num_of_bridges_and_mark: the neighbor of the island:{0}, {1} is already marked or islands[k]['num_of_bridges_left'] !>= 1".format(islands[index]["coordinates"], islands[index]["neighbors"][neighbor_index][0]))
            '''
        '''        
        else:
            print("islands[index][\"neighbors\"][neighbor_index][0] != islands[k][\"coordinates\"]: {0} != {1}".format(islands[index]["neighbors"][neighbor_index][0], islands[k]["coordinates"]))
        '''
        k += 1
    return #islands, marked_coordinates

'''
island = { "num_of_bridges": p[2], "neighbors":[], "coordinates": (p[0], p[1]), "mark": False, 'num_of_bridges_left': p[2], 'left': None, 'right': None, 'up': None, 'down': None}
'''

def hashi_puzzle_solver(puzzle, islands, marked_coordinates):
    #islands = []
    coordinates_without_right_neighbor = []
    coordinates_without_left_neighbor = []
    coordinates_without_down_neighbor = []
    coordinates_without_up_neighbor = []    
    max_x = puzzle[0][0]
    min_x = puzzle[0][0]
    x_coordinates = []
    max_y = puzzle[0][1]
    min_y = puzzle[0][1]
    y_coordinates = []
    
    for p in puzzle:
        island = { "num_of_bridges": p[2], "neighbors":[], "marked_neighbor_coordinates": [], "coordinates": (p[0], p[1]), "mark": False, 'num_of_bridges_left': p[2], 'left': None, 'right': None, 'up': None, 'down': None}
        islands.append( copy.deepcopy(island) )
        if p[0] > max_x:
            max_x = p[0]
        elif p[0] < min_x:
            min_x = p[0]
            
        if p[0] not in x_coordinates:
            x_coordinates.append(p[0])
    #print("max_x is {0}".format(max_x))
    #print("min_x is {0}".format(min_x))
    #print(x_coordinates)
        if p[1] not in y_coordinates:
            y_coordinates.append(p[1])
    y_coordinates.sort()
    print(y_coordinates)
           
    for p in puzzle:
        if (max_x == p[0]):
            coordinates_without_down_neighbor.append((p[0], p[1]))
        elif (min_x == p[0]):
            coordinates_without_up_neighbor.append((p[0], p[1]))
    
    for y in y_coordinates:
        temp_list = []
        for p in puzzle:
            if (p[1] == y):
                temp_list.append(p[0])
        minimum = min(temp_list)
        maximum = max(temp_list)
        if (minimum != min_x):
            coordinates_without_up_neighbor.append((minimum, y))
            #print("({0}, {1}) is appended to coordinates_without_up_neighbor".format(minimum, y) )
        if (maximum != max_x):
            coordinates_without_down_neighbor.append((maximum, y))
            #print("({0}, {1}) is appended to coordinates_without_down_neighbor".format(maximum, y) )
        
    for x in x_coordinates:
        count = 0
        for p in puzzle:
            if (p[0] == x):
                #print("p[0] == x ({0} == {1})".format(p[0], x))
                if (p[1] > max_y):
                    max_y = p[1]
                elif (p[1] < min_y):
                    min_y = p[1]
                count += 1
                    
        coordinates_without_right_neighbor.append((x, max_y))
        #print("{0} is appended to coordinates_without_right_neighbor".format( (x, max_y) ))
        coordinates_without_left_neighbor.append((x, min_y))
        #print("{0} is appended to coordinates_without_left_neighbor".format( (x, min_y) ))
        #print()
        
        i = 0
        while count > 0 or i < len(puzzle) :
            if x == puzzle[i][0]:
                #print("{0} is removed from the puzzle".format(puzzle.pop(i)))
                puzzle.pop(i)
                count -= 1
            else:
                i += 1
        if len(puzzle) != 0:
            max_y = puzzle[0][1]
            min_y = puzzle[0][1]
    
    print(coordinates_without_right_neighbor)
    print(coordinates_without_left_neighbor)
    print(coordinates_without_down_neighbor)
    print(coordinates_without_up_neighbor)    
    print()
        
    neighbor_i = copy.deepcopy(islands[0])#{ "num_of_bridges": -1, "neighbors":[], "coordinates": (0, 0) }
    #h_answer = []
    #v_answer = []
    i = 0
    
    
    while i < len(islands):
        j = 1
        left_found = False
        right_found = False
        up_found = False
        down_found = False
        #done = False
        neighbor_i = copy.deepcopy(islands[0])
        
        while not(right_found and left_found and down_found and up_found):# and not(done): #islands[i]["num_of_bridges"] > 0 ):#( num > 0  ):# and ( neighbor_i["coordinates"][1] != islands[i]["coordinates"][1] ) :
            
            print ("i != j ({0} != {1})".format(i, j))
            print("(neighbor_i[\"coordinates\"] and islands[i][\"coordinates\"] ({0} and {1})".format(neighbor_i["coordinates"], islands[i]["coordinates"]))
            
            if (neighbor_i["coordinates"] != islands[i]["coordinates"]):
                if (right_found == False):
                    if (islands[i]["coordinates"] in coordinates_without_right_neighbor):
                        right_found = True
                        print("right found")
               
                    elif (neighbor_i["coordinates"][0] == islands[i]["coordinates"][0]) and (neighbor_i["coordinates"][1] > islands[i]["coordinates"][1]) and (neighbor_i["coordinates"][0] == islands[i]["coordinates"][0]):#(i != j) and 
                        #checking the right neighbor
                        #print("right_found == False")
                        #if (neighbor_i["coordinates"][0] == islands[i]["coordinates"][0]) and (neighbor_i["coordinates"][1] > islands[i]["coordinates"][1]):
                        right_found = True
                        islands[i]["neighbors"].append((neighbor_i["coordinates"], neighbor_i["num_of_bridges"]))
                        print("right_found: {0} is added to {1}".format(neighbor_i["coordinates"], islands[i]["coordinates"]))
                        #islands[i]["num_of_bridges"] -= 1
                        #print("num_of_bridges is decreased to {0}".format(islands[i]["num_of_bridges"]))
                        #done = True
                    
                if (left_found == False):
                    if (islands[i]["coordinates"] in coordinates_without_left_neighbor):
                        left_found = True
                        print("left found")
                    elif ((islands[i]["coordinates"], islands[i]["num_of_bridges"]) in neighbor_i["neighbors"]) and (neighbor_i["coordinates"][1] < islands[i]["coordinates"][1]) and (neighbor_i["coordinates"][0] == islands[i]["coordinates"][0]):
                        #print("left_found == False")
                        #if (islands[i]["coordinates"] in neighbor_i["neighbors"]):#left_found
                        left_found = True
                        islands[i]["neighbors"].append((neighbor_i["coordinates"], neighbor_i["num_of_bridges"]))
                        print("left_found: {0} is added to {1}".format(neighbor_i["coordinates"], islands[i]["coordinates"]))
                        #islands[i]["num_of_bridges"] -= 1
                        #print("num_of_bridges is decreased to {0}".format(islands[i]["num_of_bridges"]))   
                
                if (down_found == False):  
                    if islands[i]["coordinates"] in coordinates_without_down_neighbor:
                        down_found = True
                        print("down found")
                    elif (neighbor_i["coordinates"][1] == islands[i]["coordinates"][1]) and (neighbor_i["coordinates"][0] > islands[i]["coordinates"][0]):# and (islands[i]["coordinates"] in neighbor_i["neighbors"]):#(i != j) and 
                        #print("down_found == False")
                        #if (neighbor_i["coordinates"][1] == islands[i]["coordinates"][1]):
                        down_found = True
                        islands[i]["neighbors"].append((neighbor_i["coordinates"], neighbor_i["num_of_bridges"]))
                        print("down_found: {0} is added to {1}".format(neighbor_i["coordinates"], islands[i]["coordinates"]))
                        #islands[i]["num_of_bridges"] -= 1
                        #print("num_of_bridges is decreased to {0}".format(islands[i]["num_of_bridges"]))
                
                if (up_found == False):    
                    if islands[i]["coordinates"] in coordinates_without_up_neighbor:
                        up_found = True
                        print("up found")
                    elif (neighbor_i["coordinates"][1] == islands[i]["coordinates"][1]) and (neighbor_i["coordinates"][0] < islands[i]["coordinates"][0]) and ((islands[i]["coordinates"], islands[i]["num_of_bridges"]) in neighbor_i["neighbors"]):#(i != j) and 
                        #print("up_found == False")
                        #if (neighbor_i["coordinates"][1] == islands[i]["coordinates"][1]):
                        up_found = True
                        islands[i]["neighbors"].append((neighbor_i["coordinates"], neighbor_i["num_of_bridges"]))
                        print("up_found: {0} is added to {1}".format(neighbor_i["coordinates"], islands[i]["coordinates"]))
                        #islands[i]["num_of_bridges"] -= 1
                        #print("num_of_bridges is decreased to {0}".format(islands[i]["num_of_bridges"]))

            if j < len(islands):
                neighbor_i = copy.deepcopy(islands[j])
                j += 1
            else:
                j = 1
            print()
        
        left_found = False 
        right_found = False
        down_found = False
        up_found = False
        #done = False 
        i += 1
        
    #island = { "num_of_bridges": p[2], "neighbors":[], "coordinates": (p[0], p[1]), "mark": False }
    #for i in islands:
    h_answer = []
    v_answer = []
    temp_h_answer = []
    temp_v_answer = []
    temp_hv_answer = []
    temp_hv_answers = []
    possible_combinations = []
    
    advanced_h_answer = []
    advanced_v_answer = []
    candidate = ()
    other_candidates = []
    candidates = []
    
    advanced_islands = []
    advanced_marked_coordinates = []
    
    prev_h = []
    prev_v = []
    
    advanced_tech = False
    advanced_tech_index = -1
    added_a_bridge_once_already = False
    
    i = 0
    done = False
    #change_islands = False
    #islands = copy.deepcopy(advanced_islands)
    
    while i < len(islands) and not(done):
        '''
        if change_islands:
            #islands = copy.deepcopy(advanced_islands)
            change_islands = False
            i = 0
        '''
        neighbor_bridges, neighbor_coordinates, neighbor_marked_and_not_blocked, neighbor_blocked = what_are_neighbor_coordinates_marked_blocked(islands, i, v_answer, h_answer)
        print("marked_coordinates: {0}".format(marked_coordinates))       
        print("neighbor coordinates are {0}".format(neighbor_coordinates))
        print("neighbor bridges are {0}".format(neighbor_bridges))
        print(islands[i]["neighbors"])
        print("neighbor_marked_and_not_blocked are {0}".format(neighbor_marked_and_not_blocked))
        print("neighbor_blocked are {0}".format(neighbor_blocked))
        
        j = 0
        basic_tech_3 = True
        
        while ((j < len(islands[i]["neighbors"])) and (islands[i]["mark"] != True)):# and (islands[i]["num_of_bridges"] != 0):    #break    # and not(change_islands)
            
            print("Coordinates: {0}".format(islands[i]["coordinates"]))
            print("Neighbor: {0}".format(islands[i]["neighbors"][j]))
            print(h_answer)
            print(v_answer)
            neighbors_length = len(neighbor_bridges)#islands[i]["neighbors"])    #isolation is [False, True]0
            #print(neighbors_length)
            
            #print((islands[i]["num_of_bridges"]%2) == 1)
            #print( ((islands[i]["num_of_bridges"]/2)+1) )
            #print(neighbors_length)
            #print(1 not in neighbor_bridges)
            
            
            #print("{0}=={1}".format(j, len(islands[i]['neighbors'])-1))
            #print(islands[i]["mark"])       
            #print("{0}=={1}".format(islands[i]["coordinates"][1],islands[i]["neighbors"][j][0][1]))                                                                                                                                                 #for (3,1) and (5,1):  3  == 5                                 or                             1 == 1
            if ((j == len(islands[i]['neighbors']) - 1) or ((islands[i]["neighbors"][j][0] not in neighbor_marked_and_not_blocked) and (islands[i]["neighbors"][j][0] not in neighbor_blocked)))   and   (islands[i]["mark"] != True)   and   ((islands[i]["coordinates"][0] == islands[i]["neighbors"][j][0][0]) or (islands[i]["coordinates"][1] == islands[i]["neighbors"][j][0][1])):#horizontal line or vertical line
                #print("islands[i][\"num_of_bridges\"] ?= len(islands[i][\"neighbors\"]) ({0} ?= {1})".format(islands[i]["num_of_bridges"], neighbors_length))
                #"(islands[i]["num_of_bridges"] == neighbors_length * 2) or" was added because of 6(3,1) of ultra easy example
                basic_tech_3 = is_this_valid_basic_3(i, j, neighbor_coordinates, neighbors_length, basic_tech_3)
                #iso_tech_1_done = False
                #neighbors_length was taken off becuz of 2nd (5, 3)
                
                #if advanced_tech and not(added_a_bridge_once_already) and connections == [] and 1 == len(temp_hv_answers[0]):
                if not(is_there_enough_num_of_edges_left_in_the_neighbors_for_the_center(i, neighbor_coordinates, islands)) and added_a_bridge_once_already:
                    print("sth went wrong bcuz the number of edges for the neighbors < the number of edges for the center")
                    #advanced_tech = False
                    added_a_bridge_once_already = False
                    
                    print("going back to when there is no isolating bridge added, and trying with a new bridge")
                    h_answer = copy.deepcopy(advanced_h_answer)
                    v_answer = copy.deepcopy(advanced_v_answer)
                    #advanced_islands = copy.deepcopy(islands)
                    #advanced_marked_coordinates = copy.deepcopy(marked_coordinates)
                    
                    if 0 != len(advanced_islands):
                        islands = copy.deepcopy(advanced_islands)
                    
                    #change_islands = True
                    marked_coordinates = copy.deepcopy(advanced_marked_coordinates)
                    print("went back to the prev answers")
                    
                    #if 0 != len(other_candidates):
                    #    candidate = 
                            
                elif (((islands[i]["num_of_bridges"] == len(islands[i]["neighbors"]) * 2) or (islands[i]["num_of_bridges_left"] == neighbors_length * 2)) and (neighbors_length > 1) and (0 == neighbor_bridges.count(1)))\
                or ((len(islands[i]["neighbors"]) == 1) and (islands[i]["num_of_bridges"] == 2)):#starting technique / basic tech 1-2
                #neighbors_length == 1 is changed to (len(islands[i]["neighbors"]) == 1)
                    if (islands[i]["num_of_bridges"] == neighbors_length * 2) and (neighbors_length > 1):
                        print("starting technique:")# Islands with 4 in the corner, 6 on the side and 8 in the middle:
                    else:
                        print("basic tech 1-2:")#1. Islands with a single neighbor ex) 1, 2
                        
                    if ((len(islands[i]["neighbors"]) == 1) and (islands[i]["num_of_bridges"] == 2) and (islands[i]["num_of_bridges_left"] == 1)):  #step 33 Coordinates: (1, 9)
                        connect_to_neighbor_and_mark(i, j, False, h_answer, v_answer, True, islands)
                    else:# Islands with 4 in the corner, 6 on the side and 8 in the middle:
                        connect_to_neighbor_and_mark(i, j, False, h_answer, v_answer, True, islands)#connect_to_neighbor_and_mark(i, j, False, h_answer, v_answer, False->True) because of (1,1,3,1)
                    #print("{0} is popped".format(islands[i]["neighbors"].pop(j)))
                    #j += 1
                    '''
                    if ( islands[i]["num_of_bridges"] == neighbors_length*2 ):
                        k = 0
                        found = False
                        while (k < len(islands)) and (not(found)):
                            if islands[i]["neighbors"][j][0] == islands[k]["coordinates"]:
                                found = True
                                if islands[k]["mark"] != True:
                                    islands[k]["mark"] = True
                                    print("islands[k]['num_of_bridges_left']: {0} is decreased to ".format(islands[k]['num_of_bridges_left']))
                                    islands[k]['num_of_bridges_left'] = islands[k]['num_of_bridges_left'] - 2
                                    print("{1}".format(islands[k]['num_of_bridges_left']))
                                else:
                                    print("{0} is already marked".format(islands[k]["coordinates"]))
                            k += 1
                        '''
                        #neighbors_length was taken off becuz of (4, 6) of very easy
                elif ((len(islands[i]["neighbors"]) == 1) and (((islands[i]["num_of_bridges"] == 1) and (1 <= how_many_left(neighbor_coordinates[0], islands))) or ((islands[i]["num_of_bridges"] == 2)and (2 <= how_many_left(neighbor_coordinates[0], islands))))) or\
                     (((islands[i]["num_of_bridges"] % 2) == 1) and (int(math.floor(islands[i]["num_of_bridges"] / 2)) + 1 == len(islands[i]["neighbors"])) and (1 not in neighbor_bridges) and not(all_neighbors_connected(islands[i]["coordinates"], islands[i]["neighbors"], h_answer, v_answer))):#basic tech 1-1 / 2    (len(islands[i]["neighbors"]) + len(neighbor_marked_and_not_blocked) == 2) and  was taken out from this line because of (1, 5) of ultra easy
                    #neighbors_length was replaced to len(islands[i]["neighbors"]) becuz of (5, 1)
                    #and not(all_neighbors_connected(islands[i]["coordinates"], islands[i]["neighbors"], h_answer, v_answer)) was added becuz of (10,1) of step 36
                    if (neighbors_length == 1) and (islands[i]["num_of_bridges"] == 1):
                        print("basic tech 1-1: ")
                    else:
                        print("basic tech 2: ")
                    
                    '''
                    h_answer, v_answer = hv_answers(islands[i], h_answer, v_answer, j, 1)
                    print("h_answer is {0}".format(h_answer))
                    print("v_answer is {0}".format(v_answer))
                    if ( (neighbors_length == 1) and (islands[i]["num_of_bridges"] == 1) ):
                        if islands[i]["mark"] != True:
                            islands[i]["mark"] = True
                            islands[i]['num_of_bridges_left'] = islands[i]['num_of_bridges_left'] - 1
                        else:
                            print("{0} is already marked".format(islands[i]["coordinates"]))
                        if islands[i]["coordinates"] not in marked_coordinates:
                            marked_coordinates.append(islands[i]["coordinates"])
                        else:
                            print("{0} is already in marked_coordinates".format(islands[i]["coordinates"]))
                    '''
                    tuple = get_line_ordered(islands[i]["coordinates"], islands[i]["neighbors"][j][0])                   
                    if ((tuple not in h_answer) and (tuple not in v_answer)) or neighbors_length == 1:
                        #(index, neighbor_index_inside_neighbors, no_two_bridges, h_answer, v_answer, double_line):
                        connect_to_neighbor_and_mark(i, j, True, h_answer, v_answer, False, islands)
                    else:
                        print("in basic tech 1-1 and basic tech 2")
                    #j += 1 because of (10,1)~(10,4)
                    #print("{0} is popped".format(islands[i]["neighbors"].pop(j)))
                elif ((neighbors_length == 1) and (islands[i]["num_of_bridges"] > 2) and (islands[i]["num_of_bridges_left"] > 2)):#basic tech 1
                    print("This violates the rules of Hashi because there is only one neighbor and islands[i][\"num_of_bridges\"] > 2)")
                    print("because of step 36-> (10, 1), the below was added")
                    connect_to_neighbor_and_mark(i, j, False, h_answer, v_answer, True, islands)#(i, j, True->False, h_answer, v_answer, True) because of (5,8) of ultra easy
                    #j += 1
                    #(islands[i]["num_of_bridges"]//2)+1 == neighbors_length was taken off due to (4,4) of easy
                    #(islands[i]["num_of_bridges"]//2)+1 == neighbors_length too
                elif ((islands[i]["num_of_bridges"] != 1) and ((islands[i]["num_of_bridges"] % 2) == 1) and ((islands[i]["num_of_bridges"] // 2) + 1 == len(islands[i]["neighbors"])) and (1 in neighbor_bridges) and (1 == neighbor_bridges.count(1)) and (basic_tech_3))\
                 or  ((islands[i]["num_of_bridges"] == 4) and (len(islands[i]["neighbors"]) == 3) and (2 == neighbor_bridges.count(1))):#basic tech 3 / 4
                    
                    if ((islands[i]["num_of_bridges"] != 1) and ((islands[i]["num_of_bridges"] % 2) == 1) and ((islands[i]["num_of_bridges"] // 2) + 1 == len(islands[i]["neighbors"])) and (1 in neighbor_bridges)):
                        print("basic tech 3: ")
                        #print("basic_tech_3: {0}".format(basic_tech_3))
                    else:
                        print("basic tech 4: ")
                        
                    #mark_and_connect_to_neighbor()    
                    connect_to_neighbor_and_mark(i, j, False, h_answer, v_answer, False, islands)
                    #j += 1
                    #print("{0} is popped".format(islands[i]["neighbors"].pop(j)))
                    #islands[i]['num_of_bridges_left'] = islands[i]['num_of_bridges_left'] - 1
                elif (islands[i]["num_of_bridges"] == 6) and (neighbors_length == 4) and (1 in neighbor_bridges) and (1 == neighbor_bridges.count(1)) and\
                     not(basic_5_neighbors_connected(islands[i]["coordinates"], islands[i]["neighbors"], h_answer, v_answer)):#basic tech 5
                    '''
                    if (islands[i]["neighbors"][j][1] != 1):
                        print("basic tech 5: ")
                        h_answer, v_answer = hv_answers(islands[i], h_answer, v_answer, j, 1)
                        print("h_answer is {0}".format(h_answer))
                        print("v_answer is {0}".format(v_answer))
                        islands[i]['num_of_bridges_left'] = islands[i]['num_of_bridges_left'] - 1
                    '''
                    print("basic tech 5: ")
                    if (islands[i]["neighbors"][j][1] != 1):#this is added because of 6(4,5) of ultra easy example
                        connect_to_neighbor_and_mark(i, j, True, h_answer, v_answer, False, islands)#(i, j, False->True, h_answer, v_answer, False) because of 6(4,5) of ultra easy example
                    #j += 1
                    #find_neighbor_deduct_num_of_bridges_and_mark(i, j)
                        
                        #print("{0} is popped".format(islands[i]["neighbors"].pop(j)))
                        #islands[i]["num_of_bridges"] = islands[i]["num_of_bridges"] - 1
                    else:
                        print("This is a basic 5 case, but the vertex and the neighbor are not connected / already connected / i'm not sure if this is a basic 5 case")
                #or (neighbors_length == 3)
                #this was changed because of (5, 3) of ultra easy        # or ((1 == how_many_left(neighbor_coordinates[0]) or 1 == how_many_left(neighbor_coordinates[1])) and 2 != how_many_left(neighbor_coordinates[0]) + how_many_left(neighbor_coordinates[1])) ))\
                #neighbors_length == 2 was changed to len(islands[i]["neighbors"]) == 2 bcuz of 5th (5, 7) get_started
                elif (len(islands[i]["neighbors"]) == 2) and\
                     (  ((islands[i]["num_of_bridges"] == 1) and (islands[i]["num_of_bridges_left"] == 1) and (((1 in neighbor_bridges) and (1 == len(neighbor_bridges) - neighbor_bridges.count(1)))) )\
                     or ((islands[i]["num_of_bridges"] == 2) and (islands[i]["num_of_bridges_left"] == 2) and (((2 in neighbor_bridges) and (1 == len(neighbor_bridges) - neighbor_bridges.count(2)))) )   )\
                     and not(iso_1_neighbor_connected(islands[i]["coordinates"], islands[i]["neighbors"], h_answer, v_answer)):#and (islands[i]["num_of_bridges_left"] == 2) was taken off because of (8, 2) of ultra easy    #or ((2 == how_many_left(neighbor_coordinates[0]) or 2 == how_many_left(neighbor_coordinates[1])) and 4 != how_many_left(neighbor_coordinates[0]) + how_many_left(neighbor_coordinates[1])) ))   ):#and (islands[i]["neighbors"][j][1] != 2) # iso 1 #or (neighbors_length == 3) was added because of step 11
                    #and is_one_or_two_not_connected_to_non_neighbors(islands[i]["neighbors"])
                    #connected_neighbor(islands[i]["coordinates"], find_neighbor_coordinate_without_the_input_vertex(neighbor_coordinates, [2]), h_answer, v_answer) was changed to
                    print("iso tech 1: ")# this was updated because of (6,2) of ultra easy
                    #(islands[i]["num_of_bridges"] == islands[i]["num_of_bridges_left"] + how_many_lines(islands[i]["coordinates"], h_answer, v_answer)
                    '''
                    h_answer, v_answer = hv_answers(islands[i], h_answer, v_answer, j, 1)
                    print("h_answer is {0}".format(h_answer))
                    print("v_answer is {0}".format(v_answer))
                    '''
                    #I got rid of the bottom because of 1(6,4)
                    #if (neighbors_length == 2) and (((islands[i]["num_of_bridges"] == 1) and (1 in neighbor_bridges) and (islands[i]["neighbors"][j][1] != 1))):
                    #    print("{0} was popped".format(islands[i]["neighbors"].pop(j)))#getting rid of 1, the non neighbor
                    tuple = get_line_ordered(islands[i]["coordinates"], islands[i]["neighbors"][j][0])# and (1 != how_many_left(islands[i]["neighbors"][j][0])))\ becuz of step 4
                    if (((tuple not in h_answer) and (tuple not in v_answer)) or neighbors_length == 1) and ((islands[i]["neighbors"][j][1] != 1))\
                                                                                                        and ((islands[i]["neighbors"][j][1] != 2)):# and (2 != how_many_left(islands[i]["neighbors"][j][0]))):#updated because of (5,3) of ultra easy
                        connect_to_neighbor_and_mark(i, j, True, h_answer, v_answer, False, islands) 
                        #j += 1
                    else:
                        print("This is an iso 1 case, but the vertex and the neighbor are not connected / already connected / i'm not sure if this is an iso 1 case")
                        #iso_tech_1_done = True
                        #print("iso_tech_1_done is set to True")
                        
                    '''
                    #this elif was added because of (6,2) of ultra easy for (4, 2, 6, 2)
                    elif (((tuple not in h_answer) and (tuple not in v_answer)) or neighbors_length == 1) and \
                    (   ((islands[i]["num_of_bridges"] == 1) and ((1 != how_many_left(islands[i]["neighbors"][j][0])))) or \
                        ((islands[i]["num_of_bridges"] == 2) and ((2 != how_many_left(islands[i]["neighbors"][j][0]))))  ):
                        connect_to_neighbor_and_mark(i, j, True, h_answer, v_answer, False)
                    '''
                    #print("{0} is popped".format(islands[i]["neighbors"].pop(j)))
                    #islands[i]["num_of_bridges"] = islands[i]["num_of_bridges"] - 1
                    #j += 1
                #+ len(neighbor_marked_and_not_blocked) #(neighbors_length == 3) was replaced with (len(islands[i]["neighbors"]) == 3) because of (1,6) after step 32
                #(islands[i]["num_of_bridges"] == 3 or islands[i]["num_of_bridges"] == 2) and \ was taken out becuz of step 7 of sample
                elif (neighbors_length == 3) and (neighbors_length + len(neighbor_marked_and_not_blocked) != 4) and \
                (islands[i]["num_of_bridges"] == islands[i]["num_of_bridges_left"] + how_many_lines(islands[i]["coordinates"], h_answer, v_answer)) and\
                ((neighbor_bridges[0]<3 and neighbor_bridges[1]<3 and islands[i]["num_of_bridges"] == neighbor_bridges[0] + neighbor_bridges[1]) or\
                 (neighbor_bridges[0]<3 and neighbor_bridges[2]<3 and islands[i]["num_of_bridges"] == neighbor_bridges[0] + neighbor_bridges[2]) or\
                 (neighbor_bridges[1]<3 and neighbor_bridges[2]<3 and islands[i]["num_of_bridges"] == neighbor_bridges[1] + neighbor_bridges[2]) or\
                 (islands[i]["num_of_bridges"] == 1 and 2 == neighbor_bridges.count(1))) and\
                not(neighbor_bridges[0] == neighbor_bridges[1] and neighbor_bridges[0] == neighbor_bridges[2] and neighbor_bridges[1] == neighbor_bridges[2]) and\
                not(connected_neighbor(islands[i]["coordinates"], find_neighbor_coordinate_without_the_input_vertex(neighbor_coordinates, [1, 2]), h_answer, v_answer)) and\
                not( (islands[i]["num_of_bridges"] == 3) and (2 == neighbor_bridges.count(1) or 2 == neighbor_bridges.count(2)) ):
                #(   ((islands[i]["num_of_bridges"] == 2) and (1 in neighbor_bridges) and (islands[i]["neighbors"][j][1] != 1))\
                #or((islands[i]["num_of_bridges"] == 3) and\
                #   (((1 in neighbor_bridges) and (2 in neighbor_bridges) and (islands[i]["neighbors"][j][1] != 1) and (islands[i]["neighbors"][j][1] != 2))or((1 not in neighbor_bridges))))   ):#iso 2
                
                #(2 == neighbor_bridges.count(1)) was replaced with (1 in neighbor_bridges) becuz of step 13     
                #or((1 not in neighbor_bridges))) was added bcuz of step 14                   
                    print("iso tech 2: ")
                    '''
                    h_answer, v_answer = hv_answers(islands[i], h_answer, v_answer, j, 1)
                    print("h_answer is {0}".format(h_answer))
                    print("v_answer is {0}".format(v_answer))
                    '''
                    tuple = get_line_ordered(islands[i]["coordinates"], islands[i]["neighbors"][j][0])
                                           #(neighbors_length == 3):# and\
                    if (((tuple not in h_answer) and (tuple not in v_answer)) or (neighbors_length == 1)) and\
                       ((islands[i]["num_of_bridges"] == neighbor_bridges[0] + neighbor_bridges[1]) and (islands[i]["neighbors"][j][1] != neighbor_bridges[0]) and (islands[i]["neighbors"][j][1] != neighbor_bridges[1])) or\
                       ((islands[i]["num_of_bridges"] == neighbor_bridges[0] + neighbor_bridges[2]) and (islands[i]["neighbors"][j][1] != neighbor_bridges[0]) and (islands[i]["neighbors"][j][1] != neighbor_bridges[2])) or\
                       ((islands[i]["num_of_bridges"] == neighbor_bridges[1] + neighbor_bridges[2]) and (islands[i]["neighbors"][j][1] != neighbor_bridges[1]) and (islands[i]["neighbors"][j][1] != neighbor_bridges[2])) or\
                       (islands[i]["num_of_bridges"] == 1 and islands[i]["neighbors"][j][1] != 1):#this is because of step 11
                            connect_to_neighbor_and_mark(i, j, True, h_answer, v_answer, False, islands)
                            #j += 1
                    else:
                        print("i'm not sure if this is an iso 2 case")
                    #print("{0} is popped".format(islands[i]["neighbors"].pop(j)))
                    #islands[i]["num_of_bridges"] = islands[i]["num_of_bridges"] - 1

                #or  (islands[i]['num_of_bridges_left'] == 2 and (2 in neighbor_bridges) and islands[i]["neighbors"][j][1] != 2 and islands[i]["neighbors"][j][0] not in marked_coordinates))\
                    '''#skipped becuz of (6,5), sudoku_4 
                    elif ((islands[i]['num_of_bridges_left'] == 1 and (1 in neighbor_bridges) and islands[i]["neighbors"][j][1] != 1 and islands[i]["neighbors"][j][0] not in marked_coordinates))\
                        and (1 <= len(islands[i]["marked_neighbor_coordinates"])) and (islands[i]["num_of_bridges"] == 3) and (islands[i]["neighbors"][j][0] not in neighbor_blocked)\
                        and (2 >= neighbors_length):# and is_there_the_only_way_without_isolation(i, target_neighbor_indexes, neighbor_blocked, h_answer, v_answer, neighbor_marked_and_not_blocked, temp_hv_answers)[0]:#iso 3 
                        print("iso tech 3: ")
                        #going in with 3 on (1,2)
                        #this might be done in a separate function
                        connect_to_neighbor_and_mark(i, j, False, h_answer, v_answer, False, islands)
                    '''
                elif (j == len(islands[i]["neighbors"]) - 1) and (is_this_iso_tech_1(neighbors_length, i, neighbor_bridges, h_answer, v_answer)):
                    found_j = find_j(i, neighbor_coordinates)
                    tuple = get_line_ordered(islands[i]["coordinates"], islands[i]["neighbors"][found_j][0])# and (1 != how_many_left(islands[i]["neighbors"][j][0])))\ becuz of step 4
                    if (((tuple not in h_answer) and (tuple not in v_answer)) or neighbors_length == 1):
                        # and ((islands[i]["neighbors"][j][1] != 1)) and ((islands[i]["neighbors"][j][1] != 2)):# and (2 != how_many_left(islands[i]["neighbors"][j][0]))):#updated because of (5,3) of ultra easy
                        connect_to_neighbor_and_mark(i, found_j, True, h_answer, v_answer, False, islands) 
                    else:
                        print("This is an iso 1 after case, but the vertex and the neighbor are not connected / already connected / i'm not sure if this is an iso 1 case")       
                elif (j == len(islands[i]["neighbors"]) - 1):#neighbors_length-1):#step 18,    neighbors_length = len(neighbor_bridges)    neighbor bridges are [2, 2]
                    j_two_list = []
                    for j_two in range(j + 1):#neighbor_marked_and_not_blocked are [(4, 6), (6, 4)]    neighbor_blocked are []
                        j_two_list.append(j_two)
                        j_two_list.append(j_two)
                        j_two_list.append(j_two)
                        
                    print("j_two_list is {0}".format(j_two_list))
                    
                    j_two_index = 0
                    
                    for j_two in j_two_list:
                        
                            
                        print("j_two: {0}".format(j_two))
                        print("islands[i][\"neighbors\"][j_two][0]={0}".format(islands[i]["neighbors"][j_two][0]))
                        if ((islands[i]["neighbors"][j_two][0] not in neighbor_marked_and_not_blocked) and (islands[i]["neighbors"][j_two][0] not in neighbor_blocked)):
                            temp_num_of_bridges_left = copy.deepcopy(islands[i]['num_of_bridges_left'])
                            #if (temp_num_of_bridges_left > 0):
                            else_done = []
                            print("temp_num_of_bridges_left is {0}".format(temp_num_of_bridges_left))
                            #print("neighbors_length is {0}".format(neighbors_length))
                            for k in range(temp_num_of_bridges_left):#neighbors_length):
                                else_done.append(False)
                                #print(done)
                                
                            print(else_done)
                            ################################################################################
                            for num_of_lines in range(1, min(3, temp_num_of_bridges_left + 1)):
                                second_time = False
                                third_time = False    
                                if j_two_index in [1,4,7,10]:
                                    second_time = True
                                    print("second time!")
                                elif j_two_index in [2,5,8,11]:
                                    third_time = True
                                    print("third time!")
                                
                                print("num_of_lines: {0}".format(num_of_lines))
                                for k in range(temp_num_of_bridges_left):#neighbors_length):
                                    else_done[k] = False
                                print("else_done is reset to {0}".format(else_done))
                                
                                if num_of_lines == 1:
                                    no_two_bridges = True
                                else:
                                    no_two_bridges = False
                                
                                l = copy.deepcopy(j_two)
                                    
                                temp = []
                                temp_hv_answer = []
                                
                                else_done_index = 0
                                temp_hv_answer_one = []
                                
                                go_back_only_once_for_third_time=True
                                
                                while temp_num_of_bridges_left != 0 and go_back_only_once_for_third_time:# and not(third_time) and j_two != j:
                                    print("while temp_num_of_bridges_left != 0:")
                                    else_done_index_found = False
                                    
                                    while not(else_done_index_found) and l < len(islands[i]['neighbors']):
                                        print("while not(else_done_index_found) and l < len(islands[i]['neighbors']):")
                                        k, neighbor_coordinates_index, else_done_index, else_done_index_found = is_it_marked_or_blocked_coordinate(neighbor_coordinates, i, l, else_done_index)
                                        print("is_it_marked_or_blocked_coordinate returned {0}, {1}, {2}, {3}".format(k, neighbor_coordinates_index, else_done_index, else_done_index_found))
                                        #if islands[i]['coordinates'] == (5, 5):
                                            #print("what?")
                                        if   not(else_done_index_found) and (0 <= l and l <= len(islands[i]['neighbors']) - 1) and third_time == False:
                                            if l != len(islands[i]['neighbors']) - 1:
                                                l += 1
                                                print("l is increased to {0}".format(l))
                                            else:#l == len(islands[i]['neighbors']) - 1
                                                l = 0
                                                print("l is reset to 0")
                                        elif not(else_done_index_found) and (0 <= l and l <= len(islands[i]['neighbors']) - 1) and third_time:
                                            if l != 0:
                                                l -= 1
                                                print("l is decreased to {0}".format(l))
                                            else:#l == 0
                                                l = copy.deepcopy(j)
                                                print("l = copy.deepcopy(j) => l: {0}".format(l))
                                        else:
                                            l = copy.deepcopy(k)
                                            print("k: {0} is assigned to l: {1}".format(k, l))
                                            
                                    
                                    if (-1 < l) and (l < len(islands[i]['neighbors'])) and (islands[i]["neighbors"][l][0] not in neighbor_blocked):# and (l != -1):# and (l >= j_two):
                                        is_it_going_thru_else=False
                                        
                                        if second_time and len(temp_hv_answer_one) != 0:
                                            print("if second_time and len(temp_hv_answer_one) != 0:")
                                            temp_hv_answer, num_bridges_to_deduct = connect_to_neighbor_temporarily(i, l, False,          temp_h_answer, temp_v_answer, temp_num_of_bridges_left, h_answer, v_answer, islands)
                                            second_time=False
                                        else:#if len(temp_hv_answer_one) == 0:
                                            print("else?!?")
                                            temp_hv_answer, num_bridges_to_deduct = connect_to_neighbor_temporarily(i, l, no_two_bridges, temp_h_answer, temp_v_answer, temp_num_of_bridges_left, h_answer, v_answer, islands)
                                            is_it_going_thru_else=True
                                            
                                            t_index=0
                                            is_there_a_neigbor_with_more_than_one_edge_left=False
                                            while not(is_there_a_neigbor_with_more_than_one_edge_left) and t_index <= j:
                                                if ( (0 == h_answer.count(get_line_ordered(islands[i]['coordinates'], islands[i]['neighbors'][t_index][0])) and (islands[i]['coordinates'][0] == islands[i]['neighbors'][t_index][0][0])) or \
                                                     (0 == v_answer.count(get_line_ordered(islands[i]['coordinates'], islands[i]['neighbors'][t_index][0])) and (islands[i]['coordinates'][1] == islands[i]['neighbors'][t_index][0][1])) ) and \
                                                   how_many_left(islands[i]['neighbors'][t_index][0], islands) > 1 and islands[i]['neighbors'][t_index][0] not in neighbor_blocked:#connected_neighbor(islands[i]['coordinates'], islands[i]['neighbors'][t_index][0], h_answer, v_answer):_#how_many_left(islands[i]['neighbors'][t_index][0]) > 1:
                                                    #print("how_many_left(islands[i]['neighbors'][t_index][0]): {0} > 1:".format(how_many_left(islands[i]['neighbors'][t_index][0])))
                                                    is_there_a_neigbor_with_more_than_one_edge_left = True
                                                    print("is_there_a_neigbor_with_more_than_one_edge_left is set to True")
                                                t_index += 1
                                                
                                            if is_there_a_neigbor_with_more_than_one_edge_left ==False:
                                                if l+1 < neighbors_length and not(third_time):#len(islands[i]['neighbors']): wa taken off bcuz of (1,14)
                                                    print("if is_there_a_neigbor_with_more_than_one_edge_left ==False: if l+1 < neighbors_length and not(third_time):")
                                                    one = 1
                                                    while is_it_already_in_temp_hv_answers(num_bridges_to_deduct, i, temp, temp_hv_answer, temp_hv_answers) and 0==num_bridges_to_deduct and l+one < j:
                                                        #temp_num_of_bridges_left = is_it_already_in_temp_hv_answers(num_bridges_to_deduct, i, temp, temp_hv_answer, temp_hv_answers, temp_num_of_bridges_left)[1]
                                                        print("l+one is {0}".format(l+one))
                                                        temp_hv_answer, num_bridges_to_deduct = connect_to_neighbor_temporarily(i, l+one, True, temp_h_answer, temp_v_answer, temp_num_of_bridges_left, h_answer, v_answer, islands)
                                                        if l+one < j:
                                                            one += 1
                                                        else:#l+one >= j:
                                                            one = 0
                                                elif l-1 > -1 and (third_time):#len(islands[i]['neighbors']): wa taken off bcuz of (1,14)
                                                    print("if is_there_a_neigbor_with_more_than_one_edge_left ==False: elif l-1 > -1 and (third_time):")
                                                    one = 1
                                                    while is_it_already_in_temp_hv_answers(num_bridges_to_deduct, i, temp, temp_hv_answer, temp_hv_answers) and 0==num_bridges_to_deduct and l-one > 0:
                                                        #temp_num_of_bridges_left = is_it_already_in_temp_hv_answers(num_bridges_to_deduct, i, temp, temp_hv_answer, temp_hv_answers, temp_num_of_bridges_left)[1]
                                                        print("l-one is {0}".format(l-one))
                                                        temp_hv_answer, num_bridges_to_deduct = connect_to_neighbor_temporarily(i, l-one, True, temp_h_answer, temp_v_answer, temp_num_of_bridges_left, h_answer, v_answer, islands)
                                                        if l-one > 0:
                                                            one += 1
                                                        else:#l-one <= 0:
                                                            one = 0
                                                '''
                                                temp_num_of_bridges_left = 0
                                                g = 0
                                                while g < len(else_done):
                                                    else_done[g]=True
                                                    g += 1
                                                '''    
                                        if not(is_it_going_thru_else) and num_bridges_to_deduct == 0:
                                            print("num_bridges_to_deduct == 0")
                                            temp_h_answer = []
                                            temp_v_answer = []
                                            temp_hv_answer, num_bridges_to_deduct = connect_to_neighbor_temporarily(i, l, True,           temp_h_answer, temp_v_answer, temp_num_of_bridges_left, h_answer, v_answer, islands)
##########################################################################
                                        if  (num_bridges_to_deduct == 2) and (else_done_index < len(else_done)-1):
                                            print("else: done[{0}] = True".format(else_done_index))#neighbor_coordinates_index))
                                            else_done[else_done_index] = True#neighbor_coordinates_index] = True
                                            else_done_index += 1
                                            print("else: done[{0}] = True".format(else_done_index))#neighbor_coordinates_index))
                                            else_done[else_done_index] = True#neighbor_coordinates_index] = True
                                            if islands[i]['num_of_bridges_left']-1 > else_done_index:#neighbors_length
                                                else_done_index += 1
                                        elif is_it_already_in_temp_hv_answers(num_bridges_to_deduct, i, temp, temp_hv_answer, temp_hv_answers):#, temp_num_of_bridges_left)[0]:
                                            #temp_num_of_bridges_left = is_it_already_in_temp_hv_answers(num_bridges_to_deduct, i, temp, temp_hv_answer, temp_hv_answers, temp_num_of_bridges_left)[1]
                                            if l+1 < neighbors_length and not(third_time):#len(islands[i]['neighbors']): wa taken off bcuz of (1,14)
                                                print("if l+1 < neighbors_length and not(third_time):")
                                                one = 1
                                                while is_it_already_in_temp_hv_answers(num_bridges_to_deduct, i, temp, temp_hv_answer, temp_hv_answers) and 0==num_bridges_to_deduct and l+one < j:
                                                    #temp_num_of_bridges_left = is_it_already_in_temp_hv_answers(num_bridges_to_deduct, i, temp, temp_hv_answer, temp_hv_answers, temp_num_of_bridges_left)[1]
                                                    temp_hv_answer, num_bridges_to_deduct = connect_to_neighbor_temporarily(i, l+one, no_two_bridges, temp_h_answer, temp_v_answer, temp_num_of_bridges_left, h_answer, v_answer, islands)
                                                    if l+one < j:
                                                        one += 1
                                            elif l-1 > -1 and (third_time):#len(islands[i]['neighbors']): wa taken off bcuz of (1,14)
                                                print("elif l-1 > -1 and (third_time):")
                                                one = 1
                                                while is_it_already_in_temp_hv_answers(num_bridges_to_deduct, i, temp, temp_hv_answer, temp_hv_answers) and 0==num_bridges_to_deduct and l-one > 0:
                                                    #temp_num_of_bridges_left = is_it_already_in_temp_hv_answers(num_bridges_to_deduct, i, temp, temp_hv_answer, temp_hv_answers, temp_num_of_bridges_left)[1]
                                                    temp_hv_answer, num_bridges_to_deduct = connect_to_neighbor_temporarily(i, l-one, no_two_bridges, temp_h_answer, temp_v_answer, temp_num_of_bridges_left, h_answer, v_answer, islands)
                                                    if l-one > 0:
                                                        one -= 1
                                            print("1. else: done[{0}] = True".format(else_done_index))#neighbor_coordinates_index))
                                            else_done[else_done_index] = True#neighbor_coordinates_index] = True
                                            if islands[i]['num_of_bridges_left']-1 > else_done_index:#neighbors_length
                                                else_done_index += 1                                                      
                                        elif (num_bridges_to_deduct != 0):
                                            print("2. else: done[{0}] = True".format(else_done_index))#neighbor_coordinates_index))
                                            else_done[else_done_index] = True#neighbor_coordinates_index] = True
                                            if islands[i]['num_of_bridges_left']-1 > else_done_index:#neighbors_length
                                                else_done_index += 1
                                            #temp_hv_answer_one = temp_hv_answer
                                        '''
                                        if (num_bridges_to_deduct != 0) and (islands[i]['num_of_bridges_left'] == len(temp+temp_hv_answer)) and (temp+temp_hv_answer not in temp_hv_answers):
                                            print('temp_num_of_bridges_left -= num_bridges_to_deduct is not operated')
                                        else:
                                        '''
                                        temp_num_of_bridges_left -= num_bridges_to_deduct
                                            
                                        temp_h_answer = []
                                        temp_v_answer = []
                                        temp_hv_answer_one = []
                                        print("l?=j_two: {0}?={1}".format(l, j_two))
                                        print("temp_num_of_bridges_left={0}".format(temp_num_of_bridges_left))
                                        #print("{0} >= {1}+{2}".format(islands[i]["neighbors"][l][1]=temp_hv_answer + temp.count(temp_hv_answer), temp_hv_answer, temp.count(temp_hv_answer))
                                        if (l == j_two) and (temp_num_of_bridges_left != 0):#(temp_num_of_bridges_left != 0) is added because of (6,6) #(is_it_done(else_done, neighbors_length) and temp == temp_hv_answer_one):#temp_num_of_bridges_left == 0:
                                            temp_hv_answer_one = []
                                            print("temp_hv_answer: {0} is ADDed ".format(temp_hv_answer), end="")
                                            print("to temp_hv_answer_one:{0}".format(temp_hv_answer_one))
                                            temp_hv_answer_one = temp_hv_answer
                                            print("temp_hv_answer_one: {0} is ADDed ".format(temp_hv_answer_one), end="")
                                            print("to temp:{0}".format(temp))
                                            temp += temp_hv_answer_one
                                        #elif 1 == len(temp_hv_answer) and what_is_vertex(extract_the_neighbor_coordies_from_temp_hv_answer(temp_hv_answer[0], i)) >= 1 + temp.count(temp_hv_answer[0]):
                                            #print("temp_hv_answer1: {0} is added ".format(temp_hv_answer), end="")
                                            #temp += temp_hv_answer
                                            #print("to temp:{0}".format(temp))
                                        #elif (l != j_two) and (temp_num_of_bridges_left != 0):
                                            #print('doing nothing')
                                        else:
                                            #1 < len(temp_hv_answer)
                                            print("the current temp is {0}".format(temp))
                                            print("the current temp_hv_answer is {0}".format(temp_hv_answer))
                                            for t in temp_hv_answer:
                                                print()
                                                #what_is_vertex() is changed to how_many_left() becuz of (3, 7) of very easy
                                                if (1+temp.count(t) < 3) and (how_many_left(extract_the_neighbor_coordy_from_t(t, i), islands) >= 1 + temp.count(t)) and (len(temp) < islands[i]['num_of_bridges_left']):#(0 != temp_num_of_bridges_left) and
                                                    print("t: {0} is added ".format(t), end="")
                                                    #if (l != j_two) and len(temp_hv_answer) != 0:
                                                    print("to temp:{0}".format(temp))
                                                    temp += (t,)
                                                elif (1+temp.count(t) >= 3):
                                                    print("t:{0} can't be added to temp ".format(t), end="")
                                                    print("because of 1 +temp.count(t): {1} >= 3".format(temp_hv_answer.count(t), temp.count(t)))   
                                                elif (len(temp) >= islands[i]['num_of_bridges_left']):
                                                    print("t:{0} can't be added to temp ".format(t), end="")
                                                    print("because of len(temp):{0} >= islands[i]['num_of_bridges_left']:{1}".format(len(temp), islands[i]['num_of_bridges_left']))                                               
                                                else:
                                                    print("t:{0} can't be added to temp ".format(t))
                                                    #what_is_vertex() is changed to how_many_left() becuz of (3, 7) of very easy
                                                    print("because of {0}<1+{1} ".format(how_many_left(extract_the_neighbor_coordy_from_t(t, i), islands), temp.count(t)))
                                                    #print("or because of temp_num_of_bridges_left == {0}".format(temp_num_of_bridges_left))
                                                    #print("num_bridges_to_deduct: {0} is about to be added to temp_num_of_bridges_left: {1}".format(num_bridges_to_deduct, temp_num_of_bridges_left))
                                                    #temp_num_of_bridges_left += num_bridges_to_deduct
                                                    
                                                    
                                             
                                        if temp_num_of_bridges_left == 0:
                                            temp.sort()
                                            t = 0
                                            stop = False
                                            #for t_hv_a in temp_hv_answers:
                                            while t < len(temp_hv_answers) and not(stop):
                                                print("{0} ?== {1} and {2} ?== {3}".format(len(temp), len(temp_hv_answers[t]), temp, temp_hv_answers[t]))
                                                if len(temp) == len(temp_hv_answers[t]) and temp == temp_hv_answers[t]:
                                                    stop = True
                                                else:
                                                    t += 1
                                                       
                                            if stop == False and t == len(temp_hv_answers) and len(temp) == islands[i]['num_of_bridges_left']:
                                                print("temp:{0} is appended to temp_hv_answers:{1}".format(temp, temp_hv_answers))
                                                temp_hv_answers.append(temp)
                                                '''
                                                if temp_num_of_bridges_left == 0:
                                                    temp = []
                                                    print("temp is cleaned since temp_num_of_bridges_left == 0")
                                                '''
                                            else:
                                                print("temp:{0} couldn't be appended to temp_hv_answers:{1}".format(temp, temp_hv_answers))
                                                print("since stop == True")
                                                print("or {0} is in {1}".format(temp, temp_hv_answers))
                                                print("or len(temp): {0} !=? islands[i]['num_of_bridges_left']: {1}".format(len(temp), islands[i]['num_of_bridges_left']))
                                            '''
                                            temp_num_of_bridges_left = 2
                                            temp_hv_answer_one, num_bridges_to_deduct = connect_to_neighbor_temporarily(i, j_two, True, temp_h_answer, temp_v_answer, temp_num_of_bridges_left)
                                            temp_num_of_bridges_left -= num_bridges_to_deduct
                                            temp_h_answer = []
                                            temp_v_answer = []
                                            '''                                
                                        if len(islands[i]['neighbors']) - 1 != l and not(third_time):# neighbors_length-1 != l:
                                            l += 1
                                            print("if: l is increased to {0}".format(l))
                                            neighbor_coordinates_index += 1
###############################################################################
                                        elif 0 == l and (third_time) and go_back_only_once_for_third_time:# neighbors_length-1 != l:
                                            l = copy.deepcopy(j)
                                            print("if: l is set to {0}".format(j))
                                            neighbor_coordinates_index = copy.deepcopy(j)
                                            go_back_only_once_for_third_time = False
                                            print("go_back_only_once_for_third_time is set to False")
                                        elif 0 == l and (third_time):# neighbors_length-1 != l:
                                            l = copy.deepcopy(j)
                                            print("elif 0 == l and (third_time):")
                                            print("if: l is set to {0}".format(j))
                                            neighbor_coordinates_index = copy.deepcopy(j)
                                            #go_back_only_once_for_third_time = False
                                            #print("go_back_only_once_for_third_time is set to False")
                                        elif (third_time):# neighbors_length-1 != l:
                                            l -= 1
                                            print("if: l is decreased to {0}".format(l))
                                            neighbor_coordinates_index -= 1
                                        else:#neighbors_length-1 == l
                                            l = 0
                                            neighbor_coordinates_index = 0
                                            
                                        #neighbors_length is replaced with temp_num_of_bridges_left
                                        if not(is_it_done(else_done, temp_num_of_bridges_left, islands[i]['num_of_bridges_left'], len(temp))) and temp_num_of_bridges_left == 0:
                                            print("num_bridges_to_deduct: {0} is added to temp_num_of_bridges_left: {1}".format(num_bridges_to_deduct, temp_num_of_bridges_left))
                                            temp_num_of_bridges_left += num_bridges_to_deduct
                                            
                                            if temp_num_of_bridges_left == 1 and len(temp) == [] :# because of after [(2, 5, 2, 7), (2, 5, 2, 7)], islands[i]['num_of_bridges_left'] != 1:#because of [(8, 9, 10, 9), (10, 7, 10, 9)]    islands[i]['num_of_bridges'] != 1 or 
                                                print("temp_hv_answer_one: {0} is assigned to {1}".format(temp_hv_answer_one, temp))
                                                temp = copy.deepcopy(temp_hv_answer_one)
                                            elif temp_num_of_bridges_left == 1:#this was added bcuz of the 2nd (4, 5) of ultra easy
                                                temp = []
                                                print("temp is cleaned 1")
                                                print("temp_hv_answer_one: {0} is assigned to temp: {1}".format(temp_hv_answer_one, temp))
                                                temp = copy.deepcopy(temp_hv_answer_one)
                                                print("after the assignment, temp is {0}".format(temp))
                                            else:#islands[i]['num_of_bridges'] == 1
                                                temp = []
                                                print("temp is cleaned 2")   
                                            #print("num_bridges_to_deduct: {0} is added to temp_num_of_bridges_left: {1}".format(num_bridges_to_deduct, temp_num_of_bridges_left))
                                            #temp_num_of_bridges_left += num_bridges_to_deduct
##################################################
                                        elif 2 == num_of_lines and temp == [] and (not(is_there_a_neigbor_with_more_than_one_edge_left) or not(go_back_only_once_for_third_time)): # and is_only_else_done(else_done):
                                            temp_num_of_bridges_left = 0
                                            print("temp_num_of_bridges_left is set to 0")
                                        else:
                                            print("what should i do here? step 18 case")
                                            print("temp_hv_answer_one: {0} ".format(temp_hv_answer_one))
                                            print("temp: {0} ".format(temp))
                                            print("temp_num_of_bridges_left = {0}".format(temp_num_of_bridges_left))
                                            
                                            
                                    elif not(third_time) and (l == len(islands[i]['neighbors']) - 1):
                                        l = 0
                                        print("l is reset to 0")
                                    elif not(third_time):
                                        l += 1
                                        print("else: l is increased to {0}".format(l))
                                    elif (third_time) and l == 0 and go_back_only_once_for_third_time:
                                        l = j
                                        print("l is reset to j: {0}".format(j))
                                        go_back_only_once_for_third_time = False
                                        print("go_back_only_once_for_third_time is set to False")
                                    else:
                                        l -= 1
                                        print("else: l is decreased to {0}".format(l)) 
                                           
                                temp = []
                                print("temp is cleaned 3")
                                #temp_hv_answer = []
                                #print("temp_hv_answer is cleaned")    
                                temp_num_of_bridges_left = copy.deepcopy(islands[i]['num_of_bridges_left'])
                        else:#((islands[i]["neighbors"][j_two][0] in neighbor_marked_and_not_blocked) or (islands[i]["neighbors"][j_two][0] in neighbor_blocked)):
                            print("else: else: {0} in {1}?".format(islands[i]["neighbors"][j_two][0], neighbor_marked_and_not_blocked))
                            print("else: else: {0} in {1}?".format(islands[i]["neighbors"][j_two][0], neighbor_blocked))
                            
                        print('temp_hv_answers is {0}'.format(temp_hv_answers))
                        print()
                        j_two_index += 1
                        
                            ################################################################################
                    temp_hv_answer = []
                    print("temp_hv_answer is cleaned")
                            
                    if (j == len(islands[i]['neighbors']) - 1) or (j == neighbors_length - 1):#step 18,    neighbors_length = len(neighbor_bridges):# and l == neighbors_length:
                        connections = []
                        if len(temp_hv_answers) != 0:
                            connections = find_duplicates(temp_hv_answers)
                            
                            if advanced_tech and not(added_a_bridge_once_already) and connections == [] and 1 == len(temp_hv_answers[0]):# and i == advanced_tech_index
                                print("if advanced_tech and not(added_a_bridge_once_already) and connections == [] and 1 == len(temp_hv_answers[0]):")
                                
                                if () == candidate:
                                    candidate, other_candidates = isolating_a_segment_by_adding_a_bridge(i, temp_hv_answers, islands)
                                    candidates.append(copy.deepcopy(candidate))
                                    connections.append( copy.deepcopy( candidate ) )
                                    #now connections is [(1, 1, 3, 1)]
                                    print("now connections is {0}".format(connections))
                                    advanced_tech_index = copy.deepcopy( i )
                                    added_a_bridge_once_already = True
                                    #i have to create advanced_h_answer and advanced_v_answer to keep the current h_answer and v_answer to go back to them when this added bridge is wrong.
                                    advanced_h_answer = copy.deepcopy(h_answer)
                                    advanced_v_answer = copy.deepcopy(v_answer)
                                    advanced_islands = copy.deepcopy(islands)
                                    advanced_marked_coordinates = copy.deepcopy(marked_coordinates)
                                    print("advanced_h_answer and advanced_v_answer are set to be h_answer and v_answer")
                                    print(advanced_h_answer)
                                    print(advanced_v_answer)
                                elif () != candidate and i == advanced_tech_index:#and [] != other_candidates 
                                    print("{0} is removed from temp_hv_answers:{1}".format(candidates, temp_hv_answers))
                                    for c in candidates:
                                        temp_hv_answers.remove( [c] )
                                    
                                    candidate, other_candidates = isolating_a_segment_by_adding_a_bridge(i, temp_hv_answers, islands)
                                    candidates.append(copy.deepcopy(candidate))
                                    connections.append( copy.deepcopy( candidate ) )
                                    
                                    print("now connections is {0}".format(connections))
                                    #advanced_tech_index = copy.deepcopy( i )
                                    #added_a_bridge_once_already = True
                                    #i have to create advanced_h_answer and advanced_v_answer to keep the current h_answer and v_answer to go back to them when this added bridge is wrong.
                                    advanced_h_answer = copy.deepcopy(h_answer)
                                    advanced_v_answer = copy.deepcopy(v_answer)
                                    advanced_islands = copy.deepcopy(islands)
                                    advanced_marked_coordinates = copy.deepcopy(marked_coordinates)
                                    print("advanced_h_answer and advanced_v_answer are set to be h_answer and v_answer")
                                    print(advanced_h_answer)
                                    print(advanced_v_answer)
                                else:#???
                                    print("Let's figure this out!")
                                    print("candidate: {0}".format(candidate))
                                    print("other_candidates: {0}".format(other_candidates))
                                    print("if this is the case added_a_bridge_once_already shouldn't be set to True")
                            else:#if advanced_tech and connections != [] or 1 != len(temp_hv_answers[0]):
                                print("if advanced_tech and connections != [] or 1 != len(temp_hv_answers[0]):")
                        '''
                        target_neighbor_indexes = []
                        #for line in connections:
                        k = 0
                        #line_found = False
                        while k < len(islands[i]["neighbors"]):# and not(line_found):#neighbors_length
                            if not( marked(islands[i]["neighbors"][k][0], islands) ):# == (line[0], line[1]) ) or ( islands[i]["neighbors"][k][0] == (line[2], line[3]) ):
                                target_neighbor_indexes.append(k)
                            else:
                                print("target_neighbor_indexes?")
                            k += 1
                        print("target_neighbor_indexes: {0}".format(target_neighbor_indexes))
                        '''
                        #is_there_isolation(i, target_neighbor_indexes, neighbor_blocked)#temp_num_of_bridges_left, num_bridges_to_deduct, 
                        #[(4, 5, 7, 5), (7, 5, 7, 8)]
                        """  
                        for line in connections:
                            print("the line is {0}".format(line))
                            k = 0
                            line_found = False
                            while k < len(islands[i]["neighbors"]) and not(line_found):#neighbors_length
                                if (islands[i]["neighbors"][k][0] == (line[0], line[1])):
                                    #is_there_isolation_for_else() was commented out because of (7, 5) of ultra easy 
                                    if (0 <= how_many_left((line[0], line[1])) - 1):# and not(is_there_isolation_for_else(i, k, neighbor_blocked, h_answer, v_answer)):# and not(is_this_neighbor_isolation(i, k, neighbor_blocked, h_answer, v_answer)):
                                        connect_to_neighbor_and_mark(i, k, True, h_answer, v_answer, True)
                                        line_found = True
                                    else:
                                        print("if: 0 !<= island[k]['num_of_bridges_left']-1")#islands[i]['num_of_bridges_left']")
                                        k = len(islands)
                                elif (islands[i]["neighbors"][k][0] == (line[2], line[3])):
                                    #is_there_isolation_for_else() was commented out because of (7, 5) of ultra easy 
                                    if (0 <= how_many_left((line[2], line[3])) - 1):# and not(is_there_isolation_for_else(i, k, neighbor_blocked, h_answer, v_answer)):# and not(is_this_neighbor_isolation(i, k, neighbor_blocked, h_answer, v_answer)):
                                        connect_to_neighbor_and_mark(i, k, True, h_answer, v_answer, True)
                                        line_found = True
                                    else:
                                        print("elif: 0 !<= island[k]['num_of_bridges_left']-1")#-islands[i]['num_of_bridges_left']")
                                        k = len(islands)
                                else:
                                    k += 1
                        """            
                        connections, h_answer, v_answer = connect_after_find_duplicates(connections, i, h_answer, v_answer, islands)
                                     
                        target_neighbor_coordies = []
                        neighbor_indexes = []
                        
                        if connections == []:
                            target_neighbor_coordies = extract_the_neighbor_coordies_from_temp_hv_answers(temp_hv_answers, i)
                            
                            if target_neighbor_coordies != []:
                                #remove the duplicates
                                #target_neighbor_coordies = copy.deepcopy(list(set(target_neighbor_coordies)))
                                #target_neighbor_coordies.sort()
                                #print("after set(): {0}".format(target_neighbor_coordies))
                                for cs in target_neighbor_coordies:#[[(2, 3), (2, 7)], [(2, 3), (5, 5)], [(2, 7), (5, 5)], [(2, 7), (2, 7)], [(5, 5), (5, 5)]]
                                    #c = [(2, 3), (2, 7)], ...
                                    temp_indexes = []
                                    for c in cs:
                                        temp = what_is_neighbor_index(c, i)
                                        if  temp not in temp_indexes:
                                            temp_indexes.append(temp)
                                    neighbor_indexes.append(temp_indexes)
                                print("neighbor_indexes: {0}".format(neighbor_indexes))  
                                
                                #if neighbor_indexes != []:
                                #line_w_count_in_list = line_with_count_in_list(temp_hv_answers)
                                ittowwi_result, index_w_no_isolation, isolation_indexes = is_there_the_only_way_without_isolation(i, neighbor_indexes, neighbor_blocked, h_answer, v_answer, neighbor_marked_and_not_blocked, temp_hv_answers, islands)
                                if (ittowwi_result):#checks if (4,6) and (6,4) for (6,6))are isolated or not
                                    #line_w_count_in_list = line_with_count_in_list(temp_hv_answers)
                                    #[(2, 3, 2, 5), (2, 5, 2, 7)]
                                    line_count_in_list = line_with_count_in_list(temp_hv_answers)
                                    for k in neighbor_indexes[index_w_no_isolation]:
                                        if islands[i]['coordinates'][0] < islands[i]['neighbors'][k][0][0]:
                                            if [ islands[i]['coordinates'] + islands[i]['neighbors'][k][0], 2 ] not in line_count_in_list[index_w_no_isolation]:
                                                no_two_bridges = True
                                            else:
                                                no_two_bridges = False
                                        elif islands[i]['coordinates'][0] == islands[i]['neighbors'][k][0][0]:
                                            if islands[i]['coordinates'][1] <= islands[i]['neighbors'][k][0][1]:
                                                if [ islands[i]['coordinates'] + islands[i]['neighbors'][k][0], 2 ] not in line_count_in_list[index_w_no_isolation]:
                                                    no_two_bridges = True
                                                else:
                                                    no_two_bridges = False
                                            else:#islands[i]['coordinates'][1] > islands[i]['neighbors'][k][0][1]:
                                                if [ islands[i]['neighbors'][k][0] + islands[i]['coordinates'], 2] not in line_count_in_list[index_w_no_isolation]:
                                                    no_two_bridges = True
                                                else:
                                                    no_two_bridges = False
                                        else: #islands[i]['coordinates'][0] > islands[i]['neighbors'][k][0][0]:
                                            if [ islands[i]['neighbors'][k][0] + islands[i]['coordinates'], 2] not in line_count_in_list[index_w_no_isolation]:
                                                no_two_bridges = True
                                            else:
                                                no_two_bridges = False
                                                
                                        double_line = True
                                        connect_to_neighbor_and_mark(i, k, no_two_bridges, h_answer, v_answer, double_line, islands)
                                    #connect_to_neighbor_and_mark(index, neighbor_index_inside_neighbors, no_two_bridges, h_answer, v_answer, double_line):
                                    '''
                                    for lines in temp_hv_answers:#[[(2, 3, 2, 5), (2, 5, 2, 7)], [(2, 3, 2, 5), (2, 5, 5, 5)], [(2, 5, 2, 7), (2, 5, 5, 5)], [(2, 5, 2, 7), (2, 5, 2, 7)], [(2, 5, 5, 5), (2, 5, 5, 5)]]
                                        print("for lines in temp_hv_answers: {0}".format(lines))
                                        #(2, 3, 2, 5)
                                        for line in lines:#[(2, 3, 2, 5), (2, 5, 2, 7)]
                                            print("for line in lines: {0}".format(line))
                                            k = 0
                                            line_found = False
                                            while k < len(islands[i]["neighbors"]) and not(line_found):#neighbors_length
                                                if ( islands[i]["neighbors"][k][0] == (line[0], line[1]) ):#checks if (6, 6) and (6, 8) or (8,6) are isolated or not
                                                    if ( 0 <= how_many_left( (line[0], line[1]) )-1) and not(is_this_neighbor_isolation(i, k, neighbor_blocked, h_answer, v_answer, line)):#, line_w_count_in_list)):# and not(is_this_neighbor_isolation(i, k, neighbor_blocked, h_answer, v_answer)):
                                                        connect_to_neighbor_and_mark(i, k, True, h_answer, v_answer, False)
                                                        line_found = True
                                                    else:
                                                        print("if2: 0 !<= island[k]['num_of_bridges_left']-1")#islands[i]['num_of_bridges_left']")
                                                        k = len(islands)
                                                elif ( islands[i]["neighbors"][k][0] == (line[2], line[3]) ):
                                                    if ( 0 <= how_many_left( (line[2], line[3]) )-1) and not(is_this_neighbor_isolation(i, k, neighbor_blocked, h_answer, v_answer, line)):#, line_w_count_in_list)):# and not(is_this_neighbor_isolation(i, k, neighbor_blocked, h_answer, v_answer)):
                                                        connect_to_neighbor_and_mark(i, k, True, h_answer, v_answer, False)
                                                        line_found = True
                                                    else:
                                                        print("elif2: 0 !<= island[k]['num_of_bridges_left']-1")#-islands[i]['num_of_bridges_left']")
                                                        k = len(islands)
                                                else:
                                                    print("islands[i]['neighbors][k][0]={0} != {1}".format(islands[i]["neighbors"][k][0], line))
                                                    k += 1
                                    '''
                                else:
                                    print("there is no one way to be non-isolated", end="")
                                    if 0 != len(isolation_indexes):
                                        print(", but trying to find the duplicates out of non-isolated combinations!")
                                        temp_hv_answers_two=copy.deepcopy(temp_hv_answers)
                                        for ii in isolation_indexes:
                                            temp_hv_answers_two.remove(temp_hv_answers[ii])
                                            
                                        if len(temp_hv_answers_two) != 0:
                                            connections_two = find_duplicates(temp_hv_answers_two)
                                            
                                        connections_two, h_answer, v_answer = connect_after_find_duplicates(connections_two, i, h_answer, v_answer, islands)
                                    else:
                                        print("what is this????????????????????????????????")
                            else:#target_neighbor_coordies == []:
                                print("target_neighbor_coordies is empty")
                        else:
                            print("if connections != []:") 
                               
                    temp_hv_answer_one = []    
                    print("temp_hv_answer_one is cleaned")
                j += 1
                
            else:
                j += 1
            print()    
        #i += 1
            
        temp_hv_answers = []
        print("temp_hv_answers is cleared")
        print(temp_hv_answers)
        
        neighbor_marked_and_not_blocked = []
        print("neighbor_marked_and_not_blocked is cleared")
        print(neighbor_marked_and_not_blocked)
        
        k = 0
        #print("k:{0}".format(k))
        while not(done) and i == len(islands) - 1 and islands[k]['mark'] == True:
            if k == len(islands) - 1:
                done = True
            k += 1
        if i == len(islands) - 1 and not(done):
            i = 0
            print("resetting i")
            h_answer.sort()
            v_answer.sort()
            
            print(h_answer)
            print(v_answer)
            '''
            [(1, 2, 1, 4), (1, 4, 1, 7), (2, 1, 2, 3), (3, 6, 3, 8), (4, 7, 4, 9), (5, 6, 5, 8), (6, 5, 6, 7), (6, 7, 6, 9), (7, 8, 7, 10), (10, 2, 10, 4), (10, 6, 10, 8)]
            [(1, 4, 3, 4), (1, 9, 4, 9), (2, 1, 5, 1), (2, 3, 4, 3), (3, 4, 5, 4), (3, 10, 5, 10), (3, 10, 5, 10), (4, 9, 6, 9), (5, 10, 7, 10), (7, 10, 9, 10)]
            
            [(1, 2, 1, 4), (1, 4, 1, 7), (1, 7, 1, 9), (2, 1, 2, 3), (3, 4, 3, 6), (3, 6, 3, 8), (4, 5, 4, 7), (4, 7, 4, 9), (4, 7, 4, 9), (5, 4, 5, 6), (5, 6, 5, 8), (6, 5, 6, 7), (6, 5, 6, 7), (6, 7, 6, 9), (7, 8, 7, 10), (10, 2, 10, 4), (10, 6, 10, 8)]
            [(1, 4, 3, 4), (1, 9, 4, 9), (2, 1, 5, 1), (2, 3, 4, 3), (3, 4, 5, 4), (3, 10, 5, 10), (3, 10, 5, 10), (4, 9, 6, 9), (4, 9, 6, 9), (5, 10, 7, 10), (7, 10, 9, 10)]
            
            [(1, 2, 1, 4), (1, 4, 1, 7), (1, 7, 1, 9), (2, 1, 2, 3), (3, 4, 3, 6), (3, 6, 3, 8), (4, 5, 4, 7), (4, 5, 4, 7), (4, 7, 4, 9), (4, 7, 4, 9), (5, 4, 5, 6), (5, 6, 5, 8), (6, 5, 6, 7), (6, 5, 6, 7), (6, 7, 6, 9), (7, 6, 7, 8), (7, 8, 7, 10), (9, 3, 9, 5), (10, 2, 10, 4), (10, 6, 10, 8)]
            [(1, 4, 3, 4), (1, 9, 4, 9), (2, 1, 5, 1), (2, 3, 4, 3), (3, 4, 5, 4), (3, 10, 5, 10), (3, 10, 5, 10), (4, 9, 6, 9), (4, 9, 6, 9), (5, 1, 7, 1), (5, 10, 7, 10), (6, 5, 9, 5), (7, 6, 10, 6), (7, 6, 10, 6), (7, 10, 9, 10), (7, 10, 9, 10)]
            
            [(1, 2, 1, 4), (1, 4, 1, 7), (1, 7, 1, 9), (2, 1, 2, 3), (3, 4, 3, 6), (3, 6, 3, 8), (4, 5, 4, 7), (4, 5, 4, 7), (4, 7, 4, 9), (4, 7, 4, 9), (5, 1, 5, 4), (5, 4, 5, 6), (5, 6, 5, 8), (6, 5, 6, 7), (6, 5, 6, 7), (6, 7, 6, 9), (7, 6, 7, 8), (7, 8, 7, 10), (9, 3, 9, 5), (10, 2, 10, 4), (10, 6, 10, 8)]
            [(1, 4, 3, 4), (1, 9, 4, 9), (2, 1, 5, 1), (2, 3, 4, 3), (3, 4, 5, 4), (3, 10, 5, 10), (3, 10, 5, 10), (4, 9, 6, 9), (4, 9, 6, 9), (5, 1, 7, 1), (5, 10, 7, 10), (6, 2, 10, 2), (6, 5, 9, 5), (7, 1, 9, 1), (7, 1, 9, 1), (7, 3, 9, 3), (7, 3, 9, 3), (7, 6, 10, 6), (7, 6, 10, 6), (7, 10, 9, 10), (7, 10, 9, 10)]
            
            
            [(1, 2, 1, 4), (1, 4, 1, 7), (1, 7, 1, 9), (2, 1, 2, 3), (3, 4, 3, 6), (3, 6, 3, 8), (4, 5, 4, 7), (4, 5, 4, 7), (4, 7, 4, 9), (4, 7, 4, 9), (5, 1, 5, 4), (5, 4, 5, 6), (5, 6, 5, 8), (6, 5, 6, 7), (6, 5, 6, 7), (6, 7, 6, 9), (7, 6, 7, 8), (7, 8, 7, 10), (9, 3, 9, 5), (10, 2, 10, 4), (10, 6, 10, 8)]
            [(1, 4, 3, 4), (1, 9, 4, 9), (2, 1, 5, 1), (2, 1, 5, 1), (2, 3, 4, 3), (2, 3, 4, 3), (3, 4, 5, 4), (3, 10, 5, 10), (3, 10, 5, 10), (4, 9, 6, 9), (4, 9, 6, 9), (5, 1, 7, 1), (5, 10, 7, 10), (6, 2, 10, 2), (6, 5, 9, 5), (7, 1, 9, 1), (7, 1, 9, 1), (7, 3, 9, 3), (7, 3, 9, 3), (7, 6, 10, 6), (7, 6, 10, 6), (7, 10, 9, 10), (7, 10, 9, 10)]
            
            [(1, 2, 1, 4), (1, 4, 1, 7), (1, 7, 1, 9), (2, 1, 2, 3), (3, 4, 3, 6), (3, 6, 3, 8), (4, 5, 4, 7), (4, 5, 4, 7), (4, 7, 4, 9), (4, 7, 4, 9), (5, 1, 5, 4), (5, 4, 5, 6), (5, 6, 5, 8), (6, 5, 6, 7), (6, 5, 6, 7), (6, 7, 6, 9), (7, 6, 7, 8), (7, 8, 7, 10), (9, 3, 9, 5), (10, 2, 10, 4), (10, 6, 10, 8)]
            [(1, 4, 3, 4), (1, 9, 4, 9), (2, 1, 5, 1), (2, 1, 5, 1), (2, 3, 4, 3), (2, 3, 4, 3), (3, 4, 5, 4), (3, 10, 5, 10), (3, 10, 5, 10), (4, 9, 6, 9), (4, 9, 6, 9), (5, 1, 7, 1), (5, 10, 7, 10), (6, 2, 10, 2), (6, 5, 9, 5), (7, 1, 9, 1), (7, 1, 9, 1), (7, 3, 9, 3), (7, 3, 9, 3), (7, 6, 10, 6), (7, 6, 10, 6), (7, 10, 9, 10), (7, 10, 9, 10)]


            '''
            if prev_h != h_answer or prev_v != v_answer:
                print("the h_answer difference is {0}".format(list_difference(h_answer, prev_h)))
                print("the v_answer difference is {0}".format(list_difference(v_answer, prev_v)))
                advanced_tech = False
                added_a_bridge_once_already = False
                candidate = ()
                candidates = []
                advanced_tech_index = -1
                other_candidates = []
            else:
                print("they were the same as the previous ones!")
                advanced_tech = True
            
            if advanced_tech != True:   
                prev_h=copy.deepcopy(h_answer)
                prev_v=copy.deepcopy(v_answer)
            else:
                print("advanced_tech == True")
        else:
            i += 1
            h_answer.sort()
            v_answer.sort()
        
    return h_answer, v_answer




sample = [ (1, 1, 2), (1, 4, 3), (1, 6, 3), (1, 9, 2), \
           (2, 3, 2), (2, 5, 2), (2, 7, 4), (2, 10, 2), \
           (3, 1, 2), (3, 9, 2), \
           (4, 4, 1), (4, 6, 1), (4, 10, 2), \
           (5, 1, 3), (5, 3, 6), (5, 5, 3), (5, 7, 3), (5, 9, 4), \
           (6, 4, 1), (6, 6, 4), (6, 8, 2), (6, 10, 3), \
           (7, 3, 4), (7, 5, 2), \
           (8, 1, 3), (8, 4, 1), (8, 6, 2), (8, 9, 1), \
           (9, 3, 2), (9, 5, 3), (9, 8, 3), (9, 10, 2), \
           (10, 1, 3), (10, 4, 2), (10, 7, 3), (10, 9, 2) ]

ultra_easy = [ (1, 1, 2), (1, 3, 2), (1, 5, 5), (1, 7, 2), \
               (2, 6, 1), (2, 8, 3), \
               (3, 1, 6), (3, 3, 3), \
               (4, 2, 2), (4, 5, 6), (4, 7, 1), \
               (5, 1, 3), (5, 3, 1), (5, 6, 2), (5, 8, 6), \
               (6, 2, 2), \
               (7, 1, 1), (7, 3, 3), (7, 5, 5), (7, 8, 3), \
               (8, 2, 2), (8, 4, 3), (8, 7, 2) ]

very_easy = [ (1, 3, 2), (1, 5, 6), (1, 7, 2), (1, 9, 1), \
              (2, 1, 3), (2, 4, 3), \
              (3, 5, 5), (3, 7, 5), (3, 9, 4), \
              (4, 2, 2), (4, 4, 3), (4, 6, 1), \
              (5, 1, 5), (5, 5, 5), (5, 9, 2), \
              (6, 3, 1), (6, 7, 2), \
              (7, 1, 4), (7, 6, 3), (7, 9, 3), \
              (8, 3, 2), (8, 5, 3), (8, 7, 1), \
              (9, 1, 3), (9, 4, 2), (9, 6, 3), (9, 8, 2) ]

easy = [ (1, 2, 2), (1, 5, 4), (1, 7, 5), (1, 10, 2), \
         (2, 4, 1), \
         (3, 1, 2), (3, 5, 4), (3, 7, 5), (3, 9, 1), \
         (4, 2, 3), (4, 4, 5), (4, 6, 1), (4, 8, 2), (4, 10, 3), \
         (5, 1, 4), (5, 3, 3), (5, 5, 2), (5, 7, 3), (5, 9, 4), \
         (6, 4, 2), (6, 6, 3), (6, 8, 2), \
         (7, 1, 4), (7, 3, 8), (7, 5, 3), (7, 10, 3), \
         (8, 6, 2), (8, 9, 2), \
         (9, 1, 1), (9, 5, 2), (9, 8, 3), (9, 10, 3), \
         (10, 3, 3), (10, 7, 2), (10, 9, 1) ]

get_started = [ (1, 1, 2), (1, 3, 4), (1, 5, 3), (1, 7, 4), (1, 9, 2), \
                (2, 4, 1), (2, 6, 3), (2, 8, 3), (2, 10, 3), \
                (3, 1, 4), (3, 3, 8), (3, 5, 2), (3, 7, 1), \
                (4, 4, 2), (4, 6, 6), (4, 8, 3), \
                (5, 1, 3), (5, 3, 5), (5, 5, 2), (5, 7, 2), (5, 10, 4), \
                (6, 2, 2), (6, 4, 5), (6, 6, 4), (6, 8, 2), \
                (7, 1, 3), (7, 3, 3), (7, 5, 1), (7, 10, 3), \
                (8, 4, 3), (8, 6, 2), \
                (9, 3, 1), (9, 5, 2), (9, 8, 4), (9, 10, 3), \
                (10, 1, 2), (10, 4, 4), (10, 6, 3), (10, 9, 2) ]

july_17_easy = [ (1,1,2), (1,5,3), (1,8,3), (1,10,3), (1,14,3), (1,16,1),\
                 (2,3,2), (2,6,2), (2,9,3), (2,12,2),\
                 (3,5,1), (3,11,4), (3,15,2),\
                 (4,1,4), (4,3,3), (4,6,5), (4,8,3), (4,13,3), (4,16,4),\
                 (5,2,3), (5,5,4), (5,7,1),\
                 (6,1,2), (6,3,1), (6,9,5), (6,11,8), (6,13,4), (6,15,1),\
                 (7,2,1), (7,6,2), (7,8,1), (7,12,1), (7,14,2), (7,16,5),\
                 (8,5,2), (8,7,3), (8,9,3),\
                 (9,1,4), (9,3,4), (9,6,4), (9,8,5), (9,11,4), (9,14,3), (9,16,3),\
                 (11,2,2), (11,6,4), (11,8,4), (11,11,2), (11,13,1), (11,16,1),\
                 (12,1,2), (12,4,3), (12,7,3), (12,10,3), (12,12,3), (12,14,3) ]

hashi = [ (1,1,1), (1,3,4), (1,5,2),\
          (2,4,2), (2,6,3),\
          (3,1,4), (3,3,7), (3,5,1),\
          (4,4,2), (4,6,5),\
          (5,3,3), (5,5,1),\
          (6,1,3), (6,4,3), (6,6,3) ]

sudoku_2 = [ (1,1,2), (1,4,3), (1,6,2), (1,8,3), (1,10,3),\
             (2,5,2), (2,7,4), (2,9,1),\
             (3,1,4), (3,3,2),\
             (4,2,1), (4,4,3), (4,6,2), (4,8,2), (4,10,3),\
             (5,1,4), (5,3,3), (5,5,3), (5,7,3), (5,9,1),\
             (6,4,1), (6,6,3), (6,8,1), (6,10,2),\
             (7,2,2), (7,5,2), (7,7,4), (7,9,4),\
             (8,1,2), (8,3,1), (8,10,3),\
             (9,4,3), (9,6,4), (9,9,2),\
             (10,2,3), (10,5,2), (10,7,3), (10,10,3) ]

sudoku_3 = [ (1,1,2), (1,3,4), (1,5,3), (1,7,2), (1,9,3),\
             (2,4,3), (2,6,3), (2,8,2),\
             (3,1,4), (3,3,2), (3,5,1), (3,7,3), (3,10,1),\
             (4,9,2),\
             (5,1,4), (5,4,5), (5,6,3), (5,8,3), (5,10,3),\
             (6,7,3),\
             (7,1,4), (7,3,2), (7,6,1), (7,8,2), (7,10,2),\
             (8,2,1), (8,4,4), (8,7,2), (8,9,1),\
             (9,5,2), (9,8,3), (9,10,1),\
             (10,1,2), (10,4,4), (10,6,3), (10,9,2) ]

sudoku_4 = [ (1,2,1), (1,4,3), (1,7,2), (1,9,2),\
             (2,1,3), (2,3,3),\
             (3,4,3), (3,6,2), (3,8,1), (3,10,2),\
             (4,3,2), (4,5,2), (4,7,4), (4,9,5),\
             (5,1,4), (5,4,3), (5,6,2), (5,8,1), (5,10,3),\
             (6,2,1), (6,5,3), (6,7,3), (6,9,3),\
             (7,1,3), (7,3,3), (7,6,3), (7,8,2), (7,10,4),\
             (9,1,2), (9,3,3), (9,5,2), (9,10,2),\
             (10,2,2), (10,4,3), (10,6,3), (10,8,2) ]

sudoku_5 = [ (1,1,2), (1,3,5), (1,5,4), (1,8,3), (1,10,2),\
             (3,1,2), (3,5,5), (3,7,2), (3,9,1),\
             (4,3,2), (4,6,2), (4,8,3), (4,10,4),\
             (5,1,4), (5,5,4), (5,7,3), (5,9,2),\
             (6,2,2), (6,4,4), (6,8,2), (6,10,4),\
             (7,5,3), (7,7,6), (7,9,1),\
             (8,1,2), (8,4,5), (8,6,2), (8,8,1), (8,10,3),\
             (9,7,3), (9,9,2),\
             (10,2,2), (10,4,4), (10,6,4), (10,8,3), (10,10,3) ]

sudoku_6 = [ (1,1,3), (1,3,3), (1,6,3), (1,8,2), (1,10,3),\
             (2,5,1), (2,7,2), (2,9,3),\
             (3,1,2), (3,6,2), (3,8,2),\
             (4,3,2), (4,5,3), (4,7,2), (4,10,3),\
             (5,1,2), (5,4,1), (5,6,2), (5,9,2),\
             (6,3,2), (6,5,4), (6,7,2),\
             (7,1,3), (7,4,1), (7,8,3), (7,10,3),\
             (8,6,1),\
             (9,1,2), (9,3,3), (9,5,4), (9,7,3), (9,9,1),\
             (10,2,1), (10,4,2), (10,6,3), (10,8,3), (10,10,2) ]

sudoku_7 = [ (1,1,1), (1,3,2), (1,5,4), (1,8,4), (1,10,2),\
             (2,9,1),\
             (3,1,3), (3,4,3), (3,6,2), (3,8,3), (3,10,3),\
             (4,2,1), (4,5,2), (4,7,2), (4,9,3),\
             (5,4,3), (5,6,4), (5,8,3), (5,10,3),\
             (6,1,3), (6,5,1), (6,7,2), (6,9,2),\
             (7,4,1), (7,6,2), (7,8,1), (7,10,3),\
             (8,2,4), (8,5,3), (8,7,3), (8,9,3),\
             (9,1,2), (9,10,2),\
             (10,2,2), (10,4,2), (10,6,3), (10,9,2) ]

sudoku_8 = [ (1,1,2), (1,3,3), (1,5,5), (1,8,4), (1,10,3),\
             (2,2,1), (2,4,2),\
             (3,1,3), (3,3,2), (3,5,3), (3,7,3), (3,9,1),\
             (4,2,2), (4,4,3), (4,6,3), (4,8,2), (4,10,3),\
             (5,1,2), (5,3,3), (5,5,4), (5,7,2),\
             (6,2,3), (6,6,1), (6,9,2),\
             (7,3,1), (7,5,5), (7,7,3),\
             (8,1,2), (8,10,3),\
             (9,2,2), (9,5,4), (9,7,3), (9,9,2),\
             (10,1,1), (10,3,1), (10,6,2), (10,8,2), (10,10,3) ]

sudoku_9 = [ (1,2,2), (1,4,3), (1,7,3), (1,10,3),\
             (2,1,2), (2,3,2), (2,5,4), (2,8,2),\
             (3,6,1), (3,10,3),\
             (4,2,1), (4,5,2),\
             (5,1,3), (5,3,2), (5,6,4), (5,9,3),\
             (6,2,2), (6,5,4),\
             (7,1,4), (7,4,2), (7,6,3), (7,8,1), (7,10,2),\
             (9,1,2), (9,3,2), (9,5,3), (9,7,1), (9,9,2),\
             (10,2,2), (10,4,3), (10,6,4), (10,8,3), (10,10,2) ]

sudoku_10 = [ (1,2,2), (1,5,4), (1,7,3), (1,9,2),\
              (2,1,1), (2,6,3), (2,8,2), (2,10,2),\
              (3,3,2), (3,5,3), (3,7,2), (3,9,1),\
              (4,2,1), (4,4,3), (4,6,3),\
              (5,1,3), (5,3,3), (5,5,1), (5,7,4), (5,10,4),\
              (6,2,1), (6,4,2),\
              (7,1,3), (7,3,2), (7,5,3), (7,7,4), (7,9,3),\
              (8,2,3), (8,4,3), (8,6,2), (8,8,2), (8,10,3),\
              (9,1,3), (9,3,2), (9,5,1), (9,7,1), (9,9,2),\
              (10,2,1), (10,4,2), (10,6,4), (10,8,5), (10,10,3) ] 

inputs=[sample, ultra_easy, very_easy, easy, get_started, july_17_easy, hashi, sudoku_2, sudoku_3, sudoku_4, sudoku_5, sudoku_6, sudoku_7, sudoku_8, sudoku_9, sudoku_10]

#sample
s_h=[(1, 1, 1, 4), (1, 4, 1, 6), (1, 6, 1, 9), (1, 6, 1, 9), (2, 5, 2, 7), (2, 7, 2, 10), (5, 1, 5, 3), (5, 3, 5, 5), (5, 3, 5, 5), (5, 7, 5, 9), (6, 4, 6, 6), (6, 6, 6, 8), (7, 3, 7, 5), (7, 3, 7, 5), (8, 4, 8, 6), (9, 3, 9, 5), (9, 5, 9, 8), (9, 5, 9, 8), (10, 1, 10, 4), (10, 4, 10, 7), (10, 7, 10, 9), (10, 7, 10, 9)]
s_v=[(1, 1, 3, 1), (1, 4, 4, 4), (2, 3, 5, 3), (2, 3, 5, 3), (2, 5, 5, 5), (2, 7, 5, 7), (2, 7, 5, 7), (2, 10, 4, 10), (3, 1, 5, 1), (3, 9, 5, 9), (3, 9, 5, 9), (4, 6, 6, 6), (4, 10, 6, 10), (5, 1, 8, 1), (5, 3, 7, 3), (5, 9, 8, 9), (6, 6, 8, 6), (6, 8, 9, 8), (6, 10, 9, 10), (6, 10, 9, 10), (7, 3, 9, 3), (8, 1, 10, 1), (8, 1, 10, 1)]
#ultra_easy
ue_h=[(1, 3, 1, 5), (1, 5, 1, 7), (1, 5, 1, 7), (2, 6, 2, 8), (3, 1, 3, 3), (3, 1, 3, 3), (4, 2, 4, 5), (4, 5, 4, 7), (5, 6, 5, 8), (5, 6, 5, 8), (7, 3, 7, 5), (7, 3, 7, 5), (7, 5, 7, 8), (8, 2, 8, 4), (8, 4, 8, 7), (8, 4, 8, 7)]
ue_v=[(1, 1, 3, 1), (1, 1, 3, 1), (1, 3, 3, 3), (1, 5, 4, 5), (1, 5, 4, 5), (2, 8, 5, 8), (2, 8, 5, 8), (3, 1, 5, 1), (3, 1, 5, 1), (4, 2, 6, 2), (4, 5, 7, 5), (4, 5, 7, 5), (5, 1, 7, 1), (5, 3, 7, 3), (5, 8, 7, 8), (5, 8, 7, 8), (6, 2, 8, 2)]
#very_easy
ve_h=[(1, 3, 1, 5), (1, 3, 1, 5), (1, 5, 1, 7), (1, 5, 1, 7), (2, 1, 2, 4), (2, 1, 2, 4), (3, 5, 3, 7), (3, 7, 3, 9), (3, 7, 3, 9), (4, 2, 4, 4), (4, 2, 4, 4), (5, 1, 5, 5), (5, 1, 5, 5), (7, 6, 7, 9), (7, 6, 7, 9), (8, 3, 8, 5), (8, 5, 8, 7), (9, 1, 9, 4), (9, 4, 9, 6), (9, 6, 9, 8), (9, 6, 9, 8)]
ve_v=[(1, 5, 3, 5), (1, 5, 3, 5), (1, 9, 3, 9), (2, 1, 5, 1), (2, 4, 4, 4), (3, 5, 5, 5), (3, 5, 5, 5), (3, 7, 6, 7), (3, 7, 6, 7), (3, 9, 5, 9), (4, 6, 7, 6), (5, 1, 7, 1), (5, 1, 7, 1), (5, 5, 8, 5), (5, 9, 7, 9), (6, 3, 8, 3), (7, 1, 9, 1), (7, 1, 9, 1)]
#easy
e_h=[(1, 2, 1, 5), (1, 5, 1, 7), (1, 5, 1, 7), (1, 7, 1, 10), (3, 5, 3, 7), (3, 5, 3, 7), (3, 7, 3, 9), (4, 2, 4, 4), (4, 2, 4, 4), (4, 6, 4, 8), (4, 8, 4, 10), (5, 1, 5, 3), (5, 5, 5, 7), (5, 7, 5, 9), (5, 7, 5, 9), (6, 6, 6, 8), (7, 1, 7, 3), (7, 1, 7, 3), (7, 3, 7, 5), (7, 3, 7, 5), (9, 5, 9, 8), (9, 8, 9, 10), (10, 3, 10, 7), (10, 7, 10, 9)]
e_v=[(1, 2, 4, 2), (1, 5, 3, 5), (1, 7, 3, 7), (1, 7, 3, 7), (1, 10, 4, 10), (2, 4, 4, 4), (3, 1, 5, 1), (3, 1, 5, 1), (3, 5, 5, 5), (4, 4, 6, 4), (4, 4, 6, 4), (4, 10, 7, 10), (5, 1, 7, 1), (5, 3, 7, 3), (5, 3, 7, 3), (5, 9, 8, 9), (5, 9, 8, 9), (6, 6, 8, 6), (6, 6, 8, 6), (6, 8, 9, 8), (7, 1, 9, 1), (7, 3, 10, 3), (7, 3, 10, 3), (7, 5, 9, 5), (7, 10, 9, 10), (7, 10, 9, 10)]
#get_started
gs_h=[(1, 3, 1, 5), (1, 3, 1, 5), (1, 5, 1, 7), (1, 7, 1, 9), (1, 7, 1, 9), (2, 4, 2, 6), (2, 8, 2, 10), (2, 8, 2, 10), (3, 1, 3, 3), (3, 1, 3, 3), (3, 3, 3, 5), (3, 3, 3, 5), (4, 4, 4, 6), (4, 4, 4, 6), (4, 6, 4, 8), (4, 6, 4, 8), (5, 1, 5, 3), (5, 1, 5, 3), (5, 3, 5, 5), (5, 5, 5, 7), (5, 7, 5, 10), (6, 2, 6, 4), (6, 2, 6, 4), (6, 4, 6, 6), (6, 6, 6, 8), (7, 1, 7, 3), (7, 1, 7, 3), (9, 5, 9, 8), (9, 8, 9, 10), (9, 8, 9, 10), (10, 1, 10, 4), (10, 1, 10, 4), (10, 4, 10, 6), (10, 6, 10, 9), (10, 6, 10, 9)]
gs_v=[(1, 1, 3, 1), (1, 1, 3, 1), (1, 3, 3, 3), (1, 3, 3, 3), (1, 7, 3, 7), (2, 6, 4, 6), (2, 6, 4, 6), (2, 8, 4, 8), (2, 10, 5, 10), (3, 3, 5, 3), (3, 3, 5, 3), (5, 1, 7, 1), (5, 10, 7, 10), (5, 10, 7, 10), (6, 4, 8, 4), (6, 4, 8, 4), (6, 6, 8, 6), (6, 6, 8, 6), (6, 8, 9, 8), (7, 3, 9, 3), (7, 5, 9, 5), (7, 10, 9, 10), (8, 4, 10, 4)]
#july_17_easy
j1e_h=[(1, 1, 1, 5), (1, 5, 1, 8), (1, 5, 1, 8), (1, 8, 1, 10), (1, 10, 1, 14), (1, 10, 1, 14), (1, 14, 1, 16), (2, 3, 2, 6), (2, 9, 2, 12), (2, 9, 2, 12), (3, 11, 3, 15), (3, 11, 3, 15), (4, 1, 4, 3), (4, 1, 4, 3), (4, 6, 4, 8), (4, 6, 4, 8), (4, 13, 4, 16), (4, 13, 4, 16), (5, 2, 5, 5), (5, 2, 5, 5), (6, 9, 6, 11), (6, 9, 6, 11), (6, 11, 6, 13), (6, 11, 6, 13), (6, 13, 6, 15), (7, 12, 7, 14), (7, 14, 7, 16), (8, 5, 8, 7), (8, 7, 8, 9), (9, 1, 9, 3), (9, 1, 9, 3), (9, 3, 9, 6), (9, 6, 9, 8), (9, 6, 9, 8), (9, 8, 9, 11), (9, 11, 9, 14), (11, 2, 11, 6), (11, 2, 11, 6), (11, 6, 11, 8), (11, 8, 11, 11), (11, 11, 11, 13), (12, 1, 12, 4), (12, 4, 12, 7), (12, 4, 12, 7), (12, 7, 12, 10), (12, 10, 12, 12), (12, 10, 12, 12), (12, 12, 12, 14)]
j1e_v=[(1, 1, 4, 1), (2, 3, 4, 3), (2, 6, 4, 6), (2, 9, 6, 9), (3, 5, 5, 5), (3, 11, 6, 11), (3, 11, 6, 11), (4, 1, 6, 1), (4, 6, 7, 6), (4, 6, 7, 6), (4, 8, 7, 8), (4, 13, 6, 13), (4, 16, 7, 16), (4, 16, 7, 16), (5, 2, 7, 2), (5, 5, 8, 5), (5, 7, 8, 7), (6, 1, 9, 1), (6, 3, 9, 3), (6, 9, 8, 9), (6, 9, 8, 9), (6, 11, 9, 11), (6, 11, 9, 11), (7, 16, 9, 16), (7, 16, 9, 16), (9, 1, 12, 1), (9, 6, 11, 6), (9, 8, 11, 8), (9, 8, 11, 8), (9, 14, 12, 14), (9, 14, 12, 14), (9, 16, 11, 16)]
#hashi
h_h=[(1, 3, 1, 5), (1, 3, 1, 5), (2, 4, 2, 6), (2, 4, 2, 6), (3, 1, 3, 3), (3, 1, 3, 3), (3, 3, 3, 5), (4, 4, 4, 6), (4, 4, 4, 6), (5, 3, 5, 5), (6, 1, 6, 4), (6, 1, 6, 4), (6, 4, 6, 6)]
h_v=[(1, 1, 3, 1), (1, 3, 3, 3), (1, 3, 3, 3), (2, 6, 4, 6), (3, 1, 6, 1), (3, 3, 5, 3), (3, 3, 5, 3), (4, 6, 6, 6), (4, 6, 6, 6)]
#sudoku_2
s_2_h= [(1, 1, 1, 4), (1, 4, 1, 6), (1, 6, 1, 8), (1, 8, 1, 10), (1, 8, 1, 10), (2, 5, 2, 7), (2, 5, 2, 7), (2, 7, 2, 9), (3, 1, 3, 3), (3, 1, 3, 3), (4, 2, 4, 4), (4, 4, 4, 6), (4, 8, 4, 10), (5, 1, 5, 3), (5, 3, 5, 5), (7, 7, 7, 9), (9, 4, 9, 6), (9, 4, 9, 6), (10, 2, 10, 5), (10, 5, 10, 7), (10, 7, 10, 10)]
s_2_v= [(1, 1, 3, 1), (1, 4, 4, 4), (1, 10, 4, 10), (2, 7, 5, 7), (3, 1, 5, 1), (4, 6, 6, 6), (4, 8, 6, 8), (4, 10, 6, 10), (5, 1, 8, 1), (5, 1, 8, 1), (5, 3, 8, 3), (5, 5, 7, 5), (5, 5, 7, 5), (5, 7, 7, 7), (5, 7, 7, 7), (5, 9, 7, 9), (6, 4, 9, 4), (6, 6, 9, 6), (6, 6, 9, 6), (6, 10, 8, 10), (7, 2, 10, 2), (7, 2, 10, 2), (7, 7, 10, 7), (7, 9, 9, 9), (7, 9, 9, 9), (8, 10, 10, 10), (8, 10, 10, 10)]
#sudoku_3
s_3_h= [(1, 1, 1, 3), (1, 3, 1, 5), (1, 3, 1, 5), (1, 5, 1, 7), (1, 7, 1, 9), (2, 4, 2, 6), (2, 4, 2, 6), (2, 6, 2, 8), (3, 1, 3, 3), (3, 5, 3, 7), (5, 1, 5, 4), (5, 4, 5, 6), (5, 4, 5, 6), (5, 8, 5, 10), (7, 1, 7, 3), (7, 1, 7, 3), (8, 2, 8, 4), (8, 4, 8, 7), (9, 5, 9, 8), (9, 5, 9, 8), (10, 1, 10, 4), (10, 4, 10, 6), (10, 4, 10, 6), (10, 6, 10, 9)]
s_3_v= [(1, 1, 3, 1), (1, 3, 3, 3), (1, 9, 4, 9), (1, 9, 4, 9), (2, 4, 5, 4), (2, 8, 5, 8), (3, 1, 5, 1), (3, 1, 5, 1), (3, 7, 6, 7), (3, 7, 6, 7), (3, 10, 5, 10), (5, 1, 7, 1), (5, 4, 8, 4), (5, 6, 7, 6), (5, 8, 7, 8), (5, 10, 7, 10), (6, 7, 8, 7), (7, 1, 10, 1), (7, 8, 9, 8), (7, 10, 9, 10), (8, 4, 10, 4), (8, 9, 10, 9)]
#sudoku_4
s_4_h= [(1, 2, 1, 4), (1, 4, 1, 7), (1, 7, 1, 9), (2, 1, 2, 3), (3, 4, 3, 6), (3, 6, 3, 8), (4, 5, 4, 7), (4, 5, 4, 7), (4, 7, 4, 9), (4, 7, 4, 9), (5, 1, 5, 4), (5, 4, 5, 6), (5, 6, 5, 8), (6, 2, 6, 5), (6, 5, 6, 7), (6, 5, 6, 7), (6, 7, 6, 9), (7, 1, 7, 3), (7, 3, 7, 6), (7, 3, 7, 6), (7, 8, 7, 10), (9, 1, 9, 3), (9, 3, 9, 5), (9, 3, 9, 5), (10, 2, 10, 4), (10, 2, 10, 4), (10, 4, 10, 6), (10, 6, 10, 8)]
s_4_v= [(1, 4, 3, 4), (1, 9, 4, 9), (2, 1, 5, 1), (2, 1, 5, 1), (2, 3, 4, 3), (2, 3, 4, 3), (3, 4, 5, 4), (3, 10, 5, 10), (3, 10, 5, 10), (4, 9, 6, 9), (4, 9, 6, 9), (5, 1, 7, 1), (5, 10, 7, 10), (7, 1, 9, 1), (7, 6, 10, 6), (7, 8, 10, 8), (7, 10, 9, 10), (7, 10, 9, 10)]
#sudoku_5
s_5_h= [(1, 1, 1, 3), (1, 1, 1, 3), (1, 3, 1, 5), (1, 5, 1, 8), (1, 5, 1, 8), (3, 5, 3, 7), (3, 5, 3, 7), (4, 6, 4, 8), (4, 6, 4, 8), (5, 1, 5, 5), (5, 7, 5, 9), (6, 2, 6, 4), (6, 2, 6, 4), (6, 8, 6, 10), (7, 5, 7, 7), (7, 5, 7, 7), (8, 1, 8, 4), (8, 4, 8, 6), (9, 7, 9, 9), (10, 2, 10, 4), (10, 2, 10, 4), (10, 4, 10, 6), (10, 6, 10, 8), (10, 6, 10, 8), (10, 8, 10, 10)]
s_5_v= [(1, 3, 4, 3), (1, 3, 4, 3), (1, 5, 3, 5), (1, 8, 4, 8), (1, 10, 4, 10), (1, 10, 4, 10), (3, 1, 5, 1), (3, 1, 5, 1), (3, 5, 5, 5), (3, 5, 5, 5), (3, 9, 5, 9), (4, 10, 6, 10), (4, 10, 6, 10), (5, 1, 8, 1), (5, 5, 7, 5), (5, 7, 7, 7), (5, 7, 7, 7), (6, 4, 8, 4), (6, 4, 8, 4), (6, 8, 8, 8), (6, 10, 8, 10), (7, 7, 9, 7), (7, 7, 9, 7), (7, 9, 9, 9), (8, 4, 10, 4), (8, 6, 10, 6), (8, 10, 10, 10), (8, 10, 10, 10)]
#sudoku_6
s_6_h= [(1, 1, 1, 3), (1, 3, 1, 6), (1, 6, 1, 8), (1, 8, 1, 10), (2, 7, 2, 9), (4, 3, 4, 5), (5, 1, 5, 4), (6, 3, 6, 5), (6, 3, 6, 5), (7, 1, 7, 4), (7, 8, 7, 10), (9, 1, 9, 3), (9, 3, 9, 5), (9, 3, 9, 5), (9, 5, 9, 7), (9, 7, 9, 9), (10, 2, 10, 4), (10, 4, 10, 6), (10, 6, 10, 8), (10, 6, 10, 8), (10, 8, 10, 10)]
s_6_v= [(1, 1, 3, 1), (1, 1, 3, 1), (1, 3, 4, 3), (1, 6, 3, 6), (1, 10, 4, 10), (1, 10, 4, 10), (2, 5, 4, 5), (2, 7, 4, 7), (2, 9, 5, 9), (2, 9, 5, 9), (3, 6, 5, 6), (3, 8, 7, 8), (3, 8, 7, 8), (4, 5, 6, 5), (4, 7, 6, 7), (4, 10, 7, 10), (5, 1, 7, 1), (5, 6, 8, 6), (6, 5, 9, 5), (6, 7, 9, 7), (7, 1, 9, 1), (7, 10, 10, 10)]
#sudoku_7
s_7_h= [(1, 1, 1, 3), (1, 3, 1, 5), (1, 5, 1, 8), (1, 5, 1, 8), (1, 8, 1, 10), (3, 1, 3, 4), (3, 1, 3, 4), (3, 6, 3, 8), (3, 6, 3, 8), (4, 5, 4, 7), (4, 7, 4, 9), (5, 4, 5, 6), (5, 6, 5, 8), (5, 6, 5, 8), (8, 2, 8, 5), (8, 2, 8, 5), (8, 7, 8, 9), (10, 2, 10, 4), (10, 4, 10, 6), (10, 6, 10, 9)]
s_7_v= [(1, 5, 4, 5), (1, 8, 3, 8), (1, 10, 3, 10), (2, 9, 4, 9), (3, 1, 6, 1), (3, 4, 5, 4), (3, 10, 5, 10), (3, 10, 5, 10), (4, 2, 8, 2), (4, 9, 6, 9), (5, 4, 7, 4), (5, 6, 7, 6), (5, 8, 7, 8), (5, 10, 7, 10), (6, 1, 9, 1), (6, 1, 9, 1), (6, 5, 8, 5), (6, 7, 8, 7), (6, 7, 8, 7), (6, 9, 8, 9), (7, 6, 10, 6), (7, 10, 9, 10), (7, 10, 9, 10), (8, 2, 10, 2), (8, 9, 10, 9)]
#sudoku_8
s_8_h= [(1, 1, 1, 3), (1, 3, 1, 5), (1, 3, 1, 5), (1, 5, 1, 8), (1, 5, 1, 8), (1, 8, 1, 10), (1, 8, 1, 10), (2, 2, 2, 4), (3, 1, 3, 3), (3, 5, 3, 7), (3, 5, 3, 7), (3, 7, 3, 9), (4, 4, 4, 6), (4, 4, 4, 6), (4, 6, 4, 8), (4, 8, 4, 10), (5, 3, 5, 5), (5, 5, 5, 7), (5, 5, 5, 7), (6, 6, 6, 9), (7, 5, 7, 7), (7, 5, 7, 7), (9, 2, 9, 5), (9, 5, 9, 7), (9, 7, 9, 9), (10, 3, 10, 6), (10, 6, 10, 8), (10, 8, 10, 10)]
s_8_v= [(1, 1, 3, 1), (1, 5, 3, 5), (1, 10, 4, 10), (2, 4, 4, 4), (3, 1, 5, 1), (3, 3, 5, 3), (4, 2, 6, 2), (4, 2, 6, 2), (4, 10, 8, 10), (5, 1, 8, 1), (5, 3, 7, 3), (5, 5, 7, 5), (6, 2, 9, 2), (6, 9, 9, 9), (7, 5, 9, 5), (7, 5, 9, 5), (7, 7, 9, 7), (8, 1, 10, 1), (8, 10, 10, 10), (8, 10, 10, 10)]
#sudoku_9
s_9_h= [(1, 2, 1, 4), (1, 2, 1, 4), (1, 4, 1, 7), (1, 7, 1, 10), (1, 7, 1, 10), (2, 1, 2, 3), (2, 3, 2, 5), (2, 5, 2, 8), (2, 5, 2, 8), (3, 6, 3, 10), (4, 2, 4, 5), (5, 1, 5, 3), (5, 3, 5, 6), (5, 6, 5, 9), (5, 6, 5, 9), (6, 2, 6, 5), (6, 2, 6, 5), (7, 1, 7, 4), (7, 1, 7, 4), (7, 6, 7, 8), (9, 1, 9, 3), (9, 3, 9, 5), (9, 7, 9, 9), (10, 2, 10, 4), (10, 2, 10, 4), (10, 4, 10, 6), (10, 6, 10, 8), (10, 6, 10, 8), (10, 8, 10, 10)]
s_9_v= [(1, 10, 3, 10), (2, 1, 5, 1), (2, 5, 4, 5), (3, 10, 7, 10), (5, 1, 7, 1), (5, 6, 7, 6), (5, 9, 9, 9), (6, 5, 9, 5), (6, 5, 9, 5), (7, 1, 9, 1), (7, 6, 10, 6), (7, 10, 10, 10)]
#sudoku_10
s_10_h= [(1, 2, 1, 5), (1, 5, 1, 7), (1, 7, 1, 9), (1, 7, 1, 9), (2, 6, 2, 8), (2, 8, 2, 10), (3, 3, 3, 5), (3, 7, 3, 9), (4, 4, 4, 6), (5, 1, 5, 3), (5, 7, 5, 10), (5, 7, 5, 10), (7, 3, 7, 5), (7, 5, 7, 7), (7, 7, 7, 9), (8, 2, 8, 4), (8, 2, 8, 4), (8, 4, 8, 6), (9, 1, 9, 3), (9, 3, 9, 5), (10, 2, 10, 4), (10, 4, 10, 6), (10, 6, 10, 8), (10, 6, 10, 8), (10, 8, 10, 10)]
s_10_v= [(1, 2, 4, 2), (1, 5, 3, 5), (1, 5, 3, 5), (2, 1, 5, 1), (2, 6, 4, 6), (2, 6, 4, 6), (2, 10, 5, 10), (3, 3, 5, 3), (3, 7, 5, 7), (4, 4, 6, 4), (4, 4, 6, 4), (5, 1, 7, 1), (5, 3, 7, 3), (5, 5, 7, 5), (5, 7, 7, 7), (5, 10, 8, 10), (6, 2, 8, 2), (7, 1, 9, 1), (7, 1, 9, 1), (7, 7, 9, 7), (7, 9, 9, 9), (7, 9, 9, 9), (8, 6, 10, 6), (8, 8, 10, 8), (8, 8, 10, 8), (8, 10, 10, 10), (8, 10, 10, 10)]

#g_index=0
'''
for i in inputs:
#while g_index < len(inputs):
    #print("inputs[g_index]={0}".format(inputs[g_index]))
    print(i)
    islands = []
    marked_coordinates = []  
    h_answer, v_answer = hashi_puzzle_solver(copy.deepcopy(i), islands, marked_coordinates)
    #print("inputs[g_index]={0}".format(inputs[g_index]))
    print(h_answer)
    print(v_answer)
    print(i)
    if i==sample:
        if s_h==h_answer and s_v==v_answer:
            print("correct sample")
        else:
            print("incorrect sample")
        islands = []
    elif i==ultra_easy:
        if ue_h==h_answer and ue_v==v_answer:
            print("correct ultra-easy")
        else:
            print("incorrect ultra-easy")
        islands = []    
    elif i==very_easy:
        if ve_h==h_answer and ve_v==v_answer:
            print("correct very-easy")
        else:
            print("incorrect very-easy")
        islands = []
    elif i==easy:
        if e_h==h_answer and e_v==v_answer:
            print("correct easy")
        else:
            print("incorrect easy")
        islands = []
    elif i==get_started:
        if gs_h==h_answer and gs_v==v_answer:
            print("correct get_started")
        else:
            print("incorrect get_started")
        islands = []
    elif i==july_17_easy:
        if j1e_h==h_answer and j1e_v==v_answer:
            print("correct july_17_easy")
        else:
            print("incorrect july_17_easy")
        islands = []
    elif i==hashi:
        if h_h==h_answer and h_v==v_answer:
            print("correct hashi")
        else:
            print("incorrect hashi")
        islands = []
    elif i==sudoku_2:
        if s_2_h==h_answer and s_2_v==v_answer:
            print("correct sudoku_2")
        else:
            print("incorrect sudoku_2")
        islands = []
    elif i==sudoku_3:
        if s_3_h==h_answer and s_3_v==v_answer:
            print("correct sudoku_3")
        else:
            print("incorrect sudoku_3")
        islands = []
    elif i==sudoku_4:
        if s_4_h==h_answer and s_4_v==v_answer:
            print("correct sudoku_4")
        else:
            print("incorrect sudoku_4")
        islands = []
    elif i==sudoku_5:
        if s_5_h==h_answer and s_5_v==v_answer:
            print("correct sudoku_5")
        else:
            print("incorrect sudoku_5")
        islands = []
    elif i==sudoku_6:
        if s_6_h==h_answer and s_6_v==v_answer:
            print("correct sudoku_6")
        else:
            print("incorrect sudoku_6")
        islands = []
    elif i==sudoku_7:
        if s_7_h==h_answer and s_7_v==v_answer:
            print("correct sudoku_7")
        else:
            print("incorrect sudoku_7")
        islands = []
    elif i==sudoku_8:
        if s_8_h==h_answer and s_8_v==v_answer:
            print("correct sudoku_8")
        else:
            print("incorrect sudoku_8")
        islands = []
    elif i==sudoku_9:
        if s_9_h==h_answer and s_9_v==v_answer:
            print("correct sudoku_9")
        else:
            print("incorrect sudoku_9")
        islands = []
    elif i==sudoku_10:
        if s_10_h==h_answer and s_10_v==v_answer:
            print("correct sudoku_10")
        else:
            print("incorrect sudoku_10")
        islands = []
    #g_index += 1      
'''
#inputs=[sample, ultra_easy, very_easy, easy, get_started, july_17_easy]
islands = []
marked_coordinates = []  
h_answer, v_answer = hashi_puzzle_solver(sudoku_10, islands, marked_coordinates)            
print("horizontal line:\n {0}".format(h_answer))
print("vertical line:\n {0}".format(v_answer))
if s_10_h==h_answer and s_10_v==v_answer:
    print("correct sample")
else:
    print("incorrect sample")