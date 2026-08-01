public class CountInversions
{
    public static long Count(int[] data, int left, int right)
    {
        if (left >= right) return 0;
        int mid = left + (right - left) / 2;
        long total = Count(data, left, mid) + Count(data, mid + 1, right);
        int[] buffer = new int[right - left + 1];
        int i = left, j = mid + 1, k = 0;
        while (i <= mid && j <= right)
        {
            if (data[i] <= data[j]) buffer[k++] = data[i++];
            else { total += (mid - i + 1); buffer[k++] = data[j++]; }
        }
        while (i <= mid) buffer[k++] = data[i++];
        while (j <= right) buffer[k++] = data[j++];
        for (int t = 0; t < buffer.Length; t++) data[left + t] = buffer[t];
        return total;
    }
}
