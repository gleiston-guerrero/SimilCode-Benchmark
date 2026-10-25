package Java.Idéntico;

public class BuscadorSecuencial {
    public static void main(String[] args) {
        int[] datos = {10, 25, 30, 45, 55, 60, 75};
        int valorBuscado = 45;
        boolean existe = false;
        int indice = -1;
        
        for(int contador = 0; contador < datos.length; contador++) {
            if(datos[contador] == valorBuscado) {
                existe = true;
                indice = contador;
                break;
            }
        }
        
        if(existe) {
            System.out.println("Número " + valorBuscado + " encontrado en posición: " + indice);
        } else {
            System.out.println("Número " + valorBuscado + " no encontrado");
        }
    }
}
