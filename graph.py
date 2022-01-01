"""
Quokka Maze
===========

This file represents the quokka maze, a graph of locations where a quokka is
trying to find a new home.

Please help the quokkas find a path from their current home to their
destination such that they have sufficient food along the way!

*** Assignment Notes ***

This is the main file that will be interacted with during testing.
All functions to implement are marked with a `TODO` comment.

Please implement these methods to help the quokkas find their new home!
"""

from typing import List, Union

from vertex import Vertex


class QuokkaMaze:
    """
    Quokka Maze
    -----------

    This class is the undirected graph class that will contain all the
    information about the locations between the Quokka colony's current home
    and their final destination.

    We _will_ be performing some minor adversarial testing this time, so make
    sure you're performing checks and ensuring that the graph is a valid simple
    graph!

    ===== Functions =====

        * block_edge(u, v) - removes the edge between vertex `u` and vertex `v`
        * fix_edge(u, v) - fixes the edge between vertex `u` and `v`. or adds an
            edge if non-existent
        * find_path(s, t, k) - find a SIMPLE path from vertex `s` to vertex `t`
            such that from any location with food along this simple path we
            reach the next location with food in at most `k` steps
        * exists_path_with_extra_food(s, t, k, x) - returns whether it’s
            possible for the quokkas to make it from s to t along a simple path
            where from any location with food we reach the next location with
            food in at most k steps, by placing food at at most x new locations
        * find_location_of_extra_food(s, t, k, x) - returns at most x locations
            where we can add food, such that afterwards there exists a valid
            path from s to t with food at most k steps between each other.
        * minimize_extra_food(s, t, k) - returns the smallest `x` locations,
            such that adding food at these x locations guarantees there exists
            a path from s to t with at most k steps between food.

    ===== Notes ======

    * We _will_ be adversarially testing, so make sure you check your params!
    * The ordering of vertices in the `vertex.edges` does not matter.
    * You MUST check that `k>=0` and `x>=0` for the respective functions
        * find_path (k must be greater than or equal to 0)
        * exists_path_with_extra_food (k and x must be greater than or equal to
            0)
    * This is an undirected graph, so you don't need to worry about the
        direction of traversing during your path finding.
    * This is a SIMPLE GRAPH, your functions should ensure that it stays that
        way.
    * All vertices in the graph SHOULD BE UNIQUE! IT SHOULD NOT BE POSSIBLE
        TO ADD DUPLICATE VERTICES! (i.e the same vertex instance)
    """

    def __init__(self) -> None:
        """
        Initialises an empty graph with a list of empty vertices.
        """
        self.vertices = []

    def add_vertex(self, v: Vertex) -> bool:
        """
        Adds a vertex to the graph.
        Returns whether the operation was successful or not.

        :param v - The vertex to add to the graph.
        :return true if the vertex was correctly added, else false
        """
        # TODO implement me, please?

        if v == None:
            return False
        if v not in self.vertices:
            self.vertices.append(v)
            return True
        else:
            while v in self.vertices:
                self.vertices.remove(v)
            self.vertices.append(v)
            return False

    def fix_edge(self, u: Vertex, v: Vertex) -> bool:
        """
        Fixes the edge between two vertices, u and v.
        If an edge already exists, then this operation should return False.

        :param u - A vertex
        :param v - Another vertex
        :return true if the edge was successfully fixed, else false.
        """

        # TODO implement me please.
        flag = 0
        if v not in self.vertices:
            flag =1
        if u not in self.vertices:
            flag =1
        if u == None:
            flag = 1
        if v == None:
            flag = 1
        if flag == 1:
            return False
        if v in u.edges and u in v.edges:
            return False
        v.rm_edge(u)
        u.rm_edge(v)
        v.add_edge(u)
        u.add_edge(v)
        return True

    def block_edge(self, u: Vertex, v: Vertex) -> bool:
        """
        Blocks the edge between two vertices, u and v.
        Removes the edge if it exists.
        If not, it should be unsuccessful.

        :param u - A vertex
        :param v - Another vertex.
        :return true if the edge was successfully removed, else false.
        """

        # TODO implement me, please!
        if u not in self.vertices or v not in self.vertices:
            return False
        if u == None or v == None:
            return False
        if v not in u.edges and u not in v.edges:
            return False
        if v in u.edges:
            u.rm_edge(v)
        if u in v.edges:
            v.rm_edge(u)
        return True

    def find_path(
            self,
            s: Vertex,
            t: Vertex,
            k: int
    ) -> Union[List[Vertex], None]:
        """
        find_path returns a SIMPLE path between `s` and `t` such that from any
        location with food along this path we reach the next location with food
        in at most `k` steps

        :param s - The start vertex for the quokka colony
        :param t - The destination for the quokka colony
        :param k - The maximum number of hops between locations with food, so
        that the colony can survive!
        :returns
            * The list of vertices to form the simple path from `s` to `t`
            satisfying the conditions.
            OR
            * None if no simple path exists that can satisfy the conditions, or
            is invalid.

        Example:
        (* means the vertex has food)
                    *       *
            A---B---C---D---E

            1/ find_path(s=A, t=E, k=2) -> returns: [A, B, C, D, E]

            2/ find_path(s=A, t=E, k=1) -> returns: None
            (because there isn't enough food!)

            3/ find_path(s=A, t=C, k=4) -> returns: [A, B, C]

        """

        # TODO implement me please
        if k < 0:
            return None
        if s not in self.vertices:
            return None
        if t not in self.vertices:
            return None
        path = []
        visited =[]
        simple_paths = []
        shortest =[False,[]]
        
        flag = 0
        self.dfs(s,t,path,visited,simple_paths)
        for i in simple_paths:
            flag = 0
            for x in i:
                if x not in self.vertices:
                    flag =1
                if i.count(x) >1:
                    flag =1
                if x == None:
                    flag =1
            if flag == 1:
                continue
            if self.is_reachable(i,k):
                if shortest[0] == False:
                    shortest[0] = True
                    shortest[1] = i
                else:
                    if len(shortest[1]) > len(i):
                        shortest[1] = i
        
        if shortest[0] ==True:
            return shortest[1]
        
        return None

    def dfs(self,s,t,path,visited,simple_paths):
        visited.append(s)
        path.append(s)
        if s == t:
            a = []
            for i in path:
                a.append(i)
            simple_paths.append(a)
            visited.remove(s)
            path.pop()
            return   
        for i in s.edges:
            if i in self.vertices:
                if i !=  s:
                    if i != None:
                        if  i not in visited:
                            self.dfs(i,t,path,visited,simple_paths)
        path.pop()
        visited.remove(s)
        
    def is_reachable(self,path,k):

        length = len(path)
        index =0
        stamina =k
        current = path[0]
        while True:
            if index == length-1:
                return True
            if stamina == 0:
                return False
            stamina -= 1
            index+=1
            if path[index] in current.edges:
                current = path[index]
            else:
                return False
            if current.has_food ==True:
                stamina = k
    


    def exists_path_with_extra_food(
        self,
        s: Vertex,
        t: Vertex,
        k: int,
        x: int
    ) -> bool:
        """
        Determines whether it is possible for the quokkas to make it from s to
        t along a SIMPLE path where from any location with food we reach the
        next location with food in at most k steps, by placing food at at most
        x new locations.

        :param s - The start vertex for the quokka colony
        :param t - The destination for the quokka colony
        :param k - The maximum number of hops between locations with food, so
        that the colony can survive!
        :param x - The number of extra foods to add.
        :returns
            * True if with x added food we can complete the simple path
            * False otherwise.

        Example:
        (* means the vertex has food)
                            *
            A---B---C---D---E

            1/ exists_with_extra_food(A, E, 2, 0) -> returns: False
                (because we can't get from A to E with k=2 and 0 extra food)

            2/ exists_with_extra_food(A, E, 2, 1) -> returns: True
                (Yes, if we put food on `C` then we can get to E with k=2)

            3/ exists_with_extra_food(A, E, 1, 6) -> returns: True
                (Yes, if we put food on `B`, `C`, `D` then we reach E!)
        """

        # TODO implement me please
        if k < 0:
            return False
        if x <0:
            return False
        if s not in self.vertices:
            return False
        if t not in self.vertices:
            return False
        path = []
        visited =[]
        simple_paths = []
        self.dfs(s,t,path,visited,simple_paths)
        
        for i in simple_paths:
            if self.is_reachable_with_extra_food(i,k,x):
                return True
        return False

    def is_reachable_with_extra_food(self,path,k,x):


        length = len(path)
        food_left =x
        stamina = k
        index =0
        while True:
            if index == length-1:
                return True
            if stamina == 0:
                if food_left >0:
                    stamina = k
                    food_left -= 1
                else:
                    return False
            stamina -= 1
            index+=1
            current = path[index]
            if current.has_food ==True:

                stamina = k
        

    def find_location_of_extra_food(
        self,
        s: Vertex,
        t: Vertex,
        k: int,
        x: int
    ) -> Union[List[Vertex], None]:
        """
        Returns the (at most) x locations where we can add food, such that
        afterwards there exists a path from s to t such that from any location
        with food, we reach the next location with food in at most k steps.

        :param s - The start vertex for the quokka colony
        :param t - The destination for the quokka colony
        :param k - The maximum number of hops between locations with food, so
                    that the colony can survive!
        :param x - The maximum number of extra foods to add.
        :returns:
                * The list of vertices to add the food, in any order :)
                * None if no path exists.

        Example:
        (* means the vertex has food)
                            *
            A---B---C---D---E

            1/ find_location_of_extra_food(A, E, 2, 0) -> returns: None
                (because we can't get from A to E with k=2 and 0 extra food)

            2/ find_location_of_extra_food(A, E, 2, 1) -> returns: [C]
                (If we put food on `C` then we can get to E with k=2)

            3/ find_location_of_extra_food(A, E, 1, 6) -> returns: [B, C, D]
                (Yes, if we put food on `B`, `C`, `D` then we reach E!)

            4/ find_location_of_extra_food(A, E, 2, 10)
                    -> returns: [C] OR [C, D] OR [B, D] OR [B, C] OR [B, C, D]
                (Any of the returned lists satisfy the criteria.)
        """
        # TODO implement me.
        path = []
        visited =[]
        simple_paths = []
        locations = [False,[]]
        self.dfs(s,t,path,visited,simple_paths)
        
        
        for i in simple_paths:
            if self.get_location(i,k,x,locations)[0]:
                return locations[1]
        return None
    def get_location(self,path,k,x,locations):


        length = len(path)
        food_left =x
        stamina = k
        index =0
        current = path[0]
        while True:
            if index == length-1:
                locations[0] = True
                return locations
            if stamina == 0:
                if food_left >0:
                    stamina = k
                    food_left -= 1
                    locations[1].append(current)
                else:
                    locations[1].clear()
                    return locations
            stamina -= 1
            index+=1
            current = path[index]
            if current.has_food ==True:

                stamina = k

    def minimize_extra_food(
        self,
        s: Vertex,
        t: Vertex,
        k: Vertex
    ) -> Union[List[Vertex], None]:
        """
        Returns the smallest x locations such that adding food at these x
        locations guarantees that there exists a path from s to t such that
        from any location with food, we reach the next location with food in at
        most k steps.

        :param s - The start vertex for the quokka colony.
        :param t - The destination vertex for the quokka colony.
        :param k - The maximum number of hops between
        :returns:
            * The minimum list of locations to place foods in at most K
            steps.
            * None if no path exists.

        Example:
        (* means the vertex has food)
                            *
            A---B---C---D---E

            1/ minimize_extra_food(A, E, 2) -> [C]
            2/ minimize_extra_food(A, E, 1) -> [B, C, D]

        """
        # TODO implement me
        path = []
        visited =[]
        simple_paths = []
        locations = []
        smallest_locations = [False,[]]
        self.dfs(s,t,path,visited,simple_paths)
        
        
        for i in simple_paths:
            self.get_location2(i,k,locations)
            if smallest_locations[0] == False:
                for i in locations:
                    smallest_locations.append(i)
                smallest_locations[0] = True 
            elif len(smallest_locations[1])> len(locations):
                smallest_locations[1].clear()
                for i in locations:
                    smallest_locations[1].append(i)
            locations.clear()
        if smallest_locations[0]:
            return smallest_locations[1]
        else:
            return None
        
    def get_location2(self,path,k,locations):

        length = len(path)
        stamina = k
        index =0
        current = path[0]
        while True:
            if index == length-1:
                return locations
            if stamina == 0:
                locations.append(current)
                stamina = k
            stamina -= 1
            index+=1
            current = path[index]
            if current.has_food == True:
                stamina = k
