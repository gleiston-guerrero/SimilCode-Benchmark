package Java.Idéntico;

public class CODE_IDENT_JAVA_005 {
    public static void main(String[] args) {
        String texto = "Java es un lenguaje de programación potente y versátil";
        String[] palabras = texto.split(" ");
        int totalPalabras = palabras.length;
        int totalCaracteres = texto.length();
        int caracteresConEspacios = texto.replace(" ", "").length();
        
        System.out.println("Texto: " + texto);
        System.out.println("Palabras: " + totalPalabras);
        System.out.println("Caracteres (con espacios): " + totalCaracteres);
        System.out.println("Caracteres (sin espacios): " + caracteresConEspacios);
        
        for(String palabra : palabras) {
            if(palabra.length() > 5) {
                System.out.println("Palabra larga: " + palabra);
            }
        }
    }
}