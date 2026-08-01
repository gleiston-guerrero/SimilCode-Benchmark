public class SequentialPasses
{
    public static long Run(int[] data)
    {
        long total = 0;
        for (int i = 0; i < data.Length; i++) total += data[i];
        int max = data[0];
        for (int i = 0; i < data.Length; i++) if (data[i] > max) max = data[i];
        int count = 0;
        for (int i = 0; i < data.Length; i++) if (data[i] > 0) count++;
        return total + max + count;
    }
}
