public class KadaneMaxSubarray
{
    public static int MaxSum(int[] data)
    {
        int best = data[0];
        int running = data[0];
        for (int i = 1; i < data.Length; i++)
        {
            running = Math.Max(data[i], running + data[i]);
            best = Math.Max(best, running);
        }
        return best;
    }
}
