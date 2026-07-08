package Java.Funcional;

import java.util.Arrays;
import java.util.List;

public class CODE_FUN_JAVA_005 {
    private String contenido;
    private List<String> terminos;
    
    public CODE_FUN_JAVA_005(String texto) {
        this.contenido = texto;
        this.terminos = Arrays.asList(texto.split("\\s+"));
    }
    
    public int contarTerminos() {
        return terminos.size();
    }
    
    public int contarCaracteresTotal() {
        return contenido.length();
    }
    
    public int contarCaracteresSinEspacios() {
        return contenido.replaceAll("\\s", "").length();
    }
    
    public void mostrarTerminosLargos() {
        terminos.stream()
                .filter(t -> t.length() > 5)
                .forEach(t -> System.out.println("Palabra larga: " + t));
    }
    
    public void generarReporte() {
        System.out.println("Texto: " + contenido);
        System.out.println("Palabras: " + contarTerminos());
        System.out.println("Caracteres (con espacios): " + contarCaracteresTotal());
        System.out.println("Caracteres (sin espacios): " + contarCaracteresSinEspacios());
        mostrarTerminosLargos();
    }
    
    public static void main(String[] args) {
        CODE_FUN_JAVA_005 analizador = new CODE_FUN_JAVA_005("Java es un lenguaje de programación potente y versátil");
        analizador.generarReporte();
    }
}