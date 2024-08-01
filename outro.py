import pandas as pd

grade = pd.read_excel("horarios.xlsx")
grade.drop(columns=["HR_INICIO","HR_FIM","PERIODO_IDEAL","NOME_DISCIPLINA","DIA_SEMANA"],inplace=True)
super_grade = pd.read_excel("SUPER-GRADE.xlsx")

nova_grade = pd.merge(grade,super_grade,on="COD_DISCIPLINA")

print(nova_grade)