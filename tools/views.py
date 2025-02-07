import os
import json
import random
from django.shortcuts import render
from django.http import HttpResponse

# Assume maps.json is in the same directory as views.py; otherwise, change to an absolute path
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'maps.json')
MAPS_DATA = None  # Global cache (optional)

def load_maps_data():
    global MAPS_DATA
    if MAPS_DATA is None:
        with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
            MAPS_DATA = json.load(f)
    return MAPS_DATA

def assign_region_colors(n):
    """
    Assign colors to region IDs 0..(n-1), assuming that the numbers in colorGrid do not exceed n-1
    """
    colors = {}
    for rid in range(n):
        hue = int(360.0 * rid / n)
        color_str = f"hsl({hue},70%,60%)"
        colors[rid] = color_str
    return colors

def puzzle_view(request):
    """
    Django view: Read map data from maps.json and render the template 'tools/crowns.html'

    URL examples:
      /puzzle/?size=4&level=2   -> Level 2 of a 4×4 map
      /puzzle/?size=5           -> If the level is invalid, randomly select a level
    """
    data = load_maps_data()  # Data format example: { "4": [...], "5": [...], ..., "14": [...] }

    # 1) Get the list of available sizes (the keys in the JSON file)
    available_sizes = list(data.keys())  # For example: ["4", "5", ..., "14"]

    # 2) Get 'size' from GET parameters; default to '4' if invalid
    size_str = request.GET.get('size', '4')
    if size_str not in data:
        size_str = '4'
    maps_list = data[size_str]  # All maps for the current board size

    # Convert size_str to an integer (for subsequent calculations)
    try:
        n = int(size_str)
    except:
        n = 4

    # 3) Determine the total number of levels based on board size n (fixed rules)
    if n in [4, 5]:
        max_level = 30
    elif n in [6, 7]:
        max_level = 50
    elif 8 <= n <= 13:
        max_level = 70
    else:
        max_level = 30

    # 4) Parse the level number from GET parameters (levels start from 1)
    try:
        level = int(request.GET.get('level', '1'))
    except:
        level = 1
    # If the level number is invalid (less than 1 or greater than the maximum level), randomly select a level
    if level < 1 or level > max_level:
        level = random.randrange(1, max_level + 1)
    # Convert the 1-based level number to a 0-based index
    index = level - 1

    # Extract the map data for the corresponding level from the map list of the current board size
    chosen_map = maps_list[index]
    # For example, chosen_map = {
    #   "name": "Map n4 #1",
    #   "caseNumber": 4,
    #   "colorGrid": [...],
    #   "queenBoard": [...]
    # }
    region_map = chosen_map["colorGrid"]
    queen_board = chosen_map["queenBoard"]  # Used for the "step-by-step hint" feature

    # Assign colors to region IDs based on the board size
    region_colors = assign_region_colors(n)

    context = {
        'size': n,                           # Board size (number, e.g., 4)
        'region_map': region_map,            # Board region data (colorGrid)
        'region_colors': region_colors,      # Mapping of region colors
        'queen_board': queen_board,          # Answer data used for hints
        'map_name': chosen_map["name"],      # Map name
        'size_str': size_str,                # Original size string (for URL parameters)
        'level': level,                      # Current level (1-based)
        'max_level': max_level,              # Total levels for the current board size
        'available_sizes': sorted(available_sizes, key=lambda x: int(x)),  # List of available sizes (e.g., ["4", "5", …])
    }
    return render(request, 'tools/crowns.html', context)
