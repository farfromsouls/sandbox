package main

import (
	"fmt"
	"os"
	"path"
)

type Entry struct {
	Name	string
	Surname	string
	Tel 	string
}

var data = []Entry{}

func list() {
	for _, v := range data {
		fmt.Printf("%s %s %s\n", v.Name, v.Surname, v.Tel)
	}
}

func search(key string) *Entry {
	for i, v := range data {
		if v.Surname == key {
			return &data[i]
		}
	}
	return nil
}

func main() {
	arguments := os.Args
	if len(arguments) == 1 {
		exe := path.Base(arguments[0])
		fmt.Printf("Usage: %s search|list <arguments>\n", exe)
		return
	}

	data = append(data, Entry{"Misha", "Ivanov", "001"})
	data = append(data, Entry{"Andrew", "Ivanov", "002"})
	data = append(data, Entry{"Sasha", "Ivanov", "003"})

	switch arguments[1] {

	case "search":

		if len(arguments) != 3 {
			fmt.Println("Usage: search Surname")
			return
		}
		
		result := search(arguments[2])
		
		if result == nil {
			fmt.Println("Entry not found:", arguments[1])
			return
		}

		fmt.Println(*result)

	case "list":
		list()

	default:
		fmt.Println("Not a valid option")
	}
}