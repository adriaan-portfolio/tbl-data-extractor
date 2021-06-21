import pandas as pd
import glob
import os

def data_extraction(session):

    total_engagement = pd.read_csv("total_engagement.csv")

    os.chdir(fr'Session {session}')
    for file in glob.glob('*UFMFMS-30-1*.csv'):
        os.rename(file,f"gradecenter_session{session}.csv")
    os.rename('analyse_results.csv',f"iRAT_session{session}.csv")
    os.chdir(os.path.dirname(os.getcwd()))

    prestudy_engagement = pd.read_csv(f"Session {session}/gradecenter_session{session}.csv")

    irat_engagement = pd.read_csv(f"Session {session}/iRAT_session{session}.csv", skiprows =1)
    irat_engagement = irat_engagement.rename(columns={"Student":"Username"})

    engagement = pd.merge(prestudy_engagement, irat_engagement, how='outer',on="Username")

    col_name = [col for col in engagement.columns if f'Session {session}' in col]
    total_engagement["Xerte"][session-1]=round(engagement[col_name].count()/engagement["Student ID"].count(),3)*100
    total_engagement["iRAT"][session-1]=round(engagement["Q3"].count()/engagement["Student ID"].count(),3)*100
    total_engagement.to_csv("total_engagement.csv",index=False)

    os.chdir(fr'Session {session}')
    for_table = total_engagement.iloc[0:session,:]
    for_table.to_latex("table.tex",index=False,label="tab:pre_study_engagement", caption="Percentages of students engaging with pre-study material.")
    os.chdir(os.path.dirname(os.getcwd()))

data_extraction(1)