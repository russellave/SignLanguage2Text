import numpy as np
import pandas as pd
import torch
import spacy
import random
import en_core_web_sm

from ModelClasses import Encoder, Decoder, Seq2Seq


def init_and_load_model(model_path):
    
    src_vocab = pd.read_pickle(r'./SRC_vocab.pkl')
    trg_vocab = pd.read_pickle(r'./TRG_vocab.pkl')
    INPUT_DIM = len(src_vocab)
    OUTPUT_DIM = len(trg_vocab)
    ENC_EMB_DIM = 256
    DEC_EMB_DIM = 256
    HID_DIM = 512
    ENC_DROPOUT = 0.5
    DEC_DROPOUT = 0.5
    
    SEED = 1234
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.cuda.manual_seed(SEED)
    torch.backends.cudnn.deterministic = True

    enc = Encoder(INPUT_DIM, ENC_EMB_DIM, HID_DIM, ENC_DROPOUT)
    dec = Decoder(OUTPUT_DIM, DEC_EMB_DIM, HID_DIM, DEC_DROPOUT)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = Seq2Seq(enc, dec, device).to(device)
    model.load_state_dict(torch.load(model_path, map_location=lambda storage, loc: storage)) #load model
    return model

def translate_sentence(model, sentence):
    read_src_vocab = pd.read_pickle(r'./SRC_vocab.pkl')
    read_trg_vocab = pd.read_pickle(r'./TRG_vocab.pkl')

    nlp = spacy.load('en_core_web_sm')
    model.eval()
    
    tokenized = nlp(sentence) 
    tokenized = ['<sos>'] + [t.lower_ for t in tokenized] + ['<eos>']
    numericalized = [read_src_vocab.stoi[t] for t in tokenized] 
    unnumericalized = [read_src_vocab.itos[t] for t in numericalized] #readable words

    
    tokenized_trg = nlp('a '*2*len(tokenized)) #just to give a target length longer than input
    tokenized_trg = ['<sos>'] + [t.lower_ for t in tokenized_trg] + ['<eos>']
    numericalized_trg = [read_trg_vocab.stoi[t] for t in tokenized_trg] 
    
    sentence_length = torch.LongTensor([len(numericalized)]).to(model.device) 
    tensor = torch.LongTensor(numericalized).unsqueeze(1).to(model.device) 

    tensor_targ = torch.LongTensor(numericalized_trg).unsqueeze(1).to(model.device) 
    
    translation_tensor_logits = model(tensor, tensor_targ, 0) 
    
    translation_tensor = torch.argmax(translation_tensor_logits.squeeze(1), 1)
    translation = [read_trg_vocab.itos[t] for t in translation_tensor]
 
    # Start at the first index.  We don't need to return the <sos> token or the <eos> token
    translation = translation[1:]
    if '<eos>' in translation:
        end_ind = translation.index('<eos>')
        translation = translation[:end_ind]
    
    translation = " ".join(translation) #join the list of words together as a string
    
    return translation, translation_tensor_logits