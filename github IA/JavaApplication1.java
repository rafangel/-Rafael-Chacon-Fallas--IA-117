/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javaapplication1;
import java.util.*;
/**
 *
 * @author rafa
 */
public class JavaApplication1 {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        String[] grid = {"-","-","p","-","-","-","-","-","-","-","-","-","m","-","-","-"};
        displayPathtoPrincess(4,grid);
    }
    
    public static void displayPathtoPrincess(int N,String[] grid){
        String[][] matrix = new String[N][N];
        int px,py,mx,my;
        px=py=mx=my = -1;
        for(int i =0;i<N;i++){
            for(int j =0;j<N;j++){
                String value = grid[i*N+j];
                matrix[i][j]=value;
                if(value.compareTo("p")==0){
                    py=i;
                    px=j;
                }
                if(value.compareTo("m")==0){
                    my=i;
                    mx=j;
                }
            }
        }
        makePath(px,py,mx,my);
    }
    private static void makePath(int px,int py,int mx, int my){
        String path = "";
        while(px!=mx || py!=my){
            if(py<my){
                path += "UP\n";
                my-=1;
            }
            if(py>my){
                path += "DOWN\n";
                my+=1;
            }
            if(px>mx){
                path += "RIGHT\n";
                mx+=1;
            }
            if(px<mx){
                path += "LEFT\n";
                mx-=1;
            }
        }
        System.out.println(path);
    }
    
}
