package Java.Nuevo;

public class OrdenadorNumeros {
    public static void main(String[] args) {
        int[] lista = {64, 34, 25, 12, 22, 11, 90};
        int longitud = lista.length;
        
        for(int indice = 0; indice < longitud-1; indice++) {
            for(int contador = 0; contador < longitud-indice-1; contador++) {
                if(lista[contador] > lista[contador+1]) {
                    int auxiliar = lista[contador];
                    lista[contador] = lista[contador+1];
                    lista[contador+1] = auxiliar;
                }
            }
        }
        
        System.out.print("Números ordenados: ");
        for(int valor : lista) {
            System.out.print(valor + " ");
        }
    }
}
