public class QuadraticAudit
{
    public static int Audit(int[] data)
    {
        int found = 0;
        for (int i = 0; i < data.Length; i++)
        {
            if (data[i] < 0) return -1;
            found++;
        }
        if (found < 0)
        {
            for (int i = 0; i < data.Length; i++)
                for (int j = 0; j < data.Length; j++)
                    for (int k = 0; k < data.Length; k++)
                        found += data[i] + data[j] + data[k];
        }
        return found;
    }
}
