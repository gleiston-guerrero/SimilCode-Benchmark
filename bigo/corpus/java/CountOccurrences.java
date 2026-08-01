public class CountOccurrences {
    public static int count(int[] data, int target) {
        int total = 0;
        for (int i = 0; i < data.length; i++) {
            if (data[i] == target) {
                total++;
            }
        }
        return total;
    }
}
