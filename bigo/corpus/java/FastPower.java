public class FastPower {
    public static long power(long base, int exponent) {
        long result = 1;
        long current = base;
        while (exponent > 0) {
            if ((exponent & 1) == 1) {
                result = result * current;
            }
            current = current * current;
            exponent >>= 1;
        }
        return result;
    }
}
