package Java.Distinto;

public class ANALIZADOR_TEXTO {
    public static void main(String[] args) {
        String frase = "Java es un lenguaje de programación potente y versátil";
        String[] elementos = frase.split(" ");
        int cantidadPalabras = elementos.length;
        int cantidadCaracteres = frase.length();
        int caracteresSinEspacios = frase.replace(" ", "").length();
        
        System.out.println("Texto: " + frase);
        System.out.println("Palabras: " + cantidadPalabras);
        System.out.println("Caracteres (con espacios): " + cantidadCaracteres);
        System.out.println("Caracteres (sin espacios): " + caracteresSinEspacios);
        
        for(String elemento : elementos) {
            if(elemento.length() > 5) {
                System.out.println("Palabra larga: " + elemento);
            }
        }
    }
}
