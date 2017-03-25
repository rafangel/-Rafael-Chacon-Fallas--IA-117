import java.io.*;
import java.util.*;
import java.text.*;
import java.math.*;
import java.util.regex.*;
public class Solution {
	static Stack<String> current_path = new Stack<String>();
	static Stack<String> final_path = new Stack<String>();
	static boolean[][] traveled;
	static boolean found = false;
	
	static boolean dfs(int x, int y, int pacman_x, int pacman_y, int food_x, int food_y, String [] grid){
        
        traveled[pacman_x][pacman_y] = true;
        Stack<String> total = new Stack<String>();
        
		if(pacman_x == food_x && pacman_y == food_y){ //condicion de finalización
			current_path.add(pacman_x + " " + pacman_y);
			final_path.add(pacman_x + " " + pacman_y);
            return true;
		}
        
		if(found == false){    
            
            //cargar nodos adjacentes al stack si son validos
            
            if((pacman_x-1 >= 0) && (grid[pacman_x-1].charAt(pacman_y) != '%') && (traveled[pacman_x-1][pacman_y] == false)){
				total.add("UP");
                traveled[pacman_x-1][pacman_y] = true;
            }
            if((pacman_y-1 >= 0) && (grid[pacman_x].charAt(pacman_y-1) != '%') && (traveled[pacman_x][pacman_y-1] == false)){
				total.add("LEFT");
                traveled[pacman_x][pacman_y-1] = true;
            }
            if((pacman_y+1 <= y) && (grid[pacman_x].charAt(pacman_y+1) != '%') && (traveled[pacman_x][pacman_y+1] == false)){
				total.add("RIGHT");
                traveled[pacman_x][pacman_y+1] = true;
            }
            if((pacman_x+1 <= x) && (grid[pacman_x+1].charAt(pacman_y) != '%') && (traveled[pacman_x+1][pacman_y] == false)){
				total.add("DOWN");
                traveled[pacman_x+1][pacman_y] = true;
            }
            
            if(!total.empty()){ 
                current_path.add(pacman_x + " " + pacman_y);
                String direction = total.pop(); 
                
                //revisa los nodos adjacentes recursivamente por profundidad
              
                if(direction.contains("DOWN") && found == false){
                    found = dfs(x, y, pacman_x+1, pacman_y, food_x, food_y, grid);
                    if(found == true){
                        final_path.add(pacman_x + " " + pacman_y);
                        total = new Stack<String>();
                    }
                    if(!total.empty() && found == false)
                        direction = total.pop();
                }
                if(direction.contains("RIGHT")&& found == false){
                    found = dfs(x, y, pacman_x, pacman_y+1, food_x, food_y, grid);
                    if(found == true){
                        final_path.add(pacman_x + " " + pacman_y);
                        total = new Stack<String>();
                    }
                    if(!total.empty() && found == false)
                        direction = total.pop();
                }
                if(direction.contains("LEFT")&& found == false){
                    found = dfs(x, y, pacman_x, pacman_y-1, food_x, food_y, grid);
                    if(found == true){
                        final_path.add(pacman_x + " " + pacman_y);
                        total = new Stack<String>();
                    }
                    if(!total.empty() && found == false)
                        direction = total.pop();
                }
                if(direction.contains("UP")&& found == false){
                    found = dfs(x, y, pacman_x-1, pacman_y, food_x, food_y, grid);
                    if(found == true){
                        final_path.add(pacman_x + " " + pacman_y);
                        total = new Stack<String>();
                    }
                }
            }
            else{ //ningun nodo era valido, camino sin salida
                current_path.add(pacman_x + " " + pacman_y);
                return false; 
            }
		}
        return found;
	}
    
	public static void main(String[] args) {
		Scanner in = new Scanner(System.in);


		int pacman_x = in.nextInt();
		int pacman_y = in.nextInt();

		int food_x = in.nextInt();
		int food_y = in.nextInt();

		int x = in.nextInt();
		int y = in.nextInt();

		String grid[] = new String[x];

		for(int i = 0; i < x; i++) {
			grid[i] = in.next();
		}

		traveled = new boolean[x][y];
        
		dfs( x, y, pacman_x, pacman_y, food_x, food_y, grid);
        
		String[] curr_path = current_path.toArray(new String[0]);
		String[] fin_path = final_path.toArray(new String[0]);
        
        // Prints finales
        
		System.out.println(curr_path.length);
		for(int i = 0; i < curr_path.length; i++){
			System.out.println(curr_path[i]);
		}
        
		System.out.println(fin_path.length - 1);
		for(int j = fin_path.length; j > 0; j--){
			System.out.println(fin_path[j-1]);
		}

	}
}

