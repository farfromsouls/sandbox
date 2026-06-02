package main

import (
	// "encoding/csv"
	"fmt"
	// "os"
)

type Task struct {
	name	string
	desc	string
	status	string
}

func printTask(task *Task) {
	fmt.Printf("%s %s %s\n", task.name, task.desc, task.status)
}

func listTasks(tasks []Task) {
	for _, v := range tasks {
		printTask(&v)
	}
}

var data = []Task{}

func main() {
	for {
		fmt.Printf("1) Создать\n2) посмотреть список\n3) удалить\n4) Выход\nКоманда: ")
		x, err := fmt.Scanln()

		if err != nil{
			return
		}

		switch x {
		default:
			fmt.Println("hi")
		}
	}
}
