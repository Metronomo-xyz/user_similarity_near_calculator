import scipy.sparse as ss
import numpy as np
import math
import time

def calculateSimilarity(data, removeWalletsPercentile=None, removeContractsPercentile=None, removeContracts=None):# -> ss.coo_matrix:
    if (removeWalletsPercentile):
        interactions_num_perc_99 = np.percentile(data.interactions_num, removeWalletsPercentile)
        print("signer interactions perc : " + str(interactions_num_perc_99))

    if (removeContractsPercentile):
        receiver_interactions_count = data[["signer_account_id", "receiver_account_id"]].groupby("receiver_account_id")\
            .count().sort_values(by="signer_account_id", ascending=False)
        receiver_interactions_perc_99 = np.percentile(receiver_interactions_count.signer_account_id, 99.9)
        leaveContracts = set(receiver_interactions_count[receiver_interactions_count.signer_account_id <= receiver_interactions_perc_99]\
                             .reset_index()["receiver_account_id"].tolist())
        print(receiver_interactions_count)
        print("receiver_interactions_perc : " + str(receiver_interactions_perc_99))

    if (removeWalletsPercentile):
        if(removeContractsPercentile):
            if(removeContracts):
                leaveContracts = leaveContracts - removeContracts
                data = data[(data.interactions_num <= interactions_num_perc_99) & (data.receiver_account_id.isin(leaveContracts))]
                data = data[data.signer_account_id != data.receiver_account_id]
            else:
                data = data[(data.interactions_num <= interactions_num_perc_99) & (data.receiver_account_id.isin(leaveContracts))]
                data = data[data.signer_account_id != data.receiver_account_id]
        else:
            if (removeContracts):
                data = data[(data.interactions_num <= interactions_num_perc_99) & (~data.receiver_account_id.isin(removeContracts))]
                data = data[data.signer_account_id != data.receiver_account_id]
            else:
                data = data[data.interactions_num <= interactions_num_perc_99]
                data = data[data.signer_account_id != data.receiver_account_id]
    else:
        if (removeContractsPercentile):
            if (removeContracts):
                leaveContracts = leaveContracts - removeContracts
                data = data[data.receiver_account_id.isin(leaveContracts)]
                data = data[data.signer_account_id != data.receiver_account_id]
            else:
                data = data[data.receiver_account_id.isin(leaveContracts)]
                data = data[data.signer_account_id != data.receiver_account_id]
        else:
            if (removeContracts):
                data = data[~data.receiver_account_id.isin(removeContracts)]
                data = data[data.signer_account_id != data.receiver_account_id]
            else:
                data = data[data.signer_account_id != data.receiver_account_id]

    print(data)
    signers = data["signer_account_id"].drop_duplicates().reset_index().drop("index", axis=1).reset_index()
    print("signers num : " + str(len(signers)))

    receivers = data["receiver_account_id"].drop_duplicates().reset_index().drop("index", axis=1).reset_index()
    print("receivers num : " + str(len(receivers)))

    data = data.set_index("signer_account_id") \
        .join(
        signers.set_index("signer_account_id"),
        how="left") \
        .reset_index(drop=True) \
        .set_index("receiver_account_id") \
        .join(
        receivers.set_index("receiver_account_id"),
        how="left", lsuffix="_signer", rsuffix="_receiver") \
        .reset_index(drop=True) \
        .drop("interactions_num", axis=1) \
        .drop_duplicates()

    print(data)

    row = np.array(data["index_signer"])
    col = np.array(data["index_receiver"])
    d = np.array(np.ones(len(data)))
    print("creating m1 & m2")
    m1 = ss.coo_matrix((d, (row, col))).astype(np.uintc).tocsr()
    m2 = m1.transpose()

    print(str((m1.data.nbytes + m1.indptr.nbytes + m1.indices.nbytes) / 1024 / 1024 / 1024))
    print(str((m2.data.nbytes + m2.indptr.nbytes + m2.indices.nbytes) / 1024 / 1024 / 1024))

    print("multiplying")
    common_contracts = m1.dot(m2).tocoo()
    print(str((common_contracts.data.nbytes + common_contracts.row.nbytes + common_contracts.col.nbytes) / 1024 / 1024 / 1024))

    a = data.groupby("index_signer").count().apply(lambda x: math.sqrt(x), axis=1).to_dict()
    print("a:")
    print(a)

    signers_index = signers.set_index("index").to_dict()["signer_account_id"]
    print("number of entries : " + str(len(common_contracts.data)))
    print("calculating similarity")

    row = [signers_index[idx] for idx in common_contracts.row]
    col = [signers_index[idx] for idx in common_contracts.col]
    data_similarity = [(d/(a[c]*a[r])) for r,c,d in zip(common_contracts.row, common_contracts.col, common_contracts.data)]

    return row,col,data_similarity