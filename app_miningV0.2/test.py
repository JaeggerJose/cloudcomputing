import subprocess
import fcntl
import os
import time
import re
import select

def set_non_blocking(fd):
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

def start_process():
    command = './app_mining b0929052'
    return subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)

def main():
    while True:
        process = start_process()  # 啟動新的進程
        set_non_blocking(process.stdout.fileno())  # 設置非阻塞

        start_time = time.time()

        while True:
            rlist, _, _ = select.select([process.stdout], [], [], 0.1)
            answerQuestion = False
            if rlist:
                try:
                    # line = process.stdout.readline()
                    time.sleep(1)
                    # read all std output to get the question
                    line = process.stdout.read().decode('utf-8')
                    # convert the line to file
                    with open('question.txt', 'w+') as f:
                        f.write(line)
                    if not line:
                        break  # 如果沒有更多輸出，則結束迴圈

                    current_time = time.time()
                    elapsed_time = current_time - start_time
                    print(f"Received question after {elapsed_time:.2f} seconds")

                    for i in range(1, 100):
                        for j in range(1, 100):
                            # diff the question file all {i}\*{j}_standard.txt, {i}\*{j}_slant.txt, {i}\*{j}_banner.txt
                            cmd_standard = f"diff {i}\*{j}_standard.txt question.txt"
                            cmd_slant = f"diff {i}\*{j}_slant.txt question.txt"
                            cmd_banner = f"diff {i}\*{j}_banner.txt question.txt"
                            result_standard = subprocess.run(cmd_standard, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            result_slant = subprocess.run(cmd_slant, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            result_banner = subprocess.run(cmd_banner, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            result_small = subprocess.run(f"diff {i}\*{j}_small.txt question.txt", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            
                            # if the diff result is empty, then we find the answer
                            if not result_standard.stdout and not result_standard.stderr:
                                print("find the answer", i, j)
                                answer = i * j
                                process.stdin.write(f"{answer}\n".encode('utf-8'))
                                process.stdin.flush()
                                answerQuestion = True
                                break
                            elif not result_slant.stdout and not result_slant.stderr:
                                print("find the answer", i, j)
                                answer = i * j
                                process.stdin.write(f"{answer}\n".encode('utf-8'))
                                process.stdin.flush()
                                answerQuestion = True
                                break
                            elif not result_banner.stdout and not result_banner.stderr:
                                print("find the answer", i, j)
                                answer = i * j
                                process.stdin.write(f"{answer}\n".encode('utf-8'))
                                process.stdin.flush()
                                answerQuestion = True
                                break
                            elif not result_small.stdout and not result_small.stderr:
                                print("find the answer", i, j)
                                answer = i * j
                                process.stdin.write(f"{answer}\n".encode('utf-8'))
                                process.stdin.flush()
                                answerQuestion = True
                                break
                            
                        if answerQuestion:
                            break
                        
                    if answerQuestion:
                        process.terminate()
                        break
                except IOError:
                    pass
            else:
                time.sleep(2)
                if answerQuestion:
                    process.terminate()
                    break
                    
                print("Waiting for output... and time is", time.time() - start_time)

        process.terminate()  # 結束當前進程
        time.sleep(1)  # 等待進程完全結束，避免產生殭屍進程

if __name__ == "__main__":
    main()
