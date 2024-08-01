import pandas as pd
from datetime import datetime

def main():
    grade = pd.read_excel("SUPER-GRADE.xlsx")

    curso = input("Qual seu Curso? (ex: BCC): ")
    grade_curso = pd.read_excel(f"CURSOS/{curso}.xlsx")
    periodo = int(input("Qual seu período? "))
    materias_realizadas = grade_curso[grade_curso["PERIODO"] >= periodo]
    
    materias_faltantes = []
    faltou = input("Deixou de fazer (ou reprovou em) alguma disciplina obrigatória? S (sim) ou N (não): ")
    if faltou == 'S' or faltou == 's':
        print("Qual(is) matéria(s)? Insira o nome exato das disciplinas.")
        i=0
        while True:
            materia = input(f"{i}) ") 
            if materia == "":
                break
            materias_faltantes.append(grade[grade["NOME_DISCIPLINA"] == materia])
            i+=1
    extra = input("Fez alguma(s) disciplina(s) optativa(s)? S (sim) ou N (não): ")
    materias_extra = []
    if extra == 'S' or extra == 's':
        print("Qual(is) matéria(s)? Insira o nome exato da(s) disciplina(s).")
        i=0
        while True:
            materia = input(f"{i}) ")
            if materia == "":
                break
            materias_extra.append(grade[grade["NOME_DISCIPLINA"] == materia])
            i+=1
            
    now = datetime.now()
    formatted_now = now.strftime("%Y-%m-%d-%H-%M-%S")
    
    # grade = materias_realizadas + materias_extra - materias_faltantes
    print(grade, materias_realizadas, materias_extra, materias_faltantes)
    
    if materias_faltantes:
        grade = pd.concat([materias_realizadas,materias_faltantes])
        print(grade)
    if materias_extra:
        grade = grade[~grade.isin(materias_extra).all(axis=1)]
        print(grade)
    grade.to_excel(f"{formatted_now}.xlsx",index=False)
    print("As disciplinas disponíveis em todo o CEFET disponíveis dentro dos requisitos cumpridos por você foram salvos no arquivo:\n"+formatted_now+".xlsx")
    
    conflitos = []
    # Comparar todas as combinações de linhas
    for i, linha1 in grade.iterrows():
        for j, linha2 in grade.loc[i + 1:].iterrows():
            if checa_conflito(linha1, linha2):
                conflitos.append((linha1['COD_DISCIPLINA'], linha2['COD_DISCIPLINA'], linha1['DIA_SEMANA'], linha1['HR_INICIO'], linha1['HR_FIM'], linha2['HR_INICIO'], linha2['HR_FIM']))

    # Mostrar conflitos
    if conflitos:
        grade_conflito = pd.DataFrame(conflitos, columns=['Disciplina1', 'Disciplina2', 'Dia', 'Hora_Início1', 'Hora_Fim1', 'Hora_Início2', 'Hora_Fim2'])
        print(grade_conflito)
        
        grade_conflito.to_excel(f"conflitos_{formatted_now}.xlsx",index=False)
        print("Os horários conflitantes foram salvos no arquivo:\n"+"conflitos_"+formatted_now+".xlsx")

def checa_conflito(linha1, linha2):
    return (linha1['DIA_SEMANA'] == linha2['DIA_SEMANA'] and
            linha1['HR_INICIO'] < linha2['HR_FIM'] and
            linha1['HR_FIM'] > linha2['HR_INICIO'])


if __name__ == "__main__":
    main()






