public class BinarySearchRecursive
{
    public static int Search(int[] sorted, int target, int low, int high)
    {
        if (low > high) return -1;
        int mid = low + (high - low) / 2;
        if (sorted[mid] == target) return mid;
        if (sorted[mid] < target) return Search(sorted, target, mid + 1, high);
        return Search(sorted, target, low, mid - 1);
    }
}
