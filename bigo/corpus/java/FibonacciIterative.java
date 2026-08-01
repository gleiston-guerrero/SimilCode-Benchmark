public class FibonacciIterative {
    public static long fib(int n) {
        if (n <= 1) {
            return n;
        }
        long previous = 0;
        long current = 1;
        for (int i = 2; i <= n; i++) {
            long next = previous + current;
            previous = current;
            current = next;
        }
        return current;
    }
}
