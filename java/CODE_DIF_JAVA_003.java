package Java.Diferente;

import java.util.Random;
import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class CODE_DIF_JAVA_003 extends JFrame implements ActionListener {
    private int numeroSecreto;
    private int intentos;
    private JTextField campoNumero;
    private JLabel etiquetaResultado;
    private JButton botonAdivinar;
    private Random random;
    
    public CODE_DIF_JAVA_003() {
        random = new Random();
        numeroSecreto = random.nextInt(100) + 1;
        intentos = 0;
        
        setTitle("Juego de Adivinanza");
        setSize(300, 150);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new FlowLayout());
        
        add(new JLabel("Adivina el número (1-100):"));
        campoNumero = new JTextField(10);
        add(campoNumero);
        
        botonAdivinar = new JButton("Adivinar");
        botonAdivinar.addActionListener(this);
        add(botonAdivinar);
        
        etiquetaResultado = new JLabel("¡Ingresa tu número!");
        add(etiquetaResultado);
    }
    
    public void actionPerformed(ActionEvent e) {
        try {
            int numero = Integer.parseInt(campoNumero.getText());
            intentos++;
            
            if(numero == numeroSecreto) {
                etiquetaResultado.setText("¡Correcto! Intentos: " + intentos);
                botonAdivinar.setEnabled(false);
            } else if(numero < numeroSecreto) {
                etiquetaResultado.setText("Muy bajo. Intento: " + intentos);
            } else {
                etiquetaResultado.setText("Muy alto. Intento: " + intentos);
            }
        } catch(NumberFormatException ex) {
            etiquetaResultado.setText("Ingresa un número válido");
        }
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new CODE_DIF_JAVA_003().setVisible(true));
    }
}