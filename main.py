# Import necessary libraries
import sys
import math
import networkx as nx
import matplotlib.pyplot as plt
import json

raw_components = [
    "Iron Ore",
    "Copper Ore",
    "Coal",
    "Stone",
    "Crude Oil",
    "Silicon Ore",
    "Titanium Ore",
    "Water",
    "Fire Ice",
    "Kimberlite Ore",
    "Fractal Silicon",
    "Optical Grating Crystal",
    "Spiniform Stalagmite Crystal",
    "Unipolar Magnet",
    "Hydrogen",  # Extracted from Water and Crude Oil
    "Deuterium",  # Rare isotope of Hydrogen, extracted or refined
    "Sulfuric Acid"  # Produced from refined materials
]

recipes_II = {
    "Iron Ingot": {
        "inputs": {
            "Iron Ore": 1
        },
        "output": 1,
        "facility": "Smelter",
        "time": 1  # in seconds
    },
    "Copper Ingot": {
        "inputs": {
            "Copper Ore": 1  
        },
        "output": 1,
        "facility": "Smelter",
        "time": 1  # in seconds
    },
    "Stone Brick": {
        "inputs": {
            "Stone": 1
        },
        "output": 1,
        "facility": "Smelter",
        "time": 1  # in seconds
    },
    "Magnum Ammo Box": {
        "inputs": {
            "Copper Ingot": 4
        },
        "output": 1,
        "facility": "Assembler",
        "time": 1  # in seconds
    },
    "Energetic Graphite": {
        "inputs": {
            "Coal": 2
        },
        "output": 1,
        "facility": "Smelter",
        "time": 2  # in seconds
    },
    "Plasma Refining": {
        "inputs": { 
            "Crude Oil": 2
        },
        "output": 1,
        "facility": "Refining Facility",
        "time": 4  # in seconds
    },
}

recipes_III = {
    "Magnet": {
        "inputs": {
            "Iron Ore": 1
        },
        "output": 1,
        "facility": "Smelter",
        "time": 1.5  # in seconds
    },
    "Magnetic Coil": {
        "inputs": {
            "Magnet": 2,
            "Copper Ingot": 1
        },
        "output": 2,
        "facility": "Assembler",
        "time": 1  # in seconds
    },
    "Glass": {
        "inputs": {
            "Stone": 2
        },
        "output": {"quantity": 1},
        "facility": "Smelter",
        "time": 2  # in seconds
    },
}

recipes_IV = {
    "Circuit Board": {
        "inputs": {
            "Iron Ingot": 2,
            "Copper Ingot": 1
        },
        "output": 2,
        "facility": "Assembler",
        "time": 1
    },
    "Assembling Machine Mk.I": {
        "inputs": {
            "Iron Ingot": 4,
            "Gear": 8,
            "Circuit Board": 4
        },
        "output": 1,
        "facility": "Assembler",
        "time": 2
    },
}

recipes_V = {
    "Gear": {
        "inputs": [
            {"material": "Iron Ingot", "quantity": 1},
        ],
        "output": {"quantity": 1},
        "facility": "Assembler",
        "time": 1
    },
    "Electromagnetic Turbine": {
        "inputs": [
            {"material": "Iron Ingot", "quantity": 1},
            {"material": "Iron Ingot", "quantity": 1},a
        ],
        "output": {"quantity": 1},
        "facility": "Assembler",
        "time": 2
    },
}

recipes_matrix = {
    "Electromagnetic Matrix": {
        "inputs": [
            {"material": "Magnetic Coil", "quantity": 1},
            {"material": "Circuit Board", "quantity": 1},
        ],
        "output": {"quantity": 1},
        "facility": "Research Facility",
        "time": 3
    },
    "Energy Matrix": {
        "inputs": [
            {"material": "Plasma Refining", "quantity": 2},
            {"material": "Energetic Graphite", "quantity": 2},
        ],
        "output": {"quantity": 1},
        "facility": "Research Facility",
        "time": 6
    },
}

recipes = recipes_II | recipes_III | recipes_IV | recipes_V | recipes_matrix



def simplify_recipe(product):
    # Base case: if the product is a raw component, return it
    if product in raw_components:
        return {product: 1}
    
    recipe = recipes.get(product)
    if not recipe:
        return {} 
    
    simplified_recipe = {}
    for input_item in recipe["inputs"]:
        material = input_item["material"]
        quantity = input_item["quantity"]

        if material in raw_components:
            simplified_recipe[material] = simplified_recipe.get(material, 0) + quantity
        else:
            sub_recipe = simplify_recipe(material)
            for sub_material, sub_quantity in sub_recipe.items():
                total_quantity = sub_quantity * quantity
                simplified_recipe[sub_material] = simplified_recipe.get(sub_material, 0) + total_quantity

    return simplified_recipe

def simplify_all():
    for key,_ in recipes.items():
        recipes[key] = sorted(simplify_recipe(key))

def get_factory_details(product, rate=1):
    # Check if product is in recipes
    if product not in recipes:
        return None
    
    recipe = recipes[product]
    output_rate = recipe["output"]["quantity"]  # rate at which the product is produced per cycle
    cycle_time = recipe["time"]  # time for one production cycle

    # Calculate number of facilities required to achieve desired rate
    facilities_needed = math.ceil(rate / (output_rate / cycle_time))
    

    # Calculate input rates
    input_details = {}
    for input_item in recipe["inputs"]:
        input_material = input_item["material"]
        input_quantity = input_item["quantity"]

        # Check if the input material is a raw component or another product
        if input_material in raw_components:
            input_rate = rate * input_quantity / output_rate
            input_details[input_material] = {"rate": input_rate}
        else:
            # Recursively get input details for the input material
            sub_input_details = get_factory_details(input_material, rate=input_quantity * facilities_needed)
            input_details[input_material] = sub_input_details

    # Construct and return the details dictionary
    factory_details = {
        "facility": recipe["facility"],
        "facilities_needed": facilities_needed,
        "inputs": input_details
    }

    return factory_details

def simplify_factory(product, factory):
    # Initialize an adjacency list to represent the graph
    graph = {}

    # Helper function to recursively process each item
    def process_item(item, material, facilities_needed=None):
        if material not in graph:
            graph[material] = {'facility': item['facility'], 'total_facilities_needed': 0, 'inputs': {}}
        
        graph[material]['total_facilities_needed'] += facilities_needed

        # Process the inputs for this material
        for input_material, input_data in item.get('inputs', {}).items():
            # Add or update the input material in the graph
            #if input_material not in graph[material]['inputs']:
            if input_material not in raw_components:
                graph[material]['inputs'][input_material] = input_data['facilities_needed']
            else:
                if input_material not in graph[material]['inputs']:
                    graph[material]['inputs'][input_material] = input_data['rate']
                else:
                    graph[material]['inputs'][input_material] += input_data['rate']

            # Recursively process the input material
            if input_material not in raw_components:
                process_item(input_data, input_material, input_data['facilities_needed'])
            else:
                process_raw_item(input_data, input_material)

    def process_raw_item(item, material):
        if material not in graph:
            graph[material] = {'rate': 0}
        
        graph[material]['rate'] += item['rate']


    # Start processing from the top-level item
    process_item(factory, product, factory['facilities_needed'])

    return graph


def generate_graph(factory_details, product_name, graph=None, parent=None, edge_labels=None, demand_tracker=None):
    if graph is None:
        graph = nx.DiGraph()
    if edge_labels is None:
        edge_labels = {}
    if demand_tracker is None:
        demand_tracker = {}

    # check if node is already in graph.

    if product_name in raw_components:
        label = f"{product_name}\n({factory_details[product_name]['rate']*60} {'/min'})"
        graph.add_node(label)

        if parent:
            # Add edge from parent to current node
            weight = factory_details[parent.split('\n')[0]]['inputs'][product_name]
            graph.add_edge(label, parent, weight=weight)
        return
    
    # Add node for the current product
    label = f"{product_name}\n({factory_details[product_name]['total_facilities_needed']} {factory_details[product_name]['facility']})"
    
    graph.add_node(label)

    if parent:
        # Add edge from parent to current node
        weight = factory_details[parent.split('\n')[0]]['inputs'][product_name]
        graph.add_edge(label, parent, weight=weight)

   
    # Iterate over inputs and recursively build graph
    for input_material, input_data in factory_details[product_name]['inputs'].items():
        
        sub_product_name = input_material
        sub_factory_details = factory_details
        generate_graph(sub_factory_details, sub_product_name, graph, label, edge_labels, demand_tracker)

    return graph, edge_labels

def draw_graph(graph, edge_labels):
    pos = nx.drawing.nx_pydot.graphviz_layout(graph, prog='circo')

    plt.figure(figsize=(12, 12))
    nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=4500, font_size=10, font_weight='bold')

    # Draw the edges
    nx.draw_networkx_edges(graph, pos)

    # Create edge labels for weights
    edge_weight_labels = nx.get_edge_attributes(graph, 'weight')

    
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_weight_labels, font_color='blue')
    plt.show()
    
# Main function
def main():
    # Main program logic here
    details = get_factory_details("Energy Matrix", 1/6)
    print(json.dumps(details, indent=4))
    new_details = simplify_factory("Energy Matrix" ,details)
    print(json.dumps(new_details, indent=4))
    graph, edge_labels = generate_graph(new_details, "Energy Matrix")
    draw_graph(graph, edge_labels)
    # simplify_all()
    # print(recipes["Processor"])

# Ensures the main function is called only when this script is executed directly
if __name__ == "__main__":
    main()
