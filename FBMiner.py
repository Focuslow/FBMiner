from facebook_scraper import get_posts
import time
import tkinter as tk
import csv


class Mine:
    def __init__(self):
        self.posts = None
        self.name = None
        self.root = tk.Tk()
        self.name_prompt = tk.Label(text="Zadaj meno účtu")
        self.name_entry = tk.Entry()
        self.info = tk.Label(text="Príklad je facebook.com/zeptejsefilipa/ -> meno je zeptejsefilipa\n")
        self.page_prompt = tk.Label(text="Zadaj počet stránok na načítanie (počet scrollov)")
        self.page_entry = tk.Entry()
        self.cookies_prompt = tk.Label(text="Zadaj path ku cookies file")
        self.cookies_entry = tk.Entry()
        self.spam = tk.Label(text="", height=1)
        self.btn = tk.Button(master=self.root, text="Mine and Export data", command=lambda: [self.handle_click()],
                             pady="5")
        self.time_info = tk.Label(text="\n")
        self.export_info = tk.Label(text="\n")

        self.name_prompt.pack()
        self.name_entry.pack()
        self.info.pack()
        self.page_prompt.pack()
        self.page_entry.pack()
        self.cookies_prompt.pack()
        self.cookies_entry.pack()
        self.spam.pack()
        self.btn.pack()
        self.time_info.pack()
        self.export_info.pack()
        self.root.mainloop()

    def export(self):
        name = f"fb_export_{self.name}.csv"
        with open(name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["url", "likes", "comments", "shares"])
            for post in self.posts:
                writer.writerow([post.url, post.likes, post.comments, post.shares])
        self.export_info["text"] = "Export done"

    def handle_click(self):
        self.name = self.name_entry.get()
        pages = self.page_entry.get()
        cookies = self.cookies_entry.get()
        self.posts, time_lapsed = read_fb(self.name, int(pages), cookies)
        self.time_info["text"] = f"\nReading took {time_lapsed} seconds.\n"
        self.export()


class Post:
    def __init__(self, url=0, likes=0, comments=0, shares=0):
        self.url = url
        self.likes = likes
        self.comments = comments
        self.shares = shares


def read_fb(page, num_pages, cookies):
    start = time.perf_counter()
    all_posts = []
    cookies_path = cookies + "\cookies.txt"
    for post in get_posts(page, pages=num_pages, cookies = cookies_path):
        all_posts.append(Post(post["post_url"], post["likes"], post["comments"], post["shares"]))
    return all_posts, time.perf_counter() - start


if __name__ == '__main__':
    app = Mine()
