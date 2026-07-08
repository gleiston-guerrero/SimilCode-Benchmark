package Java.Idéntico;

public class CODE_IDENT_JAVA_006 {
    public static void main(String[] args) {
        int[] numeros = {10, 25, 30, 45, 55, 60, 75};
        int objetivo = 45;
        boolean encontrado = false;
        int posicion = -1;
        
        for(int i = 0; i < numeros.length; i++) {
            if(numeros[i] == objetivo) {
                encontrado = true;
                posicion = i;
                break;
            }
        }
        
        if(encontrado) {
            System.out.println("Número " + objetivo + " encontrado en posición: " + posicion);
        } else {
            System.out.println("Número " + objetivo + " no encontrado");
        }
    }
}