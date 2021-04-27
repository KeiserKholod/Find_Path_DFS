import collections

class Point:
    def __init__(self, point):
        coordinates = point.split(" ")
        self.x = int(coordinates[0])
        self.y = int(coordinates[1])
        
    def __str__(self):
        return str(self.x) + " " + str(self.y)

def get_data_from_file(path_to_file="in.txt"):
    matrix_str = ""
    with open(path_to_file,"r") as file:
        rows_count = file.readline()
        columns_count = file.readline()
        matrix_str = file.read()
    maze = []
        
    lines = matrix_str.split("\n")
    last_point = lines.pop()
    firts_point = lines.pop()
    for line in lines:
        elements = line.split(" ")
        maze.append(elements)
    return int(rows_count), int(columns_count),firts_point, last_point, maze
    


def find_path_with_dfs(maze, first_point, last_point, rows_count, columns_count):
    visited_points = collections.deque()
    visited_points.append(first_point)
    # словарь, где лежит предыдущая вершина для каждой вершины(из которой в нее пришли)
    # заполняю словарь пустотой
    prev_points = {str(x) + " " + str(y): None for x in range(1, rows_count + 1) for y in range(1, columns_count + 1)}
    # print(prev_points)
    current_point = "start"
    prev_points[str(first_point)] = current_point
    while len(visited_points) != 0:
        current_point = visited_points.pop()
        
        
        left_y = current_point.y - 1
        right_y = current_point.y + 1
        up_x = current_point.x - 1
        down_x = current_point.x + 1
        
        # смотрим возможность пойти в стороны, в обратном порядеке, 
        # чтобы преимущество было у последней вершины в стеке(первой по приоритету)
        if down_x <= rows_count:
            next_point = Point(str(down_x) + " " + str(current_point.y))
            if maze[down_x-1][current_point.y-1] == "0" and prev_points[str(next_point)] is None:
                prev_points[str(next_point)] = current_point            
                visited_points.append(next_point)
                # print("down")
        if up_x > 0:
            next_point = Point(str(up_x) + " " + str(current_point.y))
            if maze[up_x-1][current_point.y-1] == "0" and prev_points[str(next_point)] is None:  
                prev_points[str(next_point)] = current_point             
                visited_points.append(next_point)   
                # print("up")    
        if right_y <= columns_count:
            next_point = Point(str(current_point.x) + " " + str(right_y))
            if maze[current_point.x-1][right_y - 1] == "0" and prev_points[str(next_point)] is None:  
                prev_points[str(next_point)] = current_point             
                visited_points.append(next_point)
                # print("right")                 
        if left_y > 0:    
            next_point = Point(str(current_point.x) + " " + str(left_y))        
            if maze[current_point.x-1][left_y-1] == "0" and prev_points[str(next_point)] is None:      
                prev_points[str(next_point)] = current_point             
                visited_points.append(next_point)      
                # print("left")  
    # проверяем, дошли мы до точки, или просто закончили обход своей компоненты связанности
    if str(current_point) != str(last_point):
        return [], "N"
    return get_path_from_chain(prev_points, first_point, last_point), "Y"
                        

def get_path_from_chain(prev_points, first_point, last_point):
    path = []
    current_point = last_point   
    while True:
        path.insert(0, str(current_point))
        current_point = prev_points[str(current_point)]
        if current_point == "start":
            break
    # print(path)
    return path

             
def write_in_file(data):
    with open('out.txt', '+w') as file:
        file.write(data)    
        
        
rows_count, columns_count, first_point, last_point, maze = get_data_from_file()
first_point = Point(first_point)
last_point = Point(last_point)

# print(first_point.x,first_point.y)
# print(last_point.x,last_point.y)

path, is_reachable = find_path_with_dfs(maze, first_point, last_point, rows_count, columns_count)
path.insert(0, is_reachable)
write_in_file("\n".join(path))

