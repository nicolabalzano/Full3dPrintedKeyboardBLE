import pexpect
import sys

child = pexpect.spawn('bluetoothctl', encoding='utf-8')
child.logfile = sys.stdout

child.sendline('agent KeyboardDisplay')
child.expect('Agent registered', timeout=2)
child.sendline('default-agent')
child.expect('Default agent request successful', timeout=2)
child.sendline('scan on')

print("\n--- Scanning for 'keyboard' ---")
# Wait for the device to appear
while True:
    index = child.expect(['Device ([0-9A-F:]+) keyboard', pexpect.TIMEOUT], timeout=5)
    if index == 0:
        mac = child.match.group(1)
        print(f"\nFound keyboard with MAC: {mac}")
        break
    else:
        print(".", end="", flush=True)

child.sendline(f'pair {mac}')
index = child.expect(['Passkey: ([0-9]{6})', 'AuthenticationCanceled', pexpect.TIMEOUT], timeout=15)

if index == 0:
    pin = child.match.group(1)
    print(f"\n\n*** SUCCESS! THE PIN IS: {pin} ***")
    print("TYPE IT ON THE KEYBOARD NOW!")
    child.expect('Pairing successful', timeout=30)
    child.sendline(f'trust {mac}')
    child.sendline(f'connect {mac}')
    child.expect('Connection successful', timeout=10)
    print("ALL DONE!")
elif index == 1:
    print("\nFAILED: Authentication Canceled immediately by host/device.")
else:
    print("\nFAILED: Timeout waiting for pairing.")
