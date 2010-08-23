import sys, traceback, StringIO

def dlog(message):
    if __debug__:
        trace = traceback.extract_stack()[-2]
        file, line, name = trace[0], trace[1], trace[2]
        print "[%s:%s \"%s\"] %s" % (file.split('/')[-1], line, name, message)
        
        
def dtrace(message):
    dlog(message)
    trace = StringIO.StringIO()
    info = sys.exc_info()
    traceback.print_exception(info[0], info[1], info[2], 99, trace)
    for line in trace.getvalue().split('\n'):
        dlog(line)
