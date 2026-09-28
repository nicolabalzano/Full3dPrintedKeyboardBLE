import os, sys, pty, time, re

mac = sys.argv[1]

pid, fd = pty.fork()

if pid == 0:
    os.execvp("bluetoothctl", ["bluetoothctl"])
else:
    output = b""
    os.set_blocking(fd, False)
    
    os.write(fd, b"agent KeyboardDisplay\n")
    time.sleep(1)
    os.write(fd, b"default-agent\n")
    time.sleep(1)
    
    for attempt in range(3):
        print(f"\n--- Pairing with {mac} (Attempt {attempt+1}) ---")
        os.write(fd, f"pair {mac}\n".encode())
        
        start_pair = time.time()
        paired = False
        pin_found = False
        while time.time() - start_pair < 25:
            try:
                data = os.read(fd, 1024)
                output += data
                sys.stdout.write(data.decode('utf-8', 'replace'))
                sys.stdout.flush()
                
                match = re.search(b"Passkey: ([0-9]{6})", output)
                if match and not pin_found:
                    pin = match.group(1).decode('utf-8')
                    print(f"\n\n=======================================")
                    print(f"!!! TYPE THIS PIN ON THE KEYBOARD: {pin} !!!")
                    print(f"=======================================\n")
                    pin_found = True
                
                if b"Pairing successful" in output:
                    paired = True
                    break
                if b"AuthenticationCanceled" in output or b"AuthenticationFailed" in output:
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
