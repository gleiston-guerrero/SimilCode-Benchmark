public class MatrixAddition
{
    public static int[,] Add(int[,] a, int[,] b, int n)
    {
        int[,] result = new int[n, n];
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                result[i, j] = a[i, j] + b[i, j];
            }
        }
        return result;
    }
}
