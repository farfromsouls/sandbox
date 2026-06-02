package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Printf("Please give me your name: ")
	var name string
	fmt.Scanln(&name)
	fmt.Println("Your name is", name)
	fmt.Println(os.Args[0])
}