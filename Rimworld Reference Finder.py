import os
import re
from tkinter.filedialog import askdirectory
import requests
from tkinter import *

main_path = r"C:\\Program Files (x86)\\Steam\\steamapps\\workshop\\content\\294100"
PATTERN = r"Spikecore_Parka"

def find(target) -> list[str] | None:
    prev_ids = []
    result = []
    for path, subdirs, files in os.walk(main_path):
        for file in files:
            if file.endswith('.xml'):
                with open(os.path.join(path, file), 'r') as stream:
                    try:
                        data = stream.read()
                    except:
                        break

                    search_result = re.search(target, data)
                    if search_result is not None:
                        ids =  re.findall(r'294100\\(\d*)', path)

                        if ids is None:
                            break

                        id = ids[0]

                        if id in prev_ids:
                            continue

                        prev_ids.append(id)

                        response = requests.get(f"https://steamcommunity.com/sharedfiles/filedetails/?id={id}")
                        if response.status_code != 200:
                            result.append(str(id + ' ' + (path + r"\\" + file)))
                            continue

                        html = response.text
                        name = re.findall(f'<title>Steam Workshop::(.*)</title>', html)
                        result.append(name[0])

    if len(result) == 0:
        return None
    else:
        return result

if __name__ == '__main__':
    win = Tk()
    win.geometry('600x700')

    path_label = Label(win, text='Set your workshop mods download folder.')
    path_entry = Entry(win, width=80)
    path_entry.insert(0, main_path)
    path_btn = Button(win, text='Browse')

    ref_label = Label(win, text='Enter reference that you are looking for.')
    ref_entry = Entry(win)

    find_btn = Button(win, text='Find')

    result_desc_label = Label(win, text="Search results:")
    result_label = Label(win)

    def browse(event: Event) -> None:
        global path
        path = askdirectory()
        path_entry.delete(0, END)
        path_entry.insert(0, path)

    def on_find_btn(event: Event) -> None:
        target = ref_entry.get()
        if target is None or len(target) < 3:
            result_desc_label.config(text='Wrong search target!')
            return
        result_desc_label.config(text='Searching ...')
        event.widget.update()
        result = find(target)
        result_desc_label.config(text='Search results:')
        if result is None:
            result_label.config(text='Nothing found.')
        else:
            result_label.config(text="\n".join(result))

    path_btn.bind('<Button-1>', browse)
    find_btn.bind('<Button-1>', on_find_btn)

    path_label.pack()
    path_entry.pack()
    path_btn.pack()
    ref_label.pack()
    ref_entry.pack()
    find_btn.pack()
    result_desc_label.pack()
    result_label.pack()

    win.mainloop()    