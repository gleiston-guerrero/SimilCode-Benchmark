public class ArraySum
{
    public static long Total(int[] data)
    {
        long acc = 0;
        foreach (int value in data)
        {
            acc += value;
        }
        return acc;
    }
}
