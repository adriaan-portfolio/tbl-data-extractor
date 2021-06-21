import pandas as pd
import numpy as np
from datetime import datetime
import logging
import os
import matplotlib.pyplot as plt
import matplotlib
from download_trat import download_trat_results
import time


matplotlib.style.use('ggplot')

def students_in_lectorial(lectorial_no):
    students = pd.read_csv(f"Groups/classList_LE{lectorial_no}.csv")
    return students


def tbl_mark_rubric():
    mark_rubric = pd.DataFrame([0,4,2,1,1], columns = ["Mark"])
    return mark_rubric


def trat_results(session_no, lectorial_number, students, mark_rubric):
    group_results = pd.DataFrame(range(1,17),columns=["Group"])
    for i in range(1,4):
        group_results[f"Q{i}"] = 0
        results = pd.read_csv(f"Session {session_no}/q{i}.csv", header = 1)
        results = results.rename(columns={"[Time][Date]": "Time", "Q1": "Mark"})
        results["Time"] =  pd.to_datetime(results["Time"], format='[%H:%M][%d:%m:%Y]')
        results.sort_values(['Time', 'Student'], ascending=[True, True], inplace=True)

        entries_submitted = results.pivot_table(index=['Student'], aggfunc='size')

        student_submitter = results.drop_duplicates(subset="Student", keep='last')
        student_submitter.reset_index(drop=True, inplace = True)
        student_submitter["Entries"] = 0
        student_submitter["Group"] = ""
        student_submitter["Total"] = 0

        for index, _ in student_submitter.iterrows():
            student_submitter["Entries"][index] = entries_submitted[student_submitter["Student"][index]]
            try:
                student_submitter["Group"][index] = students[students["Username"]==student_submitter["Student"][index]]["Group"].item()
            except:
                student_submitter["Group"][index] = None
                
            try:
                if student_submitter["Mark"][index] == 1:
                    student_submitter["Total"][index] = mark_rubric["Mark"][student_submitter["Entries"][index]]
                else:
                    student_submitter["Total"][index] = 1 #minimum mark, as student did engage
            except:
                student_submitter["Total"][index] = 1

        student_submitter.sort_values("Group", ascending=True, inplace=True)
        student_submitter.drop_duplicates(subset="Group", keep='last', inplace=True)     
        
        for index, _ in group_results.iterrows():
            try:
                group_results[f"Q{i}"][index] = student_submitter[student_submitter["Group"]==group_results["Group"][index]]["Total"].item()
            except:
                group_results[f"Q{i}"][index] = 0
        
    group_results.to_csv(f"Session {session_no}/trat_session{session_no}_lectorial{lectorial_number}_results.csv", index=False)


def visualise_trat(session_no,lectorial_number):
    data = pd.read_csv(f"Session {session_no}/trat_session{session_no}_lectorial{lectorial_number}_results.csv",index_col=["Group"], header=0,usecols=["Group","Q1","Q2","Q3"])
    data.sort_values(by=["Group"],ascending=False, inplace=True)
    graph = data.plot.barh(stacked=False, xticks=[0, 1, 2, 4])
    graph.set_xlabel("Question marks")
    plt.savefig(f"Session {session_no}/trat_session{session_no}_lectorial{lectorial_number}_results.png")
    print("--- %s seconds ---" % (time.time() - start_time))
    plt.show()
    

def main():
    lectorial_number = 1 #Needs to be either 1,2 or 3
    session_no = 1 #week number

    logging.basicConfig(level=logging.INFO)
    download_trat_results(session_no)    

    students = students_in_lectorial(lectorial_number)
    rubric = tbl_mark_rubric()
    trat_results(session_no, lectorial_number, students, rubric)
    visualise_trat(session_no,lectorial_number)


if __name__ == "__main__":
    start_time = time.time()
    main()
    
