public class CalculadoraDistancias {

    public static void main(String[] args) {
        /* 
         * Definición de las variables de entrada para el cálculo
         */
        double distanciaInicial = 1500.0;
        String accion = "metros_a_kilometros";
        
        // Llamada al método que procesa la lógica matemática
        double valorFinal = transformarMedida(distanciaInicial, accion);
        
        // Despliegue de los resultados en pantalla
        generarReporte(distanciaInicial, valorFinal, accion);
    }

    /**
     * Transforma la medida según la opción indicada.
     * Utiliza una estructura switch para mejorar la legibilidad.
     */
    private static double transformarMedida(double cantidad, String criterio) {
        double equivalencia;
        
        switch (criterio) {
            case "metros_a_kilometros":
                equivalencia = cantidad / 1000.0;
                break;
            case "metros_a_millas":
                equivalencia = cantidad / 1609.34;
                break;
            case "metros_a_pies":
                equivalencia = cantidad * 3.28084;
                break;
            case "metros_a_pulgadas":
                equivalencia = cantidad * 39.3701;
                break;
            default:
                equivalencia = 0.0;
                break;
        }
        
        return equivalencia;
    }

    /**
     * Muestra los datos en la consola respetando el formato exacto.
     */
    private static void generarReporte(double input, double output, String nombreConversion) {
        // Concatenación idéntica a la salida esperada
        String mensajePrincipal = input + " metros = " + output + " en " + nombreConversion;
        System.out.println(mensajePrincipal);
        
        // Uso de operador ternario para decidir el mensaje de tamaño
        String evaluacionTamano = (output > 1.0) ? "Resultado grande" : "Resultado pequeño";
        System.out.println(evaluacionTamano);
    }
}
