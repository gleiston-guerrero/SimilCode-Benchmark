public class SubsetSumBruteForce
{
    public static bool Exists(int[] data, int index, int target)
    {
        if (target == 0) return true;
        if (index >= data.Length) return false;
        if (Exists(data, index + 1, target - data[index])) return true;
        return Exists(data, index + 1, target);
    }
}
