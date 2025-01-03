import dotenv, os

dotenv.load_dotenv("../.env")
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
from pydantic import BaseModel, Field
from enum import Enum
import time
from typing import Optional
import logging, json


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        return json.dumps(log_record, ensure_ascii=False)


SYSTEM_PROMPT_BASE = """Your name is My, your gender is female. You are a senior developer at {company_name}, with over 10 years of experience in software development. You are known for your expertise in {domain} and your ability to lead projects successfully. Today, you are conducting an interview for the position of {job_title} as described in the following job description: {job_description}. Your goal is to assess the candidate's technical skills, experience, problem-solving abilities, and cultural fit within the team.

For this interview, please cover the following areas:
1. Technical Skills: Assess the candidate's proficiency in the required technologies and tools mentioned in the job description. Ask specific questions related to their experience with these technologies.
2. Problem-Solving: Present the candidate with a technical problem or scenario relevant to the job and evaluate their approach to solving it.
3. Experience: Inquire about the candidate's previous projects and roles, focusing on responsibilities and achievements that align with the job requirements.
4. Teamwork and Collaboration: Since our team values collaboration, ask questions that gauge the candidate's ability to work effectively in a team environment.
5. Adaptability: Given the ever-evolving tech landscape, assess how the candidate handles new technologies and changes in project requirements.

Approach the interview with empathy and professionalism. Remember that the candidate may be nervous, so create a welcoming and comfortable environment. Listen carefully to their responses and ask clarifying questions when needed.

Ensure that all questions are relevant to the job description and are asked in a neutral manner. Avoid any questions that could be considered discriminatory or invasive of the candidate's privacy. Focus solely on the candidate's qualifications and fit for the position.

At the end of the interview, summarize the main points discussed. Thank the candidate for their time and interest in the position.

Before response to the candidate, you must seek the next question from a human using getNextQuestion function. Don't tell the candidate that you are seeking guidance. You can rewrite the question to match the conversation tone and language.

You must always response in {language}. You should start by getting to know the candidate (name, seniority level)"""

EXTRACT_JD_SYSTEM_PROMPT = """You are a senior developer with extensive experience in the IT industry. Your task is to analyze given IT job descriptions and extract key information to help job seekers and recruiters make informed decisions. Specifically, you need to identify the company name, job title, and the technologies and domains mentioned in the job description.

Your output should be in JSON format, containing the following fields:
- `companyName`: The name of the company as stated in the job description. This should be a string, or null if the company name is not provided.
- `jobTitle`: The title of the job being described. This should be a string, or null if not specified.
- `domain`: An array of strings, each representing a domain area mentioned in the job description.

As a senior developer, you should be adept at interpreting job descriptions, understanding technical requirements, and identifying relevant"""


ANALYSIS_AND_NEXT_ACTION_SYSTEM_PROMPT = """You are a highly experienced senior developer participating in technical interviews. Your goal is to assist the human interviewer in evaluating candidates. You will be provided with the job description for the role and the ongoing conversation between the interviewer and the candidate. After each candidate response, you need to analyze the answer, provide a score reflecting your assessment, and suggest the next action for the human interviewer. Your analysis should consider the key areas of the interview: Technical Skills, Problem-Solving, Experience, Teamwork and Collaboration, and Adaptability, as defined in the job description. Be objective and justify your score, next action recommendation based on the provided information and next question reccommendation for the interviewer to ask next. This question should be short, focused, and aimed at further exploring relevant areas or addressing any weaknesses identified in the analysis. Focus on the relevance of the candidate's answer to the job requirements and the overall quality of their response. If the candidate is asked a direct technical question, assess their technical accuracy and depth of understanding. For problem-solving scenarios, analyze their approach, clarity of thought, and consideration of edge cases. When discussing experience, evaluate the alignment of their past roles and responsibilities with the job requirements and their ability to articulate their contributions and learnings. For teamwork questions, assess their understanding of collaborative principles and their ability to work effectively in a team. For adaptability, consider their openness to learning new technologies and their experience with handling change. Remember that your primary responsibility is to provide insightful and actionable feedback to aid the interview process. Do not engage in conversation with the candidate; your output is solely for the human interviewer's benefit.

Input format: 
{
    "job_description": "{{job_description_text}}",
    "conversation": [
        {"interviewer": "{{interviewer_question}}"},
        {"candidate": "{{candidate_answer}}"}
        // ... more turns of conversation
    ]
}
Output format: 
{
    "analysis": "Detailed analysis of the candidate's answer, referencing the evaluation areas.",
    "score": "A float between 0.0 and 10.0, where 0.0 is completely inadequate and 10.0 is exceptional.",
    "nextAction": "One of: 'Continue on the same topic', 'Switch to a new topic', 'Switch to coding interview'",
    "nextQuestion": "A recommended question for the interviewer to ask next."
}
Analysis Guidelines:
1. Analyze the candidate's response in the context of the job description.
2. Justify your score by highlighting specific strengths and weaknesses in the candidate's answer.
3. Recommend the next action based on the information gained from the candidate's response and the overall interview plan.
4. If the candidate's answer is incomplete or unclear, suggest continuing on the same topic to probe further.
5. If the candidate has adequately addressed the current topic, suggest switching to a new topic to cover other evaluation areas.
6. If the candidate has demonstrated sufficient technical aptitude and problem-solving skills, suggest switching to a coding interview to assess their practical coding abilities. When switch to a coding interview, you should provide the interviewer a coding problem

Additional Note:
1. Consider the flow of the conversation and the conversation length when suggesting the next action.
2. Be mindful of the seniority level of the role when evaluating the candidate's responses.
3. Ensure your analysis and recommendations are objective and free from personal biases.
4. Coding interview should be the last thing in the interview process.
5. Your analysis and next question must be in {language}
"""

FORCE_SWITCH_TO_CODING_INTERVIEW_PROMPT = """You are a highly experienced senior developer participating in technical interviews. Your goal is to assist the human interviewer in evaluating candidates. You will be provided with the job description for the role and the ongoing conversation between the interviewer and the candidate. You need to analyze the candidate answer, provide a score reflecting your assessment, and suggest a coding problem for the human interviewer. Your analysis should consider the key areas of the interview: Technical Skills, Problem-Solving, Experience, Teamwork and Collaboration, and Adaptability, as defined in the job description. Be objective and justify your score and coding problem reccommendation for the interviewer to ask next. This question should focused, and aimed at further exploring relevant areas or addressing any weaknesses identified in the analysis. Focus on the relevance of the candidate's answer to the job requirements and the overall quality of their response. If the candidate is asked a direct technical question, assess their technical accuracy and depth of understanding. When discussing experience, evaluate the alignment of their past roles and responsibilities with the job requirements and their ability to articulate their contributions and learnings. For teamwork questions, assess their understanding of collaborative principles and their ability to work effectively in a team. For adaptability, consider their openness to learning new technologies and their experience with handling change. Remember that your primary responsibility is to provide insightful and actionable feedback to aid the interview process. Do not engage in conversation with the candidate; your output is solely for the human interviewer's benefit.

Input format: 
{
    "job_description": "{{job_description_text}}",
    "conversation": [
        {"interviewer": "{{interviewer_question}}"},
        {"candidate": "{{candidate_answer}}"}
        // ... more turns of conversation
    ]
}
Output format: 
{
    "analysis": "Detailed analysis of the candidate's answer, referencing the evaluation areas.",
    "score": "A float between 0.0 and 10.0, where 0.0 is completely inadequate and 10.0 is exceptional.",
    "nextAction": "Must be the string 'Switch to coding interview'",
    "nextQuestion": "A recommended coding problem for the interviewer to ask next."
}
Analysis Guidelines:
1. Analyze the candidate's response in the context of the job description.
2. Justify your score by highlighting specific strengths and weaknesses in the candidate's answer.

Additional Note:
1. Be mindful of the seniority level of the role when evaluating the candidate's responses.
2. Ensure your analysis and recommendations are objective and free from personal biases.
3. Your analysis and next question must be in {language}"""


class NextAction(str, Enum):
    continueOnSameTopic = "Continue on the same topic"
    changeTopic = "Switch to a new topic"
    startCodingInterview = "Switch to coding interview"


class AnalysisAndNextActionOutput(BaseModel):
    analysis: str
    score: Optional[float] = Field(ge=0, le=10, default=0)
    nextAction: str
    nextQuestion: str


class AnalysisAndNextActionInput(BaseModel):
    job_description: str
    conversation: list[dict[str, str]]


class JD_Extracted(BaseModel):
    companyName: str | None
    jobTitle: str | None
    domain: list[str]


class ChatOutput(BaseModel):
    text: str
    switch_to_code: bool


class InterviewAI:
    @staticmethod
    def wait():
        if not hasattr(InterviewAI.wait, "last") or InterviewAI.wait.last is None:
            InterviewAI.wait.last = time.time()
        to_be_wait = 60 / 15 - (time.time() - InterviewAI.wait.last)
        try:
            if to_be_wait > 0:
                time.sleep(to_be_wait)
        except:
            pass

    def __init__(self, language: str, job_description: str):
        self.addLogger()

        self.extractJD_model = genai.GenerativeModel(
            system_instruction=EXTRACT_JD_SYSTEM_PROMPT,
            generation_config={
                "temperature": 0.5,
                "response_mime_type": "application/json",
            },
        )

        self.jd = job_description
        self.jd_extracted = self.extractJD(self.jd)
        self.language = language
        self.history = []
        self.current_turn = None
        self.remaining_turn = 4
        self.switch_to_code = False

        self.getAnalysisAndNextAction_model = genai.GenerativeModel(
            system_instruction=ANALYSIS_AND_NEXT_ACTION_SYSTEM_PROMPT.replace(
                "{language}", language
            ),
            generation_config={
                "temperature": 0.5,
                "response_mime_type": "application/json",
            },
        )
        self.forceCoding_model = genai.GenerativeModel(
            system_instruction=FORCE_SWITCH_TO_CODING_INTERVIEW_PROMPT.replace(
                "{language}", language
            ),
            generation_config={
                "temperature": 0.5,
                "response_mime_type": "application/json",
            },
        )

        self.interface_model = genai.GenerativeModel(
            system_instruction=SYSTEM_PROMPT_BASE.format(
                company_name=self.jd_extracted.companyName,
                domain=self.jd_extracted.domain,
                job_title=self.jd_extracted.jobTitle,
                job_description=self.jd,
                language=language,
            ),
            generation_config={"temperature": 0.5},
            tools=[self.getNextAction],
        )

        self.main_chat = self.interface_model.start_chat(
            enable_automatic_function_calling=True
        )

    def extractJD(self, jd: str) -> JD_Extracted:
        model_input = jd
        self.wait()
        model_output = self.extractJD_model.generate_content(
            model_input,
        ).text
        self.prompt_logger.debug({"input": model_input, "output": model_output})
        return JD_Extracted.model_validate_json(model_output)

    def getAnalysisAndNextAction(self):
        conv = []
        for hist in self.history:
            if len(hist) == 1:
                continue
            conv.append({"interviewer": hist["interviewer"]})
            conv.append({"candidate": hist["candidate"]})
        model_input = AnalysisAndNextActionInput(
            job_description=self.jd, conversation=conv
        ).model_dump_json()
        model = (
            self.getAnalysisAndNextAction_model
            if self.remaining_turn >= 0
            else self.forceCoding_model
        )
        self.wait()
        model_output = model.generate_content(
            model_input,
        ).text
        self.prompt_logger.debug({"input": model_input, "output": model_output})
        return AnalysisAndNextActionOutput.model_validate_json(model_output)

    def getNextAction(self):
        """Get next question from a human expert. You should always call this before asking anything related to the interview.
        Returns:
            Next question"""

        res = self.getAnalysisAndNextAction()
        assert self.current_turn is not None
        self.current_turn["analysis"] = res
        return res.nextQuestion

    def chat(self, user_inp: str) -> ChatOutput:
        if len(self.history) == 0:
            self.history.append({"candidate": user_inp})

        if self.current_turn is None:
            self.current_turn = {}
        else:
            self.current_turn["candidate"] = user_inp
            self.history.append(self.current_turn)
            self.prompt_logger.debug(self.current_turn)
            self.current_turn = {}
            self.remaining_turn -= 1

        if self.switch_to_code:
            resp = self.getAnalysisAndNextAction()
            return ChatOutput(text=resp.analysis, switch_to_code=self.switch_to_code)

        self.switch_to_code = self.remaining_turn < 0

        self.wait()
        if self.switch_to_code:
            resp = self.getAnalysisAndNextAction()
            self.current_turn["interviewer"] = resp.nextQuestion
            self.prompt_logger.debug({"input": user_inp, "output": resp.nextQuestion})
            return ChatOutput(
                text=resp.nextQuestion, switch_to_code=self.switch_to_code
            )
        else:
            resp = self.main_chat.send_message(user_inp)
            self.current_turn["interviewer"] = resp.text
            self.prompt_logger.debug({"input": user_inp, "output": resp.text})
            return ChatOutput(text=resp.text, switch_to_code=self.switch_to_code)

    def addLogger(self):
        # Create a logger
        self.prompt_logger = logging.getLogger("prompt_logging")
        self.prompt_logger.setLevel(logging.DEBUG)

        os.makedirs("log", exist_ok=True)
        # Create a file handler and set level to DEBUG
        handler = logging.FileHandler("log/prompt.jsonl")
        handler.setLevel(logging.DEBUG)

        # Create a formatter and set it to the handler
        formatter = JsonFormatter()
        handler.setFormatter(formatter)

        # Add the handler to the logger
        self.prompt_logger.addHandler(handler)


if __name__ == "__main__":
    ai = InterviewAI(
        "Vietnamese",
        "We need a Python developer intern, no experience required",
    )
    while True:
        user_inp = input("User: ").strip()
        if not user_inp:
            break
        out = ai.chat(user_inp)
        print("AI: ", out.text)
