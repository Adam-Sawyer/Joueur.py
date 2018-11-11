debug = True

# This is where you build your AI for the Newtonian game.

from joueur.base_ai import BaseAI

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
import sys
# Un-comment this line if you would like to use the debug map, which requires the colorama package.

# <<-- /Creer-Merge: imports -->>


class AI(BaseAI):
    """ The AI you add and improve code inside to play Newtonian. """

    @property
    def game(self):
        """The reference to the Game instance this AI is playing.

        :rtype: games.newtonian.game.Game
        """
        return self._game  # don't directly touch this "private" variable pls

    @property
    def player(self):
        """The reference to the Player this AI controls in the Game.

        :rtype: games.newtonian.player.Player
        """
        return self._player  # don't directly touch this "private" variable pls

    def get_name(self):
        """ This is the name you send to the server so your AI will control the
            player named this string.

        Returns
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "GrAIvy Gang"

    class Group:
        def __init__(self, i_unit=None, m_unit=None, p_unit=None):
            self.i_unit = i_unit
            self.m_unit = m_unit
            self.p_unit = p_unit
            self.gathering = 'blueium'#Determines if they're gathering blueium or redium

            self.updateTask()

        @property
        def units(self):
            l = []
            if self.i_unit: l.append(self.i_unit)
            if self.m_unit: l.append(self.m_unit)
            if self.p_unit: l.append(self.p_unit)

            return l

        def __len__(self):
            return len(self.units)

        def remove(self, unit):
            if unit == self.i_unit: self.i_unit = None
            if unit == self.m_unit: self.m_unit = None
            if unit == self.p_unit: self.p_unit = None
            self.phase += 1

        def updateTask(self):
            if len(self.units) == 3:
                self.phase = 1
                self.task = 'gather'
            elif len(self.units) == 2:
                self.phase = 2
                self.task = 'hunt'
            else:
                self.phase = 3
                self.task = 'link2'

        def add(self, member):
            type = member.job.title

            if type == 'physicist':
                if self.p_unit == None:
                    self.phase -= 1
                    self.p_unit = member
                    self.updateTask()
                    return True
            elif type == 'manager':
                if self.m_unit == None:
                    self.phase -= 1
                    self.m_unit = member
                    self.updateTask()
                    return True
            elif type == 'intern':
                if self.i_unit == None:
                    self.phase -= 1
                    self.i_unit = member
                    self.updateTask()
                    return True
            else:
                print("Not a recognized type")
                return False

    def start(self):
        """ This is called once the game starts and your AI knows its player and
            game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your start logic
        self.groups = []

        # Un-comment this line if you are using colorama for the debug map.
        # init()

        # <<-- /Creer-Merge: start -->>

    def game_updated(self):
        """ This is called every time the game's state updates, so if you are
        tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def group_update(self):
        for group in self.groups:
            for member in group.units:
                # See if member is dead
                if member == None or not member.health:
                    group.remove(member)

            if not len(group.units):
                self.groups.remove(group)
                continue
            group.phase = (-(len(group.units) - 2) + 2)

        # if a group in phase 2 or 3 is found append it to a temporary list
        # look through the list of phase 2 and 3 groups and see if there are any
        # combinations to make a phase 1 or 2 IF so initialize a new group with
        # all of new members and delete the old groups
        phase2_groups = []
        phase3_groups = []
        for group in self.groups:
            if group.phase == 2:
                phase2_groups.append(group)
            elif group.phase == 3:
                phase3_groups.append(group)

        for phase2 in phase2_groups:
            for phase3 in phase3_groups:
                if phase2.add(phase3.units[0]):
                    temp = phase3.units[0]
                    phase3.remove(temp)
                    break

        phase3_groups = []
        for group in self.groups:
            if group.phase == 3:
                phase3_groups.append(group)
        for phase3 in phase3_groups:
            for phase3_2 in [group for group in phase3_groups if group is not phase3]:
                if phase3 is phase3_2:
                    break
                if len(phase3_2):
                    if phase3.add(phase3_2.units[0]):
                        temp = phase3_2.units[0]
                        phase3_2.remove(temp)
                        break

    def group_logic(self, group):
        if group.phase == 1:
            self.phase_1(group)
        #elif group.phase == 2:
            #self.phase_2(group)
        #else:
            #self.phase_3(group)

    def phase_1(self, group):
        if group.task == 'gather':
            if len(self.output[group.gathering + ' ore']) != 0:
                #intern leads the group while gathering 4 resources
                #When the intern has 4 resources the function returns True
                # and the task is witch to 'refine'
                self.action('move', self.output[group.gathering + ' ore'][0]
                , group.i_unit)
                group.i_unit.pickup(self.output[group.gathering + ' ore'][0], -1,
                group.gathering + ' ore')
                self.output[group.gathering + ' ore'].pop()
                self.action('move', group.i_unit.tile, group.p_unit)
                self.action('move', group.p_unit.tile, group.m_unit)
                if group.gathering == 'blueium':
                    group.i_unit.drop(group.i_unit.tile, group.i_unit.redium_ore,
                    'redium ore')
                    group.i_unit.drop(group.i_unit.tile, group.i_unit.redium,
                    'redium')
                    group.i_unit.drop(group.i_unit.tile, group.i_unit.blueium,
                    'blueium')
                    if group.i_unit.blueium_ore == 4:
                        group.task = 'refine'
                else:
                    group.i_unit.drop(group.i_unit.tile, group.i_unit.redium,
                    'redium')
                    group.i_unit.drop(group.i_unit.tile, group.i_unit.blueium,
                    'blueium')
                    group.i_unit.drop(group.i_unit.tile, group.i_unit.bluieum_ore,
                    'blueium ore')
                    if group.i_unit.redium_ore == 4:
                        group.task = 'refine'
        elif group.task == 'refine':
            #intern leads the group to the refinery, then the physicist refines
            #materials until they are all refined, switches to 'generate' after This
            #occurs
            group.task
        else:
            #Manager and physicist fill their inventorys with refined materials
            #and manager leads to generator. After this task is completed switch
            #back to 'gather task'
            if self.player.pressure < self.player.heat:
                group.gathering = 'blueium'
            else:
                group.gathering = 'redium'

    def end(self, won, reason):
        """ This is called when the game ends, you can clean up your data and
            dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why your AI won
            or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        # <<-- /Creer-Merge: end -->>
    def createGroups(self):
        for i in self.player.units:
            inGroup = False
            for group in self.groups:
                for n in group.units:
                    if i is n:
                        inGroup = True
            if inGroup == False:
                    self.groups.append(self.Group())
                    self.groups[-1].add(i)

    def run_turn(self):
        """ This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """
        # <<-- Creer-Merge: runTurn -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your game logic here for runTurn

        """
        Please note: This code is intentionally bad. You should try to optimize everything here. THe code here is only to show you how to use the game's
                     mechanics with the MegaMinerAI server framework.
        """
        self.parsefield()
        self.createGroups()
        self.group_update()
        for group in self.groups:
            self.group_logic(group)

        return True
        """
        # Goes through all the units that you own.
        for unit in self.player.units:
            # Only tries to do something if the unit actually exists.
            if unit is not None and unit.tile is not None:
                if unit.job.title == 'physicist':
                    # If the unit is a physicist, tries to work on machines that are ready, but if there are none,
                    # it finds and attacks enemy managers.

                    # Tries to find a workable machine for blueium ore.
                    # Note: You need to get redium ore as well.
                    target = None

                    # Goes through all the machines in the game and picks one that is ready to process ore as its target.
                    for machine in self.game.machines:
                        if machine.tile.blueium_ore >= machine.refine_input:
                            target = machine.tile

                    if target is None:
                        # Chases down enemy managers if there are no machines that are ready to be worked.
                        for enemy in self.game.units:
                            # Only does anything if the unit that we found is a manager and belongs to our opponent.
                            if enemy.tile is not None and enemy.owner == self.player.opponent and enemy.job.title == 'manager':
                                # Moves towards the manager.
                                while unit.moves > 0 and len(self.find_path(unit.tile, enemy.tile)) > 0:
                                    # Moves until there are no moves left for the physicist.
                                    if not unit.move(self.find_path(unit.tile, enemy.tile)[0]):
                                        break

                                if unit.tile in enemy.tile.get_neighbors():
                                    if enemy.stun_time == 0 and enemy.stun_immune == 0:
                                        # Stuns the enemy manager if they are not stunned and not immune.
                                        unit.act(enemy.tile)
                                    else:
                                        # Attacks the manager otherwise.
                                        unit.attack(enemy.tile)
                                break

                    else:
                        # Gets the tile of the targeted machine if adjacent to it.
                        adjacent = False
                        for tile in target.get_neighbors():
                            if tile == unit.tile:
                                adjacent = True

                        # If there is a machine that is waiting to be worked on, go to it.
                        while unit.moves > 0 and len(self.find_path(unit.tile, target)) > 1 and not adjacent:
                            if not unit.move(self.find_path(unit.tile, target)[0]):
                                break

                        # Acts on the target machine to run it if the physicist is adjacent.
                        if adjacent and not unit.acted:
                            unit.act(target)

                elif unit.job.title == 'intern':
                    # If the unit is an intern, collects blueium ore.
                    # Note: You also need to collect redium ore.

                    # Goes to gather resources if currently carrying less than the carry limit.
                    if unit.blueium_ore < unit.job.carry_limit:
                        # Your intern's current target.
                        target = None

                        # Goes to collect blueium ore that isn't on a machine.
                        for tile in self.game.tiles:
                            if tile.blueium_ore > 0 and tile.machine is None:
                                target = tile
                                break

                        # Moves towards our target until at the target or out of moves.
                        if len(self.find_path(unit.tile, target)) > 0:
                            while unit.moves > 0 and len(self.find_path(unit.tile, target)) > 0:
                                if not unit.move(self.find_path(unit.tile, target)[0]):
                                    break

                        # Picks up the appropriate resource once we reach our target's tile.
                        if unit.tile == target and target.blueium_ore > 0:
                            unit.pickup(target, 0, 'blueium ore')

                    else:
                        # Deposits blueium ore in a machine for it if we have any.

                        # Finds a machine in the game's tiles that takes blueium ore.
                        for tile in self.game.tiles:
                            if tile.machine is not None and tile.machine.ore_type == 'blueium':
                                # Moves towards the found machine until we reach it or are out of moves.
                                while unit.moves > 0 and len(self.find_path(unit.tile, tile)) > 1:
                                    if not unit.move(self.find_path(unit.tile, tile)[0]):
                                        break

                                # Deposits blueium ore on the machine if we have reached it.
                                if len(self.find_path(unit.tile, tile)) <= 1:
                                    unit.drop(tile, 0, 'blueium ore')

                elif unit.job.title == 'manager':
                    # Finds enemy interns, stuns, and attacks them if there is no blueium to take to the generator.
                    target = None

                    for tile in self.game.tiles:
                        if tile.blueium > 1 and unit.blueium < unit.job.carry_limit:
                            target = tile

                    if target is None and unit.blueium == 0:
                        for enemy in self.game.units:
                            # Only does anything for an intern that is owned by your opponent.
                            if enemy.tile is not None and enemy.owner == self.player.opponent and enemy.job.title == 'intern':
                                # Moves towards the intern until reached or out of moves.
                                while unit.moves > 0 and len(self.find_path(unit.tile, enemy.tile)) > 0:
                                    if not unit.move(self.find_path(unit.tile, enemy.tile)[0]):
                                        break

                                # Either stuns or attacks the intern if we are within range.
                                if unit.tile in enemy.tile.get_neighbors():
                                    if enemy.stun_time == 0 and enemy.stun_immune == 0:
                                        # Stuns the enemy intern if they are not stunned and not immune.
                                        unit.act(enemy.tile)
                                    else:
                                        # Attacks the intern otherwise.
                                        unit.attack(enemy.tile)
                                break

                    elif target is not None:
                        # Moves towards our target until at the target or out of moves.
                        while unit.moves > 0 and len(self.find_path(unit.tile, target)) > 1:
                            if not unit.move(self.find_path(unit.tile, target)[0]):
                                break

                        # Picks up blueium once we reach our target's tile.
                        if len(self.find_path(unit.tile, target)) <= 1 and target.blueium > 0:
                            unit.pickup(target, 0, 'blueium')

                    elif target is None and unit.blueium > 0:
                        # Stores a tile that is part of your generator.
                        gen_tile = self.player.generator_tiles[0]

                        # Goes to your generator and drops blueium in.
                        while unit.moves > 0 and len(self.find_path(unit.tile, gen_tile)) > 0:
                            if not unit.move(self.find_path(unit.tile, gen_tile)[0]):
                                break

                        # Deposits blueium in our generator if we have reached it.
                        if len(self.find_path(unit.tile, gen_tile)) <= 1:
                            unit.drop(gen_tile, 0, 'blueium')


        return True
        """
        # <<-- /Creer-Merge: runTurn -->>

    @staticmethod
    def reconstruct_path(path_next, current):
        # Path_next is dictionary of space: next_space

        total_path = [current]

        while current in path_next.keys():
            current = path_next[current]
            total_path.append(current)

        return total_path

    def find_path(self, start, goal):
        print("Finding path")
        goals = goal.get_neighbors()

        def heuristic_cost_estimate(tile_1, tile_2):
            return ((tile_2.y - tile_1.y)**2 + (tile_2.x - tile_1.x)**2)**.5

        def dist_between(tile_1, tile_2):
            return abs(tile_1.x - tile_2.x) + abs(tile_1.y - tile_2.y)

        if start == goal: return []

        closed_set = set()  # The set of nodes already evaluated

        # The set of currently discovered nodes that are not evaluated yet.
        # Initially, only the start node is known.
        open_set = set()
        open_set.add(start)

        # For each node, which node it can most efficiently be reached from .
        # If a node can be reached from many nodes, cameFrom will eventually contain the
        # most efficient previous step.
        comes_from = {}

        # For each node, the cost of getting from the start node to that node.
        g_score = {}  # map with default value of Infinity
        g_score[start] = 0  # The cost of going from start to start is zero.


        # For each node, the total cost of getting from the start node to the goal
        # by passing by that node.That value is partly known, partly heuristic.
        f_score = dict()  # map with default value of Infinity

        # For the first node, that value is completely heuristic.
        f_score[start] = heuristic_cost_estimate(start, goal)

        while open_set:
            parsed_f_score = {key: value for key, value in f_score.items() if key in open_set}
            current = min(parsed_f_score, key=parsed_f_score.get)  #the node in open_set having the lowest f_score[] value

            if current in goals:
                return self.reconstruct_path(comes_from, current)

            if current in open_set:
                open_set.remove(current)

            closed_set.add(current)

            for neighbor in current.get_neighbors():
                if neighbor in closed_set:
                    continue # Ignore the neighbor which is already evaluated.

                # The distance from start to a neighbor
                tentative_gScore = g_score[current] + dist_between(current, neighbor)

                if neighbor not in open_set: # Discover a new node
                    if not neighbor.is_wall:
                        open_set.add(neighbor)

                elif tentative_gScore >= g_score[neighbor]:
                    continue # This is not a better path.

                # This path is the best until now. Record it!
                comes_from[neighbor] = current
                g_score[neighbor] = tentative_gScore
                f_score[neighbor] = g_score[neighbor] + heuristic_cost_estimate(neighbor, goal)

        return []

    def find_path_old(self, start, goal):
        """A very basic path finding algorithm (Breadth First Search) that when
            given a starting Tile, will return a valid path to the goal Tile.

        Args:
            start (games.newtonian.tile.Tile): the starting Tile
            goal (games.newtonian.tile.Tile): the goal Tile
        Returns:
            list[games.newtonian.tile.Tile]: A list of Tiles
            representing the path, the the first element being a valid adjacent
            Tile to the start, and the last element being the goal.
        """

        if start == goal:
            # no need to make a path to here...
            return []

        # queue of the tiles that will have their neighbors searched for 'goal'
        fringe = []

        # How we got to each tile that went into the fringe.
        came_from = {}

        # Enqueue start as the first tile to have its neighbors searched.
        fringe.append(start)

        # keep exploring neighbors of neighbors... until there are no more.
        while len(fringe) > 0:
            # the tile we are currently exploring.
            inspect = fringe.pop(0)

            # cycle through the tile's neighbors.
            for neighbor in inspect.get_neighbors():
                # if we found the goal, we have the path!
                if neighbor == goal:
                    # Follow the path backward to the start from the goal and
                    # # return it.
                    path = [goal]

                    # Starting at the tile we are currently at, insert them
                    # retracing our steps till we get to the starting tile
                    while inspect != start:
                        path.insert(0, inspect)
                        inspect = came_from[inspect.id]
                    return path
                # else we did not find the goal, so enqueue this tile's
                # neighbors to be inspected

                # if the tile exists, has not been explored or added to the
                # fringe yet, and it is pathable
                if neighbor and neighbor.id not in came_from and (
                    neighbor.is_pathable()
                ):
                    # add it to the tiles to be explored and add where it came
                    # from for path reconstruction.
                    fringe.append(neighbor)
                    came_from[neighbor.id] = inspect

        # if you're here, that means that there was not a path to get to where
        # you want to go; in that case, we'll just return an empty path.
        return []

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here
    def display_map(self):
        """A function to display the current state of the map, mainly used for
            debugging without the visualizer. Use this to see a live view of what
            is happening during a game, but the visualizer should be much clearer
            and more helpful. To use this, make sure to un-comment the import for
            colorama and download it with pip.
        """

        print('\033[0;0H', end='')

        for y in range(0, self.game.map_height):
            print(' ', end='')
            for x in range(0, self.game.map_width):
                t = self.game.tiles[y * self.game.map_width + x]

                if t.machine is not None:
                    if t.machine.ore_type == 'redium':
                        print(Back.RED, end='')
                    else:
                        print(Back.BLUE, end='')
                elif t.is_wall:
                    print(Back.BLACK, end='')
                else:
                    print(Back.WHITE, end='')

                foreground = ' '

                if t.machine is not None:
                    foreground = 'M'

                print(Fore.WHITE, end='')

                if t.unit is not None:
                    if t.unit.owner == self.player:
                        print(Fore.CYAN, end='')
                    else:
                        print(Fore.MAGENTA, end='')

                    foreground = t.unit.job.title[0].upper()
                elif t.blueium > 0 and t.blueium >= t.redium:
                    print(Fore.BLUE, end='')
                    if foreground == ' ':
                        foreground = 'R'
                elif t.redium > 0 and t.redium > t.blueium:
                    print(Fore.RED, end='')
                    if foreground == ' ':
                        foreground = 'R'
                elif t.blueium_ore > 0 and t.blueium_ore >= t.redium_ore:
                    print(Fore.BLUE, end='')
                    if foreground == ' ':
                        foreground = 'O'
                elif t.redium_ore > 0 and t.redium_ore > t.blueium_ore:
                    print(Fore.RED, end='')
                    if foreground == ' ':
                        foreground = 'O'
                elif t.owner is not None:
                    if t.type == 'spawn' or t.type == 'generator':
                        if t.owner == self.player:
                            print(Back.CYAN, end='')
                        else:
                            print(Back.MAGENTA, end='')

                print(foreground + Fore.RESET + Back.RESET, end='')

            if y < 10:
                print(' 0' + str(y))
            else:
                print(' ' + str(y))

        print('\nTurn: ' + str(self.game.current_turn) + ' / '
              + str(self.game.max_turns))
        print(Fore.CYAN + 'Heat: ' + str(self.player.heat)
              + '\tPressure: ' + str(self.player.pressure) + Fore.RESET)
        print(Fore.MAGENTA + 'Heat: ' + str(self.player.opponent.heat)
              + '\tPressure: ' + str(self.player.opponent.pressure) + Fore.RESET)

        return

    def parsefield(self):
        self.output = {
        'blueium': [], 'blueium ore': [], 'redium': [], 'redium ore': [], 'enemy': [],
        'team': [], 'refinery': [], 'generator': [], 'spawn': [], 'conveyor': []
        }

        for tile in self.game.tiles:
            if tile.blueium > 0:
                self.output['blueium'].append(tile)
                pass

            if tile.redium > 0:
                self.output['redium'].append(tile)
                pass

            if tile.blueium_ore > 0:
                self.output['blueium ore'].append(tile)
                pass

            if tile.redium_ore > 0:
                self.output['redium ore'].append(tile)
                pass

            if tile.machine:
                self.output['refinery'].append(tile)
                pass

            if tile.type == 'generator':
                self.output['generator'].append(tile)
                pass

            if tile.type == 'conveyor':
                self.output['conveyor'].append(tile)
                pass

            if tile.type == 'spawn':
                self.output['spawn'].append(tile)
                pass

            if tile.unit:
                if tile.unit.owner == self.player.opponent:  # TODO - double check
                    self.output['team'].append(tile)
                else:
                    self.output['enemy'].append(tile)



    def action(self, keywd, tile, unit):
        path = self.find_path(unit.tile, tile)
        if keywd != 'move':
            path.pop()

        for t in path:
            if unit.moves == 0:
                break
            unit.move(t)

        if keywd == 'attack':
            unit.attack(tile)
        elif keywd != 'move':
            unit.act(tile)

        if unit.acted == True or keywd == 'move':
            return True
        else:
            return False

    # <<-- /Creer-Merge: functions -->>
