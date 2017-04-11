#include <bits/stdc++.h>
using namespace std;

class Node{
    public:
    int value;
    vector<int> domain;

    Node(int colors){
        value = 0;
        for(int i=0;i<colors;i++){
            domain.push_back(i+1);
        }
    }
};

void initializeMap(vector<vector<int> > &M,int size){
    for(int i=0;i<size;i++){
        vector<int> v(size);
        M.push_back(v);
    }
}

int SELECT_UNASSIGNED_VARIABLE(vector<Node> nodes){
    for(int i=0;i<nodes.size();i++){
        if(nodes[i].value == 0)
            return i;
    }
    return -1;
}

bool AC3(vector<Node> nodes,vector<vector<int> > M,int var,int color){
    nodes[var].value = color;
    for(int i=0;i<nodes.size();i++){
        if(M[var][i] == 1){
            if(nodes[i].value == color)
                return false;
            /**Remove from domain*/
            if(nodes[i].value == 0){
            vector<int>::iterator position = find(nodes[i].domain.begin(), nodes[i].domain.end(), color);
            if (position != nodes[i].domain.end())
                nodes[i].domain.erase(position);

            if(nodes[i].domain.size() == 0){
                 return false;
            }

            vector<int>::iterator new_color;

            for (new_color = nodes[i].domain.begin(); new_color < nodes[i].domain.end(); new_color++){
                if (AC3(nodes,M,i,*new_color)){
                    return true;
                }
            }
            }
        }
    }
    return true;
}

bool MAC(vector<Node> &nodes,vector<vector<int> > M){
    int var = SELECT_UNASSIGNED_VARIABLE(nodes);
    if(var == -1)
        return true;       /**solved*/

     if(nodes[var].domain.size() == 0)
        return false;

    vector<int>::iterator color;

    for (color = nodes[var].domain.begin(); color < nodes[var].domain.end(); color++){
        if (AC3(nodes,M,var,*color)){
            nodes[var].value = *color;
            if (MAC(nodes,M))
                return true;
            nodes[var].value = 0;
        }
    }
    return false;
}


int main(){
    vector<vector<int> > M;
    int size;
    int colors; /**# colors*/
    ifstream infile;
    infile.open("input.txt");
    infile>>size>>colors;
    initializeMap(M,size);
    for(int i=0;i<size;i++){
        for(int j=0;j<size;j++){
            infile>>M[i][j];
        }
    }
    infile.close();

    /** Print Map
    cout<<size << " "<<colors<<endl;
    for(int i=0;i<size;i++){
        for(int j=0;j<size;j++){
            cout<<M[i][j]<<" ";
        }
        cout<<endl;
    }
    **/
    vector<Node> nodes(size,Node(colors));

     /**Using Backtracking with MAC(Maintaining Arc Consistency).*/
    if(MAC(nodes,M)){
        cout<<"Using Backtracking with MAC(Maintaining Arc Consistency)." <<'\n';
        ofstream outfile;
        outfile.open("output.txt");
        for(int i=0;i<size;i++){
            outfile<<i <<" "<< nodes[i].value << endl;
        }
        outfile.close();
    }
    else
         {ofstream outfile;
        outfile.open("output.txt");
        outfile<<"not_solvable";
        cout<<"not_solvable"<<endl;}

return 0;
}
