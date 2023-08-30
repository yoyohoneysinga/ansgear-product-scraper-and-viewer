import tkinter as tk
from tkinter import ttk
import pandas as pd
import webbrowser

# Load CSV data into a DataFrame
def load_csv_data(filename, encoding='utf-8'):
    data = pd.read_csv(filename, encoding=encoding)
    return data

# Search the CSV data
def search_products(data, search_term):
    search_results = data[data['Product Name'].str.contains(search_term, case=False)]
    return search_results

# Update the Treeview with search results
def update_treeview(search_results):
    tree.delete(*tree.get_children())
    for _, row in search_results.iterrows():
        tree.insert("", "end", values=[row['Product Name'], row['Price'], row['Product Link']])

# Search button callback
def search_button_clicked(event=None):  # Added event parameter
    search_term = entry_search.get()
    search_results = search_products(data, search_term)
    update_treeview(search_results)

# Quit button callback
def quit_button_clicked():
    root.quit()

# Open URL in web browser
def open_url():
    if tree.selection():
        item = tree.selection()[0]
        url = tree.item(item, 'values')[2]
        webbrowser.open(url)

# Load CSV data
filename = 'ansgear_products_2.csv'
data = load_csv_data(filename)

# Create the main window
root = tk.Tk()
root.title("CSV Search Tool")

# Center the window on the screen
window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create UI elements
label_search = tk.Label(root, text="Enter a product name to search:")
label_search.pack(pady=(20, 0), anchor="center")

search_frame = tk.Frame(root)
entry_search = tk.Entry(search_frame, width=30)
entry_search.pack(side="left", pady=(0, 10), padx=5)

button_search = tk.Button(search_frame, text="Search", command=search_button_clicked, width=10)
button_search.pack(side="left", pady=(0, 10), padx=5)

search_frame.pack(anchor="center")

button_quit = tk.Button(root, text="Quit", command=quit_button_clicked)
button_quit.pack(anchor="center", pady=20)

# Create a Treeview to display search results
tree = ttk.Treeview(root, columns=("Product Name", "Price", "Product Link"))
tree['show'] = 'headings'
tree.heading("#1", text="Product Name")
tree.heading("#2", text="Price")
tree.heading("#3", text="Product Link")
tree.column("#1", width=300, stretch=tk.YES, anchor="center")
tree.column("#2", width=100, stretch=tk.YES, anchor="center")
tree.column("#3", width=400, stretch=tk.YES, anchor="center")
tree.pack(fill="both", expand=True, padx=20, pady=(0, 20))

# Context menu for opening URL in browser
menu = tk.Menu(tree, tearoff=0)
menu.add_command(label="Open URL in Browser", command=open_url)
tree.menu = menu

def open_url_menu(event):
    if tree.selection():
        tree.menu.post(event.x_root, event.y_root)

tree.bind("<Button-3>", open_url_menu)  # Bind right-click to open context menu

# Bind Enter key to search function
root.bind('<Return>', search_button_clicked)

# Start the GUI event loop
root.mainloop()
