package Java.Funcional;


import java.util.OptionalInt;

public class CODE_FUN_JAVA_006 {
    private int[] elementos;
    private int valorBuscado;
    
    public CODE_FUN_JAVA_006(int[] arr, int valor) {
        this.elementos = arr.clone();
        this.valorBuscado = valor;
    }
    
    public OptionalInt buscarPosicion() {
        for(int i = 0; i < elementos.length; i++) {
            if(elementos[i] == valorBuscado) {
                return OptionalInt.of(i);
            }
        }
        return OptionalInt.empty();
    }
    
    public int buscarLineal() {
        for(int indice = 0; indice < elementos.length; indice++) {
            if(elementos[indice] == valorBuscado) {
                return indice;
            }
        }
        return -1;
    }
    
    public void mostrarResultado() {
        int resultado = buscarLineal();
        if(resultado != -1) {
            System.out.println("Número " + valorBuscado + " encontrado en posición: " + resultado);
        } else {
            System.out.println("Número " + valorBuscado + " no encontrado");
        }
    }
    
    public static void main(String[] args) {
        int[] datos = {10, 25, 30, 45, 55, 60, 75};
        CODE_FUN_JAVA_006 localizador = new CODE_FUN_JAVA_006(datos, 45);
        localizador.mostrarResultado();
    }
}