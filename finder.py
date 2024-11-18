import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pyperclip  # Kopyalama işlemi için pyperclip kütüphanesini kullanıyoruz

# Global 'result' değişkeni
result = []

# Dosya adında anahtar kelimeyi %100 eşleşme ile arama
def search_in_file(file_path, keyword, file_types):
    file_name = os.path.basename(file_path)  # Sadece dosya adı
    # Dosya türüne göre kontrol yapılacaksa, dosya uzantısı eşleşmeli
    if any(file_path.endswith(ext) for ext in file_types):
        # Eğer anahtar kelime dosya adına benziyorsa, dosyayı listele
        if not keyword or keyword.lower() in file_name.lower():  # Anahtar kelime dosya adında olmalı
            return file_name, file_path  # Dosya adı ve yolunu döndür
    return None

# Dosya yolu (klasör ismi) üzerinde de arama yapılması
def search_in_directory(directory, keyword, file_types):
    result = []
    for root, dirs, files in os.walk(directory):  # Bu satır sadece belirtilen dizinde arama yapacak
        for file in files:
            file_path = os.path.join(root, file)
            file_result = search_in_file(file_path, keyword, file_types)
            if file_result:
                result.append(file_result)  # Dosya adı ve tam yoluyla birlikte ekle
    return result

# Alfabedik sıralama fonksiyonu
def sort_alphabetically(result):
    return sorted(result, key=lambda x: x[0].lower())  # Dosya adını küçük harflerle sıralar

# Tarihsel sıralama fonksiyonu
def sort_by_date(result):
    return sorted(result, key=lambda x: os.path.getmtime(x[1]))  # Dosyanın son değiştirilme zamanına göre sıralar

# Klasör seçme fonksiyonu
def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        directory_entry.delete(0, tk.END)
        directory_entry.insert(0, directory)

# Bilgisayarınızdaki tüm sabit sürücüleri (diskleri) tarama
def get_all_drives():
    drives = []
    # Windows işletim sistemi üzerinde çalışan bir yöntem
    for drive in range(65, 91):  # A'dan Z'ye kadar (65 - 90 ASCII kodları)
        drive_letter = chr(drive) + ":\\"  # Sürücü harfini oluştur
        if os.path.isdir(drive_letter):  # Eğer o sürücü varsa
            drives.append(drive_letter)
    return drives

# Arama fonksiyonu
def perform_search():
    global result  # Global 'result' değişkenini burada kullanıyoruz
    keyword = keyword_entry.get()  # Anahtar kelimeyi alalım

    # Dosya türleri seçildiğinde, listeyi oluşturuyoruz
    selected_file_types = []
    if pdf_var.get():
        selected_file_types.append(".pdf")
    if word_var.get():
        selected_file_types.append((".docx", ".doc", ".rtf"))  # Tüm Word dökümanları
    if excel_var.get():
        selected_file_types.append((".xlsx", ".xls", ".csv"))  # Tüm Excel dökümanları
    if pptx_var.get():
        selected_file_types.append((".pptx", ".ppt", ".pps"))  # Tüm PowerPoint dökümanları
    if image_var.get():
        selected_file_types.append("image")
    if dwg_var.get():
        selected_file_types.append(".dwg")

    # Autocad dosyalarını ekledik
    if all_var.get():
        selected_file_types = [".pdf", ".docx", ".doc", ".rtf", ".xlsx", ".xls", ".csv", ".pptx", ".ppt", ".pps", "image", ".dwg"]  # Tüm dosya türleri

    # Eğer dosya türü seçilmediyse tüm türleri içeren liste kullanılır
    if not selected_file_types:
        selected_file_types = [".pdf", ".docx", ".doc", ".rtf", ".xlsx", ".xls", ".csv", ".pptx", ".ppt", ".pps", "image", ".dwg"]

    result = []  # Sonuçları temizleyelim

    # **Anahtar kelime kontrolü**
    directory = directory_entry.get()  # Klasör seçimi
    if directory:  # Klasör seçilmişse
        result = search_in_directory(directory, keyword, selected_file_types)  # Klasördeki dosyalar listelenecek
    else:  # Klasör seçilmemişse, tüm bilgisayarda arama yapılacak
        messagebox.showinfo("Bilgilendirme", "Klasör seçilmedi. Tüm bilgisayarda arama yapılacak, işlem zaman alabilir.")
        drives = get_all_drives()  # Tüm sürücüleri alalım
        for drive in drives:
            result.extend(search_in_directory(drive, keyword, selected_file_types))  # Her sürücüde arama yapalım

    # Sonuçları sıralama
    if sort_var.get() == 1:  # Alfabeye göre sıralama
        result = sort_alphabetically(result)
    elif sort_var.get() == 2:  # Tarihe göre sıralama
        result = sort_by_date(result)

    # Sonuçları listele
    if result:
        result_listbox.delete(0, tk.END)  # Önceki sonuçları temizle
        for item in result:
            file_name = item[0]  # Dosya adı
            result_listbox.insert(tk.END, file_name)
            result_listbox.itemconfig(tk.END, {'bg': '#f0f0f0'})  # Arka plan rengini değiştir
    else:
        messagebox.showinfo("Sonuç", "Anahtar kelimeye uygun dosya bulunamadı.")

# Dosya yoluna gitmek için tıklama işlemi
def on_listbox_select(event):
    global result  # Global 'result' değişkenini burada kullanıyoruz
    selection = result_listbox.curselection()
    if selection:
        selected_item = result_listbox.get(selection[0])  # Dosya yolunu bulmak için tüm sonuçları kontrol et
        for item in result:
            if item[0] == selected_item:
                file_path = item[1]  # Tam dosya yolu
                try:
                    os.startfile(file_path)  # Dosyayı açmak için os.startfile kullanıyoruz
                except Exception as e:
                    messagebox.showerror("Hata", f"Dosya açılamadı: {e}")

# Sağ tıklama menüsü
def show_right_click_menu(event):
    right_click_menu.post(event.x_root, event.y_root)

# Dosya yolunu kopyalama fonksiyonu
def copy_file_path(event):
    global result  # Global 'result' değişkenini burada kullanıyoruz
    selection = result_listbox.curselection()
    if selection:
        selected_item = result_listbox.get(selection[0])  # Seçilen dosya adını alalım
        for item in result:
            if item[0] == selected_item:
                file_path = item[1]  # Dosyanın tam yolunu bulalım
                pyperclip.copy(file_path)  # Dosya yolunu panoya kopyala
                messagebox.showinfo("Bilgi", f"Dosya yolu kopyalandı: {file_path}")
                break

# GUI Tasarımı
root = tk.Tk()
root.title("Finder")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{int(screen_width * 0.8)}x{int(screen_height * 0.8)}")  # Pencereyi ekranın %80 boyutunda aç
root.configure(bg="#f4f4f4")  # Arka plan rengi

# Stil ayarları
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6)
style.configure("TEntry", font=("Arial", 12), padding=6)
style.configure("TLabel", font=("Arial", 12, "bold"), background="#f4f4f4")  # Etiketlerin fontu kalın
style.configure("TCheckbutton", font=("Arial", 12), background="#f4f4f4")

# Klasör Seç Butonu
folder_button = ttk.Button(root, text="Klasör Seç", command=browse_directory)
folder_button.pack(pady=10)

directory_entry = ttk.Entry(root, width=60)
directory_entry.pack(pady=5)

# Anahtar kelime girişi
keyword_label = ttk.Label(root, text="Anahtar Kelime:")
keyword_label.pack(pady=10)
keyword_entry = ttk.Entry(root, width=50)
keyword_entry.pack(pady=5)

# Dosya türlerini seçme (Checkbuttons)
file_types_label = ttk.Label(root, text="Dosya Türü:")
file_types_label.pack(pady=10)

file_types_frame = ttk.Frame(root)
file_types_frame.pack(pady=5)

pdf_var = tk.BooleanVar()
word_var = tk.BooleanVar()
excel_var = tk.BooleanVar()
pptx_var = tk.BooleanVar()
image_var = tk.BooleanVar()
dwg_var = tk.BooleanVar()
all_var = tk.BooleanVar()

pdf_check = ttk.Checkbutton(file_types_frame, text="PDF", variable=pdf_var)
pdf_check.grid(row=0, column=0, padx=5)
word_check = ttk.Checkbutton(file_types_frame, text="Word Dokümanları", variable=word_var)
word_check.grid(row=0, column=1, padx=5)
excel_check = ttk.Checkbutton(file_types_frame, text="Excel Dokümanları", variable=excel_var)
excel_check.grid(row=0, column=2, padx=5)
pptx_check = ttk.Checkbutton(file_types_frame, text="PowerPoint Dokümanları", variable=pptx_var)
pptx_check.grid(row=0, column=3, padx=5)
image_check = ttk.Checkbutton(file_types_frame, text="Resimler", variable=image_var)
image_check.grid(row=0, column=4, padx=5)
dwg_check = ttk.Checkbutton(file_types_frame, text="Autocad (.dwg)", variable=dwg_var)
dwg_check.grid(row=0, column=5, padx=5)
all_check = ttk.Checkbutton(file_types_frame, text="Tüm Dosyalar", variable=all_var)
all_check.grid(row=0, column=6, padx=5)

# Sıralama seçenekleri
sort_var = tk.IntVar()
sort_label = ttk.Label(root, text="Sıralama Türü:")
sort_label.pack(pady=10)

alphabetical_rb = ttk.Radiobutton(root, text="Alfabeye Göre", variable=sort_var, value=1)
alphabetical_rb.pack(pady=5)

date_rb = ttk.Radiobutton(root, text="Tarihe Göre", variable=sort_var, value=2)
date_rb.pack(pady=5)

# Arama butonu
search_button = ttk.Button(root, text="Ara", command=perform_search)
search_button.pack(pady=20)

# Sonuçlar Listbox'ı
result_frame = ttk.Frame(root)
result_frame.pack(pady=10)

result_listbox = tk.Listbox(result_frame, width=100, height=20)
result_listbox.pack(side=tk.LEFT)

# Scrollbar ekleme
scrollbar = tk.Scrollbar(result_frame, orient=tk.VERTICAL, command=result_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_listbox.config(yscrollcommand=scrollbar.set)

# Sonuçlara tıklandığında dosya yoluna gitmek için
result_listbox.bind("<Double-1>", on_listbox_select)

# Sağ tıklama menüsünü bağlama
right_click_menu = tk.Menu(root, tearoff=0)
right_click_menu.add_command(label="Dosya Yolunu Kopyala", command=lambda event=None: copy_file_path(event))
result_listbox.bind("<Button-3>", show_right_click_menu)

# Telif Hakkı İfadesi
footer_label = ttk.Label(root, text="© 2024 İsmail Çevik - Her Hakkı Saklıdır.", font=("Arial", 10, "italic"), background="#f4f4f4")
footer_label.pack(side=tk.BOTTOM, pady=5)

# Pencereyi başlatma
root.mainloop()
