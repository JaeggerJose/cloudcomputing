package main

import (
	"fmt"
	"os"
	"bufio"
	"strings"
	"io"
	"strconv"
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
	username := os.Args[1]
	var money int = 0
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
			// fully match username
			if strings.Contains(line, username) {
				words := strings.Fields(line)
				num, _ := strconv.Atoi(words[2])
				senderInblock := strings.Split(words[0], ",")[0]
				receiverInblock := strings.Split(words[1], ",")[0]

				if senderInblock == username {
					money -= num
				} else if receiverInblock == username {
					money += num
				} else {
					continue
				}
			}
		}
	}
	fmt.Println(username, "has", money, "dollar(s).")
}