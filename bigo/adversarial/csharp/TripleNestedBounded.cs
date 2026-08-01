public class TripleNestedBounded
{
    public static long Compute(int[,] grid, int n)
    {
        long acc = 0;
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                for (int k = 0; k < 3; k++)
                {
                    acc += grid[i, j] + k;
                }
            }
        }
        return acc;
    }
}
