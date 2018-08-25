//x, y format
var node = [
411, 2065,
2111, 2041,
3121, 2000,
3283, 1282,
3373, 547,
3371, 231,
2407, 363,
1115, 427,
147, 561,
741, 1411,
1123, 1720,
1683, 1777,
2545, 205,
1821, 1009
];

//index of pairs of nodes, represent  edges
var edge =[
0, 1,
0, 8,
0, 9,
0, 10,
1, 2,
1, 11,
1, 12,
1, 13,
2, 3,
2, 12,
3, 4,
3, 12,
4, 5,
4, 6,
5, 6, 
6, 7, 
6, 13, 
7, 8, 
7, 9, 
7, 13,
8, 9, 
9, 10, 
10, 11, 
12, 13
];

var MapHandler = {
    dict : new Map(),
    dis_mtx : [],
    path_mtx : [],
    init : function(node, edge){
        var i, j, temp;
        for (i=0; i < node.length; i+=2){
            temp = [node[i], node[i+1]];
            this.dict.set(i >> 1, [temp, []]);
        }
        this.nodes_num = node.length >> 1;
        for (i=0; i < this.nodes_num; i++){
            this.dis_mtx[i] = [];
            this.path_mtx[i] = [];
        }
        for (i=0; i < this.nodes_num; i++){
            for (j=0; j < this.nodes_num; j++){
                this.dis_mtx[i][j] = Infinity;
                this.path_mtx[i][j] = null;
            }
        }
       var node1, node2, distance;
       for (j=0; j < edge.length; j+=2){
           node1 = edge[j];
           node2 = edge[j + 1];
           distance = this.get_distance(node1, node2);
           this.dict.get(node1)[1].push([node2, node1]);
           this.dict.get(node2)[1].push([node1, node2]);
           this.dis_mtx[node1][node2] = distance;
           this.dis_mtx[node2][node1] = distance;
       }
    },
    
    get_distance : function(node1, node2){
        var n1, n2;
        n1 = this.dict.get(node1)[0];
        n2 = this.dict.get(node2)[0];
        return ((n1[0] - n2[0])**2 + (n1[1] - n2[1])**2)**0.5;
    },
    
    get_min_path : function(){
        var k, i, j;
        for (k = 0; k < this.nodes_num; k++){
            for (i = 0; i < this.nodes_num; i++){
                for (j = 0; j < this.nodes_num; j++){
                    if (this.dis_mtx[i][j] > this.dis_mtx[i][k] + this.dis_mtx[k][j]){
                        this.dis_mtx[i][j] = this.dis_mtx[i][k] + this.dis_mtx[k][j];
                        this.path_mtx[i][j] = k;
                    }
                }
            }            
        }
    },
    
    get_one_path : function(node1, node2){
        node1 -= 1;
        node2 -= 1;
        var node = node1;
        var path = [];
        while(node != null){
            path.push(node + 1);
            node = this.path_mtx[node][node2];
        }
        path.push(node2 + 1);
        return path;
    }
}

MapHandler.init(node, edge);
MapHandler.get_min_path();
console.log(MapHandler.get_one_path(1, 14));