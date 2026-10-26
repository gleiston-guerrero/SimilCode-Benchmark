package Java.Distinto;

public class BUSCADOR_NUMEROS {
    public static void main(String[] args) {
        int[] valores = {10, 25, 30, 45, 55, 60, 75};
        int objetivo = 45;
        boolean encontrado = false;
        int indice = -1;
        
        for(int i = 0; i < valores.length; i++) {
            if(valores[i] == objetivo) {
                encontrado = true;
                indice = i;
                break;
            }
        }
        
        if(encontrado) {
            System.out.println("Número " + objetivo + " encontrado en posición: " + indice);
        } else {
            System.out.println("Número " + objetivo + " no encontrado");
        }
    }
}
