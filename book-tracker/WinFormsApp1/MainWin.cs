using Microsoft.Data.Sqlite;
using System.Windows.Forms.DataVisualization.Charting;

namespace WinFormsApp1
{
    public partial class MainWin : Form
    {
        public MainWin()
        {
            InitializeComponent();
            CreateTables();
            List<Book> books = GetAllBooks();
            List<string> tags = GetTags(books);
            UpdateMonthTagsStat(tags);
        }

        public List<string> GetTags(List<Book> books)
        {
            List<string> tags = new List<string>();
            foreach (Book book in books)
            {
                if (!string.IsNullOrEmpty(book.Tag) && !tags.Contains(book.Tag))
                    tags.Add(book.Tag);
            }
            return tags;
        }

        public void UpdateMonthTagsStat(List<string> tags)
        {
            chart1.Series.Clear();
            chart1.ChartAreas.Clear();
            ChartArea chartArea = new ChartArea("MainArea");
            chartArea.AxisX.Title = "Date";
            chartArea.AxisY.Title = "Pages readed";
            chartArea.AxisX.Interval = 1;
            chartArea.AxisX.LabelStyle.Format = "dd.MM";
            chartArea.AxisX.IsMarginVisible = false;
            chart1.ChartAreas.Add(chartArea);
            chart1.ChartAreas[0].AxisX.MajorGrid.Enabled = true;
            chart1.ChartAreas[0].AxisY.MajorGrid.Enabled = true;
            chart1.ChartAreas[0].BackColor = Color.AliceBlue;
            DateTime endDate = DateTime.Today;
            DateTime startDate = endDate.AddDays(-9);
            foreach (string tag in tags)
            {
                Series newSeries = new Series();
                newSeries.Name = tag;
                newSeries.ChartType = SeriesChartType.Spline;
                newSeries.ChartArea = "MainArea";
                newSeries.IsVisibleInLegend = true;
                newSeries.Font = new Font("Microsoft Sans Serif", 8f);
                newSeries.BorderWidth = 3;
                newSeries.MarkerStyle = MarkerStyle.Circle;
                newSeries.MarkerSize = 6;
                for (DateTime date = startDate; date <= endDate; date = date.AddDays(1))
                {
                    int pagesRead = GetPagesReadByTagAndDate(tag, date);
                    newSeries.Points.AddXY(date, pagesRead);
                }
                chart1.Series.Add(newSeries);
            }
            chart1.ChartAreas["MainArea"].AxisX.Minimum = startDate.ToOADate();
            chart1.ChartAreas["MainArea"].AxisX.Maximum = endDate.ToOADate();
            chart1.Invalidate();
        }

        private int GetPagesReadByTagAndDate(string tag, DateTime date)
        {
            using (var connection = new SqliteConnection("Data Source=userdata.db"))
            {
                connection.Open();
                string query = @"
                    SELECT COALESCE(SUM(h.pages_read), 0)
                    FROM History h
                    INNER JOIN Books b ON h.book_id = b._id
                    WHERE b.Tag = @tag AND date(h.read_date) = date(@date)";
                using (var command = new SqliteCommand(query, connection))
                {
                    command.Parameters.AddWithValue("@tag", tag);
                    command.Parameters.AddWithValue("@date", date.ToString("yyyy-MM-dd"));
                    return Convert.ToInt32(command.ExecuteScalar());
                }
            }
        }

        public void CreateTables()
        {
            using (var connection = new SqliteConnection("Data Source=userdata.db"))
            {
                connection.Open();
                string createBooksTable = @"
                    CREATE TABLE IF NOT EXISTS Books (
                        _id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, 
                        Title TEXT NOT NULL UNIQUE, 
                        Pages INTEGER NOT NULL, 
                        ReadedPages INTEGER DEFAULT 0, 
                        Tag TEXT
                    )";
                string createHistoryTable = @"
                    CREATE TABLE IF NOT EXISTS History (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        read_date DATE NOT NULL, 
                        book_id INTEGER NOT NULL,
                        pages_read INTEGER NOT NULL CHECK(pages_read > 0),
                        FOREIGN KEY (book_id) REFERENCES Books(_id) ON DELETE CASCADE
                    )";
                using (var command = new SqliteCommand(createBooksTable, connection))
                    command.ExecuteNonQuery();
                using (var command = new SqliteCommand(createHistoryTable, connection))
                    command.ExecuteNonQuery();
            }
        }

        public List<Book> GetAllBooks()
        {
            var books = new List<Book>();
            using (var connection = new SqliteConnection("Data Source=userdata.db"))
            {
                connection.Open();
                string query = "SELECT _id, Title, Pages, ReadedPages, Tag FROM Books ORDER BY Title";
                using (var command = new SqliteCommand(query, connection))
                using (var reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        var book = new Book
                        {
                            Id = reader.GetInt32(0),
                            Title = reader.GetString(1),
                            Pages = reader.GetInt32(2),
                            ReadedPages = reader.IsDBNull(3) ? 0 : reader.GetInt32(3),
                            Tag = reader.IsDBNull(4) ? string.Empty : reader.GetString(4)
                        };
                        books.Add(book);
                    }
                }
            }
            return books;
        }

        public void AddABook(string title, int pages, string tag = "")
        {
            using (var connection = new SqliteConnection("Data Source=userdata.db"))
            {
                connection.Open();
                string query = @"
                    INSERT INTO Books (Title, Pages, ReadedPages, Tag) 
                    VALUES (@title, @pages, 0, @tag)";
                using (var command = new SqliteCommand(query, connection))
                {
                    command.Parameters.AddWithValue("@title", title);
                    command.Parameters.AddWithValue("@pages", pages);
                    command.Parameters.AddWithValue("@tag", string.IsNullOrEmpty(tag) ? DBNull.Value : (object)tag);
                    command.ExecuteNonQuery();
                }
            }
            RefreshChart();
        }

        private void RefreshChart()
        {
            List<Book> books = GetAllBooks();
            List<string> tags = GetTags(books);
            UpdateMonthTagsStat(tags);
        }

        public void AddReadingHistory(int bookId, int pagesRead, DateTime readDate)
        {
            using (var connection = new SqliteConnection("Data Source=userdata.db"))
            {
                connection.Open();
                string query = @"
            INSERT INTO History (read_date, book_id, pages_read) 
            VALUES (@read_date, @book_id, @pages_read)";
                using (var command = new SqliteCommand(query, connection))
                {
                    command.Parameters.AddWithValue("@read_date", readDate.ToString("yyyy-MM-dd"));
                    command.Parameters.AddWithValue("@book_id", bookId);
                    command.Parameters.AddWithValue("@pages_read", pagesRead);
                    command.ExecuteNonQuery();
                }
                string updateQuery = @"
            UPDATE Books 
            SET ReadedPages = ReadedPages + @pages_read 
            WHERE _id = @book_id";
                using (var updateCommand = new SqliteCommand(updateQuery, connection))
                {
                    updateCommand.Parameters.AddWithValue("@pages_read", pagesRead);
                    updateCommand.Parameters.AddWithValue("@book_id", bookId);
                    updateCommand.ExecuteNonQuery();
                }
            }
            RefreshChart(); 
        }

        public void AddTrack_Click_1(object sender, EventArgs e)
        {
            AddTrackWin add = new AddTrackWin(this);
            add.ShowDialog();
        }

        public void AddBook_Click_1(object sender, EventArgs e)
        { 
            AddBookWin add = new AddBookWin(this);
            add.ShowDialog();
        }
    }

    public class Book
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public int Pages { get; set; }
        public int ReadedPages { get; set; }
        public string Tag { get; set; }
        public double ReadPercentage => Pages > 0 ? (double)ReadedPages / Pages * 100 : 0;
    }
}