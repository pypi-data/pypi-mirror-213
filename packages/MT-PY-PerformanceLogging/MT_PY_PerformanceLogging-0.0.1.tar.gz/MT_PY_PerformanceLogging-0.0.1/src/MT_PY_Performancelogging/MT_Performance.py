import logging
import time

# create a class for our log performance test
class MT_PerformanceLogger:
    def __init__(self, logger_name, log_level=logging.INFO): # creating function for the  performance 
        # logger names track the package/module hierarchy
        self.logger = logging.getLogger(logger_name)  # set the log levels 
        self.logger.setLevel(log_level)

        #Formatters specify the layout of log records 
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s ') # set the formatter for the logs
        self.handler = logging.StreamHandler()  # using console /stream handler        
        self.handler.setLevel(log_level)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    # logic for the performance test 
    def log_performance(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.time()       # initial starting time for the performance test
            result = func(*args, **kwargs)
            end_time = time.time()        # final  time for the performance test
            execution_time = end_time - start_time  # duration for the code to take excute the output 
            # logger info gives you the info of the code (function name and excution duration)
            # self.logger.info(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds")
            self.logger.info(f"Function '{func.__name__}' executed in = started at {start_time}   ended at {end_time} = {(execution_time ):.4f} seconds")


            return result  # after all return the result 
        return wrapper   # return to wrapper function 








import logging
import time

class MT_PerformanceLogger:
    def __init__(self, logger_name, log_level=logging.INFO, log_file='performance.log'):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(log_level)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler = logging.FileHandler(log_file)
        self.handler.setLevel(log_level)
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)

    def log_performance(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            #  for time.time()  it  measures basic unit is second .
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            # self.logger.info(f"Function '{func.__name__}' executed in = started at {start_time}   ended at {end_time} = {(execution_time )*10*3:.3f} milliseconds")
            self.logger.info(f"Function '{func.__name__}' executed in = started at {start_time}   ended at {end_time} = {(execution_time ):.4f} seconds")

            return result
        return wrapper

























































































































import logging
import time

# create a class for our log performance test
class MT_PerformanceLogger:
    def __init__(self, logger_name, log_level=logging.INFO): # craeting function for the  performance 
        self.logger = logging.getLogger(logger_name)  # set the log levels 
        self.logger.setLevel(log_level)

        
        self.handler = logging.FileHandler('basic.log',mode ='a') 
        fileHandler = logging.FileHandler("basic2.log",mode='a')    # creating file with name demo.log and setting mode to append 
        fileHandler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p') # it provides additional control over the log records
        fileHandler.setFormatter(formatter)

        # self.handler = logging.FileHandler('basic2.log',mode ='a')  # using console /stream handler        
        self.handler.setLevel(log_level)
       
        self.logger.addHandler(self.handler)

    # logic for the performance test 
    def log_performance(self, func):
        def wrapper(*args, **kwargs):
            start_time = time.time()       # initial starting time for the performance test
            result = func(*args, **kwargs)
            end_time = time.time()        # final  time for the performance test
            execution_time = end_time - start_time  # duration for the code to take excute the output 
            # logger info gives you the info of the code (function name and excution duration)
            # self.logger.info(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds")
            logging.info(f'Code execution completed. Elapsed time:{start_time} + {end_time} = {execution_time} seconds')

            return result  # after all return the result 
        return wrapper   # return to wrapper function 









