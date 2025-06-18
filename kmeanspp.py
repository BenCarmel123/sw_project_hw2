import math 
import sys
import numpy as np
import pandas as pd 

def isFloat(x):
    try:
        float(x)
        return True

    except ValueError:
        return False
        
def calcMin(x ,centroids): # Find the closest centroid to vector X
    dsitances = [np.linalg.norm(x - centroid) for centroid in centroids]
    return distances.index(min(distances))

def read_data(args): # read info from terminal 
    length = len(args)
    flag = 0 
    k = args[1]
    iter = args[2] 
    epsilon = args[3]
    # Input validity check 
    if (not k.isdigit() or k == 0):
        print("Invalid number of clusters!")
        sys.exit(1) #Error 1 - stop program 
    if length == 5:
        iter = 300
        flag = 1
        epsilon = args[2]

    elif (not iter.isdigit()) or (iter not in range(2,1000)):
        print('Invalid maximum iteration!')
        sys.exit(1) #Error 2 - stop program

    if (not isFloat(epsilon)):
        print("Invalid epsilon!")
        sys.exit() #Error 3 - stop program
    epsilon = float(epsilon)
    if (epsilon < 0.0):
        print("Invalid epsilon!")
        sys.exit() #Error 3 - stop program
    file_name1 = args[4 - flag]
    file_name2 = args[5 - flag]
    df1 = pd.read_csv(file_name1, header = None)
    df2 = pd.read_csv(file_name2, header = None)
    merged_df = pd.merge(df1, df2, how = "inner", left_on = columns[0], right_on = columns[0])
    final_data = merged_df.sort_values(by = merged_df.columns[0], ascending = True).set_index(df1.columns[0])
    df = df.drop(columns=[0])

    vectors = [] # Denote an empty list which will contain all vectors 
    for line in sys.tsdin:
        if line.strip():
            vector = [float(num) for num in line.strip().split(',')] 
            vectors.append(vector) # add to vectors list
    if len(vectors) < k: 
        print('Incorrect number of clusters!')
        sys.exit(1) #Error 1 - stop program
    return (vectors, k, iter, epsilon, final_data)

def has_converged(old_centroids, new_centroids, epsilon): # Checks if distance of all vectors < 0.001
    for old, new in zip(old_centroids, new_centroids):
        if np.linalg.norm(old - new) >= epsilon:
            return False
    return True
    
def print_cents(centroids): # Helper function for printing centroids
    for centroid in centroids:
        print(",".join(f"{float(x):.4f}" for x in centroid))

def main():
    read_data()

if __name__ == "__main__":
    main()