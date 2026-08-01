public class QuickSortLastPivot {
    public static void sort(int[] data, int low, int high) {
        if (low < high) {
            int p = partition(data, low, high);
            sort(data, low, p - 1);
            sort(data, p + 1, high);
        }
    }

    private static int partition(int[] data, int low, int high) {
        int pivot = data[high];
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (data[j] <= pivot) {
                i++;
                int temp = data[i];
                data[i] = data[j];
                data[j] = temp;
            }
        }
        int temp = data[i + 1];
        data[i + 1] = data[high];
        data[high] = temp;
        return i + 1;
    }
}
