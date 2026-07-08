package Java.Idéntico;

import java.util.Random;

public class CODE_IDENT_JAVA_007 {
    public static void main(String[] args) {
        Random random = new Random();
        int cantidad = 10;
        int minimo = 1;
        int maximo = 100;
        int suma = 0;
        
        System.out.println("Números generados:");
        for(int i = 0; i < cantidad; i++) {
            int numero = random.nextInt(maximo - minimo + 1) + minimo;
            System.out.print(numero + " ");
            suma += numero;
        }
        
        double promedio = suma / (double)cantidad;
        System.out.println("\nSuma total: " + suma);
        System.out.println("Promedio: " + promedio);
    }
}