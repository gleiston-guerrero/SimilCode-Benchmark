public class HasDuplicatesNaive {
    public static boolean check(int[] data) {
        for (int i = 0; i < data.length; i++) {
            for (int j = i + 1; j < data.length; j++) {
                if (data[i] == data[j]) {
                    return true;
                }
            }
        }
        return false;
    }
}
