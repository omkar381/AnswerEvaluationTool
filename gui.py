import tkinter as tk
from tkinter import filedialog, messagebox
from answer_eval import extract_text_from_image, evaluate_answer

def start_gui():
    """Start the main GUI."""
    def open_evaluation_window():
        """Open a new window for evaluation after entering the student's name."""
        student_name = student_name_var.get()
        if not student_name.strip():
            messagebox.showerror("Error", "Please enter the student's name!")
            return
        
        # Hide the main window
        main_window.withdraw()

        # Create a new window for evaluation
        eval_window = tk.Toplevel()
        eval_window.title("Evaluate Answer Sheet")
        eval_window.geometry("800x600")

        # Variables for text extraction and marks
        extracted_text = tk.StringVar()
        marks_per_question = tk.StringVar(value="1")
        similarity_threshold = tk.StringVar(value="75")

        def upload_and_extract():
            """Upload an image or PDF and extract the text."""
            file_path = filedialog.askopenfilename(
                filetypes=[("Image Files", "*.png *.jpg *.jpeg"), ("PDF Files", "*.pdf")]
            )
            if file_path:
                try:
                    if file_path.endswith(".pdf"):
                        extracted_text.set(extract_text_from_pdf(file_path))
                    else:
                        extracted_text.set(extract_text_from_image(file_path))
                    messagebox.showinfo("Success", "Text extracted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to extract text: {e}")

        def evaluate_answers():
            """Evaluate answers based on reference text and extracted text."""
            reference_answer = ref_answer_text.get("1.0", tk.END).strip()
            student_text = extracted_text.get()
            threshold = int(similarity_threshold.get())
            marks_per_q = int(marks_per_question.get())

            if not reference_answer or not student_text:
                messagebox.showerror("Error", "Please provide both reference and extracted answers!")
                return
            
            result, similarity = evaluate_answer(reference_answer, student_text, threshold)
            if result:
                messagebox.showinfo(
                    "Result", f"Pass! Similarity: {similarity:.2f}%\nMarks: {marks_per_q}"
                )
            else:
                messagebox.showinfo(
                    "Result", f"Fail! Similarity: {similarity:.2f}%\nMarks: 0"
                )

        # Upload Button
        tk.Label(eval_window, text=f"Student Name: {student_name}", font=("Arial", 14)).pack(pady=10)
        tk.Button(eval_window, text="Upload Answer Sheet", command=upload_and_extract).pack(pady=5)

        # Display extracted text
        tk.Label(eval_window, text="Extracted Text", font=("Arial", 12)).pack()
        tk.Label(eval_window, textvariable=extracted_text, wraplength=700, bg="lightgray", height=10).pack(pady=5)

        # Input for reference answer
        tk.Label(eval_window, text="Reference Answer", font=("Arial", 12)).pack()
        ref_answer_text = tk.Text(eval_window, height=5, width=80)
        ref_answer_text.pack(pady=5)

        # Marks per question
        tk.Label(eval_window, text="Marks Per Question", font=("Arial", 12)).pack()
        tk.Entry(eval_window, textvariable=marks_per_question).pack(pady=5)

        # Similarity threshold
        tk.Label(eval_window, text="Similarity Threshold (%)", font=("Arial", 12)).pack()
        tk.Entry(eval_window, textvariable=similarity_threshold).pack(pady=5)

        # Evaluate Button
        tk.Button(eval_window, text="Evaluate Answers", command=evaluate_answers, bg="green", fg="white").pack(pady=10)

        # Quit Button
        tk.Button(eval_window, text="Close", command=lambda: eval_window.destroy()).pack(pady=10)

    # Main Window
    main_window = tk.Tk()
    main_window.title("Answer Evaluation Tool")
    main_window.geometry("400x300")

    # Input for student name
    tk.Label(main_window, text="Enter Student's Name:", font=("Arial", 14)).pack(pady=20)
    student_name_var = tk.StringVar()
    tk.Entry(main_window, textvariable=student_name_var, width=30).pack(pady=10)

    # Proceed Button
    tk.Button(main_window, text="Proceed to Evaluation", command=open_evaluation_window, bg="blue", fg="white").pack(pady=20)

    # Quit Button
    tk.Button(main_window, text="Quit", command=main_window.destroy, bg="red", fg="white").pack(pady=10)

    main_window.mainloop()
