//with the medoids base heuristic algorithm 
#include <vector>
#include <iostream>

using namespace std;

double sum_total(
    const vector<int> medoids,
    const vector<vector<double>> dist)
{
    int n = dist.size();
    double sum = 0;

    for(int i=0;i<n;i++){
        double best = -1;

        for(int m : medoids)
            best = max(best, dist[i][m]);

        sum = sum+best;
    }
    return sum;
}

int main(){
    vector<vector<double>> dist={
        {1,0.5,0,0,0},
        {0.5,1,0,0,0},
        {0,0,1,0.5,0.5},
        {0,0,0.5,1,0},
        {0,0,0.5,0,1}
    };
    vector<int> medoids = {0,1};
    
    int n = dist.size();
    int k = medoids.size();

    bool mejora = true;

    while(mejora){

        mejora = false;
        double bestsum = sum_total(medoids,dist);

        for(int m=0;m<k;m++){
            for(int i=0;i<n;i++){

                vector<int> nuevo = medoids;
                nuevo[m] = i;

                double c = sum_total(nuevo,dist);

                if(c > bestsum){
                    medoids = nuevo;
                    bestsum = c;
                    mejora = true;
                }
            cout<<"nuevo: "<<nuevo[0]<<nuevo[1]<<"\n";
            cout<<"medoids: "<<medoids[0]<<medoids[1]<<"\n";
            }
        }
    }
}