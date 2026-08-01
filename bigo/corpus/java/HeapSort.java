public class HeapSort {
    public static void sort(int[] data) {
        int n = data.length;
        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(data, n, i);
        }
        for (int i = n - 1; i > 0; i--) {
            int temp = data[0];
            data[0] = data[i];
            data[i] = temp;
            heapify(data, i, 0);
        }
    }

    private static void heapify(int[] data, int size, int root) {
        int largest = root;
        int left = 2 * root + 1;
        int right = 2 * root + 2;
        if (left < size && data[left] > data[largest]) largest = left;
        if (right < size && data[right] > data[largest]) largest = right;
        if (largest != root) {
            int temp = data[root];
            data[root] = data[largest];
            data[largest] = temp;
            heapify(data, size, largest);
        }
    }
}
