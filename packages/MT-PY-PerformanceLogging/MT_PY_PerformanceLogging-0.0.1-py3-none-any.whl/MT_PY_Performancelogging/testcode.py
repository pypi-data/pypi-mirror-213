# test code for our package 
'''importing our custom package from our module'''
from MT_PY_Performancelogging.MT_Performance import MT_PerformanceLogger
import time
# Create an instance of PerformanceLogger
logger = MT_PerformanceLogger(__name__)

# Use the logger to measure function performance
@logger.log_performance
# example code to check the loggingperformance 
# '''Diasum number =175
# Disarum Number = 1¹ + 7² + 5³ = 1 + 49 + 125= 175
# each digit is added with incrementation in power  and the addition of the powered value should be equal to actual input '''
# function to check the code performance'''
def my_function():
    num=int(input('Enter Num value:'))
    result=0
    power=1
    for x in str(num):
        y=int(x)

        '''logic to check the dis'''
        result= result + y**power
        power=power+1
    if num==result:
        print(f'The provide {num} is Disarum')
    else:
        print(f'The Provided {num} is Not a Disarum Number')
    
    '''time sleep function is used to add delay in the execution of a program'''
    
    time.sleep(1)          # the time taken by code 

# Call the function
my_function()













# import time module 
# import time

# '''Importing our custom package from module Logperformance'''
# from Mouritech_LoggingPerformance.LogPerformance import PerformanceLogger

# # Create an instance of PerformanceLogger with a log file
# logger = PerformanceLogger(__name__, log_file='performance.log')

# # Use the logger to measure function performance
# @logger.log_performance
# def Disarum():
#     '''Code which checks the Provided Number is Disarum number or Not'''
#     num=int(input('Enter Num value:'))
#     result=0
#     power=1
#     for x in str(num):
#         y=int(x)

#         '''Logic to check the disarum Number '''
#         result= result + y**power
#         power=power+1

#         '''If the provided number is same as resultant number then it will be disarum number '''
#     if num==result:
#         print(f'The provide {num} is Disarum')
#     else:
#         print(f'The Provided {num} is Not a Disarum Number')
    

#     '''Time taken by the funtion to excute the output '''
#     time.sleep(1)

# # Call the function
# Disarum()















































# # test code for our package 
# from Mouritech_LoggingPerformance.LogPerformance import  PerformanceLogger
# import time
# # Create an instance of PerformanceLogger
# logger = PerformanceLogger(__name__)
# logging.basicConfig(level=logging.INFO,filename='demo2.log' ,format='%(asctime)s - %(levelname)s - %(message)s')

# # Use the logger to measure function performance
# @logger.log_performance
# # example code to check the loggingperformance 
# # Diasum number =175
# # Disarum Number = 1¹ + 7² + 5³ = 1 + 49 + 125= 175
# # each digit is added with incrementation in power  and the addition of the powered value should be equal to actual input
# def my_function():

#     start_time = time.time()

#     num=int(input('Enter Num value:'))
#     result=0
#     power=1
#     for x in str(num):
#         y=int(x)
#         result= result + y**power
#         power=power+1
#     if num==result:
#         print(f'The provide {num} is Disarum')
#     else:
#         print(f'The Provided {num} is Not a Disarum Number')
    
#     # time sleep function is used to add delay in the execution of a program.
    
#     # time.sleep(1)          # the time taken by code 

#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     logging.info(f'Code execution completed. Elapsed time:{start_time} + {end_time} = {elapsed_time} seconds')


#     # print("The time of excution of the your code is : " ,(end-start) * 10**3 ,"ms")
#     # print(f"The above your code is started at {start} and end at {end} ")

# # Call the function
# my_function()
