package Java.Estructural;

import java.util.Scanner;

public class CODE_ESTRU_JAVA_012 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Ingrese la cantidad de palabras: ");
        int cantidad = scanner.nextInt();
        scanner.nextLine(); // Consumir el salto de línea
        
        int contadorVocales = 0;
        for (int i = 0; i < cantidad; i++) {
            System.out.print("Palabra " + (i + 1) + ": ");
            String palabra = scanner.nextLine().toLowerCase();
            
            for (char letra : palabra.toCharArray()) {
                if (letra == 'a' || letra == 'e' || letra == 'i' || 
                    letra == 'o' || letra == 'u') {
                    contadorVocales++;
                }
            }
        }
        
        System.out.println("Cantidad total de vocales: " + contadorVocales);
        scanner.close();
    }
}
