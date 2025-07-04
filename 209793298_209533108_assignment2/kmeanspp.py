import sys
import numpy as np
import pandas as pd 
import mykmeanspp 

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
    if length > 6:
        print("An Error Has Occurred")
        sys.exit(1)
    flag = 0 
    try:
        k_val = float(args[1])
        if not k_val.is_integer() or k_val < 2:
            raise Exception
        k = int(k_val)
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
            iter_val = float(iter)
            if not iter_val.is_integer() or not (2 <= iter_val < 1000):
                raise Exception
            iter = int(iter_val)
        except:
            print('Invalid maximum iteration!')
            sys.exit(1) #Error 2 - stop program

    if (not isFloat(epsilon)):
        print("Invalid epsilon!")
        sys.exit(1) #Error 3 - stop program
    epsilon = float(epsilon)
    if (epsilon < 0.0):
        print("Invalid epsilon!")
        sys.exit(1) #Error 3 - stop program

    file_name1 = args[4 - flag]
    file_name2 = args[5 - flag]
    df1 = pd.read_csv(file_name1, header = None)
    df2 = pd.read_csv(file_name2, header = None)
    merged_df = pd.merge(df1, df2, how = "inner", left_on = df1.columns[0], right_on = df2.columns[0])
    final_data = merged_df.sort_values(by = merged_df.columns[0], ascending = True).set_index(df1.columns[0])
    final_data = final_data.reset_index(drop=True)
    n = final_data.shape[0]
    if k > n:
        print("Invalid number of clusters!")
        sys.exit(1)
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
        try: # Division-by-zero exception handling
            prob = distances / total_dist 
        except ZeroDivisionError:
            print()
            print("An Error Has Occured")
            sys.exit(1)
        new_choice = np.random.choice(data.shape[0], p = prob)
        print ("," + str(data.index[new_choice]), end = "")
        new_centroid = data.iloc[new_choice]
        data = data.drop(data.index[new_choice])
        centroids.append(new_centroid)
    print()
    return centroids
    
def print_cents(centroids): # Helper function for printing centroids
    for centroid in centroids:
        print(",".join(f"{float(x):.4f}" for x in centroid))

def npToList(list): # Helper function for converting Numpy matrix to Python list
    new_list = []
    for vector in list:
        new_list.append(vector.tolist())
    return new_list

def main():
    k, iter, epsilon, np_data = read_data(sys.argv)
    np_initial_centroids = create_centroids(k, np_data)
    initial_centroids = npToList(np_initial_centroids)
    data = npToList(np_data.values)
    try: # Handling of any error encountered in C program
        final = mykmeanspp.fit(k, iter, epsilon, data, initial_centroids)
        print_cents(final)
    except:
        print("An Error Has Occured")
        sys.exit(1)

if __name__ == "__main__":
    main()
    