package Java.Diferente;

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import java.util.Random;

public class CODE_DIF_JAVA_009 extends JPanel implements ActionListener {
    private Timer timer;
    private Particula[] particulas;
    private Random random;
    private final int NUM_PARTICULAS = 50;
    
    class Particula {
        double x, y, dx, dy;
        Color color;
        int tamaño;
        
        public Particula() {
            x = random.nextDouble() * getWidth();
            y = random.nextDouble() * getHeight();
            dx = (random.nextDouble() - 0.5) * 4;
            dy = (random.nextDouble() - 0.5) * 4;
            color = new Color(random.nextInt(256), random.nextInt(256), random.nextInt(256));
            tamaño = random.nextInt(10) + 5;
        }
        
        public void actualizar() {
            x += dx;
            y += dy;
            
            if(x < 0 || x > getWidth()) dx = -dx;
            if(y < 0 || y > getHeight()) dy = -dy;
            
            x = Math.max(0, Math.min(getWidth(), x));
            y = Math.max(0, Math.min(getHeight(), y));
        }
        
        public void dibujar(Graphics g) {
            g.setColor(color);
            g.fillOval((int)x, (int)y, tamaño, tamaño);
        }
    }
    
    public CODE_DIF_JAVA_009() {
        random = new Random();
        particulas = new Particula[NUM_PARTICULAS];
        
        for(int i = 0; i < NUM_PARTICULAS; i++) {
            particulas[i] = new Particula();
        }
        
        timer = new Timer(16, this);
        timer.start();
        
        setBackground(Color.BLACK);
        setPreferredSize(new Dimension(800, 600));
    }
    
    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2d = (Graphics2D) g;
        g2d.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        
        for(Particula p : particulas) {
            p.dibujar(g);
        }
    }
    
    @Override
    public void actionPerformed(ActionEvent e) {
        for(Particula p : particulas) {
            p.actualizar();
        }
        repaint();
    }
    
    public static void main(String[] args) {
        JFrame frame = new JFrame("Simulador de Partículas");
        CODE_DIF_JAVA_009 simulador = new CODE_DIF_JAVA_009();
        
        frame.add(simulador);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setResizable(false);
        frame.pack();
        frame.setLocationRelativeTo(null);
        frame.setVisible(true);
    }
}