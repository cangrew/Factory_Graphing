
# Factory Planner for Resource Management Game

This repository contains a Python script designed for planning and visualizing factory setups in a resource management game. The script analyzes production recipes, calculates the required number of facilities, and displays the production hierarchy and dependencies as a graph. This tool is invaluable for strategizing and optimizing resource allocation in-game.

## Features

- **Recipe Analysis**: Parses and processes in-game recipes to determine the production chain for various products.
- **Facility Calculation**: Calculates the number of facilities needed for each step in the production chain to meet a specified production rate.
- **Graph Visualization**: Generates a graph to visualize the production hierarchy, showing the dependencies and flow of materials.
- **Raw Material Handling**: Incorporates raw materials directly available in the game environment, such as ores and gases.
- **Flexible Production Rate**: Allows specifying the desired production rate for final products, adjusting the entire production chain accordingly.
- **Extensible**: Can be easily expanded or modified to include more recipes or adapt to game updates.

## Installation

To use this script, you need Python installed on your system. Clone the repository and install the required dependencies:

```bash
git clone https://github.com/your-username/factory-planner.git
cd factory-planner
pip install -r requirements.txt
```

## Usage

To run the script, execute:

```bash
python factory_planner.py
```

You can modify the script to plan for different products or change the production rate by editing the `main()` function.

## Visualization

The script outputs a graph visualization representing the production chain. Each node in the graph is a facility, and edges represent the flow of materials. This visualization aids in understanding the complex interdependencies in the production process.

## Contributing

Contributions to this project are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

*Note: This script is a fan-made tool and is not affiliated with the game's developers. All game-related terms and references are the property of their respective owners.*
