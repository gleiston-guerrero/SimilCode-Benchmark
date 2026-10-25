public class TareaMatrices {
    
    public static void main(String[] args) {
        /* 
         * Definicion de la estructura bidimensional base
         * con los valores iniciales requeridos.
         */
        int[][] arregloBase = {
            { 1, 2, 3 },
            { 4, 5, 6 },
            { 7, 8, 9 }
        };
        
        System.out.println("Matriz original:");
        volcarPantalla(arregloBase);
        
        // Generamos la nueva estructura con los ejes invertidos
        int[][] arregloModificado = calcularReflejo(arregloBase);
        
        System.out.println("\nMatriz transpuesta:");
        volcarPantalla(arregloModificado);
    }
    
    /**
     * Metodo encargado de intercambiar las filas por las columnas
     * de un arreglo bidimensional dado.
     */
    private static int[][] calcularReflejo(int[][] origen) {
        int limiteY = origen.length;
        int limiteX = origen[0].length;
        
        int[][] matrizResultante = new int[limiteX][limiteY];
        
        int y = 0;
        while (y < limiteY) {
            int x = 0;
            while (x < limiteX) {
                matrizResultante[x][y] = origen[y][x];
                x++;
            }
            y++;
        }
        
        return matrizResultante;
    }

    /* 
     * Funcion auxiliar para recorrer y mostrar los elementos
     * separados por un espacio en blanco.
     */
    private static void volcarPantalla(int[][] cuadricula) {
        for (int[] vector : cuadricula) {
            int indice = 0;
            while (indice < vector.length) {
                System.out.print(vector[indice] + " ");
                indice++;
            }
            System.out.println();
        }
    }
}
