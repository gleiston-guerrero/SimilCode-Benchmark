public class AnalizadorDeArreglos {

    /* 
     * Punto de entrada principal de la aplicación.
     * Se encarga de definir los datos y mostrar los resultados en consola.
     */
    public static void main(String[] argumentos) {
        // Definición explícita de los valores a procesar
        int[] coleccionDatos = new int[] { 10, 25, 30, 45, 55, 60, 75 };
        int valorRequerido = 45;
        
        // Delegamos la lógica de búsqueda a un método auxiliar
        int indiceObtenido = ejecutarBusqueda(coleccionDatos, valorRequerido);
        
        // Evaluamos el resultado devuelto para imprimir el mensaje exacto
        if (indiceObtenido > -1) {
            System.out.println("Número " + valorRequerido + " encontrado en posición: " + indiceObtenido);
        } else {
            System.out.println("Número " + valorRequerido + " no encontrado");
        }
    }

    /**
     * Método que recorre un arreglo de enteros utilizando un bucle while.
     * Si encuentra el criterio de búsqueda, devuelve su índice inmediatamente.
     * En caso de no existir, retorna -1.
     */
    private static int ejecutarBusqueda(int[] fuenteDatos, int criterio) {
        int contador = 0;
        int limite = fuenteDatos.length;
        
        // Reemplazo del bucle for original por un while
        while (contador < limite) {
            if (fuenteDatos[contador] == criterio) {
                return contador; // Retorno anticipado en lugar de usar break
            }
            contador++;
        }
        
        // Retorno por defecto si finaliza el recorrido sin éxito
        return -1; 
    }
}
