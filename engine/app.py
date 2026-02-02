import customtkinter as ctk
from core.genesis_engine import GenesisEngine
import threading
import asyncio

class LucidDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Lucid Empire Console")
        self.geometry("800x600")
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Add tabs
        self.tabview.add("Identity")
        self.tabview.add("Proxy")
        self.tabview.add("Target")
        self.tabview.add("Genesis")
        
        # Identity tab
        self.tabview.tab("Identity").grid_columnconfigure(0, weight=1)
        self.identity_text = ctk.CTkTextbox(self.tabview.tab("Identity"))
        self.identity_text.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.identity_text.insert("0.0", "Paste Fullz here...")
        
        # Proxy tab
        self.tabview.tab("Proxy").grid_columnconfigure(0, weight=1)
        self.proxy_entry = ctk.CTkEntry(self.tabview.tab("Proxy"), placeholder_text="socks5://user:pass@host:port")
        self.proxy_entry.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.check_proxy_button = ctk.CTkButton(self.tabview.tab("Proxy"), text="Check Proxy", command=self.check_proxy)
        self.check_proxy_button.grid(row=1, column=0, padx=20, pady=20)
        
        # Target tab
        self.tabview.tab("Target").grid_columnconfigure(0, weight=1)
        self.target_combobox = ctk.CTkComboBox(self.tabview.tab("Target"), values=["Amazon", "Eneba", "Stripe"])
        self.target_combobox.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        # Genesis tab
        self.tabview.tab("Genesis").grid_columnconfigure(0, weight=1)
        self.generate_button = ctk.CTkButton(self.tabview.tab("Genesis"), text="GENERATE", command=self.generate)
        self.generate_button.grid(row=0, column=0, padx=20, pady=20)
    
    def check_proxy(self):
        """Check proxy validity and geo-location"""
        # Placeholder for proxy validation
        print("Checking proxy...")
        
    def generate(self):
        """Launch the genesis engine"""
        # Get the identity data
        identity_data = self.identity_text.get("1.0", "end")
        # Get the proxy
        proxy = self.proxy_entry.get()
        # Get the target
        target = self.target_combobox.get()
        
        # Run the genesis engine in a separate thread
        thread = threading.Thread(target=self.run_genesis, args=(identity_data, proxy, target))
        thread.start()
        
    def run_genesis(self, identity_data, proxy, target):
        """Run the genesis engine with the provided parameters"""
        # Parse identity data (simplified)
        # In a real scenario, parse the Fullz to extract details
        
        # Configure the genesis engine
        engine = GenesisEngine(persona="student", proxy_geo="New York", proxy_country="US")
        asyncio.run(engine.execute_90_day_cycle())
        
if __name__ == "__main__":
    app = LucidDashboard()
    app.mainloop()
