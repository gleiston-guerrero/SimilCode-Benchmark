package Java.Idéntico;

public class CODE_IDENT_JAVA_008 {
    public static void main(String[] args) {
        double metros = 1500.0;
        String tipoConversion = "metros_a_kilometros";
        double resultado = 0.0;
        
        if(tipoConversion.equals("metros_a_kilometros")) {
            resultado = metros / 1000.0;
        } else if(tipoConversion.equals("metros_a_millas")) {
            resultado = metros / 1609.34;
        } else if(tipoConversion.equals("metros_a_pies")) {
            resultado = metros * 3.28084;
        } else if(tipoConversion.equals("metros_a_pulgadas")) {
            resultado = metros * 39.3701;
        }
        
        System.out.println(metros + " metros = " + resultado + " en " + tipoConversion);
        
        if(resultado > 1.0) {
            System.out.println("Resultado grande");
        } else {
            System.out.println("Resultado pequeño");
        }
    }
}