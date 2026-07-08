package Java.Funcional;

import java.util.Scanner;

public class CODE_FUN_JAVA_014 {
    private double primerOperando;
    private double segundoOperando;
    private String tipoOperacion;
    
    public void capturarDatos() {
        Scanner input = new Scanner(System.in);
        
        System.out.print("Primer operando: ");
        this.primerOperando = input.nextDouble();
        
        System.out.print("Segundo operando: ");
        this.segundoOperando = input.nextDouble();
        
        System.out.print("Tipo de operación (suma, resta, multiplicacion, division): ");
        this.tipoOperacion = input.next().toLowerCase();
        
        input.close();
    }
    
    public double ejecutarCalculo() {
        return switch (tipoOperacion) {
            case "suma" -> primerOperando + segundoOperando;
            case "resta" -> primerOperando - segundoOperando;
            case "multiplicacion" -> primerOperando * segundoOperando;
            case "division" -> dividir();
            default -> {
                System.out.println("Operación no reconocida");
                yield 0;
            }
        };
    }
    
    private double dividir() {
        if (segundoOperando == 0) {
            System.out.println("Error: No se puede dividir por cero");
            return 0;
        }
        return primerOperando / segundoOperando;
    }
    
    public void mostrarResultado(double resultado) {
        System.out.println("El resultado de la operación es: " + resultado);
    }
    
    public static void main(String[] args) {
        CODE_FUN_JAVA_014 calculadora = new CODE_FUN_JAVA_014();
        calculadora.capturarDatos();
        double resultado = calculadora.ejecutarCalculo();
        calculadora.mostrarResultado(resultado);
    }
}
