from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
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

#create a blank dictionary called map
map = {}
# create explore method
def explore(player, moves):
# Make it into a bfs
    #initialize Queue
    queue = Queue()
    #add starting room to queue
    queue.enqueue([player.current_room.id])
    #initialize visited
    visited = set()
    #while the queue has places to go
    while queue.size() > 0:
        #as exploration continues, remove from queue
        route = queue.dequeue()
        #grab the last visited room
        last_visited = route[-1]
        #if the last room isn't in visited, add to visited
        if last_visited not in visited:
            visited.add(last_visited)
        # note the exits
            for exit in map[last_visited]:
                #if the exit in the map dict is ?, return route
                if map[last_visited][exit] == '?':
                    return route
                #otherwise, get rid of the explored route
                else:
                    been_there = list(route)
                    been_there.append(map[last_visited][exit])
                    queue.enqueue(been_there)
    return [] #***COME BACK AND RETURN VISITED
#create method to check for exits that haven't been tried
def untried(player, new_moves):
    #set exits
    exits = map[player.current_room.id]
    #create empty list for untried exits to be used later
    untried = []
    #check exits of the current room for unexplored areas
    for direction in exits:
        if exits[direction] == "?":
            #add to untried so they can be explored
            untried.append(direction)
    #if there aren't any untried exits
    if len(untried) == 0:
        #explore until you find a room with unexplored exits
        unexplored = explore(player, new_moves)
        #set new room to the player's current room
        new_room = player.current_room.id
        #go through each unexplored room
        for room in unexplored:
            #then in that room, check for unexplored exits and add them to new moves
            for direction in map[new_room]:
                if map[new_room][direction] == room:
                    new_moves.enqueue(direction)
                    new_room = room
                    break
    #otherwise, try a random untried exit
    else:
        new_moves.enqueue(untried[random.randint(0, len(untried) -1)])

#create moves that only use untried exits
#create an unexplored room dictionary
unexplored_room = {}
#go through the exits in the current room
for direction in player.current_room.get_exits():
    #add all ? exits to unexplored_room
    unexplored_room[direction] = "?"
    #the starting room should be an unexplored room
map[world.starting_room.id] = unexplored_room

#turn new_moves into a queue
new_moves = Queue()
#call untried 
untried(player, new_moves)

#set the reverse directions, just like in the adventure game
reverse_dir = {"n": "s", "s": "n", "e": "w", "w": "e"}

#while new_moves has items in it
while new_moves.size() > 0:
    #set the starting room
    start = player.current_room.id
    #grab a direction from new_moves
    move = new_moves.dequeue()
    #move that direction
    player.travel(move)
    #add that to traversal_path
    traversal_path.append(move)
    #set the player's new room to a variable
    next_room = player.current_room.id
    #set the map entry for the move to next_room
    map[start][move] = next_room
    #if it isn't in the map
    if next_room not in map:
        map[next_room] = {}
        #for each exit found in the current room
        for exit in player.current_room.get_exits():
            #set each unexplored exit to ?
            map[next_room][exit] = "?"
    #map the reverse compass and set it to the next start
    map[next_room][reverse_dir[move]] = start
    #if there are no moves left in new_moves
    if new_moves.size() == 0:
        #run untried again
        untried(player, new_moves)


# TRAVERSAL TEST
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
