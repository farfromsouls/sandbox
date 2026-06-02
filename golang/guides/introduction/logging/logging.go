package main

import (
	"log"
	"log/syslog"
	"os"
	"path"
	"fmt"
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
	
	// if len(os.Args) != 1 {
	// 	log.Fatal("Fatal: Hello World!") // дропает программу
	// }
	// log.Panic("Panic: Hello World!") // exit status 1

	LOGFILE := path.Join(os.TempDir(), "mGo.log")
	f, err := os.OpenFile(LOGFILE, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)

	if err != nil {
		fmt.Println(err)
		return
	}
	defer f.Close()

	LstdFlags := log.Ldate | log.Lshortfile
	iLog := log.New(f, "iNum", LstdFlags)
	iLog.Println("Mastering Go 3rd edition!")

	iLog.SetFlags(log.Lshortfile | log.LstdFlags)
	iLog.Println("Another log entry")
}