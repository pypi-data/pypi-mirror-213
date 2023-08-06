import MSG
import pgraph as nd
from pulp import *
from itertools import chain, combinations

def maximalMappingver2(process):
    maximal_map = {}
    materials = MSG.listMaterial(process)
    for i in materials:
        maximal_map[i] = []
        for j in MSG.setP(process):
            if i in j[1]:
                maximal_map[i].append(j)
        maximal_map[i] = set(maximal_map[i])
    return maximal_map

def maximalMappingMaterial(process, x):
    max_map = maximalMappingver2(process)
    if x in max_map:
        return max_map[x]
        #return {x: max_map[x]}
    else:
        #return set()
        return set()

def complementMapver2(process, mapping:dict, x):
    if x in mapping:
        complement = set(maximalMappingMaterial(MSG.setP(process), x)) - mapping[x]
    else:
        complement = set(maximalMappingMaterial(MSG.setP(process), x))
    return {x: complement}

def powerSetNoEmpty(set):
    s = list(set)
    power_set = list(chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1)))
    # power_set = list(filter(None, power_set))
    return power_set

def SSGbranchCondition(unit, material_set:list, process, mapping:dict, product):
    to_extend = False
    #print("Unit: ", unit)
    #print("Material List: ", material_set)
    #print("Product: ", product)
    #print("Mapping: ", mapping)
    #print("To extend value: ", to_extend)
    for material in material_set:
        first_con = set(unit) & set(complementMapver2(process, mapping, material)[material])
        second_con_1 = set(maximalMappingMaterial(process, product)) - set(unit)
        second_con_2 = set(mapping.get(material, []))
        second_con = second_con_1 & second_con_2
        extend = bool(first_con) | bool(second_con)
        to_extend = to_extend | extend
        #print("Set Unit: ", set(unit))
        #print("Set comp\u03B4: ", complementMapver2(process, mapping, material)[material])
        #print("First Condition: ", first_con, bool(first_con))
        #print("Second Condition (1) :", second_con_1)
        #print("Second Condition (2) :", second_con_2)
        #print("Second Condition: ", second_con, bool(second_con))
        #print("To continue? ", not to_extend)
    return to_extend

#x = product, m = material_list, c = unit, R = raw_materials, delta = mapping
def mappingUpdate(material_list, product, product_list, unit, raw_materials, mapping):
    material_set = set(material_list) | set([product])
    product_set = (set(product_list) | set(MSG.inputMaterials(unit))) - (set(raw_materials) | set(material_list) | set([product]))
    mapping_new = mapping.copy()
    mapping_new[product] = set(unit)
    #print("New Material Set: ", material_set)
    #print("New Product Set: ", product_set)
    #print("New Mapping: ", mapping_new)
    return product_set, list(material_set), mapping_new

def SSG_nb_condition(mapping, unit, process_list):
    solution = set.union(*list(mapping.values()))
    units_in_solution_structure = [j for k in solution for j in process_list if k == j.unitFlow]
    input_mats = MSG.inputMaterials(units_in_solution_structure)
    new_input = MSG.inputMaterials(list(unit))
    if set(input_mats) & set(new_input):
        return False
    else:
        return True

def SSG(process, product:list, raw_materials):
    process = MSG.setP(process)
    mats = []
    maps = {}
    solution_structure =[]
    if not product:
        print('No products declared. No solution structure generated')
    def solnGenerator(product_set, material_set, mapping):
        #print("To SSG: ", product_set, material_set, mapping)
        if not product_set:
            solution_structure.append(mapping)
            return
        x = list(product_set)[0]
        Unit_x_combination = powerSetNoEmpty(maximalMappingMaterial(process, x))
        mapping_copy = mapping.copy()
        for y in Unit_x_combination:
            #print("Unit: " , y)
            if not SSGbranchCondition(y, material_set, process, mapping_copy, x):
                input_SG = mappingUpdate(material_set, x, product_set, y, raw_materials, mapping_copy)
                solnGenerator(*input_SG)
    solnGenerator(product, mats, maps)
    return solution_structure


def SSG_nb(process, product:list, raw_materials):
    process = MSG.setP(process)
    mats = []
    maps = {}
    solution_structure = []
    def solnGenerator(product_set, material_set, mapping):
        #print("To SSG: ", product_set, material_set, mapping)
        if not product_set:
            solution_structure.append(mapping)
            return
        x = list(product_set)[0]
        Unit_x_combination = powerSetNoEmpty(maximalMappingMaterial(process, x))
        mapping_copy = mapping.copy()
        for y in Unit_x_combination:
            #print("Unit: " , y)
            if not SSGbranchCondition(y, material_set, process, mapping_copy, x):
                if SSG_nb_condition(mapping_copy, y, process):
                    input_SG = mappingUpdate(material_set, x, product_set, y, raw_materials, mapping_copy)
                    solnGenerator(*input_SG)
    solnGenerator(product, mats, maps)
    return solution_structure

def SSG_translate(solution_structure, process_list):
    solution_structure_list = []
    for i in solution_structure:
        solution = set.union(*list(i.values()))
        units_in_solution_structure = [j for k in solution for j in process_list if k == j.unitFlow]
        solution_structure_list.append(units_in_solution_structure)
    return solution_structure_list

def ListMaterialsfromOperatingUnit(process):
    input_list = {j for i in process for j in list(i.input)}
    output_list = {j for i in process for j in list(i.output)}
    return list(input_list | output_list)

def ListInputsfromOperatingUnits(process):
    return list({j for i in process for j in list(i.input)})

def ListOutputsfromOperatingUnits(process):
    return list({j for i in process for j in list(i.output)})

def generate_process_matrix(process):
    material_list = ListMaterialsfromOperatingUnit(process)
    process_matrix ={}
    for i in process:
        for j in material_list:
            if j in i.input:
                process_matrix[(j,i)]= -i.in_edge[j]
            elif j in i.output:
                process_matrix[(j,i)]= i.out_edge[j]
            else:
                process_matrix[(j,i)]= 0
    return process_matrix

def optimize_structure(process, econ):
    streams = ListMaterialsfromOperatingUnit(process)
    prob = LpProblem(name='Process_Design', sense=LpMaximize)
    scale_up = LpVariable.dicts("Process_Scale", process, 0, None)
    #decision_var = LpVariable.dicts("Process_choice",  process, 0, None, LpBinary)
    demand_satisfied = LpVariable.dicts('Final_Output', streams, None, None)
    prices = {i:i.price for i in streams}
    fixed_costs = {i: i.fixed_cap_cost + i.fixed_OM for i in process}
    var_costs = {i: i.var_cap_cost + i.var_OM for i in process}
    process_matrix = generate_process_matrix(process)
    demand_lower_bound = {i:i.demand_lower for i in streams}
    demand_upper_bound = {i:i.demand_upper for i in streams}
    annual_factor = econ.AF
    flow_conversion = econ.hours_per_year

    prob += (flow_conversion * lpSum([prices[i] * demand_satisfied[i] for i in streams]) -
             #annual_factor * lpSum([fixed_costs[j] + decision_var[j] + var_costs[j] * scale_up[j] for j in process]))
             annual_factor * lpSum([fixed_costs[j] + var_costs[j] * scale_up[j] for j in process]))
    for i in streams:
        prob += (
            lpSum([process_matrix[(i, j)] * scale_up[j] for j in process]) == demand_satisfied[i],
            'Total_Input_Output_of_Stream_' + i.name,
        )
    for i in streams:
        prob += (
                demand_satisfied[i] <= demand_upper_bound[i]
        )
    for i in streams:
        prob += (
                demand_satisfied[i] >= demand_lower_bound[i]
        )
    prob.solve(GLPK_CMD(msg=0))
    if LpStatus[prob.status] == 'Optimal':
        return {i: scale_up[i].varValue for i in process}, {i:demand_satisfied[i].varValue for i in streams}, prob.objective.value(), [i for i in process]
    else:
    #elif prob.status == -1:
        return -1

def SSGplusLP(process:list, product:list, raw_materials:list, econ):
    solution_structures = SSG(nd.operunitstoprocess(process), product, raw_materials)
    condensed_solution_structure = SSG_translate(solution_structures, process)
    optimal_solutions = {}
    count = 1
    for i in condensed_solution_structure:
        optimal = optimize_structure(i, econ)
        if optimal != -1:
            if all(list(optimal[0].values())):
                optimal_solutions['Solution '+ str(count)] = optimal
                count += 1
    count = 1
    return optimal_solutions