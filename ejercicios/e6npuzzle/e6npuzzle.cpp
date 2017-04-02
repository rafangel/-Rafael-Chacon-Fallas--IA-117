#include <string>
#include <vector>
#include <queue>
#include <map>
#include <cstdio>
using namespace std;

int main(){
	int N,i,j,l;
	vector<int>problem;
    
    //input scans
	scanf("%d",&N);
	for(i=0;i<N*N;i++)scanf("%d",&l),problem.push_back(l);

	int Y=N;
    
    //this code uses map, vector, pair and queue data structures
	map<vector<int>,pair<int,int>>m;
	map<vector<int>,pair<vector<int>,string>>prev;
	queue<vector<int>>q; //FIFO
	vector<int>v;
    vector<int>next;
    
    for(i=0;i<N*Y;i++){//create goal state
        v.push_back(i);
    }
    
    m[v]=make_pair(0,0); //maps vector V with pair (0,0)
	prev[v]=make_pair(v,"");//maps vector V with pair (V,"")
    
	for(q.push(v);!q.empty();){ //insert vector V at the tail of Q
        
		v=q.front();
        q.pop();
        
		int coor=m[v].first; // first value of pair
        
        int x=coor%N; //coordenates of space or 0
        int y=coor/N;
        
		int depth=m[v].second; //second value of pair
		next=v;
		if(0<x){
			swap(v[coor],v[coor-1]); //move O to left
            if(m.find(v)==m.end()){ //use end() function as a heuristic, sorting the vector to a "higher" state
                m[v]=make_pair(coor-1,depth+1);
                q.push(v);
                prev[v]=make_pair(next,"RIGHT");
            }
			swap(v[coor],v[coor-1]);//restore v
		}
		if(x<N-1){
			swap(v[coor],v[coor+1]); //move 0 to right
            if(m.find(v)==m.end()){
                m[v]=make_pair(coor+1,depth+1);
                q.push(v);
                prev[v]=make_pair(next,"LEFT");
            }
			swap(v[coor],v[coor+1]);//restore v
		}
		if(0<y){
			swap(v[coor],v[coor-N]); //move 0 up
            if(m.find(v)==m.end()){
                m[v]=make_pair(coor-N,depth+1);
                q.push(v);
                prev[v]=make_pair(next,"DOWN");
            }
			swap(v[coor],v[coor-N]);//restore v
		}
		if(y<Y-1){
			swap(v[coor],v[coor+N]); // move 0 down
            if(m.find(v)==m.end()){
                m[v]=make_pair(coor+N,depth+1);
                q.push(v);
                prev[v]=make_pair(next,"UP");
            }
			swap(v[coor],v[coor+N]);//restore v
		}
        if(m.find(problem)!=m.end()){ //finalization state (input state)
            break;
        }
	}

	printf("%d\n",m[problem].second); //total depth
	while(prev[problem].first!=problem){
		printf("%s\n",prev[problem].second.c_str());
		problem=prev[problem].first; //advance problem to next step (vector) in prev
	}
}
