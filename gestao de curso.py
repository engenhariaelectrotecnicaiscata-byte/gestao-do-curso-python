import tkinter as tk
from tkinter import ttk, messagebox
import os

# ================== ARQUIVOS ==================
ARQ_CURSOS = "cursos.txt"
ARQ_DISC = "disciplinas.txt"
ARQ_PROF = "professores.txt"

for arq in [ARQ_CURSOS, ARQ_DISC, ARQ_PROF]:
    if not os.path.exists(arq):
        open(arq, "w", encoding="utf-8").close()

# ================== UTIL ==================
def ler(arq):
    with open(arq, "r", encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]

def escrever(arq, linhas):
    with open(arq, "w", encoding="utf-8") as f:
        for l in linhas:
            f.write(l + "\n")

# ================== COMBOBOX ==================
def atualizar_comboboxes():
    cursos = ler(ARQ_CURSOS)
    nomes = [c.split(";")[1] for c in cursos]

    combo_curso_disc["values"] = nomes
    combo_curso_prof["values"] = nomes

    combo_disc_prof["values"] = [d.split(";")[1] for d in ler(ARQ_DISC)]

# ================== CURSOS ==================
def cadastrar_curso():
    cod = ent_cod_curso.get()
    nome = ent_nome_curso.get()
    dur = ent_duracao.get()

    if not cod or not nome:
        messagebox.showerror("Erro", "Preencha todos os campos")
        return

    escrever(ARQ_CURSOS, ler(ARQ_CURSOS) + [f"{cod};{nome};{dur}"])
    listar_cursos()
    atualizar_comboboxes()

    ent_cod_curso.delete(0, tk.END)
    ent_nome_curso.delete(0, tk.END)
    ent_duracao.delete(0, tk.END)

def listar_cursos():
    tabela_cursos.delete(*tabela_cursos.get_children())
    for l in ler(ARQ_CURSOS):
        tabela_cursos.insert("", tk.END, values=l.split(";"))

def eliminar_curso():
    sel = tabela_cursos.selection()
    if not sel:
        messagebox.showwarning("Aviso", "Selecione um curso")
        return

    if not messagebox.askyesno("Confirmar", "Eliminar este curso e tudo ligado a ele?"):
        return

    codigo = tabela_cursos.item(sel)["values"][0]

    escrever(ARQ_CURSOS, [c for c in ler(ARQ_CURSOS) if not c.startswith(codigo + ";")])
    escrever(ARQ_DISC, [d for d in ler(ARQ_DISC) if d.split(";")[2] != codigo])
    escrever(ARQ_PROF, [p for p in ler(ARQ_PROF) if p.split(";")[3] != codigo])

    listar_cursos()
    listar_disciplinas()
    listar_professores()
    atualizar_comboboxes()

# ================== DISCIPLINAS ==================
def cadastrar_disciplina():
    cod = ent_cod_disc.get()
    nome = ent_nome_disc.get()
    curso = combo_curso_disc.get()

    if not cod or not nome or not curso:
        return

    cod_curso = [c.split(";")[0] for c in ler(ARQ_CURSOS) if c.split(";")[1] == curso][0]
    escrever(ARQ_DISC, ler(ARQ_DISC) + [f"{cod};{nome};{cod_curso}"])

    listar_disciplinas()
    atualizar_comboboxes()

    ent_cod_disc.delete(0, tk.END)
    ent_nome_disc.delete(0, tk.END)

def listar_disciplinas():
    tabela_disc.delete(*tabela_disc.get_children())
    cursos = {c.split(";")[0]: c.split(";")[1] for c in ler(ARQ_CURSOS)}

    for l in ler(ARQ_DISC):
        c, n, cod_curso = l.split(";")
        tabela_disc.insert("", tk.END, values=(c, n, cursos.get(cod_curso, "")))

# ================== PROFESSORES ==================
def cadastrar_professor():
    nome = ent_nome_prof.get()
    disc = combo_disc_prof.get()
    curso = combo_curso_prof.get()

    if not nome or not disc or not curso:
        return

    cod_disc = [d.split(";")[0] for d in ler(ARQ_DISC) if d.split(";")[1] == disc][0]
    cod_curso = [c.split(";")[0] for c in ler(ARQ_CURSOS) if c.split(";")[1] == curso][0]

    escrever(ARQ_PROF, ler(ARQ_PROF) + [f"{nome};{disc};{cod_disc};{cod_curso}"])
    listar_professores()

    ent_nome_prof.delete(0, tk.END)

def listar_professores():
    tabela_prof.delete(*tabela_prof.get_children())
    cursos = {c.split(";")[0]: c.split(";")[1] for c in ler(ARQ_CURSOS)}

    for l in ler(ARQ_PROF):
        nome, disc, _, cod_curso = l.split(";")
        tabela_prof.insert("", tk.END, values=(nome, disc, cursos.get(cod_curso, "")))

# ================== SAIR ==================
def sair():
    if messagebox.askyesno("Sair", "Deseja sair do sistema?"):
        root.destroy()

# ================== INTERFACE ==================
root = tk.Tk()
root.title("Sistema de Gestão Escolar")
root.geometry("820x600")

abas = ttk.Notebook(root)
abas.pack(expand=True, fill="both")

# ----- CURSOS -----
aba1 = ttk.Frame(abas)
abas.add(aba1, text="Cursos")

ent_cod_curso = ttk.Entry(aba1)
ent_nome_curso = ttk.Entry(aba1)
ent_duracao = ttk.Entry(aba1)

ttk.Label(aba1, text="Código").grid(row=0, column=0)
ttk.Label(aba1, text="Nome").grid(row=1, column=0)
ttk.Label(aba1, text="Duração").grid(row=2, column=0)

ent_cod_curso.grid(row=0, column=1)
ent_nome_curso.grid(row=1, column=1)
ent_duracao.grid(row=2, column=1)

ttk.Button(aba1, text="Cadastrar", command=cadastrar_curso).grid(row=3, column=1)
ttk.Button(aba1, text="Eliminar", command=eliminar_curso).grid(row=3, column=2)

tabela_cursos = ttk.Treeview(aba1, columns=("c", "n", "d"), show="headings")
for col in ("c", "n", "d"):
    tabela_cursos.heading(col, text=col)
tabela_cursos.grid(row=4, column=0, columnspan=3, pady=10)

# ----- DISCIPLINAS -----
aba2 = ttk.Frame(abas)
abas.add(aba2, text="Disciplinas")

ent_cod_disc = ttk.Entry(aba2)
ent_nome_disc = ttk.Entry(aba2)
combo_curso_disc = ttk.Combobox(aba2)

ent_cod_disc.grid(row=0, column=1)
ent_nome_disc.grid(row=1, column=1)
combo_curso_disc.grid(row=2, column=1)

ttk.Button(aba2, text="Cadastrar", command=cadastrar_disciplina).grid(row=3, column=1)

tabela_disc = ttk.Treeview(aba2, columns=("c", "n", "cu"), show="headings")
for col in ("c", "n", "cu"):
    tabela_disc.heading(col, text=col)
tabela_disc.grid(row=4, column=0, columnspan=3)

# ----- PROFESSORES -----
aba3 = ttk.Frame(abas)
abas.add(aba3, text="Professores")

ent_nome_prof = ttk.Entry(aba3)
combo_disc_prof = ttk.Combobox(aba3)
combo_curso_prof = ttk.Combobox(aba3)

ent_nome_prof.grid(row=0, column=1)
combo_disc_prof.grid(row=1, column=1)
combo_curso_prof.grid(row=2, column=1)

ttk.Button(aba3, text="Cadastrar", command=cadastrar_professor).grid(row=3, column=1)

tabela_prof = ttk.Treeview(aba3, columns=("p", "d", "c"), show="headings")
for col in ("p", "d", "c"):
    tabela_prof.heading(col, text=col)
tabela_prof.grid(row=4, column=0, columnspan=3)

# ----- SAIR -----
ttk.Button(root, text="Sair", command=sair).pack(pady=5)

# ================== START ==================
listar_cursos()
listar_disciplinas()
listar_professores()
atualizar_comboboxes()

root.mainloop()