package Java.Idéntico;

import java.util.Scanner;

public class CODE_IDENT_JAVA_012 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Ingrese la cantidad de números: ");
        int cantidad = scanner.nextInt();
        
        int contadorPares = 0;
        for (int i = 0; i < cantidad; i++) {
            System.out.print("Número " + (i + 1) + ": ");
            int numero = scanner.nextInt();
            
            if (numero % 2 == 0) {
                contadorPares++;
            }
        }
        
        System.out.println("Cantidad de números pares: " + contadorPares);
        scanner.close();
    }
}