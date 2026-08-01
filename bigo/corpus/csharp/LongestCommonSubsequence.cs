public class LongestCommonSubsequence
{
    public static int Length(string a, string b)
    {
        int n = a.Length, m = b.Length;
        int[,] table = new int[n + 1, m + 1];
        for (int i = 1; i <= n; i++)
        {
            for (int j = 1; j <= m; j++)
            {
                if (a[i - 1] == b[j - 1]) table[i, j] = table[i - 1, j - 1] + 1;
                else table[i, j] = Math.Max(table[i - 1, j], table[i, j - 1]);
            }
        }
        return table[n, m];
    }
}
