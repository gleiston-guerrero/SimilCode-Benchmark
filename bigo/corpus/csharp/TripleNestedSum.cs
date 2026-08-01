public class TripleNestedSum
{
    public static long Total(int[] data)
    {
        long acc = 0;
        int n = data.Length;
        for (int i = 0; i < n; i++)
        {
            for (int j = 0; j < n; j++)
            {
                for (int k = 0; k < n; k++)
                {
                    acc += data[i] + data[j] + data[k];
                }
            }
        }
        return acc;
    }
}
