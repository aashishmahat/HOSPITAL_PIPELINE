from pipeline.extract import load_datasets
from pipeline.transform import transforms_data
from pipeline.load import store
def main():
    print("=== Starting Hospital Analytics Pipeline ===\n")
    #Extract datasets
    datasets = load_datasets()
    #Transform datasets
    cleaned_data=transforms_data(datasets)
    #load data 
    store(cleaned_data)
    print("\n=== Pipeline Execution Completed ===")

if __name__ == "__main__":
    main()