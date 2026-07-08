package Java.Funcional;

public class CODE_FUN_JAVA_004 {
    private double primerOperando;
    private double segundoOperando;
    private char simbolo;
    
    public CODE_FUN_JAVA_004(double a, double b, char op) {
        this.primerOperando = a;
        this.segundoOperando = b;
        this.simbolo = op;
    }
    
    public double ejecutarOperacion() {
        switch(simbolo) {
            case '+': return primerOperando + segundoOperando;
            case '-': return primerOperando - segundoOperando;
            case '*': return primerOperando * segundoOperando;
            case '/': 
                if(segundoOperando == 0) throw new ArithmeticException("División por cero");
                return primerOperando / segundoOperando;
            default: throw new IllegalArgumentException("Operación no válida");
        }
    }
    
    public void mostrarResultado() {
        try {
            double res = ejecutarOperacion();
            System.out.println(primerOperando + " " + simbolo + " " + segundoOperando + " = " + res);
        } catch(Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }
    
    public static void main(String[] args) {
        CODE_FUN_JAVA_004 proc = new CODE_FUN_JAVA_004(15.5, 4.2, '+');
        proc.mostrarResultado();
    }
}