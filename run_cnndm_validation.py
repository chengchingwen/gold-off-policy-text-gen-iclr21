import torch
from fairseq.models.bart import BARTModel

num_checkpoints = 100
for i in range(1, num_checkpoints+1):
    bart = BARTModel.from_pretrained('/path/to/model/directory/', checkpoint_file='checkpoint'+str(i)+'.pt', data_name_or_path='cnn_dm-bin')
    bart.cuda()
    bart.eval()
    bart.half()
    count = 1
    bsz = 32
    with open('cnn_dm/val.source') as source, open('cnn_dm/val.hypo', 'w') as fout:
        sline = source.readline().strip()
        slines = [sline]
        for sline in source:
            if count % bsz == 0:
                with torch.no_grad():
                    hypotheses_batch = bart.sample(slines, beam=4, lenpen=2.0, max_len_b=140, min_len=55, no_repeat_ngram_size=3, fix_summarization_bug=1)
                for hypothesis in hypotheses_batch:
                    fout.write(hypothesis + '\n')
                    fout.flush()
                slines = []
            slines.append(sline.strip())
            count += 1
        if slines != []:
            hypotheses_batch = bart.sample(slines, beam=4, lenpen=2.0, max_len_b=140, min_len=55, no_repeat_ngram_size=3, fix_summarization_bug=1)
            for hypothesis in hypotheses_batch:
                fout.write(hypothesis + '\n')
                fout.flush()