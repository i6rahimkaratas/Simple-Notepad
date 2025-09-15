import tkinter as tk
from tkinter import scrolledtext
import os
import json

class NotDefteri:
    def __init__(self):
        self.dosya_adi = "notlar.json"
        self.ayarlar_dosyasi = "ayarlar.json"
        
        # Ana pencereyi oluştur
        self.root = tk.Tk()
        self.root.title("Not Defteri")
        self.root.geometry("800x600")
        self.root.configure(bg='black')
        
        # Pencere kapatılırken kaydet
        self.root.protocol("WM_DELETE_WINDOW", self.cikis_yap)
        
        # Metin alanını oluştur
        self.metin_alani = scrolledtext.ScrolledText(
            self.root,
            bg='black',
            fg='white',
            insertbackground='white',  # İmleç rengi
            font=('Consolas', 12),
            wrap=tk.WORD,
            undo=True,
            selectbackground='gray40',
            selectforeground='white'
        )
        
        # Metin alanını pencereye yerleştir (tam ekran)
        self.metin_alani.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Otomatik kaydetme için değişiklik takibi
        self.metin_alani.bind('<KeyRelease>', self.otomatik_kaydet)
        self.metin_alani.bind('<Button-1>', self.otomatik_kaydet)
        
        # Daha önce kaydedilmiş içeriği yükle
        self.notlari_yukle()
        
        # Pencere boyutunu ve pozisyonunu yükle
        self.pencere_ayarlarini_yukle()
        
        # İmleç pozisyonunu en sona getir
        self.metin_alani.focus()
        
    def otomatik_kaydet(self, event=None):
        """Metin değiştiğinde otomatik olarak kaydet"""
        self.root.after(1000, self.notlari_kaydet)  # 1 saniye sonra kaydet
        
    def notlari_kaydet(self):
        """Notları dosyaya kaydet"""
        try:
            metin = self.metin_alani.get("1.0", tk.END)
            imlek_pozisyonu = self.metin_alani.index(tk.INSERT)
            
            veri = {
                'metin': metin,
                'imlek_pozisyonu': imlek_pozisyonu
            }
            
            with open(self.dosya_adi, 'w', encoding='utf-8') as f:
                json.dump(veri, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Kaydetme hatası: {e}")
    
    def notlari_yukle(self):
        """Daha önce kaydedilmiş notları yükle"""
        try:
            if os.path.exists(self.dosya_adi):
                with open(self.dosya_adi, 'r', encoding='utf-8') as f:
                    veri = json.load(f)
                    
                self.metin_alani.insert("1.0", veri.get('metin', ''))
                
                # İmleç pozisyonunu geri yükle
                imlek_pozisyonu = veri.get('imlek_pozisyonu', 'end')
                try:
                    self.metin_alani.mark_set(tk.INSERT, imlek_pozisyonu)
                except:
                    self.metin_alani.mark_set(tk.INSERT, 'end')
                    
        except Exception as e:
            print(f"Yükleme hatası: {e}")
    
    def pencere_ayarlarini_kaydet(self):
        """Pencere boyutu ve pozisyonunu kaydet"""
        try:
            ayarlar = {
                'geometry': self.root.geometry()
            }
            with open(self.ayarlar_dosyasi, 'w', encoding='utf-8') as f:
                json.dump(ayarlar, f)
        except Exception as e:
            print(f"Ayar kaydetme hatası: {e}")
    
    def pencere_ayarlarini_yukle(self):
        """Pencere boyutu ve pozisyonunu yükle"""
        try:
            if os.path.exists(self.ayarlar_dosyasi):
                with open(self.ayarlar_dosyasi, 'r', encoding='utf-8') as f:
                    ayarlar = json.load(f)
                    self.root.geometry(ayarlar.get('geometry', '800x600'))
        except Exception as e:
            print(f"Ayar yükleme hatası: {e}")
    
    def cikis_yap(self):
        """Program kapatılırken yapılacak işlemler"""
        self.notlari_kaydet()
        self.pencere_ayarlarini_kaydet()
        self.root.destroy()
    
    def baslat(self):
        """Uygulamayı başlat"""
        self.root.mainloop()

# Uygulamayı başlat
if __name__ == "__main__":
    uygulama = NotDefteri()
    uygulama.baslat()