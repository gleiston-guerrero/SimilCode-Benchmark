package Java.Idéntico;

public class ConversorDeUnidades {
    public static void main(String[] args) {
        double distanciaEnMetros = 1500.0;
        String tipoDeConversion = "metros_a_kilometros";
        double valorConvertido = 0.0;
        
        if(tipoDeConversion.equals("metros_a_kilometros")) {
            valorConvertido = distanciaEnMetros / 1000.0;
        } else if(tipoDeConversion.equals("metros_a_millas")) {
            valorConvertido = distanciaEnMetros / 1609.34;
        } else if(tipoDeConversion.equals("metros_a_pies")) {
            valorConvertido = distanciaEnMetros * 3.28084;
        } else if(tipoDeConversion.equals("metros_a_pulgadas")) {
            valorConvertido = distanciaEnMetros * 39.3701;
        }
        
        System.out.println(distanciaEnMetros + " metros = " + valorConvertido + " en " + tipoDeConversion);
        
        if(valorConvertido > 1.0) {
            System.out.println("Resultado grande");
        } else {
            System.out.println("Resultado pequeño");
        }
    }
}
