# TODO LIST
# Copyright (C) 2021 MAYUSH, RITHVIK

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from tkinter import *


class Storage:
    def __init__(self) -> None:
        self.tasks = []
        self.task_widgets = []
        self.widget_structure = [None, None, self.task_widgets, None]
        self.creation = False
        self.colors = {
            "add_tasks_fg": "#ff4747",
            "add_tasks_bg": "#333333",
            "add_tasks_active_bg": "#1a1a1a",
            "clear_btn_fg": "#000000",
            "clear_btn_bg": "#eeeeee",
            "clear_btn_active_bg": "#aaaaaa",
            "delete_btn_bg": "#ff4747",
            # "delete_btn_active_bg": "#1a1a1a",
            "delete_btn_active_bg": "#777777",
        }


class GlobalFunctions:
    def __init__(self, root, storage) -> None:
        self.root = root
        self.storage = storage

    def add_task(self, input_task):
        input_value = input_task.get()
        if input_value != "":
            self.storage.tasks.append(input_value)
            self.storage.creation.render()

    def remove_all_below(self):
        for index, widget in enumerate(self.storage.widget_structure):
            if index == 2:
                for widget_data in widget:
                    widget_data[0].destroy()
                    widget_data[1].destroy()
                self.storage.task_widgets = []
                continue
            self.storage.widget_structure[index].destroy()
            self.storage.widget_structure[index] = None

    def clear_all_tasks(self):
        self.storage.tasks = []
        self.remove_all_below()
        self.storage.widget_structure = [None, None, self.storage.task_widgets, None]
        self.storage.creation.render()

    def remove_task(self, btn):
        for index, item in enumerate(self.storage.task_widgets):
            if item[1] == btn:
                self.storage.tasks.pop(index)
                break
        self.storage.task_widgets[index][0].destroy()
        self.storage.task_widgets[index][1].destroy()
        self.storage.task_widgets.pop(index)

    def generate_tasks(self, position_dict):
        row_num = position_dict["row"]
        for task in self.storage.tasks:
            label_01 = Label(
                self.root,
                text=f"{task}",
                anchor="w",
                padx=5,
                pady=5,
                width=40,
                bg="#f4f4f4",
            )
            delete_btn = Button(
                self.root,
                text="❌",
                bg=self.storage.colors["delete_btn_bg"],
                activebackground=self.storage.colors["delete_btn_active_bg"],
                borderwidth=0,
            )
            delete_btn.configure(
                command=lambda delete_btn=delete_btn: self.remove_task(delete_btn)
            )

            label_01.grid(row=row_num, column=0, pady=5)
            delete_btn.grid(row=row_num, column=1, ipady=2)

            self.storage.task_widgets.append([label_01, delete_btn])
            self.storage.widget_structure[2] = self.storage.task_widgets
            row_num += 1
        return row_num


class create_tk:
    def __init__(self, root, objects_dict) -> None:
        self.root = root
        self.storage = objects_dict["storage"]()
        self.storage.creation = self
        self.global_functions = objects_dict["global_func"](self.root, self.storage)
        self.render()

    def render(self):
        if self.storage.widget_structure[3] is not None:
            self.global_functions.remove_all_below()
        # -----------------
        input_task = Entry(self.root, width=40, bg="#f4f4f4")
        my_button = Button(
            self.root,
            text="Add Task",
            command=(lambda x=input_task: self.global_functions.add_task(x)),
            fg=self.storage.colors["add_tasks_fg"],
            bg=self.storage.colors["add_tasks_bg"],
            activeforeground=self.storage.colors["add_tasks_fg"],
            activebackground=self.storage.colors["add_tasks_active_bg"],
            width=40,
            borderwidth=0,
        )

        input_task.grid(row=0, column=0, pady=5, ipady=5, columnspan=2)
        my_button.grid(row=1, column=0, pady=5, ipady=5, columnspan=2)
        # -----------------
        new_row_num = self.global_functions.generate_tasks({"row": 2})
        # -----------------
        clear_tasks_btn = Button(
            self.root,
            text="Clear Tasks",
            command=self.global_functions.clear_all_tasks,
            width=40,
            fg=self.storage.colors["clear_btn_fg"],
            bg=self.storage.colors["clear_btn_bg"],
            activeforeground=self.storage.colors["clear_btn_fg"],
            activebackground=self.storage.colors["clear_btn_active_bg"],
            borderwidth=0,
        )
        clear_tasks_btn.grid(row=new_row_num + 1, ipady=5, column=0, columnspan=2)

        self.storage.widget_structure[0] = input_task
        self.storage.widget_structure[1] = my_button
        self.storage.widget_structure[3] = clear_tasks_btn


def main():
    root = Tk()
    root["bg"] = "#ffffff"
    dict_of_objects = {"storage": Storage, "global_func": GlobalFunctions}
    create_app = create_tk(root, dict_of_objects)
    root.mainloop()


if __name__ == "__main__":
    main()
