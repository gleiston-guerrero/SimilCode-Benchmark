public class ValidacionDeCredencial {

    // Método principal que inicia la ejecución del programa
    public static void main(String[] parametros) {
        // Variable que almacena el texto a evaluar
        String textoSecreto = "MiClave123";
        
        // Evaluamos el resultado y mostramos el mensaje correspondiente
        if (cumpleReglasDeSeguridad(textoSecreto)) {
            System.out.println("Contraseña válida");
        } else {
            System.out.println("Contraseña inválida");
        }
    }

    /*
     * Función auxiliar que analiza si la cadena ingresada 
     * tiene los requisitos mínimos de seguridad.
     */
    private static boolean cumpleReglasDeSeguridad(String cadena) {
        int cantidadMayusculas = 0;
        int cantidadMinusculas = 0;
        int cantidadNumeros = 0;

        // Convertimos el texto a un arreglo y lo recorremos con un foreach
        for (char elemento : cadena.toCharArray()) {
            
            // Evaluamos usando los valores decimales de la tabla ASCII
            // 97 a 122 corresponde a las letras minúsculas (a-z)
            if (elemento >= 97 && elemento <= 122) {
                cantidadMinusculas++;
            }
            // 65 a 90 corresponde a las letras mayúsculas (A-Z)
            else if (elemento >= 65 && elemento <= 90) {
                cantidadMayusculas++;
            }
            // 48 a 57 corresponde a los dígitos numéricos (0-9)
            else if (elemento >= 48 && elemento <= 57) {
                cantidadNumeros++;
            }
        }

        // Verificamos la longitud mínima requerida
        boolean tamañoCorrecto = cadena.length() >= 8;
        
        // Comprobamos que exista al menos un carácter de cada categoría
        boolean tieneMayus = cantidadMayusculas > 0;
        boolean tieneMinus = cantidadMinusculas > 0;
        boolean tieneNum = cantidadNumeros > 0;

        // Retorna verdadero solo si todas las condiciones se cumplen simultáneamente
        return tamañoCorrecto && tieneMinus && tieneMayus && tieneNum;
    }
}
