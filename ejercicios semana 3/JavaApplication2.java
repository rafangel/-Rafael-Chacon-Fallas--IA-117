/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javaapplication2;

import java.util.Scanner;

/**
 *
 * @author rafa
 */
public class JavaApplication2 {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int [] pos = new int[2];
        String board[] = new String[5];
        for(int i=0;i<2;i++) pos[i] = in.nextInt();
        for(int i=0;i<5;i++) board[i] = in.next();
        next_move(pos[0], pos[1], board);
    }
    
    static void next_move(int posr, int posc, String[] board){
        String[][] matrix = new String[5][5];
        String[] line;
        for(int i =0;i<5;i++){
            
            line = board[i].split("");
            for(int j =0;j<5;j++){
                String value = line[j];
                matrix[i][j]=value;
                
                
            }
        }
        
        if(matrix[posr][posc].compareTo("d")==0){
            System.out.println("CLEAN");
            matrix[posr][posc]="-";
        }
        else{
            int dx,dy;
            dx=dy=-1;
            for(int i =0;i<5;i++){
                boolean flag = false;
                for(int j=0;j<5;j++){
                    if(matrix[i][j].compareTo("d")==0){
                        dy=i;
                        dx=j;
                        flag=true;
                        break;
                    }
                }
                if(flag){
                    break;
                }
            }
            if(dx!=-1 && dy!=-1){
                makePath(dx,dy,posc,posr);
            }
        }
    }
    
    
    private static void makePath(int px,int py,int mx, int my){
            if(py<my){
                System.out.println("UP");
            }
            else if(py>my){
                System.out.println("DOWN");
            }
            else if(px>mx){
                System.out.println("RIGHT");
            }
            else if(px<mx){
                System.out.println("LEFT");
            }
        
    }
    
}
