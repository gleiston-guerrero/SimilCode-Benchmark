public class DfsAdjacencyMatrix {
    public static void traverse(int[][] graph, int n, int current, boolean[] visited) {
        visited[current] = true;
        for (int j = 0; j < n; j++) {
            if (graph[current][j] == 1 && !visited[j]) {
                traverse(graph, n, j, visited);
            }
        }
    }
}
