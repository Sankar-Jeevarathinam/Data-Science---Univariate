class Univariate():
    def QuanQual(dataset):
        Quan=[]
        Qual=[]
        for col in dataset.columns:
            if dataset[col].dtype != 'object':
                Quan.append(col)
            else:
                Qual.append(col)
        return Quan, Qual