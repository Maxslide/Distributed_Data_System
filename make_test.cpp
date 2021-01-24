#include "bits/stdc++.h"
#include "ext/pb_ds/assoc_container.hpp"
#include "ext/pb_ds/tree_policy.hpp"

using namespace std;
using namespace __gnu_pbds;


#define ll long long int
#define pb push_back
#define mp make_pair
#define ff first
#define ss second
#define all(a) a.begin(),a.end()

typedef tree <ll, null_type, less <ll>, rb_tree_tag, tree_order_statistics_node_update> ordered_set;
// order_of_key(val): returns the number of values less than val
// find_by_order(k): returns an iterator to the kth largest element (0-based)
int adj[101][101];
int main(void)
{
	ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    srand (time(NULL));
    int N = rand() % 100 + 1, M = rand() % 500 + 1;
    fstream out_stream;
    out_stream.open("in.txt", ios::out);
    M = min(M, (N * ( N - 1)) / 2);
    vector<pair<ll, ll>> edges;
    for(int i = 1; i <= N; i++) {
    	for(int j = i + 1; j <= N; j++) {
    		edges.push_back({i, j});
    	}
    }
    out_stream << N << " " << M << "\n";
    int size = edges.size();
    while(M--) {
    	int ind = rand() % size;
    	out_stream << edges[ind].first << " " << edges[ind].second << "\n";
    	edges.erase(edges.begin() + ind);
    	size--;
    }
}