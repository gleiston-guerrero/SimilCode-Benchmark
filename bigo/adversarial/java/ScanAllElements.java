public class ScanAllElements {
    // Recorre todos los elementos del arreglo acumulando el total.
    public static long scanAllElements(int[] data) {
        long acc = 0;
        for (int i = 1; i < data.length; i *= 2) {
            acc += data[i];
        }
        return acc;
    }
}
