
#include <cstdio>
#include <cstring>
#include <string>
#include <cmath>
#include <cstdlib>
#include <map>
#include <set>
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;


int main() {
    int tt;
    scanf("%d",&tt);
    while (tt--)
    {
        int n,m;
        scanf("%d %d",&n,&m);
        vector<int> con[1001];
        for (int i=0;i<m;i++)
        {
            int a,b;
            scanf("%d %d",&a,&b);
            con[a].push_back(b); // matriz de conexiones
            con[b].push_back(a);
        }
        int s;
        scanf("%d",&s); //inicial
        int dis[1001];//lista de distancias
        memset(dis,-1,sizeof(dis)); // todos los nodos seteado como no visitados
        int frontera[1001],be=0,ed=1; // FIFO 
        frontera[0] = s;
        dis[s] = 0;  
        while(be<ed)
        {
            for (int i=0;i<con[frontera[be]].size();i++)//recorre todos los hijos
            {
                if (dis[con[frontera[be]][i]] == -1)//nodo no visitado
                {
                    dis[con[frontera[be]][i]] = dis[frontera[be]] + 1;//aumenta la distancia
                    frontera[ed++] = con[frontera[be]][i];//agrega el hijo i a la frontera
                }
            }
            be++;
        }
        for (int i=1;i<=n;i++)
            if (i == s)
                continue;
            else if (dis[i] == -1)
                printf("%d ",-1);
            else
                printf("%d ",dis[i]*6); //fixing para valor 6 de distancia
        printf("\n");
    }
    return 0;
}
