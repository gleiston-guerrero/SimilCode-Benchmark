public class SelectionSort
{
    public static void Sort(int[] data)
    {
        for (int i = 0; i < data.Length - 1; i++)
        {
            int min = i;
            for (int j = i + 1; j < data.Length; j++)
            {
                if (data[j] < data[min]) min = j;
            }
            int temp = data[i];
            data[i] = data[min];
            data[min] = temp;
        }
    }
}
