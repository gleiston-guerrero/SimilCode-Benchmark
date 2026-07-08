package Java.Funcional;

import java.util.HashMap;
import java.util.Map;

public class CODE_FUN_JAVA_008 {
    private Map<String, Double> factoresConversion;
    private double valorOriginal;
    
    public CODE_FUN_JAVA_008(double valor) {
        this.valorOriginal = valor;
        inicializarFactores();
    }
    
    private void inicializarFactores() {
        factoresConversion = new HashMap<>();
        factoresConversion.put("metros_a_kilometros", 0.001);
        factoresConversion.put("metros_a_millas", 1.0 / 1609.34);
        factoresConversion.put("metros_a_pies", 3.28084);
        factoresConversion.put("metros_a_pulgadas", 39.3701);
    }
    
    public double convertir(String tipoTransformacion) {
        Double factor = factoresConversion.get(tipoTransformacion);
        return factor != null ? valorOriginal * factor : 0.0;
    }
    
    public void mostrarConversion(String tipo) {
        double valorConvertido = convertir(tipo);
        System.out.println(valorOriginal + " metros = " + valorConvertido + " en " + tipo);
        
        String categoria = valorConvertido > 1.0 ? "Resultado grande" : "Resultado pequeño";
        System.out.println(categoria);
    }
    
    public static void main(String[] args) {
        CODE_FUN_JAVA_008 transformador = new CODE_FUN_JAVA_008(1500.0);
        transformador.mostrarConversion("metros_a_kilometros");
    }
}
