package Java.Idéntico;

public class MatrizTranspuesta {
    public static void main(String[] args) {
        int[][] datos = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        int numFilas = datos.length;
        int numColumnas = datos[0].length;
        int[][] resultado = new int[numColumnas][numFilas];
        
        System.out.println("Matriz original:");
        for(int i = 0; i < numFilas; i++) {
            for(int j = 0; j < numColumnas; j++) {
                System.out.print(datos[i][j] + " ");
            }
            System.out.println();
        }
        
        // Calcular transpuesta
        for(int i = 0; i < numFilas; i++) {
            for(int j = 0; j < numColumnas; j++) {
                resultado[j][i] = datos[i][j];
            }
        }
        
        System.out.println("\nMatriz transpuesta:");
        for(int i = 0; i < numColumnas; i++) {
            for(int j = 0; j < numFilas; j++) {
                System.out.print(resultado[i][j] + " ");
            }
            System.out.println();
        }
    }
}
