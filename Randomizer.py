import time
import tkinter as tk
from tkinter import messagebox, font
import random
from textwrap import wrap
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph, Spacer
from datetime import datetime

class RandomNumberGeneratorApp:
    def create_pdf(self):
        nowdate = datetime.now().strftime("%d/%m/%Y")
        nowtime = datetime.now().strftime("%H:%M:%S")
        excluded = [int(x.strip()) for x in self.entry_exclude.get(1.0, tk.END).split('\n') if x.strip()]
        n=[int(x.strip()) for x in self.output_text.get(1.0, tk.END).split('\n') if x.strip()]
        w,h = A4
        c = canvas.Canvas("Estrazione.pdf", pagesize=A4)
        t=c.beginText(50, h-50)
        wrapped_excluded = "\n".join(wrap(', '.join(map(str,excluded)),80))
        wrapped_n = "\n".join(wrap(', '.join(map(str,n)),80))
        pdfstring = (
            f"Il giorno {nowdate} alle ore {nowtime} con i seguenti parametri:\n"
            f"\nValore minimo: {self.entry_min.get()}"
            f"\nValore massimo: {self.entry_max.get()}"
            f"\nNumeri generati: {self.entry_count.get()}"
            f"\nSeme generatore: {self.entry_seed.get()} "
            f"\nNumeri esclusi: {wrapped_excluded}\n"
            f"\nSono stati estratti i numeri:\n"
            f"\n{wrapped_n}"
        )
        t.setFont("Times-Roman",20)
        t.textLines("ASL - Lanciano Vasto Chieti")
        t.textLines("\n\n\n\n\n")
        t.setFont("Times-Roman",14)
        t.textLines(pdfstring)
        c.drawText(t)
        # Altezza della riga per il testo
        line_height = 14

        # Definisci il testo con parte del testo come link
        normal_text = 'L\'estrazione è stata effettuta tramite il software "Randomizer", il codice sorgente è pubblicamente consultabile su https://github.com/sp-asl2abruzzo/Randomizer' 

        # Posiziona il testo normale
        c.setFont("Times-Roman", 8)
        c.drawString(40, 40, normal_text)
        c.showPage()
        c.save()

    def __init__(self, master):
        self.master = master
        self.master.config(padx=30)
        
        self.frame1 = tk.Frame(master)
        self.frame1.grid(row=1,column=0, pady=30)

        self.frame2 = tk.Frame(master)
        self.frame2.grid(row=1,column=2)
        

        
        master.title("Generatore di Numeri Casuali")


        self.label_min = tk.Label(self.frame1, text="Valore minimo:")
        self.label_min.grid(row=1, column=0)

        self.entry_min = tk.Entry(self.frame1, bg="#ffff99")
        self.entry_min.grid(row=1, column=1)

        self.label_max = tk.Label(self.frame1, text="Valore massimo:")
        self.label_max.grid(row=2, column=0)

        self.entry_max = tk.Entry(self.frame1, bg="#ffff99")
        self.entry_max.grid(row=2, column=1)

        self.label_count = tk.Label(self.frame1, text="Quanti numeri generare:")
        self.label_count.grid(row=3, column=0)

        self.entry_count = tk.Entry(self.frame1, bg="#ffff99")
        self.entry_count.grid(row=3, column=1)

        self.label_seed = tk.Label(self.frame1, text="Seme generatore:")
        self.label_seed.grid(row=4, column=0)

        self.entry_seed = tk.Entry(self.frame1, bg="#ffff99")
        self.entry_seed.grid(row=4, column=1)
        self.clock_button = tk.Button(self.frame1, text='\u23F0', command=self.update_entry_with_timestamp)
        self.clock_button.grid(row=4, column=2)

        self.label_exclude = tk.Label(self.frame1, text="Numeri da Escludere:")
        self.label_exclude.grid(row=5, column=0, sticky="N", pady=40)

        self.entry_exclude = tk.Text(self.frame1, width=15)
        self.entry_exclude.grid(row=5, column=1, pady=40)


        self.generate_button = tk.Button(master, text="Genera Numeri Casuali", command=self.generate_random_numbers)
        self.generate_button.grid(row=1, column=1, padx=30)


        self.output_label = tk.Label(self.frame2, text="Numeri Generati")
        self.output_label.grid(row=0, column=4)

        self.output_text = tk.Text(self.frame2, height=20, width=15)
        self.output_text.grid(row=1, column=4, sticky="N", pady=30)
        self.output_text.config(state="disabled",font=('Times New Roman', 15, 'bold'))
        self.generate_button = tk.Button(master, text="Esporta pdf...", command=self.create_pdf)
        self.generate_button.grid(row=1, column=3, padx=30)


    def generate_random_numbers(self):
        try:
            min_val = int(self.entry_min.get())
            max_val = int(self.entry_max.get())
            seed_val = int(self.entry_seed.get())
            exclude_val = [int(x.strip()) for x in self.entry_exclude.get(1.0, tk.END).split('\n') if x.strip()]
            count = int(self.entry_count.get())
            
            random.seed(seed_val)
            numbers = [num for num in range(min_val, max_val+1) if num not in exclude_val]
            
            if not numbers:
                messagebox.showinfo("Errore", "Nessun numero valido disponibile.")
                return

            random_numbers = random.sample(numbers, count)
            self.output_text.config(state="normal")
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, '\n'.join(map(str, random_numbers)))
            self.output_text.config(state="disabled")
        except ValueError:
            messagebox.showerror("Errore", "Assicurati di inserire valori validi per i campi.")

    def update_entry_with_timestamp(self):
        # Ottenere il timestamp locale
        local_timestamp = int(time.time_ns())


        # Scrivere il timestamp nella Entry
        self.entry_seed.delete(0, tk.END)  # Cancella il contenuto attuale della Entry
        self.entry_seed.insert(0, local_timestamp)  # Inserisci il timestamp nella Entry


def main():
    root = tk.Tk()
    root.minsize(600,400)
    app = RandomNumberGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
