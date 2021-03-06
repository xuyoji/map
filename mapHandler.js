//x, y format
var node = [
 178, 936,
 325, 806,
 325, 616,
 383, 433,
 352, 345,
 163, 421,
 70, 432,
 266, 533,
 100, 298,
 260, 217,
 577, 186,
 683, 216,
 830, 204,
 1115, 160,
 1529, 116,
 1534, 265,
 1522, 442,
 1502, 579,
 1412, 723,
 1361, 927,
 948, 939,
 975, 792,
 488, 804,
 497, 951,
 947, 510,
 1173, 570,
 1076, 803,
 1318, 771,
 159, 805,
 733, 381
];

//index of pairs of nodes, represent  edges
var edge =[
1, 24,
1, 29,
2, 3,
2, 6,
2, 7,
2, 8,
2, 23,
2, 29,
3, 7,
3, 8,
3, 29,
4, 5,
4, 8,
5, 6,
5, 12,
6, 7,
6, 8,
6, 29,
7,  8,
7, 9,
7, 29,
8, 29,
9, 10,
10, 11,
11, 12,
12, 13,
12, 30, 
13, 14,
13, 30,
14, 15,
14, 16,
15, 16,
16, 17,
17, 18,
18, 19,
18, 26,
19, 20,
19, 26,
19, 27,
19, 28,
20, 21,
21, 22,
21, 24,
22, 23,
22, 25,
22, 27,
23, 24,
25, 26,
26, 28,
27, 28
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
           node1 = edge[j] - 1;
           node2 = edge[j + 1] - 1;
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