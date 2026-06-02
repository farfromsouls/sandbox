package main

import (
	"fmt"
	"os"
	"strconv"
)

func main() {
	arguments := os.Args
	
	if len(arguments) != 2 {
		fmt.Println("Needs 1 argument!")
		return
	}

	var x string = arguments[1]
	n, _ := strconv.Atoi(x)

	input1 := strconv.Itoa(n)
	fmt.Printf("1) string (Itoa): %s\n", input1)

	input2 := strconv.FormatInt(int64(n), 10)
	fmt.Printf("2) string (FormatInt): %s\n", input2)

	input3 := string(n)
	fmt.Printf("3) string (string()): %s\n", input3)
}