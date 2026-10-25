package Java.Nuevo;

import java.util.Scanner;

public class CALCULADORA_014 {
    public static void main(String[] args) {
        Scanner entrada = new Scanner(System.in);
        
        System.out.print("Ingrese el primer número: ");
        double primerNumero = entrada.nextDouble();
        
        System.out.print("Ingrese el segundo número: ");
        double segundoNumero = entrada.nextDouble();
        
        System.out.print("Ingrese la operación (+, -, *, /): ");
        char operador = entrada.next().charAt(0);
        
        double resul = 0;
        
        switch (operador) {
            case '+':
                resul = primerNumero + segundoNumero;
                break;
            case '-':
                resul = primerNumero - segundoNumero;
                break;
            case '*':
                resul = primerNumero * segundoNumero;
                break;
            case '/':
                if (segundoNumero != 0) {
                    resul = primerNumero / segundoNumero;
                } else {
                    System.out.println("Error: División por cero");
                    return;
                }
                break;
            default:
                System.out.println("Operación no válida");
                return;
        }
        
        System.out.println("Resultado: " + resul);
        entrada.close();
    }
}
