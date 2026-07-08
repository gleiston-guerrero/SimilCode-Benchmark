package Java.Estructural;

public class CODE_ESTRU_JAVA_004 {
    public static void main(String[] args) {
        double celsius = 25.0;
        double fahrenheit = 77.0;
        String conversion = "CtoF";
        double resultado = 0;
        
        if(conversion.equals("CtoF")) {
            resultado = (celsius * 9/5) + 32;
        } else if(conversion.equals("FtoC")) {
            resultado = (fahrenheit - 32) * 5/9;
        } else if(conversion.equals("CtoK")) {
            resultado = celsius + 273.15;
        } else if(conversion.equals("KtoC")) {
            if(celsius >= -273.15) {
                resultado = celsius - 273.15;
            } else {
                System.out.println("Error: Temperatura inválida");
                return;
            }
        }
        
        System.out.println("Conversión " + conversion + ": " + resultado + "°");
    }
}