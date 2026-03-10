using System;
using System.Collections.Generic;
using System.Windows.Forms;

namespace WinFormsApp1
{
    public partial class AddTrackWin : Form
    {
        private MainWin mainForm;
        private List<Book> unfinishedBooks;

        public AddTrackWin(MainWin mainForm)
        {
            InitializeComponent();
            this.mainForm = mainForm;
            this.Shown += AddTrackWin_Shown;
            textBox2.ReadOnly = true;
            this.comboBox1.SelectedIndexChanged += comboBox1_SelectedIndexChanged;
        }

        private void AddTrackWin_Shown(object sender, EventArgs e)
        {
            LoadUnfinishedBooks();
        }

        private void LoadUnfinishedBooks()
        {
            unfinishedBooks = mainForm.GetAllBooks().FindAll(b => b.ReadedPages < b.Pages);
            comboBox1.DisplayMember = "Title";
            comboBox1.ValueMember = "Id";
            comboBox1.DataSource = unfinishedBooks;
            if (unfinishedBooks.Count > 0)
                comboBox1.SelectedIndex = 0;
        }

        private void comboBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (comboBox1.SelectedItem is Book selectedBook)
            {
                textBox2.Text = $"{selectedBook.ReadedPages} / {selectedBook.Pages}";
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (comboBox1.SelectedItem is not Book selectedBook)
            {
                MessageBox.Show("Выберите книгу.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            string input = textBox1.Text.Trim();
            if (!int.TryParse(input, out int newPage))
            {
                MessageBox.Show("Введите целое число.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            if (newPage <= selectedBook.ReadedPages)
            {
                MessageBox.Show("Новая страница должна быть больше текущей.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            if (newPage > selectedBook.Pages)
            {
                MessageBox.Show("Новая страница не может превышать общее количество страниц.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            int pagesRead = newPage - selectedBook.ReadedPages;

            try
            {
                mainForm.AddReadingHistory(selectedBook.Id, pagesRead, DateTime.Today);
                this.DialogResult = DialogResult.OK;
                this.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при сохранении: {ex.Message}", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}