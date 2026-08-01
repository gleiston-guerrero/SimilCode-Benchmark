public class FindMax {
    public static int max(int[] data) {
        int best = data[0];
        for (int i = 1; i < data.length; i++) {
            if (data[i] > best) {
                best = data[i];
            }
        }
        return best;
    }
}
