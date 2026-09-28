import os, sys, pty, time, re

pid, fd = pty.fork()

if pid == 0:
    os.execvp("bluetoothctl", ["bluetoothctl"])
else:
    output = b""
    os.set_blocking(fd, False)
    
    os.write(fd, b"scan on\n")
    
    mac = None
    start_scan = time.time()
    while time.time() - start_scan < 15:
        try:
            data = os.read(fd, 1024)
            output += data
            sys.stdout.write(data.decode('utf-8', 'replace'))
            sys.stdout.flush()
            match = re.search(b"Device ([0-9A-F:]+) keyboard", output)
            if match:
                mac = match.group(1).decode('utf-8')
                print(f"\n*** FOUND KEYBOARD AT {mac} ***")
                break
        except BlockingIOError:
            time.sleep(0.1)
        except OSError:
            break
            
    if not mac:
        print("\nCould not find 'keyboard'.")
        sys.exit(1)
        
    os.write(fd, b"scan off\n")
    time.sleep(1)
    
    for attempt in range(5):
        print(f"\n--- Pairing with {mac} (Attempt {attempt+1}) ---")
        os.write(fd, f"pair {mac}\n".encode())
        
        start_pair = time.time()
        paired = False
        while time.time() - start_pair < 10:
            try:
                data = os.read(fd, 1024)
                output += data
                sys.stdout.write(data.decode('utf-8', 'replace'))
                sys.stdout.flush()
                if b"Pairing successful" in output:
                    paired = True
                    break
                if b"AuthenticationCanceled" in output or b"AuthenticationFailed" in output or b"not available" in output:
                    print("\nFAILED attempt.")
                    break
            except BlockingIOError:
                time.sleep(0.1)
            except OSError:
                break
                
        if paired:
            print("\n!!! PAIRING SUCCESSFUL !!!")
            os.write(fd, f"trust {mac}\n".encode())
            time.sleep(1)
            os.write(fd, f"connect {mac}\n".encode())
            time.sleep(3)
            sys.exit(0)
            
        time.sleep(2)
        
    print("\nPairing failed completely.")
    os.close(fd)
