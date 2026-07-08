package Java.Estructural;

import java.util.Random;

public class CODE_ESTRU_JAVA_007 {
    public static void main(String[] args) {
        Random random = new Random();
        int cantidad = 10;
        int minRGB = 0;
        int maxRGB = 255;
        int sumaRed = 0;
        
        System.out.println("Colores RGB generados:");
        for(int i = 0; i < cantidad; i++) {
            int red = random.nextInt(maxRGB - minRGB + 1) + minRGB;
            int green = random.nextInt(maxRGB - minRGB + 1) + minRGB;
            int blue = random.nextInt(maxRGB - minRGB + 1) + minRGB;
            
            System.out.println("RGB(" + red + "," + green + "," + blue + ")");
            sumaRed += red;
        }
        
        double promedioRed = sumaRed / (double)cantidad;
        System.out.println("Suma componente Red: " + sumaRed);
        System.out.println("Promedio Red: " + promedioRed);
    }
}