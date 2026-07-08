package Java.Idéntico;

public class CODE_IDENT_JAVA_004 {
    public static void main(String[] args) {
        double num1 = 15.5;
        double num2 = 4.2;
        String operacion = "+";
        double resultado = 0;
        
        if(operacion.equals("+")) {
            resultado = num1 + num2;
        } else if(operacion.equals("-")) {
            resultado = num1 - num2;
        } else if(operacion.equals("*")) {
            resultado = num1 * num2;
        } else if(operacion.equals("/")) {
            if(num2 != 0) {
                resultado = num1 / num2;
            } else {
                System.out.println("Error: División por cero");
                return;
            }
        }
        
        System.out.println(num1 + " " + operacion + " " + num2 + " = " + resultado);
    }
}
