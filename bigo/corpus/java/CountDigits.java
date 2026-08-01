public class CountDigits {
    public static int count(int number) {
        if (number == 0) {
            return 1;
        }
        int digits = 0;
        int value = Math.abs(number);
        while (value > 0) {
            value = value / 10;
            digits++;
        }
        return digits;
    }
}
