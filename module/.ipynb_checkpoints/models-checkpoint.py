import pickle as __pickle
from keras.models import load_model as __load_model
from keras.preprocessing import sequence as __sequence
import re as __re
import os as __os

def __find_dir(path):
    full_model = []
    for fd in __os.listdir(path):
        full_path=__os.path.join(path,fd)
        if __os.path.isdir(full_path):
            pass
        else:
            model = ''.join(__re.findall('h5/(.*)\.h5',full_path))
            full_model.append(model)
    return full_model

def get_pickle_file(pickle_path):
    with open(pickle_path, 'rb') as file:
        return __pickle.load(file)

    
# load_models   
for m in __find_dir('module/h5/'):
    path = 'module/h5/{}.h5'.format(m)
    locals()['_'+m] = __load_model(path)

# tokenizer
soap_tokenizer = get_pickle_file("module/pickle/clinicalDB_soap_tokenizer.pickle")
report_tokenizer = get_pickle_file("module/pickle/clinicalDB_report_tokenizer.pickle")


def __get_input_seq(text, tokenize,max_seq_len=500):
    input_seq = __sequence.pad_sequences(tokenize.texts_to_sequences([text]), maxlen = max_seq_len)
    return input_seq

# preprocessing
def _soap_preprocessing(soap):
    output = __re.sub('\s?\(?see description\)?\s?','',soap)
    return output
def _rm_ref(report):
    report = __re.sub('\n','\t',report)
    reference_context = __re.findall(r'(.*)Reference.*',report)
    while bool(reference_context):
        report = '\t'.join(reference_context)
        reference_context = __re.findall(r'(.*)Reference.*',report)
    
    reference_context = __re.findall(r'(.*)Ref:.*',report)
    while bool(reference_context):
        report = '\t'.join(reference_context)
        reference_context = __re.findall(r'(.*)Ref:.*',report)
    report = __re.sub('\t','\n',report).strip()
    return report
def _get_EGRF_context(context):
    context_sub = __re.sub('\n',' ',context)
    output = ''.join(__re.findall('EGFR exon 18.*',context_sub))
    if bool(output)==False:
        output = context
    return output
def _gene_context(gene,context):
    context_split = context.split()
    if gene in context_split:
        i = context_split.index(gene)
        if i >10:
            output = __re.sub(r"\s+", " ", ' '.join(context_split[i-10:]))
        else:
            output = __re.sub(r"\s+", " ", context)
    else:
        output = __re.sub(r"\s+", " ", context)
    return output

def _get_histologic_type(report):
    report_split = report.split('\n')
    volume_size, tumor_size = '-', '-'
    kw_tumor_size = ['on cut', 'firm tumor', 'tumor measuring']
    for i in range(len(report_split)):
        for kw in kw_tumor_size:
            if kw in report_split[i].lower():
                find_pattern = "(\.?.*{}.*)".format(kw)
                volume_context = __re.findall(find_pattern ,report_split[i].lower())
                volume_context = ' '.join(volume_context)
                volume_size = __re.findall(r'(\d+\s?\.?\s?\d+?\s?x\s?\d+\s?\.?\s?\d+?\s?x\s?\d+\s?\.?\s?\d+?\s?cm)',volume_context) 
                volume_size = [s for s in volume_size if s != '']
                if len(volume_size)<=2:
                    volume_size = ''.join(volume_size[-1]) if len(volume_size)==2 else ''.join(volume_size)
                elif len(volume_size)>=3:
                    volume_size = ''.join(volume_size[0]) if len(volume_size)>=3 else ''.join(volume_size)
                if bool(volume_size):
                    volume_size_split = __re.split(r'x', volume_size)
                    s1, s2, s3 = float(volume_size_split[0].replace(" ","")), float(volume_size_split[1].replace(" ","")), float(volume_size_split[2].replace(" ","").strip('cm').strip())
                    volume_size = '{}x{}x{} cm'.format(s1, s2, s3)
                    tumor_size = max(s1, s2, s3)
                    break
    return tumor_size
def get_detect_result(soap, report, SK=soap_tokenizer, RT=report_tokenizer):
    Histology_dict = {0:'NoRCP',1:'SCLC',2:'NSCLC',3:'AIS',4:'ADC',5:'Sqcc',6:'LCC',7:'unknown'}
    Stage_dict = {0:'0',1:'I',2:'II',3:'III',4:'IV',5:'unknown'}
    EGFR_dict = {0:'U',1:'PN'}
    gene_dict = {0:'N',1:'P'}
    
    soap = _soap_preprocessing(soap)
    report = _rm_ref(report)
    soap_input_seq = __get_input_seq(soap, SK)
    report_input_seq = __get_input_seq(report, RT)
    EGFR_input_seq = __get_input_seq(_get_EGRF_context(report), report_tokenizer,200)
    EGFR20_input_seq = __get_input_seq(_get_EGRF_context(report), report_tokenizer,150)
    ALK_input_seq = __get_input_seq(_gene_context('ALK',report), report_tokenizer,300)
    ROS1_input_seq = __get_input_seq(_gene_context('ROS1',report),report_tokenizer)
    KRAS_input_seq = __get_input_seq(_gene_context('KRAS',report), report_tokenizer,100)
#     =========
    Histology = Histology_dict[_Histology_model.predict(soap_input_seq).argmax(axis=-1)[0]]
    Operation = _Operation_model.predict(soap_input_seq).argmax(axis=-1)[0] #0/1
    PDL1 = _PDL1_model.predict(report_input_seq).argmax(axis=-1)[0] #0/1
    Stage = Stage_dict[_Stage_model.predict(report_input_seq).argmax(axis=-1)[0]] 
    EGFR = EGFR_dict[_gene_EGFR_model.predict(report_input_seq).argmax(axis=-1)[0]] #U/PN
    if EGFR=='PN':
        EGFR = []
        EGFR_18 = _gene_EGFR_18_model.predict(EGFR_input_seq).argmax(axis=-1)[0]
        EGFR_19 = _gene_EGFR_19_model.predict(EGFR_input_seq).argmax(axis=-1)[0]
        EGFR_20 = _gene_EGFR_20_model.predict(EGFR20_input_seq).argmax(axis=-1)[0]
        EGFR_21 = _gene_EGFR_21_model.predict(EGFR_input_seq).argmax(axis=-1)[0]
        for exon in ['18','19','20','21']:
            if locals()['EGFR_'+exon]==1:
                EGFR.append(exon)
        if bool(EGFR):
            EGFR = ','.join(EGFR)
        else:
            EGFR = 'N'
    for gene in ['ALK','ROS1','KRAS']:
        if gene in report:
            gene_model = locals()['_{}_II_model'.format(gene)]
            input_seq = locals()['{}_input_seq'.format(gene)]
            globals()[gene] = gene_dict[gene_model.predict(input_seq).argmax(axis=-1)[0]]
        else:
            globals()[gene] = 'U'

    Tumor_size = _get_histologic_type(report)
    return [Operation, Histology, Tumor_size, Stage, EGFR, ALK, ROS1, KRAS, PDL1]

# "BRAF","RET","NTRK","MET","P53"
def phenotype_9(soap, report): 
    values = get_detect_result(soap, report)
    key = ["operation","histology","Tumor_size","stage","EGFR","ALK","ROS1","KRAS","PDL1"]
    output_json = dict(zip(key, values))
    return output_json
    
    
    
    
    
    
    
    
