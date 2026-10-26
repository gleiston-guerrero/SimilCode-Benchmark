package Java.Modificado;

import java.util.Scanner;

public class NOTAS_ESTUDIANTE {
    public static void main(String[] args) {
        Scanner entrada = new Scanner(System.in);
        
        System.out.print("Ingrese el número de materias: ");
        int cantidadMaterias = entrada.nextInt();
        
        double total = 0;
        for (int indice = 0; indice < cantidadMaterias; indice++) {
            System.out.print("Ingrese nota " + (indice + 1) + ": ");
            double calificacion = entrada.nextDouble();
            total += calificacion;
        }
        
        double resultadoPromedio = total / cantidadMaterias;
        System.out.println("El promedio es: " + resultadoPromedio);
        
        if (resultadoPromedio >= 3.0) {
            System.out.println("APROBADO");
        } else {
            System.out.println("REPROBADO");
        }
        
        entrada.close();
    }
}
