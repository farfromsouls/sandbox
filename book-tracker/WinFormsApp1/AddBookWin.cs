using System;
using System.Windows.Forms;

namespace WinFormsApp1
{
    public partial class AddBookWin : Form
    {
        private MainWin mainForm;

        public AddBookWin(MainWin mainForm)
        {
            InitializeComponent();
            this.mainForm = mainForm;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            string title = textBox1.Text.Trim();
            string pagesText = textBox2.Text.Trim();
            string tag = textBox3.Text.Trim();

            if (string.IsNullOrEmpty(title))
            {
                MessageBox.Show("Введите название книги.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            if (!int.TryParse(pagesText, out int pages) || pages <= 0)
            {
                MessageBox.Show("Количество страниц должно быть положительным целым числом.", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            try
            {
                mainForm.AddABook(title, pages, tag);
                this.DialogResult = DialogResult.OK;
                this.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Ошибка при добавлении книги: {ex.Message}", "Ошибка", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}