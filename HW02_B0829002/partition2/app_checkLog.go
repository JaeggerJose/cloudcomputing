package main

import (
	"fmt"
	"os"
	"bufio"
	"io"
	"strings"
)

func checkBlock() int {
	i := 1
	for {
		_, err := os.Open(fmt.Sprintf("%d.txt", i))
		if err != nil {
			return i
		}
		i++
	}
}

func main() {
	if len(os.Args) != 2 {
		fmt.Println("Usage: go run app_checkLog.go username")
		os.Exit(1)
	}
	//username := os.Args[1]
	currentBlock := checkBlock()
	for i := 1; i < currentBlock; i++ {
		file, err := os.Open(fmt.Sprintf("%d.txt", i))
		if err != nil {
			fmt.Println("Error opening file:", err)
			return
		}
		defer file.Close()

		reader := bufio.NewReader(file)
		for {
			line, err := reader.ReadString('\n')
			if err == io.EOF {
				break
			} else if err != nil {
				fmt.Println("Error reading file:", err)
				return
			}
			if strings.Contains(line, "Sha256") {
				continue
			}
			if strings.Contains(line, "block:") {
				continue
			}
			sender := strings.Split(line, ",")[0]
			receiver := strings.Split(line, ",")[1]
			receiver = strings.TrimSpace(receiver)
			if sender == os.Args[1] {
				fmt.Printf(line)
			}
			if receiver == os.Args[1] {
				fmt.Printf(line)
			}
		
		}
	}
}