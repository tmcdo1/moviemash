from math import log

def ndcg(ground_truth, our_result):
    idcg = 0.0
    for i, gt in enumerate(ground_truth):
        idcg += (2**(gt) - 1)/(log(i+2, 2))

    #print("idcg " + str(idcg))

    dcg_ours = 0.0
    for i, our_rank in enumerate(our_result):
        dcg_ours += (2**(ground_truth[our_rank]) - 1)/(log(i+2, 2))

    #print("dcg_ours " + str(dcg_ours))

    ndcg = dcg_ours/idcg
    #print("ndcg " + str(ndcg))
    return ndcg 

#dcg([10, 5, 2, 0], [0, 1, 3, 2], 3)
