from room import Room
from player import Player
from world import World
from queue import Queue
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
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

opposite_path = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

# init graph
graph = {}

def bfs_map(graph, starting_room):
    queue = Queue()
    visited = set()
    
    queue.enqueue([starting_room])
    
    while queue.size():
        path = queue.dequeue()
        rooms = path[-1]
        
        if rooms not in visited:
            visited.add(rooms)
            
            for room in graph[rooms]:
                
                if graph[rooms][room] == '?':
                    
                    return path

            for adjacent_rooms in graph[rooms]:
                
                surrounding_rooms = graph[rooms][adjacent_rooms]
                new_path = list(path)
                new_path.append(surrounding_rooms)
                queue.enqueue(new_path)


while len(graph) < len(room_graph):
    
    cur_room_id = player.current_room.id
    
    if cur_room_id not in graph:
        graph[cur_room_id] = {}
        
        for room_exits in player.current_room.get_exits():
            
            graph[cur_room_id][room_exits] = "?"

    for direction in graph[cur_room_id]:
        
        if direction not in graph[cur_room_id]:
            break
        
        if graph[cur_room_id][direction] == '?':
            
            available_room = direction

            if available_room is not None:
                traversal_path.append(available_room)
                player.travel(available_room)
                
                new_room_id = player.current_room.id
                
                if new_room_id not in graph:
                    
                    graph[new_room_id] = {}
                    
                    for room_exits in player.current_room.get_exits():
                        
                        graph[new_room_id][room_exits] = '?'
            
            graph[cur_room_id][available_room] = new_room_id
            
            graph[new_room_id][opposite_path[available_room]] = cur_room_id
            cur_room_id = new_room_id

    room_traversal = bfs_map(graph, player.current_room.id)
    
    if room_traversal is not None:
        
        for r in room_traversal:
            
            for room_exits in graph[cur_room_id]:
                
                if graph[cur_room_id][room_exits] == r:
                    
                    traversal_path.append(room_exits)
                    
                    player.travel(room_exits)
    
    cur_room_id = player.current_room.id



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
