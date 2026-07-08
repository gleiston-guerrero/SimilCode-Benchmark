package Java.Funcional;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class CODE_FUN_JAVA_011 {
    private List<Double> calificaciones;
    
    public CODE_FUN_JAVA_011() {
        this.calificaciones = new ArrayList<>();
    }
    
    public void ingresarCalificaciones() {
        Scanner entrada = new Scanner(System.in);
        System.out.print("¿Cuántas calificaciones desea ingresar? ");
        int cantidad = entrada.nextInt();
        
        for (int contador = 0; contador < cantidad; contador++) {
            System.out.print("Calificación #" + (contador + 1) + ": ");
            double calificacion = entrada.nextDouble();
            calificaciones.add(calificacion);
        }
        entrada.close();
    }
    
    public double calcularPromedio() {
        double total = 0.0;
        for (Double calif : calificaciones) {
            total += calif;
        }
        return total / calificaciones.size();
    }
    
    public String determinarEstado(double promedio) {
        return promedio >= 3.0 ? "APROBADO" : "REPROBADO";
    }
    
    public static void main(String[] args) {
        CODE_FUN_JAVA_011 sistema = new CODE_FUN_JAVA_011();
        sistema.ingresarCalificaciones();
        
        double promedioFinal = sistema.calcularPromedio();
        String resultado = sistema.determinarEstado(promedioFinal);
        
        System.out.println("Promedio final: " + promedioFinal);
        System.out.println("Estado: " + resultado);
    }
}