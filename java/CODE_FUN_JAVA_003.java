package Java.Funcional;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Arrays;

public class CODE_FUN_JAVA_003 {
    private ArrayList<Integer> valores;
    
    public CODE_FUN_JAVA_003() {
        valores = new ArrayList<>(Arrays.asList(64, 34, 25, 12, 22, 11, 90));
    }
    
    public void ordenarAscendente() {
        Collections.sort(valores);
    }
    
    public void mostrarResultado() {
        System.out.print("Números ordenados: ");
        valores.forEach(v -> System.out.print(v + " "));
    }
    
    public static void main(String[] args) {
        CODE_FUN_JAVA_003 clasificador = new CODE_FUN_JAVA_003();
        clasificador.ordenarAscendente();
        clasificador.mostrarResultado();
    }
}
