import time
from PIL import  Image
import streamlit as s
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import seaborn as sns

# progress
progress = s.progress(0)
for i in range(100):
    time.sleep(0.1)
    progress.progress(i + 1)
about = s.sidebar.radio("", ['Home', 'About us'])

#home
if about == "Home":
    s.write(""" # DECISION SUPPORT SYSTEM """)  # title
    # s.subheader(""" Tag: Just upload and predict """)
    s.subheader(""" MODEL PREDICTIONS BASED ON ALREADY TRAINED MODEL""")
    s.write("Pickle file [link] (https://drive.google.com/file/d/1lvJinJcoRIwERhgcImoBC5jIy2Cs438F/view?usp=sharing) ")
    s.subheader(""" steps
                 1. upload file
                 2. File must contain REQUIRED  columns
                 3. select NAN preprocessing according your requiremet
                 4. Download the Example dataset file from link if required
                 """)

    # configurations
    # s.set_option('deprecation.showfileUploderEncoding',False)
    # side bar
    s.write(
        "Download Example dataset[link](https://drive.google.com/file/d/1af84QZB4l13DWEyKPIxlBjtJWG2m6okb/view?usp=sharing)")
    s.sidebar.subheader("upload file")

    # upload file
    file = s.sidebar.file_uploader(label="CSV or EXCEL FILE", type=['csv', 'xlsx'])
    global df
    if file is not None:
        s.write(''' ## Orginal file''')
        try:
            df = pd.read_csv(file)
        except Exception as e:
            df = pd.read_excel(file)
    try:
        s.write(df)
    except:
        s.write('Please upload file in SIDEBAR')

    try:
        if df is not None:
            s.subheader('''Required columns''')
            s.write(''''VARIANT_CLASS', 'TLOD', 'shiftscore', 'Sample.AF', 'SIFT', 'MBQ', 'MFRL', 'MMQ', 'Sample.AD', 'Sample.F1R2',
                 'Sample.F2R1', 'DP', 'GERMQ', 'MPOS',
                 'POPAF', 'Sample.DP''')
            data = df[
                ['VARIANT_CLASS', 'TLOD', 'shiftscore', 'Sample.AF', 'SIFT', 'MBQ', 'MFRL', 'MMQ', 'Sample.AD',
                 'Sample.F1R2',
                 'Sample.F2R1', 'DP', 'GERMQ', 'MPOS',
                 'POPAF', 'Sample.DP']]
            # s.write(data)
            s.write('''## categorical value conversion''')
            a = {'SNV': 0, 'substitution': 1, 'deletion': 2, 'insertion': 3}
            data['VARIANT_CLASS'] = data['VARIANT_CLASS'].map(a)
            b = {'deleterious': 0, 'tolerated': 1, 'deleterious_low_confidence': 2,
                 'tolerated_low_confidence': 3}
            data['SIFT'] = data['SIFT'].map(b)
        else:
            s.write('Please upload correct file')
        # s.write(data)
    except:
        s.write("")

    # counting nan values
    # s.write("NAN values count")
    try:
        a = data.isna().sum()
        aa = dict(a)
        key_list = list(aa.keys())
        value_list = list(aa.values())
        if len(key_list) == len(value_list):
            for i in range(len(value_list)):
                if value_list[i] > 0:
                    value_index = i
                    null_values = key_list[value_index]
                    # print(null_values)
        else:
            s.write("columns are not matching")
        # s.write(null_values, " ", "columns countain NAN values")
    except:
        print("d")
    try:
        s.sidebar.subheader("Select NAN process method")
        NAN = s.sidebar.selectbox("", {"DROP", "MEAN"})
        if NAN == "DROP":
            data = data.dropna()
        if NAN == "MEAN":
            mean_null = data[null_values].mean()
            data[null_values].fillna(value=mean_null, inplace=True)
        s.write("Final Shape of Dataset :", data.shape)
        # s.subheader(''' CORRELATION HEATMAP ''')
        # fig = plt.figure(figsize=(12, 10))
        # cor = data.corr()
        # sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
        # s.write(fig)

    except:
        s.write("")
#     s.sidebar.subheader("Select type of traing and testing")
#     with s.sidebar.beta_expander("see explanation"):
#         s.write("""
#            1.In Already trained option ,using pretrained data prediction are carried out      
#            2.In Training and testinig option, Using supervised learning algorithms you are going to train first then testing
#            """)
#     s.sidebar.radio("Select",['None','Already trained','Training and testing'])

    #data vizualization
    s.write("Select type of operation you want to perform ")
    with s.beta_expander("See explanation"):
        s.write("""
          1. In Datavizualtion option one can perform heatmap and pairplot operation
          2. In Testing option one can perform testing the data with trained model and can observe the graphical output
          3. Both option includes step 1 & 2 process
          """)
    data_choose = s.radio("select", ["Only Datavizualization", "Only Testing", "Both"])
    try:
        if data_choose == "Only Datavizualization":
            s.subheader(""" Select type of graph""")
            choose = s.selectbox("select", ['None','Heatmap', 'pairplot'])


            def grsph(g):

                if g=='None':
                    s.write('')

                elif g == 'pairplot':
                    fig = sns.pairplot(data)
                    s.pyplot(fig)
                    s.write('PairPlot')
                    s.write(fig)
                    if s.button("Save image"):
                        fig.savefig('pairplot.png')
                        s.success('saved!!')

                elif g == 'Heatmap':
                    s.write('correlation Heatmap')
                    fig = plt.figure(figsize=(12, 10))
                    cor = data.corr()
                    plt.title("Heatmap")
                    sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
                    s.write(fig)
                    if s.button("Save image"):
                        fig.savefig('heatmap.png')
                        s.success('saved!!')



            grsph(choose)

        if data_choose == "Only Testing":
            s.write("Testing......")
            with s.beta_expander("See explanation"):
                s.image(Image.open('file/aa.PNG'),caption="Model Results")
                s.write("""
                    1. In this method we are using the already trained model 
                    2. Random forest model used for training
                    3. Model score and pickle file are below
                    4. Download pickle file [link] (https://drive.google.com/file/d/1lvJinJcoRIwERhgcImoBC5jIy2Cs438F/view?usp=sharing)
                 """)
            try:
                # s.sidebar.subheader("Pickle file")
                # s.sidebar.write(
                #     "DOWNLOAD [link](https://drive.google.com/file/d/1lvJinJcoRIwERhgcImoBC5jIy2Cs438F/view?usp=sharing)")
                # pickle_file = s.sidebar.file_uploader(label="Download and Upload")
                if data is not None:
                    with open('file/model.pkl', 'rb') as f:
                        model_load = pickle.load(f)
                    out = model_load.predict(data)

                    # model_load = pickle.load(pickle_file)
                    # out = model_load.predict(data)
                    # s.write(out)
                    s.subheader("PREDICTIONS OUTPUT")
                    p1 = pd.DataFrame(out)
                    p1_count = p1[0].value_counts()
                    p1_pd = pd.DataFrame(p1_count)
                    p = p1[0].value_counts().to_dict()
                    r1 = max(p, key=p.get)
                    r2 = max(list(p.values()))
                    s.info('''Probability of prediction is "{}" type with count of {}'''.format(r1, r2))
                    s.write(p1_pd.rename(columns={0: 'count'}))
                    label = []
                    sizes = []
                    for x, y in p.items():
                        label.append(x)
                        sizes.append(y)
                    try:
                        s.subheader('PIE CHART')
                        f1 = plt.figure(figsize=(10, 30))
                        plt.pie(sizes, labels=label, autopct="%1.1f%%")
                        s.pyplot(f1)
                        if s.button("save image"):
                            f1.savefig('pie.png')
                            s.success('saved!!')

                        s.subheader('BAR CHART')
                        f2 = plt.figure(figsize=(10, 10))
                        plt.bar(label, sizes)
                        plt.xlabel("cancer type")
                        plt.ylabel("Frequency")
                        plt.yticks(rotation=60)
                        plt.xticks(rotation=70)
                        plt.show()
                        s.pyplot(f2)
                        if s.button("Save image"):
                            f2.savefig('barchart.png')
                            s.success('saved!!')

                    except:
                        s.write("error with graphs")
                else:
                    s.write("error with data")
            except:
                s.write("")
        if data_choose == "Both":
            s.write("Both data  vizualization and testing ")
            s.subheader(""" Select type of graph""")
            choose = s.selectbox("", ['Heatmap', 'pairplot'])


            def grsph(g):
                if g=='None':
                    s.write('')
                    
                elif g == 'pairplot':
                    fig = sns.pairplot(data)
                    s.pyplot(fig)
                    s.write('PairPlot')
                    s.write(fig)
                    if s.button("Save Image"):
                        fig.savefig('pairplot.png')
                        s.success('saved!!')
                elif g == 'Heatmap':
                    s.write('correlation Heatmap')
                    fig = plt.figure(figsize=(12, 10))
                    cor = data.corr()
                    sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
                    s.write(fig)
                    if s.button("Save Image"):
                        fig.savefig('heatmap.png')
                        s.success('saved!!')
                else:
                    s.write('Error with graph')


            grsph(choose)
            s.write("Testing......")
            with s.beta_expander("See explanation"):
                s.image(Image.open('file/aa.PNG'),caption="Model Results")
                s.write("""
                    1. In this method we are using the already trained model 
                    2. Random forest model used for training
                    3. Model score and pickle file are below
                    4. Download pickle file [link] (https://drive.google.com/file/d/1lvJinJcoRIwERhgcImoBC5jIy2Cs438F/view?usp=sharing)
                 """)
            try:
                # s.sidebar.subheader("Pickle file")
                # s.sidebar.write(
                #     "DOWNLOAD [link](https://drive.google.com/file/d/1lvJinJcoRIwERhgcImoBC5jIy2Cs438F/view?usp=sharing)")
                # pickle_file = s.sidebar.file_uploader(label="Download and Upload")
                if data is not None:
                    with open('file/model.pkl', 'rb') as f:
                        model_load = pickle.load(f)
                    out = model_load.predict(data)

                    # model_load = pickle.load(pickle_file)
                    # out = model_load.predict(data)
                    # s.write(out)
                    s.subheader("PREDICTIONS OUTPUT")
                    p1 = pd.DataFrame(out)
                    p1_count = p1[0].value_counts()
                    p1_pd = pd.DataFrame(p1_count)
                    p = p1[0].value_counts().to_dict()
                    r1 = max(p, key=p.get)
                    r2 = max(list(p.values()))
                    s.info('''Probability of prediction is "{}" type with count of {}'''.format(r1, r2))
                    s.write(p1_pd.rename(columns={0: 'count'}))
                    label = []
                    sizes = []
                    for x, y in p.items():
                        label.append(x)
                        sizes.append(y)
                    try:
                        s.subheader('PIE CHART')
                        f1 = plt.figure(figsize=(10, 30))
                        plt.pie(sizes, labels=label, autopct="%1.1f%%")
                        s.pyplot(f1)
                        if s.button("save image"):
                            f1.savefig('pie.png')
                            s.success('saved!!')

                        s.subheader('BAR CHART')
                        f2 = plt.figure(figsize=(10, 10))
                        plt.bar(label, sizes)
                        plt.xlabel("cancer type")
                        plt.ylabel("Frequency")
                        plt.yticks(rotation=60)
                        plt.xticks(rotation=70)

                        plt.show()
                        s.pyplot(f2)
                        if s.button("Save image"):
                            f2.savefig('Barchart.png')
                            s.success('saved!!')

                    except:
                        s.write("error with graphs")
                else:
                    s.write("error with data")
            except:
                s.write("Error")
    except:
        s.write("")



    

if about == 'About us':
    s.write("""# DECISION SUPPORT SYSTEM""")
    s.subheader("HI..!")
    s.write(
        "Decision support system for cancer exome datasets,which helps to predict the percentage probability of cancer type for particular features,"
        "through which one can under go personized treatements based on persentage of prediction and early dignosis of cancer also possible.")
    s.write(
        "For model source code click on link: [link] (https://github.com/sabhapathi0306/DSS-for-cancer-exome-datasets) ")
#     s.subheader("Creators")
#     s.write("1. Satyam suresh raiker ")
#     s.write("   RVCE, Biotechnology")
#     s.write("2. Adithya sabhapathi")
#     s.write("   RVCE, Biotechnology")
#     s.write("3. Satyam singh")
#     s.write("   RVCE, Biotechnology")
