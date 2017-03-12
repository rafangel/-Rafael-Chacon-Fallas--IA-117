/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package javaapplication3;


import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;
import java.lang.Object;
/**
 *
 * @author rafa
 */
public class JavaApplication3 {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int q = in.nextInt();
        
        
       for(int k=0;k<q;k++){
            int[] pos = new int[2];
            for(int i=0;i<2;i++) pos[i] = in.nextInt();
            int n = pos[0];
            int m = pos[1];
            int graph[][] = createGraph(n);
            for(int j=0;j<m;j++){
                int[] pos2 = new int[2];
                for(int i=0;i<2;i++) pos2[i] = in.nextInt();
                int u = pos2[0];
                int v = pos2[1];
                graph[u-1][v-1]=1;
                graph[v-1][u-1]=1;
            }
            int s = in.nextInt();
            s-=1;
            path(n,m,s,graph);
        }
    }
    
    private static int[][] createGraph(int n){
        int[][] g = new int[n][n];
        for(int i=0;i<n;i++){
            Arrays.fill(g[i], 0);
        }
        return g;
    }
    
    private static void path(int n,int m, int s, int[][] graph){
        String result = "";
        int[] fifo = new int[n];
        Arrays.fill(fifo, -1);
        fifo[0]=s; 
        for(int i=0;i< n;i++){
            if(s!=i){
                result += (String.valueOf(singlePath(s,i,n,m,graph,fifo)));
                result += " ";
            }
        }
        
        System.out.println(result);
    }
    
    private static int singlePath(int start,int end,int n,int m,int[][] graph, int[] fifo){
        int len =0;
        int current = 0;
        while(fifo[current] != -1){
            
            if(graph[fifo[current]][end]==1){//llego directamente
                return len+6;
            }
            else{
                fifo = add(n,fifo,graph[fifo[current]]);
                current++;
                len+=6;
            }

        }
        return -1;
    }
    
    private static int[] add(int n,int[] fifo, int[] lines){
        for(int i=0;i<n;i++){
            if(lines[i]==1 && !contains(n,fifo,i)){
               int pos = index(fifo);
               if(pos<fifo.length){
                   fifo[pos]=i;
               }
            }
        }
        return fifo;
    } 
    
    private static int index(int[] fifo){
        for(int i=0;i<fifo.length;i++){
            if(fifo[i]==-1){
                return i;
            }
        }
        return fifo.length;
    }
    
    private static boolean contains(int n,int[] fifo, int num){
        for(int i=0;i<n;i++){
            if(fifo[i]==num){
                return true;
            }
        }
        return false;
    }
    
}
