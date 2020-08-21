import socket  
import time 
import threading 
from queue import Queue 

socket.setdefaulttimeout(0.55)
print_lock = threading.Lock() # lock thread during print so we get cleaner outputs
target = input('Host to Scan: ') # convert to ip if given hostname
t_IP = socket.gethostbyname(target)
print ('Scanning Host for Open Ports: ', t_IP)

def portscan(port):
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      conx = s.connect((t_IP, port))
      with print_lock:
         print(port, 'is open')
      conx.close()
   except:
      pass

# threader thread pulls worker from queue and processes
def threader():
   while True:
      worker = q.get() # gets worker from queue# gets worker from queue
      portscan(worker) # run job with worker in queue (thread)
      q.task_done()

# create queue for threader      
q = Queue()
startTime = time.time()

# number of threads  
for x in range(400):
   t = threading.Thread(target = threader)
   t.daemon = True
   t.start() 
for worker in range(1, 65536):
   q.put(worker)  
q.join()

runtime = float("%0.2f" % (time.time() - startTime))
print("Run Time: ", runtime, "seconds")