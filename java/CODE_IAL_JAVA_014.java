package Java.Identico;

import java.util.Scanner;

public class CALCULADORA {
    public static void main(String[] args) {
        Scanner entrada = new Scanner(System.in);
        
        System.out.print("Ingrese el primer número: ");
        double valor1 = entrada.nextDouble();
        
        System.out.print("Ingrese el segundo número: ");
        double valor2 = entrada.nextDouble();
        
        System.out.print("Ingrese la operación (+, -, *, /): ");
        char operador = entrada.next().charAt(0);
        
        double resul = 0;
        
        if (operador == '+') {
            resul = valor1 + valor2;
        } else if (operador == '-') {
            resul = valor1 - valor2;
        } else if (operador == '*') {
            resul = valor1 * valor2;
        } else if (operador == '/') {
            if (valor2 != 0) {
                resul = valor1 / valor2;
            } else {
                System.out.println("Error: División por cero");
                return;
            }
        } else {
            System.out.println("Operación no válida");
            return;
        }
        
        System.out.println("Resultado: " + resul);
        entrada.close();
    }
}
