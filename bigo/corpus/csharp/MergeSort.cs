public class MergeSort
{
    public static void Sort(int[] data, int left, int right)
    {
        if (left >= right) return;
        int mid = left + (right - left) / 2;
        Sort(data, left, mid);
        Sort(data, mid + 1, right);
        Merge(data, left, mid, right);
    }

    private static void Merge(int[] data, int left, int mid, int right)
    {
        int[] buffer = new int[right - left + 1];
        int i = left, j = mid + 1, k = 0;
        while (i <= mid && j <= right)
        {
            buffer[k++] = data[i] <= data[j] ? data[i++] : data[j++];
        }
        while (i <= mid) buffer[k++] = data[i++];
        while (j <= right) buffer[k++] = data[j++];
        for (int t = 0; t < buffer.Length; t++) data[left + t] = buffer[t];
    }
}
