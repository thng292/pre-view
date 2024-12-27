import os, dotenv

dotenv.load_dotenv(".env")
import google.generativeai as genai

SYSTEM_INSTRUCTION = """You are an interviewer for job with description:
Mô tả công việc
LG CNS is looking for full stack developers for cloud domain project

Develop software/web applicant
Business Analyst
Cooperate between HQ and VNB

Yêu cầu ứng viên
[Required]

Bachelor's degree of Information Technology or higher
Have working experiment and excellent knowledge at software developing using Java, Spring boot
Have working experiment and excellent knowledge at software developing using React, HTML, JavaScript
Good knowledge about AI (Azure OpenAI and GenAI)
Good knowledge about public cloud (Azure, AWS,)
Database: MariaDB (or MySQL).
[Preferred]

Having experiment with Python and Google cloud
You will use function call get_qestion to get interview question to ask interviewee then receive answer from interviewee, 
you analyitc the answer then use function call result to send your evaluate and get next step you will do.
"""
def result(evaluate: str):
    print("- review:", evaluate)
    global i
    i += 1
    """send evaluate and get next step command.
    Args: 
        evaluate: your evaluate about the anser provided by interviewee.
    Returns:
        A string that is next step you will do.
    """
    return "ask interviewee next question, use function call get_qestion to get interview question" if i <= 3 else "stop interview"

i = 0

qes = [
    "What are the top Java Features",
    "What is JVM",
    "What is JIT",
    """
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.
You may assume that each input would have exactly one solution, and you may not use the same element twice.
You can return the answer in any order.
Example 1:
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
Example 2:
Input: nums = [3,2,4], target = 6
Output: [1,2]
Example 3:
Input: nums = [3,3], target = 6
Output: [0,1]
Constraints:
2 <= nums.length <= 104
-109 <= nums[i] <= 109
-109 <= target <= 109
Only one valid answer exists.
    """
]

def get_qestion():
    global i
    #print(i)
    """Get Qestion for interview

    Args:
        
    Returns:
        A string that is a qestion you will ask interviewee.
    """
    return qes[i]

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel(model_name='gemini-1.5-flash',
                              system_instruction=SYSTEM_INSTRUCTION,
                              tools=[get_qestion, result])
chat = model.start_chat(enable_automatic_function_calling=True)
response = chat.send_message('hello')
print("- chatbot: ",response.candidates[0].content.parts)
input()

print("- me:", """
Simple: Java is quite simple to understand and the syntax
Platform Independent: Java is platform independent means we can run the same program in any software and hardware and will get the same result.
Interpreted: Java is interpreted as well as a compiler-based language. 
Robust: features like Garbage collection, exception handling, etc that make the language robust.
Object-Oriented: Java is an object-oriented language that supports the concepts of class,  objects, four pillars of OOPS, etc. 
Secured: As we can directly share an application with the user without sharing the actual program makes Java a secure language. 
High Performance:  faster than other traditional interpreted programming languages.
Dynamic: supports dynamic loading of classes and interfaces.
Distributed: feature of Java makes us able to access files by calling the methods from any machine connected.
Multithreaded: deal with multiple tasks at once by defining multiple threads
Architecture Neutral: it is not dependent on the architecture.
""")
response = chat.send_message("""
Simple: Java is quite simple to understand and the syntax
Platform Independent: Java is platform independent means we can run the same program in any software and hardware and will get the same result.
Interpreted: Java is interpreted as well as a compiler-based language. 
Robust: features like Garbage collection, exception handling, etc that make the language robust.
Object-Oriented: Java is an object-oriented language that supports the concepts of class,  objects, four pillars of OOPS, etc. 
Secured: As we can directly share an application with the user without sharing the actual program makes Java a secure language. 
High Performance:  faster than other traditional interpreted programming languages.
Dynamic: supports dynamic loading of classes and interfaces.
Distributed: feature of Java makes us able to access files by calling the methods from any machine connected.
Multithreaded: deal with multiple tasks at once by defining multiple threads
Architecture Neutral: it is not dependent on the architecture.
""")
print("- chatbot: ",response.candidates[0].content.parts)
input()

print("- me: ","""
JVM stands for Java Virtual Machine it is a Java interpreter. It is responsible for loading, verifying, and executing the bytecode created in Java.
Although it is platform dependent which means the software of JVM is different for different Operating Systems it plays a vital role in making Java platform Independent.
To know more about the topic refer to JVM in Java.
""")
response = chat.send_message("""
JVM stands for Java Virtual Machine it is a Java interpreter. It is responsible for loading, verifying, and executing the bytecode created in Java.
Although it is platform dependent which means the software of JVM is different for different Operating Systems it plays a vital role in making Java platform Independent.
To know more about the topic refer to JVM in Java.
""")
print("- chatbot: ",response.candidates[0].content.parts)
input()

print("- me: ", """
JIT stands for (Just-in-Time) compiler is a part of JRE(Java Runtime Environment), it is used for better performance of the Java applications during run-time. The use of JIT is mentioned in step by step process mentioned below:
Source code is compiled with javac to form bytecode
Bytecode is further passed on to JVM 
JIT is a part of JVM, JIT is responsible for compiling bytecode into native machine code at run time.
The JIT compiler is enabled throughout, while it gets activated when a method is invoked. For a compiled method, the JVM directly calls the compiled code, instead of interpreting it.
As JVM calls the compiled code that increases the performance and speed of the execution.
      """)
response = chat.send_message("""
JIT stands for (Just-in-Time) compiler is a part of JRE(Java Runtime Environment), it is used for better performance of the Java applications during run-time. The use of JIT is mentioned in step by step process mentioned below:
Source code is compiled with javac to form bytecode
Bytecode is further passed on to JVM 
JIT is a part of JVM, JIT is responsible for compiling bytecode into native machine code at run time.
The JIT compiler is enabled throughout, while it gets activated when a method is invoked. For a compiled method, the JVM directly calls the compiled code, instead of interpreting it.
As JVM calls the compiled code that increases the performance and speed of the execution.
""")
print("- chatbot: ",response.candidates[0].content.parts)
input()

print("- me: ", """
 vector<int> twoSum(vector<int>& nums, int target) {
         vector<int> result;
        for (int i = 0; i< nums.size() ; i++) {
            for (int j= i +1;j < nums.size() ; j++) {
                if (nums[i] + nums[j] == target) {
                    result.push_back(i);
                    result.push_back(j);
                    return result;
                }
            }
        }
        return result;
    }
""")
response = chat.send_message("""
 vector<int> twoSum(vector<int>& nums, int target) {
         vector<int> result;
        for (int i = 0; i< nums.size() ; i++) {
            for (int j= i +1;j < nums.size() ; j++) {
                if (nums[i] + nums[j] == target) {
                    result.push_back(i);
                    result.push_back(j);
                    return result;
                }
            }
        }
        return result;
    }
""")
print("- chatbot: ",response.candidates[0].content.parts)
input()
