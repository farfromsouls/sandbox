package main

import (
	"fmt"
	"os"
	"time"
)

func main() {
	var start time.Time = time.Now()

	if len(os.Args) != 2 {
		fmt.Println("Usage: datatime parse_string")
	}

	dateString := os.Args[1]

	d, err := time.Parse("02 January 2006", dateString)
	// тут по сути в ковычках могла быть любая дата,
	// это нужно только для проверки формата (совпадает ли)
	if err != nil {
		fmt.Println("Error during parsing (dd month year)")
	} else {
		fmt.Println("Full:", d)
		fmt.Println("Time:", d.Day(), d.Month(), d.Year())
	}

	d, err = time.Parse("02 January 2006 15:04", dateString)
	if err != nil {
		fmt.Println("Error during parsing (dd month year hh:mm)")
	} else {
		fmt.Println("Full:", d)
		fmt.Println("Date:", d.Day(), d.Month(), d.Year())
		fmt.Println("Time:", d.Hour(), d.Minute())
	}

	d, err = time.Parse("02-01-2006 15:04", dateString)
	if err != nil {
		fmt.Println("Error during parsing (dd-mm-yyyy hh:mm)")
	} else {
		fmt.Println("Full:", d)
		fmt.Println("Date:", d.Day(), d.Month(), d.Year())
		fmt.Println("Time:", d.Hour(), d.Minute())
	}

	d, err = time.Parse("15:04", dateString)
	if err != nil {
		fmt.Println("Error during parsing (hh:mm)")
	} else {
		fmt.Println("Full:", d)
		fmt.Println("Time:", d.Hour(), d.Minute())
	}

	d, err = time.Parse("15:04", dateString)
	if err != nil {
		fmt.Println("Error during parsing (hh:mm)")
	} else {
		fmt.Println("Full:", d)
		fmt.Println("Time:", d.Hour(), d.Minute())
	}
	var t time.Time = time.Now()

	fmt.Println("Epoch time:", t)

	d = time.Unix(int64(t.Second()), 0)

	fmt.Println("Date:", d.Day(), d.Month(), d.Year())
	fmt.Printf("Time: %d:%d\n", d.Hour(), d.Minute())

	// часовые пояса:
	loc, _ := time.LoadLocation("America/New_York")
	fmt.Printf("New York Time: %s\n", time.Now().In(loc))

	var duration time.Duration = time.Since(start)
	fmt.Println("Execution time:", duration)
}
