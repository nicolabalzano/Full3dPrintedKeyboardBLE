import os, sys, pty, time, re

pid, fd = pty.fork()

if pid == 0:
    os.execvp("bluetoothctl", ["bluetoothctl"])
else:
    output = b""
    os.set_blocking(fd, False)
    
    print("\n--- Starting scan ---")
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
        print("\nCould not find 'keyboard'. Make sure it's turned on and unplugged from USB!")
        sys.exit(1)
        
    os.write(fd, b"scan off\n")
    time.sleep(1)
    
    print(f"\n--- Pairing with {mac} ---")
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
            if b"AuthenticationCanceled" in output or b"AuthenticationFailed" in output:
                print("\nFAILED: Authentication rejected!")
                break
        except BlockingIOError:
            time.sleep(0.1)
        except OSError:
            break
            
    if paired:
        print("\n=======================================")
        print("!!! PAIRING SUCCESSFUL !!!")
        print("=======================================\n")
        os.write(fd, f"trust {mac}\n".encode())
        time.sleep(1)
        os.write(fd, f"connect {mac}\n".encode())
        time.sleep(3)
        print("ALL DONE!")
    else:
        print("\nPairing failed or timed out.")
        
    os.close(fd)
