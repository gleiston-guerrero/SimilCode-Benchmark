public class HeapInsert
{
    public static void Insert(int[] heap, ref int size, int value)
    {
        heap[size] = value;
        int i = size;
        size++;
        while (i > 0)
        {
            int parent = (i - 1) / 2;
            if (heap[parent] <= heap[i]) break;
            int temp = heap[parent];
            heap[parent] = heap[i];
            heap[i] = temp;
            i = parent;
        }
    }
}
