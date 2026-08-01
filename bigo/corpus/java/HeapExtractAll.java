public class HeapExtractAll {
    public static int[] drain(int[] heap) {
        int size = heap.length;
        int[] output = new int[size];
        for (int i = size / 2 - 1; i >= 0; i--) {
            siftDown(heap, size, i);
        }
        for (int out = 0; size > 0; out++) {
            output[out] = heap[0];
            heap[0] = heap[size - 1];
            size--;
            siftDown(heap, size, 0);
        }
        return output;
    }

    private static void siftDown(int[] heap, int size, int root) {
        while (true) {
            int smallest = root;
            int left = 2 * root + 1;
            int right = 2 * root + 2;
            if (left < size && heap[left] < heap[smallest]) smallest = left;
            if (right < size && heap[right] < heap[smallest]) smallest = right;
            if (smallest == root) return;
            int temp = heap[root];
            heap[root] = heap[smallest];
            heap[smallest] = temp;
            root = smallest;
        }
    }
}
