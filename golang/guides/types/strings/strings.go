package main

import (
	"fmt"
)

func main() {
	aString := "Hello World €"
	fmt.Println("First character", string(aString[0]))

	r := '€'
	fmt.Println("As an int32 value:", r)
	fmt.Printf("As a string: %s and as a character: %c\n", r, r)

	for _, v := range aString {
		fmt.Printf("%x ", v)
	}
	fmt.Println()

	for _, v := range aString {
		fmt.Printf("%c", v)
	}
	fmt.Println()
}