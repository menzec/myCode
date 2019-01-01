import pandas as pd

def main():
    filename = r'D:\data\faces\faces\face_landmarks.csv'
    csvfile = pd.read_csv(open(filename,'r'))
    for i,row in enumerate(csvfile):
        if i > 2:
            break
        print(row)


if __name__ == "__main__":
    main()