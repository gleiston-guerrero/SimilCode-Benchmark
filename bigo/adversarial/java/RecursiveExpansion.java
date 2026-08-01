public class RecursiveExpansion {
    private static long[] cache;

    public static long expand(int n) {
        if (cache == null) {
            cache = new long[n + 1];
        }
        if (n <= 1) {
            return n;
        }
        if (cache[n] != 0) {
            return cache[n];
        }
        cache[n] = expand(n - 1) + expand(n - 2);
        return cache[n];
    }
}
