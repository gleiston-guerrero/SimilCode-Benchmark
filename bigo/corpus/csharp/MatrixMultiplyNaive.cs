public class MatrixMultiplyNaive
{
    public static int[,] Multiply(int[,] a, int[,] b, int n)
    {
        int[,] result = new int[n, n];
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                int acc = 0;
                for (int k = 0; k < n; k++)
                {
                    acc += a[i, k] * b[k, j];
                }
                result[i, j] = acc;
            }
        }
        return result;
    }
}
