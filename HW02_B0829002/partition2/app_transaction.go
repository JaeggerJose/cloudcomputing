package main

import (
	"crypto/sha256"
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
)

// checkBlock determines the current block by checking the existence of block files.
func checkBlock() int {
	i := 1
	for {
		if _, err := os.Stat(strconv.Itoa(i) + ".txt"); os.IsNotExist(err) {
			break
		}
		i++
	}
	return i
}

// writeBlock writes the transaction to the specified block.
func writeBlock(currentBlock int, sender, receiver, amount string) {
	fileName := fmt.Sprintf("%d.txt", currentBlock)
	f, err := os.OpenFile(fileName, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		fmt.Println("Error opening file:", err)
		return
	}
	defer f.Close()
	_, err = f.WriteString(fmt.Sprintf("%s, %s, %s\n", sender, receiver, amount))
	if err != nil {
		fmt.Println("Error writing to file:", err)
		return
	}
	fmt.Printf("Transaction written to block %s\n", fileName)
}

func main() {
	if len(os.Args) != 4 {
		fmt.Println("Usage: go run app_transaction.go sender receiver amount")
		os.Exit(1)
	}

	sender := os.Args[1]
	receiver := os.Args[2]
	amount := os.Args[3]

	currentBlock := checkBlock()
	fmt.Printf("Current block: %d.txt\n", currentBlock-1)

	fileName := fmt.Sprintf("%d.txt", currentBlock-1)
	data, err := ioutil.ReadFile(fileName)
	if err != nil {
		fmt.Println("Error reading file:", err)
		return
	}
	// if file length is greater than 8, create a new block
	lines := 0
	for _, b := range data {
		if b == '\n' {
			lines++
		}
	}
	

	if lines >= 7 {
		text := string(data)
		fmt.Println("Text: ", text)
		hash := sha256.Sum256([]byte(text))
		hashStr := fmt.Sprintf("%x", hash)
		fmt.Println("Hash: ", hashStr)

		newFileName := fmt.Sprintf("%d.txt", currentBlock)
		f, err := os.Create(newFileName)
		if err != nil {
			fmt.Println("Error creating file:", err)
			return
		}
		defer f.Close()
		f.WriteString(fmt.Sprintf("Sha256 of previous block: %s\n", hashStr))
		f.WriteString(fmt.Sprintf("Next block: %d.txt\n", currentBlock+1))
		writeBlock(currentBlock, sender, receiver, amount)
	} else {
		writeBlock(currentBlock-1, sender, receiver, amount)
	}
}
