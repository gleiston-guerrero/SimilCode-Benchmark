public class ReverseArray
{
    public static void Reverse(int[] data)
    {
        int left = 0;
        int right = data.Length - 1;
        while (left < right)
        {
            int temp = data[left];
            data[left] = data[right];
            data[right] = temp;
            left++;
            right--;
        }
    }
}
