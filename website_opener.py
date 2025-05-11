import tkinter as tk
from tkinter import messagebox
import webbrowser
import json
from pypinyin import lazy_pinyin, Style

# 存储关键词和网址的映射
url_mapping = {}
# 存储映射信息的文件路径
DATA_FILE = 'url_mapping.json'

# 从文件加载映射信息
try:
    with open(DATA_FILE, 'r') as f:
        url_mapping = json.load(f)
except FileNotFoundError:
    pass

# 修改 add_url 函数，添加更新列表的操作
def add_url():
    keyword = entry_keyword.get()
    url = entry_url.get()
    if keyword and url:
        url_mapping[keyword] = url
        messagebox.showinfo('成功', '关键词和网址已添加')
        update_listbox()
        # 保存映射信息到文件
        with open(DATA_FILE, 'w') as f:
            json.dump(url_mapping, f)
    else:
        messagebox.showerror('错误', '请输入关键词和网址')

# 打开对应网址的函数
def open_url():
    keyword = entry_search.get()
    if keyword in url_mapping:
        webbrowser.open(url_mapping[keyword])
    else:
        messagebox.showerror('错误', '未找到对应的关键词')

# 关键词查询函数
def search_keywords(event=None):
    search_term = entry_search_query.get().lower()
    listbox.delete(0, tk.END)
    for keyword, url in url_mapping.items():
        keyword_pinyin = ''.join(lazy_pinyin(keyword))
        keyword_initials = ''.join([p[0] for p in lazy_pinyin(keyword, style=Style.FIRST_LETTER)])
        if search_term in keyword.lower() or search_term in keyword_pinyin or search_term in keyword_initials:
            listbox.insert(tk.END, f'{keyword}: {url}')

# 创建主窗口
root = tk.Tk()
root.title('网址快捷打开工具')
root.geometry('400x600')
root.configure(bg='#f0f0f0')

# 设置字体样式
font_style = ('Arial', 12)

# 创建输入框和标签
label_keyword = tk.Label(root, text='请输入关键词:', font=font_style, bg='#f0f0f0')
label_keyword.pack(pady=5)
entry_keyword = tk.Entry(root, font=font_style)
entry_keyword.pack(pady=5, padx=20, fill='x')

label_url = tk.Label(root, text='请输入网址:', font=font_style, bg='#f0f0f0')
label_url.pack(pady=5)
entry_url = tk.Entry(root, font=font_style)
entry_url.pack(pady=5, padx=20, fill='x')

# 创建添加按钮
button_add = tk.Button(root, text='添加', command=add_url, font=font_style, bg='#4CAF50', fg='white')
button_add.pack(pady=20)

# 创建搜索输入框和标签
label_search = tk.Label(root, text='请输入要打开的关键词:', font=font_style, bg='#f0f0f0')
label_search.pack(pady=5)
entry_search = tk.Entry(root, font=font_style)
entry_search.pack(pady=5, padx=20, fill='x')
entry_search.bind('<Return>', lambda event: open_url())
button_open = tk.Button(root, text='打开', command=open_url, font=font_style, bg='#2196F3', fg='white')
button_open.pack(pady=20)

# 更新列表显示的函数
def update_listbox():
    listbox.delete(0, tk.END)
    for keyword, url in url_mapping.items():
        listbox.insert(tk.END, f'{keyword}: {url}')

# 创建滑块组件
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox = tk.Listbox(root, font=font_style, bg='white', selectmode=tk.EXTENDED, yscrollcommand=scrollbar.set)
listbox.bind('<Double-1>', lambda event: open_selected_url())
listbox.pack(pady=10, padx=20, fill='both', expand=True, side=tk.LEFT)
scrollbar.config(command=listbox.yview)

# 添加提示标签
label_prompt = tk.Label(root, text='双击打开，双击试试', font=font_style, bg='#f0f0f0')
label_prompt.pack(pady=5)

# 初始化列表框
update_listbox()

# 批量添加网址的函数
def add_urls_batch():
    input_text = text_batch.get('1.0', tk.END).strip()
    # 处理多余字符
    input_text = input_text.replace('`', '').replace('：', ':')
    lines = input_text.split('\n')
    success_count = 0
    for line in lines:
        parts = line.split(':', 1)
        if len(parts) == 2:
            keyword = parts[0].strip()
            url = parts[1].strip()
            if keyword and url:
                url_mapping[keyword] = url
                success_count += 1
    if success_count > 0:
        messagebox.showinfo('成功', f'成功添加 {success_count} 个关键词和网址')
        update_listbox()
        # 保存映射信息到文件
        with open(DATA_FILE, 'w') as f:
            json.dump(url_mapping, f)
    else:
        messagebox.showerror('错误', '未找到有效的关键词和网址')

# 创建批量输入标签
label_batch = tk.Label(root, text='请批量输入（格式：关键词: 网址，每行一组）:', font=font_style, bg='#f0f0f0')
label_batch.pack(pady=5)

# 创建批量输入文本框
text_batch = tk.Text(root, font=font_style, height=5, bg='white')
text_batch.pack(pady=5, padx=20, fill='both', expand=True)

# 创建批量添加按钮
button_batch_add = tk.Button(root, text='批量添加', command=add_urls_batch, font=font_style, bg='#4CAF50', fg='white')
button_batch_add.pack(pady=20)

# 批量删除关键词和网址的函数
def delete_urls_batch():
    selected_indices = listbox.curselection()
    if selected_indices:
        success_count = 0
        for index in reversed(selected_indices):
            selected_item = listbox.get(index)
            keyword = selected_item.split(':')[0].strip()
            if keyword in url_mapping:
                del url_mapping[keyword]
                success_count += 1
        if success_count > 0:
            messagebox.showinfo('成功', f'成功删除 {success_count} 个关键词和网址')
            update_listbox()
            # 保存映射信息到文件
            with open(DATA_FILE, 'w') as f:
                json.dump(url_mapping, f)
    else:
        messagebox.showerror('错误', '请选择要删除的关键词和网址')

# 删除关键词和网址的函数
def delete_url():
    selected_index = listbox.curselection()
    if selected_index:
        selected_item = listbox.get(selected_index)
        keyword = selected_item.split(':')[0].strip()
        if keyword in url_mapping:
            del url_mapping[keyword]
            messagebox.showinfo('成功', '关键词和网址已删除')
            update_listbox()
            # 保存映射信息到文件
            with open(DATA_FILE, 'w') as f:
                json.dump(url_mapping, f)
    else:
        messagebox.showerror('错误', '请选择要删除的关键词和网址')

# 创建批量删除按钮
button_batch_delete = tk.Button(root, text='批量删除', command=delete_urls_batch, font=font_style, bg='#f44336', fg='white')
button_batch_delete.pack(pady=20)

# 创建删除按钮
button_delete = tk.Button(root, text='删除', command=delete_url, font=font_style, bg='#f44336', fg='white')
button_delete.pack(pady=20)
root.bind('<Delete>', lambda event: delete_url())

# 创建查询输入框和标签
label_search_query = tk.Label(root, text='请输入关键词进行查询:', font=font_style, bg='#f0f0f0')
label_search_query.pack(pady=5)
entry_search_query = tk.Entry(root, font=font_style, width=80)
entry_search_query.pack(pady=5, padx=20, fill='x')
entry_search_query.bind('<KeyRelease>', search_keywords)

# 打开选中项对应网址的函数
def open_selected_url():
    selected_index = listbox.curselection()
    if selected_index:
        selected_item = listbox.get(selected_index)
        keyword = selected_item.split(':')[0].strip()
        if keyword in url_mapping:
            webbrowser.open(url_mapping[keyword])
        else:
            messagebox.showerror('错误', '未找到对应的关键词')
    else:
        messagebox.showerror('错误', '请选择要打开的关键词和网址')

# 运行主循环
root.mainloop()