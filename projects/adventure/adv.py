from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

"""

- Add room visited (map dictionary)
- Get exits for the room.
- Navigate towards one direction, then add to traversal path
- then remove directions linked to the room
- Find opposite direction, then add to reverse path for backtracking
- Get exits for next room, track in map dictionary
- Keep moving player, add direction to traversal path and remove from possible directions
- Move til dead-end reached
- backtrack along last direction and add to the traversal path, and check room for unexplored directions
- Repeat til number of rooms visited matches length of the rooms graph
"""

visited = {} 
reverse_path = [] 
reverse_nav = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'} 

room_id = player.current_room.id
visited[room_id] = player.current_room.get_exits()

# As long as all rooms haven't been visited, carry out the if/else block.
while len(visited) < len(room_graph):
    # If the room that the player is currently in hasn't been visited.
    if player.current_room.id not in visited:
    # Add the room id to visited and find it's exits.
        visited[player.current_room.id] = player.current_room.get_exits()
        # After the room has been visited, remove it from unexplored paths. The player just came from that direction.
        previous_direction = reverse_path[-1]
        visited[player.current_room.id].remove(previous_direction)

    # If all rooms have been explored.
    if len(visited[player.current_room.id]) is 0:
        # Reverse until a room that has not been explored is found.
        previous_direction = reverse_path[-1]
        # Remove it from reverse_path since the reserval has already been done by -1
        reverse_path.pop()
        # Add previous direction to the traversal_path so we remember the route.
        traversal_path.append(previous_direction)
        # The player moves in that direction.
        player.travel(previous_direction)

    else: # if directions left unexplored
        # get 1st available direction in the room
        direction = visited[player.current_room.id][-1]
        visited[player.current_room.id].pop() # remove from visited
        # add direction to traversal_path
        traversal_path.append(direction)
        # add opposite direction to reverse_path
        reverse_path.append(reverse_nav[direction])
        # move player to explore new room
        player.travel(direction)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")