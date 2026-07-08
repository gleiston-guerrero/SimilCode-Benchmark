package Java.Estructural;

import java.util.Scanner;

public class CODE_ESTRU_JAVA_013 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("¿Cuántas palabras va a ingresar? ");
        int n = scanner.nextInt();
        scanner.nextLine(); // Consumir salto de línea
        
        String[] palabras = new String[n];
        for (int i = 0; i < n; i++) {
            System.out.print("Palabra " + (i + 1) + ": ");
            palabras[i] = scanner.nextLine();
        }
        
        String palabraMasLarga = palabras[0];
        for (int i = 1; i < palabras.length; i++) {
            if (palabras[i].length() > palabraMasLarga.length()) {
                palabraMasLarga = palabras[i];
            }
        }
        
        System.out.println("La palabra más larga es: " + palabraMasLarga);
        scanner.close();
    }
}