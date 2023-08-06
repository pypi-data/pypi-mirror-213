import MSG
import SSG


class MaterialNode:
    def __init__(self, name, price=0.0, demand_upper=1e12, demand_lower=0.0):
        self.name = name
        self.price = price
        self.demand_upper = demand_upper
        self.demand_lower = demand_lower
        self.nodetype = "Material"

    def __repr__(self):
        return self.name


class ProductNode(MaterialNode):
    def __init__(self, name, price=0, demand_upper=1e12, demand_lower=0):
        super().__init__(name, price, demand_upper, demand_lower)
        self.nodetype = "Product"


class RawMaterialNode(MaterialNode):
    def __init__(self, name, price=0, demand_upper=0, demand_lower=-1e12):
        super().__init__(name, price, demand_upper, demand_lower)
        self.nodetype = "Raw Material"


class IntermediateNode(MaterialNode):
    def __init__(self, name, price=0, demand_upper=0, demand_lower=0):
        super().__init__(name, price, demand_upper, demand_lower)
        self.nodetype = "Intermediate"


class OperatingUnit:
    def __init__(self, name, input_streams: list, output: list):
        self.name = name
        self.input = input_streams
        self.output = output
        self.unitFlow = (self.input, self.output)

    def __repr__(self):
        return self.name


class OperatingUnitEdged:
    def __init__(self, name, input_flow: dict, output_flow: dict,
                 fixed_cap_cost=0, var_cap_cost=0,
                 fixed_om=0, var_om=0,
                 lifetime=25):
        self.name = name
        self.in_edge = input_flow
        self.out_edge = output_flow
        self.input = input_flow.keys()
        self.output = output_flow.keys()
        self.unitFlow = (tuple(self.input), tuple(self.output))
        self.fixed_cap_cost = fixed_cap_cost
        self.var_cap_cost = var_cap_cost
        self.fixed_OM = fixed_om
        self.var_OM = var_om
        self.lifetime = lifetime

    def __repr__(self):
        return self.name


class OtherData:
    def __init__(self, interest_rate=0.10, hours_per_year=8000, af=0.10):
        self.interest_rate = interest_rate
        self.hours_per_year = hours_per_year
        self.AF = af


class GraphEdge:
    def __init__(self, from_node, to_node, value=0):
        self.name = from_node.name + ' to ' + to_node.name
        self.value = value

    def __repr__(self):
        return self.name


class PNSproblem:
    def __init__(self, products, rawmaterials, otherdata, name="P-graph Problem"):
        self.name = name
        self.units = []
        self.optimal_solutions = []
        self.products = products
        self.rawmaterial = rawmaterials
        self.otherdata = otherdata
        self.MSGStructure = []
        self.SSGsolutions = []
        self.edges = []

    def __iadd__(self, other):
        if isinstance(other, OperatingUnitEdged):
            self.units.append(other)
        return self

    def generateEdges(self, edgeclass):
        for i in self.units:
            for j in i.in_edge:
                self.edges.append(edgeclass(j, i, value=i.in_edge[j]))
            for j in i.out_edge:
                self.edges.append(edgeclass(i, j, value=i.out_edge[j]))
        return self.edges

    def runMSG(self):
        self.MSGStructure = MSG.MSG(operunitstoprocess(self.units), self.products, self.rawmaterial)
        return self

    def runSSG(self):
        self.runMSG()
        structures = SSG.SSG(operunitstoprocess(self.units), self.products, self.rawmaterial)
        self.SSGsolutions = SSG.SSG_translate(structures, self.units)
        return self

    def runSSGLP(self):
        self.optimal_solutions = SSG.SSGplusLP(self.units, self.products, self.rawmaterial, self.otherdata)


def operunitstoprocess(operating_units_list: list):
    process = []
    for i in operating_units_list:
        unit_node = (tuple(j for j in i.input), tuple(j for j in i.output))
        process.append(unit_node)
    return set(process)


def processUnits(*argv):
    return [arg for arg in argv]


def extractMaterials(process):
    inputs = []
    outputs = []
    process = [process[i].unitFlow for i in range(len(process))]
    for i in range(len(process)):
        for j in range(len(process[i][0])):
            if process[i][0][j] not in inputs:
                inputs.append(process[i][0][j])
        for j in range(len(process[i][1])):
            if process[i][1][j] not in outputs:
                outputs.append(process[i][1][j])
    return [inputs, outputs]


def classify(process):
    materials = extractMaterials(process)
    products = []
    intermediates = []
    raw_materials = []
    for i in range(len(materials[1])):
        if materials[1][i] not in materials[0]:
            products.append(materials[1][i])
        else:
            intermediates.append(materials[1][i])
    for i in range(len(materials[0])):
        if materials[0][i] not in materials[1]:
            raw_materials.append(materials[0][i])
    return products, intermediates, raw_materials


def specifyMaterial(process):
    material_list = classify(process)
    raw_materials = []
    products = []
    for i in material_list[0]:
        raw_mats = RawMaterialNode(i)
        raw_materials.append(raw_mats)
    for j in material_list[1]:
        product = ProductNode(j)
        products.append(product)
    return raw_materials, products


# The ones that can be bought consumed and produced must be specified explicitly. The rest can be classified
'''
def getProducts(process):
    product_list =[]
    products = classify(process)[0]
    for i in range(len(products)):
        product_list.append(productNode(products[i]))
    return product_list
'''


def getRawMaterials(process):
    raw_materials_list = []
    raw_materials = classify(process)[2]
    for i in range(len(raw_materials)):
        raw_materials_list.append(RawMaterialNode(raw_materials[i]))
    return raw_materials_list


def getIntermediates(process):
    intermediates_list = []
    intermediates = classify(process)[1]
    for i in range(len(intermediates)):
        intermediates_list.append(IntermediateNode(intermediates[i]))
    return intermediates_list
