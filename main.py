import tkinter as tk
import grades
import course

class ClassMate(tk.Frame):
    def __init__(self, root):
        self.white = '#FFFFFF'
        self.green = '#1D9919'
        self.black = '#000000'
        self.red = '#E41E1E'
        self.grey = '#ABABAB' 
        self.darkgrey = '#808080'

        


        super().__init__(
            root,
            bg=self.white
        )

        self.main_frame = self
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=0)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=0)
        self.main_frame.rowconfigure(1, weight=1)

        self.load_main_widgets()

    def load_main_widgets(self):
        self.create_page()
        self.create_header()
        self.create_sidebar()
        self.home_page()

    def clear_frame(self, frame):
        for child in frame.winfo_children():
            child.destroy()


    def create_page(self):
        self.page = tk.Frame(
            self.main_frame,
            bg=self.grey
        )
        self.page.grid(row=1, column=1, sticky = tk.NSEW)


    def create_header(self):
        self.header = tk.Frame(
            self.main_frame,
            bg=self.white
        )
        self.header.grid(row=0, column=0, columnspan=2, sticky=tk.EW)
        self.header.columnconfigure(1, weight=1)

        page_header = tk.Label(
            self.header,
            fg=self.black,
            bg=self.white,
            font=('Times New Roman', 30, "bold"),
            text='ClassMate',
            pady=10, padx=10
        )
        page_header.grid(column=0, row=0)

        add_class_button = tk.Button(
            self.header,
            fg=self.black,
            bg=self.grey,
            highlightbackground=self.white,
            text='Add Class',
            highlightthickness=0,
            font=('Times New Roman', 14),
            padx=10,
            command= self.new_class_page
        )
        add_class_button.grid(column=2, row=0)

    def new_category_page(self, code):
        self.clear_frame(self.page)
        name_var = tk.StringVar()
        weight_var = tk.StringVar()
        assignments_var = tk.StringVar()

        title = tk.Label(
            self.page,
            fg = self.black,
            bg = self.grey,
            font = ('Times New Roman', 24, 'bold'),
            text = 'Add a Category:'
        )
        title.grid(column=0, row=0, padx=10, pady=10)

        name_label = tk.Label (
            self.page,
            fg = self.black,
            bg=self.grey,
            font=('Times New Roman', 18),
            text='Category Name:',
            
        )
        name_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        name_entry = tk.Entry (
            self.page,
            font=('Times New Roman', 18),
            bg=self.white,
            fg=self.black,
            width=40,
            textvariable=name_var
        )
        name_entry.grid(column=1, row=1, padx=10, pady=10, sticky=tk.W)

        weight_label = tk.Label (
            self.page,
            fg = self.black,
            bg=self.grey,
            font=('Times New Roman', 18),
            text='Category Weight:'
        )
        weight_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

        weight_entry = tk.Entry (
            self.page,
            font=('Times New Roman', 18),
            bg=self.white,
            fg=self.black,
            width=20,
            textvariable=weight_var
        )
        weight_entry.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)

        assignments_label = tk.Label (
            self.page,
            fg = self.black,
            bg=self.grey,
            font=('Times New Roman', 18),
            text='Number of Assignments:'
        )
        assignments_label.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)

        assignments_entry = tk.Entry (
            self.page,
            font=('Times New Roman', 18),
            bg=self.white,
            fg=self.black,
            width=20,
            textvariable=assignments_var
        )
        assignments_entry.grid(column=1, row=3, padx=10, pady=10, sticky=tk.W)

        def assembleCategory(code, name, weight, assignments):
            weightReal=float(weight)
            assignmentsInt = int(assignments)
            assembledCategory = course.Category(code, name, weightReal, assignmentsInt)
            grades.insert_category(assembledCategory)
            name_entry.delete(0, 'end')
            weight_entry.delete(0, 'end')
            assignments_entry.delete(0, 'end')
            total=grades.check_category_weights(code)
            if total==100: self.class_page(code)
            if total < 100: self.new_category_page(code)
            if total > 100:
                self.obese(code, name)
            
            

        save_category_button = tk.Button(
            self.page,
            text = 'Save Category',
            bg=self.white,
            fg='black',
            highlightbackground=self.grey,
            command=lambda: assembleCategory(code, name_entry.get(), weight_entry.get(), assignments_entry.get())
        )
        save_category_button.grid(column=0, row=4)

    def obese(self, code, category):
        self.clear_frame(self.page)
        grades.remove_category(code, category)
        message = tk.Label (
            self.page,
            text = 'Total weight exceeded 100%.',
            font=('Times New Roman', 40, 'bold'),
            fg='red',
            bg=self.grey 
        )
        message.grid(row=0, column=0)
        okay_button = tk.Button (
            self.page,
            text = 'Okay',
            highlightbackground=self.grey,
            command=lambda: self.new_category_page(code)
        )
        okay_button.grid(row=1, column=0)


    def obeseGrades(self, code, category):
        self.clear_frame(self.page)
        message = tk.Label (
            self.page,
            text = 'Overflow. Cannot input more grades.',
            font=('Times New Roman', 40, 'bold'),
            fg='red',
            bg=self.grey 
        )
        message.grid(row=0, column=0)
        okay_button = tk.Button (
            self.page,
            text = 'Okay',
            highlightbackground=self.grey,
            command=lambda: self.category_page(code, category)
        )
        okay_button.grid(row=1, column=0)

    def add_grade(self, code, category, score):
        scoreInt=float(score)
        if grades.add_grade(code, category, scoreInt) == 0:
            self.obeseGrades(code, category)
        else:
            self.category_page(code, category)

    def update_grade(self, code, category, oldScore, newScore):
        oldScoreInt=float(oldScore)
        newScoreInt=float(newScore)
        if grades.update_grade(code, category, oldScoreInt, newScoreInt) == 0:
            self.invalid_update(code, category)
        self.category_page(code, category)
    
    def invalid_update(self, code, category):
        self.clear_frame(self.page)
        message = tk.Label (
            self.page,
            text = 'Enter a valid grade.',
            font=('Times New Roman', 40, 'bold'),
            fg='red',
            bg=self.grey 
        )
        message.grid(row=0, column=0)
        okay_button = tk.Button (
            self.page,
            text = 'Okay',
            highlightbackground=self.grey,
            command=lambda: self.category_page(code, category)
        )
        okay_button.grid(row=1, column=0)

    def remove_grade(self, code, category, score):
        if grades.remove_grade(code, category, score) == 0:
            self.invalid_update(code, category)
        self.category_page(code, category)



    def category_page(self, code, category):
        self.clear_frame(self.page)
        new_grade_var = tk.StringVar()
        replaced_grade_var = tk.StringVar()
        updated_grade_var = tk.StringVar()
        info=grades.get_category_info(code, category)
        scores=grades.get_category_grades(code, category)
        progress_text = str(grades.grade_progress(code, category))
        potential_text = str(grades.grade_potential(code, category))
        scoresString=''
        if len(scores) > 0:
            for i in range(len(scores)-1):
                string=f'{scores[i]}, '
                scoresString+=string
            scoresString+=str(scores[len(scores)-1])
        else: scoresString = 'None'
        nameLabel = tk.Label(
            self.page,
            text=f'{code}: {category}',
            font=('Times New Roman', 30, 'bold'),
            fg='black',
            bg=self.grey
        )
        gradesLabel = tk.Label (
            self.page,
            text=f'Grades: {scoresString}',
            font=('Times New Roman', 20),
            fg='black',
            bg=self.grey,
            wraplength=600,
            justify=tk.LEFT
        )
        nameLabel.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        gradesLabel.grid(row=1, column=0, columnspan=3, rowspan=2, sticky=tk.W)
        assignmantsLabel = tk.Label (
            self.page,
            text = f'Assignments Remaining: {info[3]-info[4]}',
            font = ('Times New Roman', 20),
            fg='black',
            bg=self.grey,
        )
        assignmantsLabel.grid(row=5, column=0, sticky=tk.W, columnspan=3)
        averageLabel = tk.Label (
            self.page,
            text = f'Average: {grades.grade_average(code, category)} ({grades.category_letter_grade(code, category)})',
            font = ('Times New Roman', 20),
            fg='black',
            bg=self.grey,
        )
        averageLabel.grid(row=3, column=0, sticky=tk.W, columnspan=3)
        progressLabel = tk.Label(
            self.page,
            text = f'Progress: {progress_text}/{potential_text}',
            bg=self.grey,
            fg='black',
            font=('Times New Roman', 20),
        )
        progressLabel.grid(row=4, column=0, sticky=tk.W, columnspan=3)
        new_grade_label = tk.Label(
            self.page,
            text='New Grade: ',
            fg='black',
            bg=self.grey,
            font=('Times New Roman', 20)
        )
        new_grade_label.grid(row=8, column=0, sticky=tk.W)
        new_grade_entry = tk.Entry (
            self.page,
            textvariable=new_grade_var,
            width=10
        )
        new_grade_entry.grid(row=8, column=1, sticky=tk.W)
        new_grade_button = tk.Button (
            self.page,
            text = 'Save Grade',
            highlightbackground=self.grey,
            command=lambda: self.add_grade(code, category, new_grade_entry.get())
        )
        new_grade_button.grid(row=9, column=0, sticky=tk.W)
        edit_grade_entry = tk.Entry (
            self.page,
            textvariable=replaced_grade_var,
            width=10,
        )
        edit_grade_entry.grid(row=10, column=1, sticky=tk.W)
        old_grade_label = tk.Label(
            self.page,
            text='Old Grade: ',
            fg='black',
            bg=self.grey,
            font=('Times New Roman', 20)
        )
        old_grade_label.grid(row=10, column=0, sticky=tk.W)
        updated_grade_entry = tk.Entry (
            self.page,
            textvariable=updated_grade_var,
            width=10
        )
        updated_grade_entry.grid(row=11, column=1, sticky=tk.W)
        new_grade_label = tk.Label(
            self.page,
            text='Updated Grade: ',
            fg='black',
            bg=self.grey,
            font=('Times New Roman', 20)
        )
        new_grade_label.grid(row=11, column=0, sticky=tk.W)
        edit_grade_button = tk.Button (
            self.page,
            text = 'Edit Grade',
            highlightbackground=self.grey,
            command=lambda: self.update_grade(code, category, edit_grade_entry.get(), updated_grade_entry.get())
        )
        edit_grade_button.grid(row=12, column=0, sticky=tk.W)
        remove_grade_label = tk.Label (
            self.page,
            text='Remove Grade: ',
            fg='black',
            bg=self.grey,
            font=('Times New Roman', 20)
        )
        remove_grade_label.grid(row=13, column=0, sticky=tk.W)
        remove_grade_entry = tk.Entry (
            self.page,
            width=10
        )
        remove_grade_entry.grid(row=13, column=1, sticky=tk.W)
        remove_grade_button = tk.Button (
            self.page,
            text = 'Remove Grade',
            highlightbackground=self.grey,
            command=lambda: self.remove_grade(code, category, remove_grade_entry.get())
        )
        remove_grade_button.grid(row=14, column=0, sticky=tk.W)

    
    

    def class_page(self, code):
        self.clear_frame(self.page)
        classInfo = grades.get_class_by_code(code)
        className = classInfo[0]
        classCode = classInfo[1]
        classCategories=grades.get_course_categories(code)

        nameLabel = tk.Label(
            self.page,
            text = f'{classCode} - {className}',
            foreground='black',
            bg=self.grey,
            font=('Times New Roman', 30, 'bold'),
        )
        nameLabel.grid(row=0, column=0, columnspan=3)

        letterLabel = tk.Label(
            self.page,
            text=f'({grades.letter_grade(code)})',
            foreground='black',
            bg=self.grey,
            font=('Times New Roman', 30, 'bold'),
        )
        letterLabel.grid(row=0, column=3, sticky = tk.W)

        nameHeader = tk.Label (
            self.page,
            text = 'Category',
            font = ('Times New Roman', 24, 'underline'),
            fg='black',
            bg=self.grey
        )
        nameHeader.grid(row=1, column=0, sticky=tk.W)

        weightHeader = tk.Label (
            self.page,
            text = 'Weight',
            font = ('Times New Roman', 24, 'underline'),
            fg='black',
            bg=self.grey
        )
        weightHeader.grid(row=1, column=1, sticky=tk.W)

        progressHeader = tk.Label (
            self.page,
            text = 'Progress',
            font = ('Times New Roman', 24, 'underline'),
            fg='black',
            bg=self.grey
        )
        progressHeader.grid(row=1, column=2, sticky=tk.W)

        averageHeader = tk.Label (
            self.page,
            text = 'Average',
            font = ('Times New Roman', 24, 'underline'),
            fg='black',
            bg=self.grey
        )
        averageHeader.grid(row=1, column=3, sticky=tk.W)

        
        for i in range(len(classCategories)):
            info=classCategories[i]
            average=grades.grade_average(code, classCategories[i])
            progress_text=str(grades.grade_progress(code, classCategories[i]))
            if average == -1: average_text='No Grades'
            else: 
                average_text=str(average)
                average_text+='%'
            potential_text=str(grades.grade_potential(code, classCategories[i]))
            categoryInfo=grades.get_category_info(code, classCategories[i])
            row=i+2
            categoryLabel = tk.Label(
                self.page,
                text = f'{classCategories[i]}:',
                fg='black',
                bg=self.grey,
                font=("Times New Roman",20)
            )
            categoryLabel.grid(row=row, column=0, sticky=tk.W)
            weightLabel = tk.Label(
                self.page,
                text = f'{categoryInfo[2]}%',
                fg='black',
                bg=self.grey,
                font=("Times New Roman",20)
            )
            weightLabel.grid(row=row, column=1, sticky=tk.W)
            progressLabel = tk.Label(
                self.page,
                text = f'{progress_text}/{potential_text}',
                bg=self.grey,
                fg='black',
                font=('Times New Roman', 20),
            )
            progressLabel.grid(row=row, column=2, sticky=tk.W)
            averageLabel = tk.Label(
                self.page,
                text = average_text,
                bg=self.grey,
                fg='black',
                font=('Times New Roman', 20),
            )
            averageLabel.grid(row=row, column=3, sticky=tk.W)
            
            editButton = tk.Button(
                self.page,
                text = f'Edit/View {classCategories[i]}',
                highlightbackground=self.grey,
                command=lambda code=code, info=info: self.category_page(code, info)
            )
            editButton.grid(row=row, column=4, sticky=tk.W)

        categoryLabel = tk.Label(
            self.page,
            text = f'{code} Total:',
            fg='black',
            bg=self.grey,
            font=("Times New Roman",20, 'bold')
        )
        categoryLabel.grid(row=len(classCategories)+3, column=0, sticky=tk.W)
        weightLabel = tk.Label(
            self.page,
            text = '100%',
            fg='black',
            bg=self.grey,
            font=("Times New Roman",20, 'bold')
        )
        weightLabel.grid(row=len(classCategories)+3, column=1, sticky=tk.W)
        progressLabel = tk.Label(
            self.page,
            text = f'{grades.course_progress(code)}/{grades.course_potential(code)}',
            bg=self.grey,
            fg='black',
            font=('Times New Roman', 20, 'bold'),
        )
        progressLabel.grid(row=len(classCategories)+3, column=2, sticky=tk.W)
        averageLabel = tk.Label(
            self.page,
            text = f'{grades.course_average(code)}%',
            bg=self.grey,
            fg='black',
            font=('Times New Roman', 20, 'bold'),
        )
        averageLabel.grid(row=len(classCategories)+3, column=3, sticky=tk.W)
        edit_letters_button = tk.Button (
            self.page,
            text='Grade Cutoffs',
            highlightbackground=self.grey,
            command=lambda: self.edit_letter_page(code)
        )
        edit_letters_button.grid(column=4, row=len(classCategories)+3, sticky=tk.SW)
        remove_class_button = tk.Button (
            self.page,
            text=f'Remove {code}',
            highlightbackground=self.grey,
            command=lambda: self.remove_class(code)
        )
        remove_class_button.grid(column=0, row=len(classCategories)+4, sticky=tk.SW)
        
    def remove_class(self, code):
        grades.remove_class(code)
        self.create_sidebar()
        self.home_page()



    def create_sidebar(self):
        self.courses = grades.get_course_codes()
        self.sidebar = tk.Frame(
            self.main_frame,
            bg = self.darkgrey
        )
        self.sidebar.grid(row=1, column=0, sticky=tk.NSEW)
        homeButton = tk.Button (
            self.sidebar,
            text = 'All Classes',
            highlightbackground=self.darkgrey,
            width=12,
            command=self.home_page
        )
        homeButton.grid(row=0, column=0)
        if len(self.courses) == 0:
            pass
        else:
            for i in range(len(self.courses)):
                info = self.courses[i]
                courseButton = tk.Button (
                    self.sidebar,
                    text = self.courses[i],
                    highlightbackground=self.darkgrey,
                    width=12,
                    command=lambda info=info: self.class_page(info)
                )
                courseButton.grid(row=i+1, column=0)
        print()

    def new_class_page(self):
        self.clear_frame(self.page)

        name_var = tk.StringVar()
        code_var = tk.StringVar()
        hours_var = tk.StringVar()

        title = tk.Label(
            self.page,
            fg = self.black,
            bg = self.grey,
            font = ('Times New Roman', 24, 'bold'),
            text = 'New Class:'
        )
        title.grid(column=0, row=0, padx=10, pady=10)

        name_label = tk.Label (
            self.page,
            fg = self.black,
            bg=self.grey,
            font=('Times New Roman', 18),
            text='Course Name:',
            
        )
        name_label.grid(row=1, column=0, padx=10, pady=10, sticky = tk.W)

        name_entry = tk.Entry (
            self.page,
            font=('Times New Roman', 18),
            bg=self.white,
            fg=self.black,
            width=40,
            textvariable=name_var
        )
        name_entry.grid(column=1, row=1, padx=10, pady=10, sticky=tk.W)

        code_label = tk.Label (
            self.page,
            fg = self.black,
            bg=self.grey,
            font=('Times New Roman', 18),
            text='Course Code:'
        )
        code_label.grid(row=2, column=0, padx=10, pady=10, sticky = tk.W)

        code_entry = tk.Entry (
            self.page,
            font=('Times New Roman', 18),
            bg=self.white,
            fg=self.black,
            width=20,
            textvariable=code_var
        )
        code_entry.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)

        hours_label = tk.Label (
            self.page,
            fg = self.black,
            bg=self.grey,
            font=('Times New Roman', 18),
            text='Credit Hours:'
        )
        hours_label.grid(row=3, column=0, padx=10, pady=10, sticky = tk.W)

        hours_entry = tk.Entry (
            self.page,
            font=('Times New Roman', 18),
            bg=self.white,
            fg=self.black,
            width=20,
            textvariable=hours_var
        )
        hours_entry.grid(column=1, row=3, padx=10, pady=10, sticky=tk.W)

        def assemble_course(name_var, code_var, hours_var):
            assembledCourse = course.Course(name_var, code_var, hours_var)
            grades.insert_class(assembledCourse)
            grades.add_letters(str(code_var))
            name_entry.delete(0, "end")
            code_entry.delete(0, "end")
            hours_entry.delete(0, "end")
            self.courses.append(code_var)
            self.create_sidebar()
            self.new_category_page(code_var)


        class_entry_button = tk.Button (
            self.page,
            font=('Times New Roman', 14),
            bg=self.white,
            fg=self.black,
            highlightbackground=self.grey,
            text='Save Class',
            command=lambda: assemble_course(name_var.get(), code_var.get(), hours_var.get())
        )
        class_entry_button.grid(row=4, column=0, sticky=tk.W, padx=20, pady=10)
    
    def home_page(self):
        self.clear_frame(self.page)
        self.courses=grades.get_course_codes()
        average_header = tk.Label (
            self.page,
            text = 'Average:',
            font=('Times New Roman', 24, 'bold', 'underline'),
            fg='black',
            bg=self.grey 
        )
        average_header.grid(row=0, column=1, sticky=tk.W)
        progress_header = tk.Label (
            self.page,
            text = 'Progress:',
            font=('Times New Roman', 24, 'bold', 'underline'),
            fg='black',
            bg=self.grey 
        )
        progress_header.grid(row=0, column=2, sticky=tk.W, padx=10)
        grade_header = tk.Label (
            self.page,
            text = 'Grade:',
            font=('Times New Roman', 24, 'bold', 'underline'),
            fg='black',
            bg=self.grey 
        )
        grade_header.grid(row=0, column=3, sticky=tk.W, padx=10)
        max_grade_header = tk.Label (
            self.page,
            text = 'Max Grade:',
            font=('Times New Roman', 24, 'bold', 'underline'),
            fg='black',
            bg=self.grey 
        )
        max_grade_header.grid(row=0, column=4, sticky=tk.W, padx=10)


        if len(self.courses) == 0: self.new_class_page()
        else:
            for i in range(len(self.courses)):
                row=i+2
                code=self.courses[i]
                average=grades.course_average(code)
                potential=grades.course_potential(code)
                progress=grades.course_progress(code)
                name=grades.get_class_by_code(code)[0]
                progress_string=f'{progress}/{potential}'
                course_name = tk.Label (
                    self.page,
                    text = f'{name}: ',
                    font=('Times New Roman', 24, 'bold'),
                    fg='black',
                    bg=self.grey 
                )
                course_name.grid(row=row, column=0, sticky=tk.W)
                average_label = tk.Label (
                    self.page,
                    text=f'{average}%',
                    font = ('Times New Roman', 24),
                    fg='black',
                    bg=self.grey
                )
                average_label.grid(row=row, column=1, sticky=tk.W)
                progress_label = tk.Label (
                    self.page,
                    text = progress_string,
                    font = ('Times New Roman', 24),
                    fg='black',
                    bg=self.grey
                )
                progress_label.grid(row=row, column=2, sticky=tk.W, padx = 10)
                grade_label = tk.Label (
                    self.page,
                    text = grades.letter_grade(code),
                    font = ('Times New Roman', 24),
                    fg='black',
                    bg=self.grey
                )
                grade_label.grid(row=row, column=3, sticky=tk.W, padx = 10)
                maxgrade_label = tk.Label (
                    self.page,
                    text = grades.max_letter_grade(code),
                    font = ('Times New Roman', 24),
                    fg='black',
                    bg=self.grey
                )
                maxgrade_label.grid(row=row, column=4, sticky=tk.W, padx = 10)
        gpa_label = tk.Label (
            self.page,
            text=f'GPA: {grades.gpa()}',
            fg='black',
            bg=self.grey,
            font=('Times New Roman', 24, 'bold'),
        )
        gpa_label.grid(row=len(self.courses)+3, column=0)

    def update_letter_cutoff(self, code, letter, entry):
        new=float(entry.get())
        if grades.update_letter_cutoff(code, letter, new) == 0:
            self.letter_update_error(code)
        self.edit_letter_page(code)
        
    def letter_update_error(self, code):
        self.clear_frame(self.page)
        message = tk.Label (
            self.page,
            text = 'Invalid Value.',
            font=('Times New Roman', 40, 'bold'),
            fg='red',
            bg=self.grey 
        )
        message.grid(row=0, column=0)
        okay_button = tk.Button (
            self.page,
            text = 'Okay',
            highlightbackground=self.grey,
            command=lambda: self.edit_letter_page(code)
        )
        okay_button.grid(row=1, column=0)
    
    def edit_letter_page(self, code):
        self.clear_frame(self.page)
        letter_cutoffs = grades.get_letters(code)
        letter_cutoffs.append(0)
        x=['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']
        header = tk.Label (
            self.page,
            text = "Letter Grades:",
            font=('Times New Roman', 24, 'bold'),
            fg='black',
            bg=self.grey,
        )
        header.grid(row=0, column=0, sticky=tk.W, columnspan=2)
        for i in range(len(letter_cutoffs)):
            row=i+1
            info = x[i]
            label = tk.Label (
                self.page,
                text = f'{info} ≥ {letter_cutoffs[i]}',
                bg=self.grey,
                fg='black',
                font=('Times New Roman', 20)
            )
            label.grid(row=row, column=0, sticky=tk.E)
            if i==len(letter_cutoffs)-1: pass
            else:
                entry = tk.Entry (
                    self.page, width=10
                )
                entry.grid(row=row, column=1)
                button = tk.Button (
                    self.page,
                    text=f"Update {info} Cutoff",
                    highlightbackground=self.grey,
                    command=lambda info=info, entry=entry: self.update_letter_cutoff(code, info, entry)
                )
                button.grid(row=row, column=2)
        return_button = tk.Button(
            self.page,
            text=f'Back to {code}',
            highlightbackground=self.grey,
            command = lambda: self.class_page(code)
        )
        return_button.grid(row=len(letter_cutoffs)+2, column=0)







window = tk.Tk()
window.title("ClassMate")
window.geometry('1000x600')
window.resizable(width=False, height=False)
classmate_instance = ClassMate(window)
window.mainloop()
