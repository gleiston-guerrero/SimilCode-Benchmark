package Java.Diferente;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.atomic.AtomicBoolean;

public class CODE_DIF_JAVA_006 {
    private BlockingQueue<Integer> cola;
    private AtomicBoolean ejecutando;
    private final int CAPACIDAD = 10;
    
    public CODE_DIF_JAVA_006() {
        cola = new LinkedBlockingQueue<>(CAPACIDAD);
        ejecutando = new AtomicBoolean(true);
    }
    
    class Productor implements Runnable {
        public void run() {
            int contador = 1;
            while(ejecutando.get() && contador <= 20) {
                try {
                    cola.put(contador);
                    System.out.println("Producido: " + contador);
                    contador++;
                    Thread.sleep(500);
                } catch(InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
            ejecutando.set(false);
        }
    }
    
    class Consumidor implements Runnable {
        public void run() {
            while(ejecutando.get() || !cola.isEmpty()) {
                try {
                    Integer elemento = cola.take();
                    System.out.println("Consumido: " + elemento);
                    Thread.sleep(1000);
                } catch(InterruptedException e) {
                    Thread.currentThread().interrupt();
                    break;
                }
            }
        }
    }
    
    public void iniciar() {
        Thread hiloProductor = new Thread(new Productor());
        Thread hiloConsumidor = new Thread(new Consumidor());
        
        hiloProductor.start();
        hiloConsumidor.start();
        
        try {
            hiloProductor.join();
            hiloConsumidor.join();
        } catch(InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        
        System.out.println("Procesamiento completado");
    }
    
    public static void main(String[] args) {
        new CODE_DIF_JAVA_006().iniciar();
    }
}
