package Java.Idéntico;

public class CalculadoraBasica {
    public static void main(String[] args) {
        double valorUno = 15.5;
        double valorDos = 4.2;
        String operador = "+";
        double total = 0;
        
        if(operador.equals("+")) {
            total = valorUno + valorDos;
        } else if(operador.equals("-")) {
            total = valorUno - valorDos;
        } else if(operador.equals("*")) {
            total = valorUno * valorDos;
        } else if(operador.equals("/")) {
            if(valorDos != 0) {
                total = valorUno / valorDos;
            } else {
                System.out.println("Error: División por cero");
                return;
            }
        }
        
        System.out.println(valorUno + " " + operador + " " + valorDos + " = " + total);
    }
}
