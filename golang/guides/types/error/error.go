package main

import (
	"errors"
	"fmt"
	"os"
	"strconv"
)

func check(a, b int) error {
	if a == 0 && b == 0 {
		return errors.New("This is a custom error message")
	}
	return nil
}

func formatError(a, b int) error {
	if a == 0 && b == 0 {
		return fmt.Errorf("a %d and b %d. UserID: %d", a, b, os.Getegid())
	}
	return nil
}

func main() {
	err := check(0, 10)

	if err == nil {
		fmt.Println("check() ended normally")
	} else {
		fmt.Println(err)
	}

	err = check(0, 0)

	if err.Error() == "This is a custom error message" {
		fmt.Println("Custom error detected")
	}

	err = formatError(0, 0)

	if err != nil {
		fmt.Println(err)
	}

	i, err := strconv.Atoi("-123")

	if err == nil {
		fmt.Println("Int value is", i)
	}

	i, err = strconv.Atoi("Y123")

	if  err != nil {
		fmt.Println(err)
	}
}