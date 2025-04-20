import time, os
def main():
    print("[TEST] Starting HIL Test Runner (polling mode)...")
    max_attempts = 10
    attempt = 0
    found = False
    
    while attempt < max_attempts:
        if os.path.exists("/logs/can_output.log"):
            with open("/logs/can_output.log") as f:
                lines = f.readlines()
                for line in lines:
                    if "0000CC00" in line:
                        print("[PASS] CAN message received!")
                        found = True
                        break
        if found:
            break
        print(f"[INFO] Waiting for CAN message... attempt {attempt+1}")
        time.sleep(1)
        attempt += 1
    
    if not found:
        print("[FAIL] Expected CAN message not found.")

if __name__ == "__main__":
    main()