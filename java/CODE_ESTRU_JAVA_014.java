package Java.Estructural;

import java.util.Scanner;

public class CODE_ESTRU_JAVA_014 {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        System.out.print("Ingrese la cantidad: ");
        double cantidad = scanner.nextDouble();
        
        System.out.print("Ingrese la unidad origen (m, cm, km): ");
        String unidadOrigen = scanner.next();
        
        System.out.print("Ingrese la unidad destino (m, cm, km): ");
        String unidadDestino = scanner.next();
        
        double resultado = 0;
        
        if (unidadOrigen.equals("m") && unidadDestino.equals("cm")) {
            resultado = cantidad * 100;
        } else if (unidadOrigen.equals("m") && unidadDestino.equals("km")) {
            resultado = cantidad / 1000;
        } else if (unidadOrigen.equals("cm") && unidadDestino.equals("m")) {
            resultado = cantidad / 100;
        } else if (unidadOrigen.equals("km") && unidadDestino.equals("m")) {
            resultado = cantidad * 1000;
        } else if (unidadOrigen.equals(unidadDestino)) {
            resultado = cantidad;
        } else {
            System.out.println("Conversión no soportada");
            return;
        }
        
        System.out.println("Resultado: " + resultado + " " + unidadDestino);
        scanner.close();
    }
}