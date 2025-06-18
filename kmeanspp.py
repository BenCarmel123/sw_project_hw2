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
    distances = [np.linalg.norm(x - centroid) for centroid in centroids]
    return min(distances)

def read_data(args): # read info from terminal 
    length = len(args)
    flag = 0 
    try:
        k = int(args[1])
        if k == 0:
            raise Exception
    except:
        print("Invalid number of clusters!")
        sys.exit(1) #Error 1 - stop program 

    iter = args[2] 
    epsilon = args[3]
    if length == 5:
        iter = 300
        flag = 1
        epsilon = args[2]
    else:
        try:
            if int(iter) in range(2,1000):
                iter = int(iter)
        except:
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
    merged_df = pd.merge(df1, df2, how = "inner", left_on = df1.columns[0], right_on = df2.columns[0])
    final_data = merged_df.sort_values(by = merged_df.columns[0], ascending = True).set_index(df1.columns[0])
    final_data = final_data.reset_index(drop=True)
    return (k, iter, epsilon, final_data)

def create_centroids(k, data):
    np.random.seed(1234)
    random_choice = np.random.choice(data.shape[0])
    print(random_choice, end = "")
    first_centroid = data.iloc[random_choice]
    centroids = [first_centroid]
    data = data.drop(random_choice)
    for i in range (1, k):
        distances = []
        total_dist = 0
        for index, vector in data.iterrows():
            d = calcMin(vector, centroids)
            distances.append(d)
            total_dist += d
        distances = np.array(distances)
        prob = distances / total_dist
        new_choice = np.random.choice(data.shape[0], p = prob)
        print ("," + str(new_choice), end = "")
        new_centroid = data.iloc[new_choice]
        data = data.drop(new_choice)
        centroids.append(new_centroid)
    return centroids

def has_converged(old_centroids, new_centroids, epsilon): # Checks if distance of all vectors < 0.001
    for old, new in zip(old_centroids, new_centroids):
        if np.linalg.norm(old - new) >= epsilon:
            return False
    return True
    
def print_cents(centroids): # Helper function for printing centroids
    for centroid in centroids:
        print(",".join(f"{float(x):.4f}" for x in centroid))

def main():
    k, iter, epsilon, data = read_data(sys.argv)
    initial_centroids = create_centroids(k, data)
    return (k, iter, epsilon, initial_centroids)

if __name__ == "__main__":
    main()