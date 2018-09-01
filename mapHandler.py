from newData import *
class Map():
    def __init__(self, node, edge):
        #data structure output in this case
        #{0:[(1, 4), [(1, 2.344), (3, 4.566), (5, 7.688), (6, 8.900)]], 1:[(2, 5),  ......}
        self.dict = {}
        for i in range(0, len(node), 2):
            temp = (node[i], node[i+1])
            self.dict[i >>1] = (temp,[])
        self.nodes_num = len(node) >> 1
        self.dis_mtx = [[float('inf') for j in range(self.nodes_num)] for i in range(self.nodes_num)]
        self.path_mtx = [[None for j in range(self.nodes_num)] for i in range(self.nodes_num)]
        
        for j in range(0, len(edge), 2):
            node1 = edge[j] - 1
            node2 = edge[j + 1] - 1
            assert node1 in self.dict
            assert node2 in self.dict
            distance = self.get_distance(node1, node2)
            self.dict[node1][1].append((node2, distance))
            self.dict[node2][1].append((node1, distance))
            self.dis_mtx[node1][node2] = distance
            self.dis_mtx[node2][node1] = distance
            self.path_mtx[node1][node2] = node2
            self.path_mtx[node2][node1] = node1
        
        self.current_location = None
        self.destination = None
       
        
        
    def set_destination(self, destination):
        assert destination in self.dict
        self.destination = destination
    
    def set_current_location(self, current_location):
        assert current_location in self.dict
        self.current_location = current_location
    
    def get_distance(self, node1, node2):
        n1 = self.dict[node1][0]
        n2 = self.dict[node2][0]
        return ((n1[0] - n2[0])**2 + (n1[1] - n2[1])**2)**0.5
        
    def get_min_path(self):
        for k in range(self.nodes_num):
            for i in range(self.nodes_num):
                for j in range(self.nodes_num):
                    if self.dis_mtx[i][j] > self.dis_mtx[i][k] + self.dis_mtx[k][j]:
                        self.dis_mtx[i][j] = self.dis_mtx[i][k] + self.dis_mtx[k][j]
                        self.path_mtx[i][j] = k
        
    def get_one_path(self, node1, node2):
        node1 -= 1
        node2 -= 1
        path = [node1 + 1]
        def get_path(self, node1, node2, path):
            if(node1 == node2):
                return
            if(self.path_mtx[node1][node2]==node2):
               path.append(node2 + 1)
            else:
                get_path(self, node1, self.path_mtx[node1][node2], path)
                get_path(self, self.path_mtx[node1][node2], node2, path)        
        get_path(self, node1, node2, path)
        return path
    
instance = Map(node, edge)
instance.get_min_path()
print(instance.get_one_path(1, 14))
