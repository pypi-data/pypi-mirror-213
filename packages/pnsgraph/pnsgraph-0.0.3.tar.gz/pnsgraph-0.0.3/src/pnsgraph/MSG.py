# process in form of [([I1, I2...],[O1, O2...])...]
def materialsAsOutput(process, materials):
    return [i for i in process for j in materials if j in i[1]]


def materialsAsInput(process, materials):
    return [i for i in process for j in materials if j in i[0]]


def inputMaterials(process):
    return list({j for i in process for j in i[0]})


def outputMaterials(process):
    return list({j for i in process for j in i[1]})


def listMaterial(process):
    return list(set(inputMaterials(process)) | set(outputMaterials(process)))


# setP returns as set of operating units as tuples with tuple input and output sets
def setP(process):
    return {(tuple(i[0]), tuple(i[1])) for i in process}


# listP returns input and output sets for each operating unit as list and the return value is a list
def listP(process):
    return [(list(i[0]), list(i[1])) for i in process]


def MSG(process, product, raw_materials):
    operating_units = []
    produce_raw_material = materialsAsOutput(process, raw_materials)
    process = list(setP(process) - setP(produce_raw_material))
    materials = listMaterial(process)
    non_declared_raw_materials = list(set(inputMaterials(process))
                                      - (set(raw_materials) | set(outputMaterials(process))))
    while non_declared_raw_materials:
        for i in non_declared_raw_materials:
            materials = list(set(materials) - {i})
            produce_i = materialsAsInput(listP(process), [i])
            process = list(setP(process) - setP(produce_i))
            non_declared_raw_materials = list((set(non_declared_raw_materials) |
                                               (set(inputMaterials(produce_i)) - set(outputMaterials(process)))) - {i})
    if set(materials) | set(product) != set(materials):
        print("No Maximal Structure")
    else:
        materials = []
        while product:
            for i in product:
                materials = list(set(materials) | {i})
                consume_i = materialsAsOutput(process, [i])
                operating_units = list(setP(operating_units) | setP(consume_i))
                product = list((set(inputMaterials(consume_i)) | set(product)) - (set(raw_materials) | set(materials)))
    maximal_structure = listP(operating_units)
    return maximal_structure


def searchNameUnit(process, processUnit):
    return [j for i in process for j in processUnit if i == j.unitFlow]
