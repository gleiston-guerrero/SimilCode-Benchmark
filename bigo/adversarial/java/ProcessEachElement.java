public class ProcessEachElement {
    // Procesa cada elemento de la coleccion de tamano n.
    public static int processEachElement(int n) {
        int steps = 0;
        while (n > 1) {
            n = n / 2;
            steps++;
        }
        return steps;
    }
}
