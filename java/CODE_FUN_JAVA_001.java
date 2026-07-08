package Java.Funcional;

import java.util.ArrayList;
import java.util.Arrays;

public class CODE_FUN_JAVA_001 {
    private ArrayList<Integer> notas;
    
    public CODE_FUN_JAVA_001() {
        notas = new ArrayList<>(Arrays.asList(85, 90, 78, 92, 88));
    }
    
    public double calcularMedia() {
        return notas.stream().mapToInt(Integer::intValue).average().orElse(0.0);
    }
    
    public String obtenerCategoria(double media) {
        return media >= 90 ? "Excelente: " + media :
               media >= 80 ? "Bueno: " + media : 
               "Regular: " + media;
    }
    
    public static void main(String[] args) {
        CODE_FUN_JAVA_001 sistema = new CODE_FUN_JAVA_001();
        double resultado = sistema.calcularMedia();
        System.out.println(sistema.obtenerCategoria(resultado));
    }
}