import notify

if __name__ == "__main__":
    worker = notify.notified("localhost", 55556)
    worker.start()