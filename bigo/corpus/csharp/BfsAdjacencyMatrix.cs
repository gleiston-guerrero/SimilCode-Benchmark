public class BfsAdjacencyMatrix
{
    public static bool[] Traverse(int[,] graph, int n, int start)
    {
        bool[] visited = new bool[n];
        int[] queue = new int[n];
        int head = 0, tail = 0;
        visited[start] = true;
        queue[tail++] = start;
        while (head < tail)
        {
            int current = queue[head++];
            for (int j = 0; j < n; j++)
            {
                if (graph[current, j] == 1 && !visited[j])
                {
                    visited[j] = true;
                    queue[tail++] = j;
                }
            }
        }
        return visited;
    }
}
