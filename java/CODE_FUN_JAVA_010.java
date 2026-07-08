package Java.Funcional;

public class CODE_FUN_JAVA_010 {
    private int[][] datosOriginales;
    private int[][] resultado;
    private int numeroFilas;
    private int numeroColumnas;
    
    public CODE_FUN_JAVA_010(int[][] entrada) {
        this.datosOriginales = entrada;
        this.numeroFilas = entrada.length;
        this.numeroColumnas = entrada[0].length;
        this.resultado = new int[numeroColumnas][numeroFilas];
    }
    
    public void calcularTransformacion() {
        for(int fila = 0; fila < numeroFilas; fila++) {
            for(int columna = 0; columna < numeroColumnas; columna++) {
                resultado[columna][fila] = datosOriginales[fila][columna];
            }
        }
    }
    
    public void imprimirMatrizOriginal() {
        System.out.println("Matriz original:");
        imprimirMatriz(datosOriginales, numeroFilas, numeroColumnas);
    }
    
    public void imprimirMatrizTransformada() {
        System.out.println("\nMatriz transpuesta:");
        imprimirMatriz(resultado, numeroColumnas, numeroFilas);
    }
    
    private void imprimirMatriz(int[][] mat, int f, int c) {
        for(int i = 0; i < f; i++) {
            for(int j = 0; j < c; j++) {
                System.out.print(mat[i][j] + " ");
            }
            System.out.println();
        }
    }
    
    public static void main(String[] args) {
        int[][] datos = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
        CODE_FUN_JAVA_010 procesador = new CODE_FUN_JAVA_010(datos);
        procesador.imprimirMatrizOriginal();
        procesador.calcularTransformacion();
        procesador.imprimirMatrizTransformada();
    }
}