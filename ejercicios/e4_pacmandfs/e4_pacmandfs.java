import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;

public class Solution {
static void dfs(int r, int c, int pacman_r, int pacman_c, int food_r, int food_c, String [] grid){
        //Your logic here
    }
public static void main(String[] args) {
        Scanner in = new Scanner(System.in);


        int pacman_r = in.nextInt();
        int pacman_c = in.nextInt();

        int food_r = in.nextInt();
        int food_c = in.nextInt();

        int r = in.nextInt();
        int c = in.nextInt();
    
        String grid[] = new String[r];

        for(int i = 0; i < r; i++) {
            grid[i] = in.next();
        }

        dfs( r, c, pacman_r, pacman_c, food_r, food_c, grid);
    }
}

