from dataset import Dataset

ds = Dataset("data/log.xlsx")
ds.process_data()
print(ds.get_data())