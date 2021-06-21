# jinja2 tutorial https://tug.org/tug2019/slides/slides-ziegenhagen-python.pdf

import jinja2
import os


latex_jinja_env = jinja2.Environment(
    block_start_string = '\BLOCK{',
    block_end_string = '}',
    variable_start_string = '\VAR{',
    variable_end_string = '}',
    comment_start_string = '\#{',
    comment_end_string = '}',
    line_statement_prefix = '%-',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader(os.path.abspath('.')) 
)

session = 1

# load template from file
template = latex_jinja_env.get_template('template.tex')
# combine template and variables
document = template.render(session=session)
#write document
path = fr"C:\Users\a-vanniekerk\OneDrive - UWE Bristol (Staff)\UWE\2020_2021\UFMFMS30-1 Dynamics, Modelling, and Simulation\TBL-data-extractor\Session {session}"
with open(os.path.join(path,f"report_session{session}.tex"),'w') as output:
    output.write(document)
