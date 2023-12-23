# Import necessary libraries
import numpy as np
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
    "Conveyor Belt MK.I": {
        "inputs": { 
            "Iron Ingot": 2,
            "Gear": 1
        },
        "output": 3,
        "facility": "Assembler",
        "time": 1  # in seconds
    },
    "Conveyor Belt MK.II": {
        "inputs": { 
            "Conveyor Belt MK.I": 3,
            "Electromagnetic Turbine": 1
        },
        "output": 3,
        "facility": "Assembler",
        "time": 1  # in seconds
    },
    "Splitter": {
        "inputs": { 
            "Iron Ingot": 3,
            "Gear": 2,
            "Circuit Board": 1
        },
        "output": 1,
        "facility": "Assembler",
        "time": 2  # in seconds
    }
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
        "output": 1,
        "facility": "Smelter",
        "time": 2  # in seconds
    },
    "Sorter MK.I": {
        "inputs": {
            "Iron Ingot": 1,
            "Circuit Board": 1
        },
        "output": 1,
        "facility": "Smelter",
        "time": 1  # in seconds
    },
    "Sorter MK.II": {
        "inputs": {
            "Sorter MK.I": 2,
            "Electric Motor": 1
        },
        "output": 2,
        "facility": "Smelter",
        "time": 1  # in seconds
    }
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
    "Electric Motor": {
        "inputs": {
            "Iron Ingot": 2,
            "Magnetic Coil": 1,
            "Gear": 1,
        },
        "output": 1,
        "facility": "Assembler",
        "time": 2
    },
}

recipes_V = {
    "Gear": {
        "inputs": {
            "Iron Ingot": 1,
        },
        "output": 1,
        "facility": "Assembler",
        "time": 1
    },
    "Electromagnetic Turbine": {
        "inputs": {
            "Electric Motor": 2,
            "Magnetic Coil": 2,
        },
        "output": 1,
        "facility": "Assembler",
        "time": 2
    },
}

recipes_matrix = {
    "Electromagnetic Matrix": {
        "inputs": {
            "Magnetic Coil": 1,
            "Circuit Board": 1,
        },
        "output": 1,
        "facility": "Research Facility",
        "time": 3
    },
    "Energy Matrix": {
        "inputs": {
            "Plasma Refining": 2,
            "Energetic Graphite": 2
        },
        "output": 1,
        "facility": "Research Facility",
        "time": 6
    },
}

recipes = recipes_II | recipes_III | recipes_IV | recipes_V | recipes_matrix



# def simplify_recipe(product):
#     # Base case: if the product is a raw component, return it
#     if product in raw_components:
#         return {product: 1}
    
#     recipe = recipes.get(product)
#     if not recipe:
#         return {} 
    
#     simplified_recipe = {}
#     for input_item in recipe["inputs"]:
#         material = input_item["material"]
#         quantity = input_item["quantity"]

#         if material in raw_components:
#             simplified_recipe[material] = simplified_recipe.get(material, 0) + quantity
#         else:
#             sub_recipe = simplify_recipe(material)
#             for sub_material, sub_quantity in sub_recipe.items():
#                 total_quantity = sub_quantity * quantity
#                 simplified_recipe[sub_material] = simplified_recipe.get(sub_material, 0) + total_quantity

#     return simplified_recipe

# def simplify_all():
#     for key,_ in recipes.items():
#         recipes[key] = sorted(simplify_recipe(key))

def get_factory_details(products, rate=1):
    factory = {
        "Storage": {
            "facility": "Storage",
            "total_facilities_needed": 1,
            "inputs": {},
            "level": 0
        }
    }

    def do_factory_details(product, factory, min_rate, level=1):

        recipe = recipes[product]
        output_rate = recipe["output"]  # rate at which the product is produced per cycle
        cycle_time = recipe["time"]  # time for one production cycle
        output_rate_in_seconds = (output_rate / cycle_time) # rate of production per second
        facilities_needed = math.ceil(min_rate / output_rate_in_seconds)
        
        if product not in factory:
            factory[product] = {'facility': recipe['facility'], 'total_facilities_needed': 0, 'inputs': {}}

        factory[product]['total_facilities_needed'] += facilities_needed
        factory[product]['level'] = level

        for input_product, input_quantity in recipe["inputs"].items():
            
            if input_product in raw_components:
                if input_product not in factory[product]['inputs']:
                    factory[product]['inputs'][input_product] = 0
                factory[product]['inputs'][input_product] += (input_quantity * facilities_needed)
                handle_raw(input_product, factory, input_quantity * facilities_needed, level + 1)
            else:
                if input_product not in factory[product]['inputs']:
                    factory[product]['inputs'][input_product] = {'requested': 0, 'rate': 0}
                
                factory[product]['inputs'][input_product]['requested'] += (input_quantity * facilities_needed)/(recipes[input_product]['output'] / recipes[input_product]['time'])
                factory[product]['inputs'][input_product]['rate'] += (input_quantity * facilities_needed)
                do_factory_details(input_product, factory, input_quantity * facilities_needed, level + 1)
    
    def handle_raw(product, factory, min_rate, level):
        if product not in factory:
            factory[product] = {'facility': 'Vein', 'rate': 0}
        
        factory[product]['rate'] += min_rate
        factory[product]['level'] = level

    for product in products:
        factory['Storage']['inputs'][product] = {
            'requested': 1 /(recipes[product]['output'] / recipes[product]['time']),
            'rate': 1
        }
        do_factory_details(product, factory, rate)

    return factory

def generate_graph(factory_details):
    # Create a directed graph
    G = nx.DiGraph()

    G.graph['root'] = next(iter(factory_details))

    # Add nodes with levels
    for node, attributes in factory_details.items():
        if node in raw_components:
            label = f"{node}\n({attributes['rate']*60}{'/min'})"
        else:
            label =  f"{node}\n({attributes['total_facilities_needed']} {attributes['facility']})"
        G.add_node(node, label=label, level=attributes['level'])

    # Add edges with weights
    for node, attributes in factory_details.items():
        if 'inputs' in attributes:
            for input_node, weight in attributes['inputs'].items():
                if isinstance(weight,dict):
                    formated_weight = f"{weight['requested']}\n{weight['rate']*60}/m"
                else:
                    formated_weight = f"{weight * 60}/m"
                G.add_edge(node, input_node, weight=formated_weight)
    
    return G

def draw_graph(graph):
    def create_center_aligned_layout(graph):
        root = graph.graph["root"]
        levels = {}
        for node in nx.bfs_tree(graph, root):
            level = graph.nodes[node]['level']
            levels.setdefault(level, []).append(node)

        pos = {}
        for level, nodes in levels.items():
            width = len(nodes)
            for i, node in enumerate(nodes):
                # Center aligning nodes at each level
                pos[node] = ((i - width / 2) * 1.5, -level)

        # Create a list of all edges with their data
        edges = list(graph.edges(data=True))

        # Iterate over the list and reverse each edge
        for u, v, data in edges:
            graph.add_edge(v, u, **data)
            graph.remove_edge(u, v)

        return pos
    
    pos = create_center_aligned_layout(graph)
    # pos = nx.circular_layout(graph)

    plt.figure(figsize=(12, 12))


    nx.draw(graph, pos, with_labels=False, node_color='skyblue', node_size=4500, font_size=10, font_weight='bold')


    # Create edge labels for weights
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    for edge, label in edge_labels.items():
        source, target = edge
        x, y = pos[source]
        dx, dy = pos[target]
        label_pos = (x*0.6 + dx*0.4, y*0.6 + dy*0.4)

        # Draw labels with background for better readability
        plt.text(label_pos[0], label_pos[1], label, size=12, 
             bbox=dict(facecolor='white', alpha=1, edgecolor='none'),
             horizontalalignment='center', verticalalignment='center', color='blue')

    for node, data in graph.nodes(data=True):
        plt.text(pos[node][0], pos[node][1], data['label'], fontsize=9, ha='center', va='center')

    plt.show()
    
# Main function
def main():
    # Main program logic here
    # details = get_factory_details(["Splitter", "Conveyor Belt MK.II", "Sorter MK.II"], 1)
    details = get_factory_details(["Copper Ingot"], 9)
    print(json.dumps(details, indent=4))
    graph = generate_graph(details)
    draw_graph(graph)
    

# Ensures the main function is called only when this script is executed directly
if __name__ == "__main__":
    main()
