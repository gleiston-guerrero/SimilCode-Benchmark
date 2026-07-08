package Java.Estructural;

public class CODE_ESTRU_JAVA_008 {
    public static void main(String[] args) {
        double dolares = 1000.0;
        String tipoConversion = "dolares_a_euros";
        double resultado = 0.0;
        
        if(tipoConversion.equals("dolares_a_euros")) {
            resultado = dolares * 0.85;
        } else if(tipoConversion.equals("dolares_a_pesos")) {
            resultado = dolares * 18.50;
        } else if(tipoConversion.equals("dolares_a_yenes")) {
            resultado = dolares * 110.0;
        } else if(tipoConversion.equals("dolares_a_libras")) {
            resultado = dolares * 0.75;
        }
        
        System.out.println(dolares + " dólares = " + resultado + " en " + tipoConversion);
        
        if(resultado > 1000.0) {
            System.out.println("Cantidad alta");
        } else {
            System.out.println("Cantidad baja");
        }
    }
}