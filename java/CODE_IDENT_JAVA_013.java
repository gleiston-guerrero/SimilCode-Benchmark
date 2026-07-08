package Java.Idéntico;

import java.util.Scanner;

public class CODE_IDENT_JAVA_013 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("¿Cuántos números va a ingresar? ");
        int n = scanner.nextInt();
        
        int[] numeros = new int[n];
        for (int i = 0; i < n; i++) {
            System.out.print("Número " + (i + 1) + ": ");
            numeros[i] = scanner.nextInt();
        }
        
        int maximo = numeros[0];
        for (int i = 1; i < numeros.length; i++) {
            if (numeros[i] > maximo) {
                maximo = numeros[i];
            }
        }
        
        System.out.println("El número máximo es: " + maximo);
        scanner.close();
    }
}