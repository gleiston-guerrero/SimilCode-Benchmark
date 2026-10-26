import java.util.Scanner;

/*
 * Este programa solicita una serie de valores enteros al usuario
 * y determina cuántos de ellos son números pares.
 */
public class AnalizadorDePares {

    public static void main(String[] argumentos) {
        Scanner entradaConsola = new Scanner(System.in);
        
        System.out.print("Ingrese la cantidad de números: ");
        int totalIteraciones = entradaConsola.nextInt();
        
        // Delegamos la lógica principal a un método auxiliar
        int totalPares = procesarValores(totalIteraciones, entradaConsola);
        
        System.out.println("Cantidad de números pares: " + totalPares);
        
        entradaConsola.close();
    }

    /**
     * Lee los datos ingresados y cuenta cuántos son pares usando un ciclo while.
     */
    private static int procesarValores(int limite, Scanner lector) {
        int paresEncontrados = 0;
        int iterador = 1;
        
        // Reemplazo del ciclo for original por una estructura while
        while (iterador <= limite) {
            System.out.print("Número " + iterador + ": ");
            int valorIngresado = lector.nextInt();
            
            if (verificarParidad(valorIngresado)) {
                paresEncontrados = paresEncontrados + 1;
            }
            
            iterador++;
        }
        
        return paresEncontrados;
    }

    // Método extraído para evaluar si un entero es par
    private static boolean verificarParidad(int numeroEvaluar) {
        return (numeroEvaluar % 2) == 0;
    }
}
