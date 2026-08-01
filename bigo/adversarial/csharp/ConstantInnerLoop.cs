public class ConstantInnerLoop
{
    public static long Process(int[] data)
    {
        long acc = 0;
        for (int i = 0; i < data.Length; i++)
        {
            for (int j = 0; j < 100; j++)
            {
                acc += data[i] * j;
            }
        }
        return acc;
    }
}
