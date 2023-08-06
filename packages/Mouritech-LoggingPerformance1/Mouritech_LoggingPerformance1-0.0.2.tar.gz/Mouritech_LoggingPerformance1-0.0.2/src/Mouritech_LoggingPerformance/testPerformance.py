# # test code for our package 
# '''importing our custom package from our module'''
# from Mouritech_LoggingPerformance.LogPerformance import  PerformanceLogger
# import time
# # Create an instance of PerformanceLogger
# logger = PerformanceLogger(__name__)

# # Use the logger to measure function performance
# @logger.log_performance
# # example code to check the loggingperformance 
# # '''Diasum number =175
# # Disarum Number = 1¹ + 7² + 5³ = 1 + 49 + 125= 175
# # each digit is added with incrementation in power  and the addition of the powered value should be equal to actual input '''
# # function to check the code performance'''
# def my_function():
#     num=int(input('Enter Num value:'))
#     result=0
#     power=1
#     for x in str(num):
#         y=int(x)

#         '''logic to check the dis'''
#         result= result + y**power
#         power=power+1
#     if num==result:
#         print(f'The provide {num} is Disarum')
#     else:
#         print(f'The Provided {num} is Not a Disarum Number')
    
#     '''time sleep function is used to add delay in the execution of a program'''
    
#     time.sleep(1)          # the time taken by code 

# # Call the function
# my_function()













# # import time module 
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




#














































# # test code for our package 
# '''importing our custom package from our module'''
# from Mouritech_LoggingPerformance.LogPerformance import  PerformanceLogger
# import time
# # Create an instance of PerformanceLogger
# logger = PerformanceLogger(__name__)

# # Use the logger to measure function performance
# @logger.log_performance


# def addition(func):
#     def inner(a,b):
#             print("I'm in addition")
#             sum = a+b
#             print("Sum of", a, "and", b, "is", sum)        
#             print("Returning addition")
#             func(sum, a)
#     return inner
# # @logger.log_performance

 

# def subtraction(func):
#     def inner(a,b):
#         print("I'm in subtraction")
#         subtraction = a-b
#         print("Subtraction of", a, "and", b, "is", subtraction)       
#         print("Returning subtraction")
#         func(a, b)
#     return inner
# # @logger.log_performance


 
# # @logger.log_performance
# @addition
# # @logger.log_performance
# @subtraction



# # @logger.log_performance
# def mOperations(a, b):
#     print("I'm in mOperations")
#     print("mOperations execution completed")
# mOperations(15, 10)
   
# time.sleep(1)          # the time taken by code 

# # Call the function
# # my_function()








import time

import logging
from Mouritech_LoggingPerformance.LogPerformance import  PerformanceLogger


logging.basicConfig(level=logging.INFO)

logger = PerformanceLogger(__name__)

@logger.log_performance
def outer_decorator(func):
    @logger.log_performance
    def inner_decorator(*args, **kwargs):
        # Code within inner_decorator
        
        time.sleep(1)
        print("Inner decorator code executed.")
    return inner_decorator



@outer_decorator
def example_function():
    # Code you want to measure
    time.sleep(1)
    print("Example function code executed.")

example_function()


