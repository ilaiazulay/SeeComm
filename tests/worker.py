import notify

if __name__ == "__main__":
    worker = notify.Worker("localhost", 55556)
    worker.start()