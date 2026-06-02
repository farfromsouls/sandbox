package main

import (
	"log"
	"log/syslog"
)

// РАБОТАЕТ ТОЛЬКО ДЛЯ LINUX
func main() {
	sysLog, err := syslog.New(syslog.LOG_SYSLOG, "logging.go")

	if err != nil {
		log.Println(err)
		return
	} else {
		log.SetOutput(sysLog)
		log.Print("Everything is fine!")
	}
}