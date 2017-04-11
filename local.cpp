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

bool isConsistent(vector<Node> nodes,vector<vector<int> > M,int var,int color){
    for(int i=0;i<nodes.size();i++){    //Seriously!!
        if(M[var][i] == 1 && nodes[i].value == color)
            return false;
    }
    return true;
}

bool IS_SOLUTION(vector<Node> nodes,vector<vector<int> > M){
     for(int i=0;i<nodes.size();i++){
        if(!isConsistent(nodes,M,i,nodes[i].value))
            return false;
    }
    return true;
}

int SELECT_INCONSISTENT_VARIABLE(vector<Node> nodes,vector<vector<int> > M){
    int k=nodes.size();
    while(1){
    int l=rand()%k;
    cout<<"r"<<l;
    if(!isConsistent(nodes,M,l,nodes[l].value))
           {return l;}
    }
    // for(int i=0;i<nodes.size();i++){
    //     if(!isConsistent(nodes,M,i,nodes[i].value))
    //         return i;
}

int MIN_CONFLICTS_VALUE(vector<Node> nodes,vector<vector<int> > M,int var){
    map<int,int> conflict;
    vector<int>::iterator color;
    for (color = nodes[var].domain.begin(); color < nodes[var].domain.end() ; color++){
        conflict[*color] = 0;
    }
    for(int j=0;j<nodes.size();j++){
        if(M[var][j] == 1){
            conflict[nodes[j].value]++;
        }
    }
     int choosen = 0;
     int count = INT_MAX;
     for (map<int,int>::iterator it=conflict.begin(); it!=conflict.end(); ++it){
        if(it->second <= count){
            count = it->second;
            choosen = it->first;
        }
        cout<<count<<"*"<<choosen<<endl;
     }
    return choosen;
}

bool RANDOM_SOLUTION(vector<Node> &nodes,vector<vector<int> > M){
     for(int i=0;i<nodes.size();i++){
        int domain_count = nodes[i].domain.size();
        if(domain_count == 0)
            return false;
        int r = rand()%domain_count;
        nodes[i].value = nodes[i].domain[r];
        cout<<i<<"$"<<nodes[i].value<<endl;
        /**update domains
        for(int j=i+1;j<nodes.size();j++){
            if(M[i][j] == 1){
                //delete from domain
                 vector<int>::iterator position = find(nodes[j].domain.begin(), nodes[j].domain.end(), nodes[i].value);
                if (position != nodes[j].domain.end())
                    nodes[j].domain.erase(position);
            }
        }*/
    }
    return true;
}

int LOCAL_SEARCH(vector<Node> &nodes,vector<vector<int> > M,int steps){
    if(!RANDOM_SOLUTION(nodes,M))
        return -1;
    if(IS_SOLUTION(nodes,M))
        return 0;
    for(int i=0;i<steps;i++){
        int var = SELECT_INCONSISTENT_VARIABLE(nodes,M);
        int color = MIN_CONFLICTS_VALUE(nodes,M,var);
        nodes[var].value = color;
        cout<<var<<" "<<color<<endl;
        if(IS_SOLUTION(nodes,M))
            return i+1;
    }
    return -1;
}

int main(){
    vector<vector<int> > M;
    int size;
    int colors,steps; /**# colors*/
    ifstream infile;
    infile.open("input.txt");
    infile>>size>>colors>>steps;
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

    /**Using Local Search with Min-Conflicts*/
    int moves = LOCAL_SEARCH(nodes,M,steps);
    if(moves != -1){
        ofstream outfile;
        outfile.open("output.txt");
        outfile << moves << endl;
        cout<<"Map coloring using Local Search with Min-Conflicts using " << moves<< " steps." <<'\n';
        
        for(int i=0;i<size;i++){
            outfile<<i <<" "<< nodes[i].value << endl;
        }
        
        outfile.close();
    }
    else
        {ofstream outfile;
        outfile.open("output.txt");
        outfile<<"-1\n";
        for(int i=0;i<size;i++){
            outfile<<i <<" "<< nodes[i].value << endl;
        }
        cout<<"not_solvable"<<endl;}
    return 0;
}



