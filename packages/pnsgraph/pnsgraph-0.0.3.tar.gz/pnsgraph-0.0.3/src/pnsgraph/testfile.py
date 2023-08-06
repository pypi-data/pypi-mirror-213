import pgraph as pg

steam = pg.ProductNode("Steam", price=40.0, demand_upper=23.0, demand_lower=18.0)
electricity = pg.ProductNode("Electricity", price =90.0, demand_upper=10.0, demand_lower=8.0)
cooling = pg.ProductNode("Cooling", price=40, demand_upper=9.0, demand_lower=7.5)
chilled_water = pg.ProductNode("Chilled Water", price=50, demand_upper=3.5, demand_lower=1.5)
hot_water = pg.ProductNode("Hot Water", price=30, demand_upper=2.5, demand_lower=1.0)
natural_gas = pg.RawMaterialNode("Natural Gas", price=30)

products = [steam, electricity, cooling, chilled_water, hot_water]
raw_materials = [natural_gas]
other_data = pg.OtherData(af=0.13)

polygen = pg.PNSproblem(products, raw_materials, other_data, name="Polygeneration Case Study")
polygen += pg.OperatingUnitEdged("Steam Boiler", {natural_gas:1.18, }, {steam:1, }, var_cap_cost=0.07, fixed_cap_cost=0.036)
polygen += pg.OperatingUnitEdged("Hot Water Boiler", {natural_gas:1.22, }, {hot_water:1, }, var_cap_cost=0.08, fixed_cap_cost=0.03677)
polygen += pg.OperatingUnitEdged("Gas Turbine", {natural_gas:3.03}, {steam:0.59, electricity:1, hot_water:0.66}, var_cap_cost=2.00, fixed_cap_cost=1.00)
polygen += pg.OperatingUnitEdged("Gas Engine", {natural_gas:1.18}, {steam:0.7, electricity:1, hot_water:0.41, cooling:0.23}, var_cap_cost=1.65, fixed_cap_cost=1.0333)
polygen += pg.OperatingUnitEdged("Steam-Hot Water HX", {steam:1, }, {hot_water:1, }, var_cap_cost=0.0045, fixed_cap_cost=0.003)
polygen += pg.OperatingUnitEdged("Hot Water-Cooling HX", {hot_water:1, }, {cooling:1, }, var_cap_cost=0.0022, fixed_cap_cost=0.003017)
polygen += pg.OperatingUnitEdged("Absorption Chiller", {electricity:0.01, hot_water:1.36}, {cooling:2.36, chilled_water:1}, var_cap_cost=0.05, fixed_cap_cost=0.10333)
polygen += pg.OperatingUnitEdged("Mechanical Chiller", {electricity:0.17}, {cooling:1.17, chilled_water:1}, var_cap_cost=0.10, fixed_cap_cost=0.15833)
polygen += pg.OperatingUnitEdged("Cooling Tower", {electricity:0.1}, {cooling:1}, var_cap_cost=0.030, fixed_cap_cost=0.0305)

polygen.generateEdges(pg.GraphEdge)







