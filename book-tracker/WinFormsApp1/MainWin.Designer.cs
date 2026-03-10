namespace WinFormsApp1
{
    partial class MainWin
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.Windows.Forms.DataVisualization.Charting.ChartArea chartArea1 = new System.Windows.Forms.DataVisualization.Charting.ChartArea();
            System.Windows.Forms.DataVisualization.Charting.Legend legend1 = new System.Windows.Forms.DataVisualization.Charting.Legend();
            System.Windows.Forms.DataVisualization.Charting.Series series1 = new System.Windows.Forms.DataVisualization.Charting.Series();
            AddTrack = new Button();
            ShowFullStats = new Button();
            AddBook = new Button();
            chart1 = new System.Windows.Forms.DataVisualization.Charting.Chart();
            ((System.ComponentModel.ISupportInitialize)chart1).BeginInit();
            SuspendLayout();
            // 
            // AddTrack
            // 
            AddTrack.Location = new Point(12, 12);
            AddTrack.Name = "AddTrack";
            AddTrack.Size = new Size(164, 29);
            AddTrack.TabIndex = 1;
            AddTrack.Text = "Add track";
            AddTrack.UseVisualStyleBackColor = true;
            AddTrack.Click += AddTrack_Click_1;
            // 
            // ShowFullStats
            // 
            ShowFullStats.Location = new Point(12, 82);
            ShowFullStats.Name = "ShowFullStats";
            ShowFullStats.Size = new Size(164, 29);
            ShowFullStats.TabIndex = 2;
            ShowFullStats.Text = "Show Full Stats";
            ShowFullStats.UseVisualStyleBackColor = true;
            // 
            // AddBook
            // 
            AddBook.Location = new Point(12, 47);
            AddBook.Name = "AddBook";
            AddBook.Size = new Size(164, 29);
            AddBook.TabIndex = 3;
            AddBook.Text = "Add Book";
            AddBook.UseVisualStyleBackColor = true;
            AddBook.Click += AddBook_Click_1;
            // 
            // chart1
            // 
            chart1.BackColor = Color.Transparent;
            chart1.BackSecondaryColor = Color.Black;
            chart1.BorderlineColor = Color.Transparent;
            chartArea1.Name = "ChartArea1";
            chart1.ChartAreas.Add(chartArea1);
            legend1.Docking = System.Windows.Forms.DataVisualization.Charting.Docking.Bottom;
            legend1.Name = "Legend1";
            chart1.Legends.Add(legend1);
            chart1.Location = new Point(182, 12);
            chart1.Name = "chart1";
            series1.BorderWidth = 3;
            series1.ChartArea = "ChartArea1";
            series1.ChartType = System.Windows.Forms.DataVisualization.Charting.SeriesChartType.Spline;
            series1.Legend = "Legend1";
            series1.Name = "Series1";
            chart1.Series.Add(series1);
            chart1.Size = new Size(443, 317);
            chart1.TabIndex = 4;
            chart1.Text = "chart1";
            // 
            // MainWin
            // 
            AutoScaleDimensions = new SizeF(8F, 20F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(637, 341);
            Controls.Add(chart1);
            Controls.Add(AddBook);
            Controls.Add(ShowFullStats);
            Controls.Add(AddTrack);
            MaximumSize = new Size(655, 388);
            MinimumSize = new Size(655, 388);
            Name = "MainWin";
            Text = "Book Tracker";
            ((System.ComponentModel.ISupportInitialize)chart1).EndInit();
            ResumeLayout(false);
        }

        #endregion

        private ContextMenuStrip contextMenuStrip1;
        private Button AddTrack;
        private Button ShowFullStats;
        private Button AddBook;
        private System.Windows.Forms.DataVisualization.Charting.Chart chart1;
    }
}
